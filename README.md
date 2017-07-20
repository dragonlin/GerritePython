# GerritePython

    1. 使用gerrit API 抓取数据 
    2. 存储在MongoDB
    3. 使用 Dijango 做数据访问
    4. 数据可视化展示


## 一、 准备事项

安装 pygerrit2
```
pip install pygerrit2
```
填写你的用户名和密码
```
GERRITE_USER = ""
GERRITE_PWD = ""
GERRITE_URL_AUTH = "http://gerrite1.ext.net.[yourcompany].com"

```
link:
https://gerrite1.ext.net.nokia.com/Documentation/rest-api.html

这个Demo，只是打通了RestAPI的调用过程


## 二、 需求
我们可以到年底发布“开发者成就”，
例如提交了多少Request，
给了多少Comment, 
Review了多少代码，
平均Comment时间等

也能搞个预警，例如几小时之内，没有Comment等

至于对那些收到的数据做什么二次开发，就看我们怎么做了
