# ZhihuDTW

- 知乎答题王自动开房答题 保存题目

- 参考头脑王者项目 https://github.com/lyh2668/TNWZ

- 博客 : [获取知乎答题王题库](https://www.ggbond.cc/知乎答题王/)

*免责声明：仅供学习交流使用，请勿进行非法用途*

参考TNWZ项目，准备学习撸一个python版的 ， 无奈头脑王者违规下线. 时隔半月,(全新)知乎答题王上线...

## 环境要求
- python3
- mongodb 

## 使用

### 1 安装代理工具
- 参考别处 安装 fiddler、charles、anyproxy ,设置手机代理... 
进入知乎答题王，可抓取到`question/player/login` 请求，返回参数最后有token和uid

### 2.clone项目
```
git clone https://github.com/ctguggbond/ZhihuDTW
cd ZhihuDTW
#安装依赖
pip3 install -r requirements.txt 
```
### 3 开房对战
在friendFight.py 填入player1 player2的uid和token
`python friendFight.py` 开始对战.

## More
- 题目拿到了就下来就是如何排位赛了，可以全自动排位，可以修改返回数据，指示答案，也可以在电脑显示答案.
- 过年火车票好难买...

- 再次声明，进攻交流学习，勿做非法用途
 ![](https://www.ggbond.cc/wp-content/uploads/2018/03/notice.png)