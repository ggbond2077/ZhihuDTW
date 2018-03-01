import requests
import hashlib
import time
import json

headers = {
    'charset': 'utf-8',
    'Accept-Encoding': 'gzip',
    'content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1; M3s Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.2.1240(0x26060235) NetType/WIFI Language/zh_CN MicroMessenger/6.6.2.1240(0x26060235) NetType/WIFI Language/zh_CN'
}

userInfo = {
    'player1':{
        'uid': '175926088',
        'token': 'fe12f894b266401493330744c3f8a6d8'
    },
    'player2':{
        'uid': '215584489',
        'token': '  '
    }
}

roomID = -1
#时间戳生成
nowTime = lambda:int(round(time.time() * 1000))
session = requests.session()
intoRoomUrl = 'https://question-zh.hortor.net/question/bat/intoRoom'
leaveRoomUrl = 'https://question-zh.hortor.net/question/bat/leaveRoom'
beginFightUrl = 'https://question-zh.hortor.net/question/bat/beginFight'
findQuizUrl = 'https://question-zh.hortor.net/question/bat/findQuiz'
chooseUrl = 'https://question-zh.hortor.net/question/bat/choose'
showLoginUrl = 'https://question-zh.hortor.net/question/role/showLogin'

#生成签名
def genSign(params,player):
    tempParams = params.copy()
    tempParams['token'] = userInfo[player]['token']+userInfo[player]['uid']
    tempParams = sorted(tempParams.items(), key=lambda e:e[0])
    originStr = ''
    for key, value in tempParams:
        originStr = originStr + key + '=' + str(value)
    m = hashlib.md5()   
    m.update(originStr.encode(encoding='utf-8'))
    return m.hexdigest()
    
def intoRoom(player):
    global roomID
    print(roomID)
    params = {
        'roomID' : roomID,
        'uid' : userInfo['player1']['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,player)
    resp = session.post(url=intoRoomUrl,data=params,headers=headers)
    print(resp.text)
    try:
        jdata = json.loads(resp.text)
        roomID = jdata.get('data')['roomId']
    except:
        leaveRoom('player1')
        leaveRoom('player2')

def leaveRoom(player):
    params = {
        'roomID' : roomID,
        'uid' : userInfo['player1']['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,player)
    resp = session.post(url=leaveRoomUrl,data=params,headers=headers)
    jdata = json.loads(resp.text)
    print(jdata)
   
def beginFight():
    params = {
        'roomID' : roomID,
        'uid' : userInfo['player1']['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,'player1')
    resp = session.post(url=beginFightUrl,data=params,headers=headers)
    jdata = json.loads(resp.text)
    if jdata.get('errcode') == 0:
        print('开始好友对战...')

def findQuiz(quizNum):
    params = {
        'roomID' : roomID,
        'quizNum' : quizNum,
        'uid' : userInfo['player1']['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,'player1')
    resp = session.post(url=findQuizUrl,data=params,headers=headers)
    jdata = json.loads(resp.text)
    if jdata.get('errcode') == 0:
        print('获取题目成功...')
        return jdata.get('data')
    else:
        print('获取题目失败')
    
def choose(player,quizNum,option,cfTime,magic):
    params = {
        'roomID' : roomID,
        'uid' : userInfo[player]['uid'],
        't' : nowTime(),
        'option' : option,
        'quizNum': quizNum,
        'cfTime': cfTime,
        'ccTime' : nowTime(),
        'magic' : magic
    }
    params['sign'] = genSign(params,player)
    resp = session.post(url=chooseUrl,data=params,headers=headers)
    jdata = json.loads(resp.text)
    if jdata.get('errcode') == 0:
        print('选择成功...')
        return jdata.get('data')
    else:
        print('选择失败...')

def genMagic(optionList):
    optionList.sort()
    originStr = optionList[0]+optionList[1]+optionList[2]+optionList[3]
    m = hashlib.md5()   
    m.update(originStr.encode(encoding='utf-8'))
    return m.hexdigest()

def showLogin():
    params = {
        'roomID' : roomID,
        'quizNum' : quizNum,
        'uid' : userInfo['player1']['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,'player1')
    resp = session.post(url=findQuizUrl,data=params,headers=headers)
    jdata = json.loads(resp.text)
    
def startAnswer():
    for i in range(1,6):
        #请求数据与接收到数据延时
        cfTime = nowTime()
        quizInfo = findQuiz(i)
        cfTime = nowTime() - cfTime
        print(quizInfo)   
        magic = genMagic(quizInfo['options'])
        chooseResult = choose('player1',i,1,cfTime,magic)
        choose('player2',i,2,cfTime+10,magic)

        print(chooseResult)
if __name__ == '__main__':
    intoRoom('player1')
    intoRoom('player2')
    beginFight()
    startAnswer()