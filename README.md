# GerritePython

    1. 使用gerrit API 抓取数据 
    2. 存储在MongoDB
    3. 使用 Dijango 做数据访问
    4. 数据可视化展示


## 一、 准备事项

安装 [pygerrit2](https://dragonlin.github.io/2017/07/20/20170720Mac-install-pip/)
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
https://review.openstack.org/Documentation/rest-api.html

这个Demo，只是打通了RestAPI的调用过程


## 二、 需求

我们可以到年底发布“开发者成就”，
例如

### 提交了多少Request，

- >who 提交了多少 mr  按月 周计算
- >who 提交了多少行代码 每月 文件类型（.html .js .ts)
- >MR 提交的类型 根据提交的commit message 信息来区分

    - 包含 NF 代表是new feature
    - BUG 代码修改的bug

### 给了多少Comment, 
- who 日期
    - who 给累最多的comment
- comment 内容是什么 类型 来自什么文件

### Review了多少代码，
－reviewer 
### 平均Comment时间等
### 平均提交的速度 多久才能提交到master
- 一个mr 从产生到提交 需要经过多久 天/周 
## 也能搞个预警，例如几小时之内，没有Comment等
### 等待comment
- >代码提交 && verify＋1 && 包含reviewer && 无review记录
- >正常工作日：提交时间 绿色(<12h) 黄色告警(>12h) 橙色(<24h) 红色告警(>3*24h)

    - 提醒到reviewer  代码ok **verify +1**
    - 提醒到committer 代码异常 **verify -1**
>python 使用xmpppy模块向 Jabber 发送消息 或者jabber.py
### 已经给了comment 需要committer 修改
- > \>7*24h 红色告警  提醒到 committer



至于对那些收到的数据做什么二次开发，就看我们怎么做了
### 目前mr的状态
- 饼状图 呈现 status 列表
### 代码优化
我们开发过程中是不断的增加代码 有时候为了赶进度，就忽略了代码质量等

多少个提交是在减少代码的  **[lines_deleted > lines_inserted]**
>(u'doc/source/configuration/pluggable_panels.rst', {u'lines_deleted': 15, u'lines_inserted': 19})

## 三、 Gerrit REST API代码 [gerrit_python](https://github.com/dragonlin/GerritePython/tree/master/src/gerrit)
```
Status_list = ['open','closed','merged','pending','reviewed','abandoned','draft']
GERRITE_USER = ""
GERRITE_PWD = ""
PROJECT_NAME = "openstack/horizon"
GERRITE_URL_AUTH = "https://review.openstack.org"
rest = GerritRestAPI(url=GERRITE_URL_AUTH)
```

### 获取所有的某个branch的changes
res = rest.get('/changes/?q=status:{}+project:{}'.format(Status_list[2],PROJECT_NAME))
change_id = res[0]['change_id']
### 某个change的信息
url = '/changes/{}/?o=CURRENT_REVISION&o=CURRENT_FILES'.format(change_id)
current_files = rest.get(url)
打印对象信息
print json.dumps(current_files,indent=4)
>{
    "status": "MERGED",
    "topic": "zanata/translations",
    "updated": "2017-07-20 12:09:11.306000000",
    "insertions": 39,
    "created": "2017-07-20 11:20:28.000000000",
    "change_id": "I7ed522c865ea23648d6ca1551ef3ae17cbb3c0c2",
    "hashtags": [],
    "deletions": 3,
    "current_revision": "980f0a204831894c5b83aa6fef60c5040ac2fd35",
    "submitted": "2017-07-20 12:09:11.000000000",
    "project": "openstack/horizon",
    "branch": "stable/newton",
    "owner": {
        "_account_id": 11131
    },
    "_number": 485561,
    "revisions": {
        "980f0a204831894c5b83aa6fef60c5040ac2fd35": {
            "files": {
                "openstack_dashboard/locale/id/LC_MESSAGES/django.po": {
                    "lines_deleted": 3,
                    "lines_inserted": 39
                }
            },
            "created": "2017-07-20 11:20:28.000000000",
            "uploader": {
                "_account_id": 11131
            },
            "ref": "refs/changes/61/485561/1",
            "fetch": {
                "git": {
                    "url": "git://git.openstack.org/openstack/horizon",
                    "ref": "refs/changes/61/485561/1"
                },
                "anonymous http": {
                    "url": "https://git.openstack.org/openstack/horizon",
                    "ref": "refs/changes/61/485561/1"
                }
            },
            "_number": 1
        }
    },
    "id": "openstack%2Fhorizon~stable%2Fnewton~I7ed522c865ea23648d6ca1551ef3ae17cbb3c0c2",
    "subject": "Imported Translations from Zanata"
}
current_revision = current_files['current_revision']

### 获得提交的文件信息
commit_files = current_files['revisions'][current_revision]['files']



