import re
from concurrent import futures
from datetime import datetime
from os.path import splitext
from typing import Optional


def concurrentMap(fn, *args, timeout=None, max_workers=None):
    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        return tuple(executor.map(fn, *args, timeout=timeout))


def extractTitle(_s: str) -> str:
    return re.sub(r'[a-zA-Z0-9]+[-_]?[a-zA-Z0-9]+[-_ ]', '', _s)


def parseVID(name: str) -> tuple[str, bool]:
    name, _ = splitext(name.strip())
    name = re.sub(r'[\-._]CD\d+$', '', name, flags=re.IGNORECASE)

    if name[-2:].upper() in ('-C', '-R'):
        return name[:-2], True
    return name, False


def extractYear(_s: str) -> Optional[int]:
    try:
        return datetime.strptime(_s, '%Y-%m-%d').year
    except (ValueError, TypeError):
        return


if __name__ == '__main__':
    print(parseVID('abp-113'))
    print(parseVID('abp-113.mp4'))
    print(parseVID('abp-113-c-cd1.mp4'))
    print(parseVID('abp-113-C.cd2.mkv'))
