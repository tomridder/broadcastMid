<img width="249" alt="image" src="https://github.com/user-attachments/assets/ff7f1070-488c-4b81-8eb4-7b426a8f7e51">



# broadcastMid
broadcast on bilibili to catch the danmu into Midjourney on Website

## 如何使用
1.用 cmd 在本地电脑 8888端口 启动 chrome 窗口

2.chrome 打开两个tab 一个是bilibili的网页直播窗口 live.bilibili.com/xxxx , 一个 tab 是  http://154.40.47.174:3003/ （一个 AI 绘画窗口）

3.启动本地 py 脚本

## 脚本思路
1.从 第一个是bilibili的网页直播窗口 live.bilibili.com/xxxx 的 弹幕窗口处 获取弹幕列表

2.将 弹幕列表 的最新弹幕 放到 第二个 tab  http://154.40.47.174:3003/  的输入

3.www.tomproxy.win 自动 绘画 弹幕的内容
