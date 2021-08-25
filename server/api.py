import json
import os
import re
from functools import wraps
from typing import Any, Callable, Optional

from avdc.actress import gfriends
from avdc.actress import xslist
from avdc.model.actress import Actress
from avdc.model.cover import Cover
from avdc.model.metadata import Metadata
from avdc.provider import arzon
from avdc.provider import fc2
from avdc.provider import javbus
from avdc.provider import javdb
from avdc.utility.image import (cropImage,
                                autoCropImage,
                                getRawImageSize,
                                getRawImageByURL,
                                getRawImageFormat,
                                imageToBytes,
                                bytesToImage)
from avdc.utility.misc import parseVID, concurrentMap
from server import app
from server import db_api


def extract_vid(fn: Callable[[str], Any]):
    @wraps(fn)
    def wrapper(vid: str):
        return fn(parseVID(vid)[0])

    return wrapper


def is_valid_metadata(_m: Any) -> bool:
    return isinstance(_m, Metadata)


def is_valid_actress(_a: Any) -> bool:
    return isinstance(_a, Actress)


def str_to_bool(s: str) -> bool:
    try:
        return True if json.loads(s) else False
    except (TypeError, json.decoder.JSONDecodeError):
        return False


_s_list = ('ara', 'bnjc', 'dcv', 'endx', 'endw', 'eva', 'ezd', 'gana',
           'HAMENETS', 'hmdn', 'hoi', 'imdk', 'ion', 'jac',
           'jkz', 'jotk', 'ksko', 'lafbd', 'luxu', 'maan',
           'mium', 'mntj', 'nama', 'ntk', 'nttr', 'obut',
           'ore', 'orebms', 'orec', 'orerb', 'oretd', 'orex',
           'per', 'pkjd', 'scp', 'scute', 'cute', 'shyn', 'simm',
           'siro', 'srcn', 'sqb', 'sweet', 'svmm', 'urf', 'fcp')

_providers = {
    'arzon': arzon.main,
    'fc2': fc2.main,
    'javdb': javdb.main,
    'javbus': javbus.main,
}

_priority = 'javbus,avsox,javdb,arzon,fc2'


def _is_in_s_list(keyword: str) -> bool:
    return True if [i for i in _s_list if i.upper() in keyword.upper()] else False


def _getSources(keyword: str) -> list[str]:
    sources = _priority.split(',')  # default priority

    # if "avsox" in sources and (re.match(r"^\d{5,}", keyword) or
    #                            "HEYZO" in keyword.upper() or "BD" in keyword.upper()):
    #     sources.insert(0, sources.pop(sources.index("avsox")))

    if "fc2" in sources and "FC2" in keyword.upper():
        sources.insert(0, sources.pop(sources.index("fc2")))

    return sources


def _getRemoteMetadata(vid: str, providers: Optional[str] = None) -> Optional[Metadata]:
    def no_exception_call(source: str) -> Optional[Metadata]:
        try:
            return _providers[source](vid)
        except Exception as e:
            app.logger.warning(f'match metadata from {source}: {vid}: {e}')
            return

    for m in (providers.split(',') if providers is not None else _getSources(vid)):
        if not m.strip():
            continue

        results = [r for r in concurrentMap(no_exception_call,
                                            m.split('+'),
                                            max_workers=len(m.split('+')))
                   if is_valid_metadata(r)]

        if not results:
            continue

        m = results[0]
        for result in results[1:]:
            m += result
        return m


def _getLocalMetadata(vid: str) -> Optional[Metadata]:
    return db_api.GetMetadataByVID(vid)


def GetMetadataByVID(vid: str, update: bool = False, *args, **kwargs) -> Optional[Metadata]:
    if not update:  # try from database
        m = _getLocalMetadata(vid)
        if is_valid_metadata(m):
            return m

    m = _getRemoteMetadata(vid, *args, **kwargs)
    if not is_valid_metadata(m):
        return

    # store to database
    db_api.StoreMetadata(m, update=update)
    app.logger.info(f'store {m.vid} to database')
    return m


def GetActressByName(name: str, update: bool = False) -> Optional[Actress]:
    if not update:
        actress = db_api.GetActressByName(name)
        if is_valid_actress(actress):
            return actress

    images = gfriends.search(name)
    if not images:
        return

    actress = xslist.main(name)
    if not is_valid_actress(actress):
        actress = Actress(name=name)

    # attach images
    actress.images = images

    # store to database
    db_api.StoreActress(actress=actress, update=update)
    app.logger.info(f'store {name} images to database')
    return actress


