# AV Data Capture (API)

[CLI 版本](https://github.com/yoshiko2/AV_Data_Capture)

![](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat)
![](https://img.shields.io/github/license/yoshiko2/av_data_capture.svg?style=flat)
![](https://img.shields.io/github/release/yoshiko2/av_data_capture.svg?style=flat)
![](https://img.shields.io/badge/Python-3.8-yellow.svg?style=flat&logo=python)

[GUI 版本](https://github.com/moyy996/AVDC)

![](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat)
![](https://img.shields.io/github/license/moyy996/avdc.svg?style=flat)
![](https://img.shields.io/github/release/moyy996/avdc.svg?style=flat)
![](https://img.shields.io/badge/Python-3.6-yellow.svg?style=flat&logo=python)
![](https://img.shields.io/badge/Pyqt-5-blue.svg?style=flat)

API 版本

![](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat)
![](https://img.shields.io/github/license/xjasonlyu/avdc-api.svg?style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/xjasonlyu/avdc-api)
![](https://img.shields.io/badge/Python-3.9-yellow.svg?style=flat&logo=python)
![](https://img.shields.io/badge/Flask-1.1.x-blue.svg?style=flat)

## 简介

- **日本电影元数据 抓取工具 | 刮削器**，配合本地影片管理软件 Emby, Jellyfin, Kodi 等管理本地影片，该软件起到分类与元数据（metadata）抓取作用，利用元数据信息来分类，仅供本地影片分类整理使用。
- 提供 [Jellyfin.Plugin.AVDC](https://github.com/xjasonlyu/jellyfin-plugin-avdc) 基于`Flask`的API后端的支持
- 封面海报裁剪基于 [face_recognition](https://github.com/ageitgey/face_recognition) 的人脸识别，无需百度/谷歌等外部翻译
- 元数据存储在本地Sqlite数据库中，方便**数据快速存取**以及**共享服务端**

## 文档

见➡️： [Wiki](https://github.com/xjasonlyu/avdc-api/wiki)

## API

| Endpoint | Description |
| --- | ----------- |
| `/actress/<name>` | 获取女优的信息 |
| `/metadata/<vid>` | 获取影片的元数据 |
| `/image/actress/<name>` | 获取`2:3`比例的女优头像 |
| `/image/primary/<vid>` | 获取`2:3`比例的海报封面 |
| `/image/thumb/<vid>` | 获取`16:9`比例的海报封面 |
| `/image/backdrop/<vid>` | 获取原影片全尺寸的封面 |

## 申明

当你查阅、下载了本项目源代码或二进制程序，即代表你接受了以下条款

* 本软件仅供技术交流，学术交流使用
* **请勿在热门的社交平台上宣传此项目**
* 本软件作者编写出该软件旨在学习 Python ，提高编程水平
* 本软件不提供任何影片下载的线索
* 用户在使用本软件前，请用户了解并遵守当地法律法规，如果本软件使用过程中存在违反当地法律法规的行为，请勿使用该软件
* 用户在使用本软件时，若用户在当地产生一切违法行为由用户承担
* 严禁用户将本软件使用于商业和个人其他意图
* 源代码和二进制程序请在下载后24小时内删除
* 卖源码的死个妈
* 本软件作者yoshiko2保留最终决定权和最终解释权
* 若用户不同意上述条款任意一条，请勿使用本软件
---
When you view and download the source code or binary program of this project, it means that you have accepted the following terms

* This software is only for technical exchange and academic exchange
* **Please do not promote this project on popular social platforms**
* The software author wrote this software to learn Python and improve programming
* This software does not provide any clues for video download
* Before using this software, please understand and abide by local laws and regulations. If there is any violation of local laws and regulations during the use of this software, * please do not use this software
* When the user uses this software, if the user has any illegal acts in the local area, the user shall bear
* It is strictly forbidden for users to use this software for commercial and personal intentions
* Please delete the source code and binary program within 24 hours after downloading
* The author of this software yoshiko2 reserves the right of final decision and final interpretation
* If the user does not agree with any of the above terms, please do not use this software
---
本プロジェクトのソースコード、バイナリファイルをダウンロード、または表示することによって、あなたは次の規約に拘束されることに同意したことになります。

* このソフトウェアは、開発技術学習することのみに使用できます。
* **ソーシャルメディアで本プロジェクトの宣伝をご遠慮ください**
* 作者はPythonの勉強と技術力の向上のために、このソフトウェアを作成しました
* 本ソフトウェアは、動画ダウンロード機能一切提供しません
* 本ソフトウェアを使用する前に、現地の法令をよく理解する必要があります。あなたは、適用される現地の法令を順守する責任を負います
* 本ソフトウェアを使用した結果生じた損害や法的責任につきまして作者は一切責任を負いません
* 本ソフトウェアを商用、業務、その他の営利目的のために使用することはできません
* 本プロジェクトのソースコード、バイナリファイルをダウンロードした場合、24時間以内に削除してください
* 最終解釈権は作者yoshiko2に属します
* 本規約およびすべての適用法、規約および規則を遵守する場合にのみ本ソフトウェアを使用することができます
