# ZhihuDTW

- 知乎答题王自动开房好友对战答题 保存题目到mongo数据库 ， 排位赛电脑端显示答案

- 参考头脑王者项目 https://github.com/lyh2668/TNWZ

- 博客 : [获取知乎答题王题库](https://www.ggbond.cc/知乎答题王/)

*免责声明：仅供学习交流使用，请勿进行非法用途*

参考TNWZ项目，准备学习撸一个python版的 ， 无奈头脑王者违规下线. 时隔半月,(全新)知乎答题王上线...

- 2018.3.6 : 用mitmproxy提供的addon功能简单实现了排位辅助


## 环境要求
- python3
- mongodb3

## 使用

### 一 环境安装
1. [下载安装mongo数据库](https://www.mongodb.com/download-center?jmp=nav#community)
2. [安装python3](https://www.python.org/downloads/)
3. clone代码,安装依赖
```
git clone https://github.com/ctguggbond/ZhihuDTW
cd ZhihuDTW
pip install -i http://pypi.douban.com/simple -- trusted-host pypi.douban.com -r requirements.txt

```

### 二 好友开房对战抓题

#### 准备

1. 终端运行`rankingFight`:  `mitmdump --flow-detail 0  -s ./rankingFight.py` 启动代理
2. 手机与电脑处于同一wifi网络,设置wifi代理为 电脑ip 端口为8080
3. 访问`mitmproxy.it` 安装证书
4. 登录答题王账号1，可看到输出: token和uid 填入到friendFight.py player1处(失败多试一次)
5. 同理登录账号2 填入player2的token和uid

#### 开始对战
- 可更改代码中开房次数 i 
- 运行`friendFight` 
`python friendFight.py`
- 开始自动对战，题目信息保存在 zhdtw库中的quizs集合中
![](https://www.ggbond.cc/wp-content/uploads/2018/03/friendfight.png)

### 三 排位辅助
- 同上，运行`rankingFight.py` 设置手机代理，进入排位，可看到屏幕输出答案. 题库没有的题目会保存

![](https://www.ggbond.cc/wp-content/uploads/2018/03/rankingfight.png)


## More
- 参考文档: [mitmproxy](https://mitmproxy.org/docs/latest/)
- 只做了个简单的辅助，不是很爽. 1.实现自动选择(拦截数据后直接发送choose请求)，2.修改返回数据，指示答案.(后台会验证magic和sign，返回数据的时候按照friendFight.py中逻辑生成) (为了保持游戏性，最好是把题库打印出来背完 :)


- 再次声明，仅供交流学习，勿做非法用途
 ![](https://www.ggbond.cc/wp-content/uploads/2018/03/notice.png)