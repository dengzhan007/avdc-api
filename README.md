# AVDC

AVDC Powered by Flask

## QuickStart

### Clone Project

```shell
git clone https://github.com/xjasonlyu/AVDC.git
```

### Install Requirements

```shell
pip3 install -r requirements.txt
```

### Run Application

```shell
python3 main.py
```

## Docker

```text
docker run -d \
    -p 5000:5000 \
    -v $PWD/avdc.db:/avdc.db \                # optional
    -e HTTP_PROXY=http://192.168.1.1:1080 \   # optional
    -e HTTPS_PROXY=http://192.168.1.1:1080 \  # optional
    ghcr.io/xjasonlyu/avdc:latest
```

## API

| Endpoint | Description |
| --- | ----------- |
| `/metadata/<id>` | Fetch Video Metadata |
| `/people/<name>` | Fetch Actress Avatar |
| `/image/people/<name>` | Fetch `2/3` People Image |
| `/image/primary/<id>` | Fetch `2/3` Cropped Cover Image |
| `/image/backdrop/<id>` | Fetch Full Size Cover Image |