def UpdateCoverPositionByVID(m: Metadata, pos: float):
    pos = pos if 0 <= pos <= 1 else -1

    cover = db_api.GetCoverByVID(m.vid)
    if not cover:
        data = getRawImageByURL(m.cover)
        fmt = getRawImageFormat(data)
        height, width = getRawImageSize(data)
    else:
        if abs(cover.pos - pos) < 0.01:  # almost equal
            return
        fmt, data, height, width = (cover.fmt, cover.data,
                                    cover.height, cover.width)

    db_api.StoreCover(m.vid, data, fmt=fmt, pos=pos,
                      width=width, height=height, update=True)


def GetBackdropImageByVID(vid: str, update: bool = False) -> Optional[Cover]:
    if not update:
        cover = db_api.GetCoverByVID(vid)
        if cover:
            return cover

    m = GetMetadataByVID(vid)
    if not is_valid_metadata(m) or not m.cover:
        return

    # -- for arzon --
    headers = {}
    if 'arzon' in m.cover:
        headers.update(referer='https://www.arzon.jp/')
    # ---------------

    cover_url = m.cover

    # -- for fc2 --
    if 'fc2' in m.providers and m.images:
        # use first image for backdrop cover
        cover_url = m.images[0]
        # store primary cover
        data = getRawImageByURL(m.cover)
        fmt = getRawImageFormat(data) or os.path.splitext(m.cover)[-1].strip('.')
        height, width = getRawImageSize(data)
        cover = Cover(vid=m.vid + '@PRIMARY',
                      data=data, fmt=fmt, pos=0.5,
                      width=width, height=height)
        db_api.StoreCover(**cover.toDict(), update=update)
    # -------------

    data = getRawImageByURL(cover_url, headers=headers or None)
    fmt = getRawImageFormat(data)
    height, width = getRawImageSize(data)

    if fmt is None:
        raise Exception(f'{m.vid}: cover image format detection failed')

    cover = Cover(vid=m.vid, data=data, fmt=fmt, pos=-1,
                  width=width, height=height)
    db_api.StoreCover(**cover.toDict(), update=update)
    return cover


def GetPrimaryImageByVID(vid: str, *args, **kwargs) -> Optional[bytes]:
    cover = db_api.GetCoverByVID(vid + '@PRIMARY')  # try primary
    if not cover:
        cover = GetBackdropImageByVID(vid, *args, **kwargs)
        if not cover:
            return

    face_detection = False  # disabled by default
    if re.match(r'^\d+[\-_]\d+', vid, re.IGNORECASE) \
            or re.match(r'^\d+[a-zA-Z]+[\-_]\d+', vid, re.IGNORECASE) \
            or re.match(r'^n\d+', vid, re.IGNORECASE) \
            or [i for i in ('HEYZO', 'BD', 'HD', '3D', 'MSFH') if i in vid.upper()] \
            or _is_in_s_list(vid):
        face_detection = True

    return imageToBytes(autoCropImage(bytesToImage(cover.data), pos=cover.pos, face_detection=face_detection))


def GetThumbImageByVID(vid: str, *args, **kwargs) -> Optional[bytes]:
    cover = db_api.GetCoverByVID(vid + '@THUMB')  # try thumb
    if not cover:
        cover = GetBackdropImageByVID(vid, *args, **kwargs)
        if not cover:
            return

    return imageToBytes(cropImage(bytesToImage(cover.data), scale=16 / 9, default_to_top=False))


def GetBackdropImageSizeByVID(vid: str, *args, **kwargs) -> Optional[tuple[int, int]]:
    cover = GetBackdropImageByVID(vid, *args, **kwargs)
    if not cover:
        return

    return cover.height, cover.width  # height, width


if __name__ == '__main__':
    # print(GetMetadataByVID('abp-233', update=True))
    # print(GetActressByName('通野未帆'))
    print(_getRemoteMetadata('100518-766'))
    # models.UpdateMetadata(m)

    # print(str_to_bool('true'))
    # print(str_to_bool('True'))
    # print(str_to_bool('1'))
    # print(str_to_bool('0'))
    # print(str_to_bool('idk'))
