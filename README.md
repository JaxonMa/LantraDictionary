# LantraDict（No longer supported/不再维护）
一个使用 Flask 框架制作的查字项目（数据来源于 Python 包 xy_zidian ）  

> ### 开发环境
> - Python 3.10.5
> - macOS Monterey 12.5

## 使用
- 使用前需安装以下Python包：xy_zidian, pypinyin, zhconv, flask。推荐版本（开发版本）见下：
> xy_zidian==1.0.0  
> pypinyin==0.46.0  
> zhconv==1.4.3  
> flask==2.1.3  

- 如果运行时出现错误可尝试更改端口：
~~~ Python
app.run(port=你的端口_YOUR_PORT, debug=True)
~~~

## 注意
该项目已提供 **纯 html+css+js** 版本，见：[LantraDict-js(No longer supported/不再维护)](https://github.com/JaxonMa/LantraDict-js)。

更新：xy_zidian已不再可用。请使用其他功能相似的包实现查词功能。
该项目已停止维护，所以不会对以上问题进行修复。
