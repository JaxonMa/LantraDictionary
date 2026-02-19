# Lantra Dictionary 蓝雀词典

## 项目介绍

这是一个在线中文词典，使用 flask 开发，可以查询汉字的读音、部首、详细解释等信息，同时提供查词服务，可以帮助用户快速了解一个词语的释义。
计划在后期加入英语词典的功能。

## 注意事项

鉴于仓库大小，字典（词典）数据文件没有上传。<br>
如果想要运行该项目，请进入[参考资料](#参考资料)中的字典数据来源，下载在 process_data.py 中 DICTIONARY_PATH 提及的字典文件，并放置到对应的目录。
运行以下命令即可处理原始字典数据，得到处理后的字典数据：

~~~ bash
python process_data.py
~~~

## 开发环境

> Python 3.12

使用以下命令安装依赖
~~~ bash
pip install -r requirements.txt
~~~

## 运行截图
| 说明     | 图示                                                                                                                              |
|--------|---------------------------------------------------------------------------------------------------------------------------------|
| 首页     | ![首页](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBZvtpjynvSm3K6hm8plj9ki5RjLa4XAAC0QtrG5FxeES2yDNu1LM49wEAAwIAA3cAAzoE.png)     |
| 单字搜索   | ![单字搜索结果](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBZvxpjyoQhx_DKiNH6Xn7qakPR4UR-gAC0gtrG5FxeERON-i9kbHUzwEAAwIAA3cAAzoE.png) |
| 词语搜索   | ![词语搜索结果](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBZv1pjyrWNc07hyr0f0GOM_zG6sffgQAC1AtrG5FxeETsh9cGmL4CPQEAAwIAA3cAAzoE.png) |
| 含字母的词语 | ![含字母的词语](https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBZv5pjysZleTreyzocoqqU83Pjt6XYAAC1QtrG5FxeERXCFjwGDW23AEAAwIAA3cAAzoE.png) |


## 参考资料

本项目的字典数据来源：

- [GitHub] [chinese-dictionary](https://github.com/mapull/chinese-dictionary)

## TODO

- 增加英语词典功能
