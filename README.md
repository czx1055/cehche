一个剑网3机器人 车哥制作
支持 日常 物价  金价 攻略  沙盘 开服 维护公告 等等功能
加入了gpt对话@特机器人就可以了。
QQ群交流1667910

git clone https://github.com/czx1055/cehche.git
输入
pip install -r requirements.txt
安装环境依赖

打开kai文件夹在文件夹内 安装定时器和gocq插件

定时任务安装模块

nb plugin install nonebot_plugin_apscheduler

gocq启动网页版

nb plugin install nonebot-plugin-gocqhttp


输入 nb run 启动项目

![image](https://user-images.githubusercontent.com/128042750/227760263-72d9c5e2-00ea-42f0-a656-c9d8c482e0c1.png)

定时器会有报错：需要修改此文件，会有提示按这个路径去找就好了

你的python安装目录下面的 Python310\Lib\site-packages\nonebot_plugin_apscheduler\__init__.py
按照下面的格式取修改

![image](https://user-images.githubusercontent.com/128042750/227760394-b7359e54-c26e-4c7d-9873-74fe765814c2.png)

保存后再次启动bot

安装完gocq网页版插件

输入：http://127.0.0.1:8080/go-cqhttp/

登录QQ，尽量选择手表模式登录,

其他方式我不知道了


