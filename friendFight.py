import requests
import hashlib
import time
import json

headers = {
    'content-type': 'application/x-www-form-urlencoded',
}

userInfo = {
    'player1':{
        'uid': '玩家1号的uid',
        'token': '玩家1号的token'
    },
    'player2':{
        'uid': '玩家2号的token',
        'token': ''
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
fightResultUrl = 'https://question-zh.hortor.net/question/bat/fightResult'

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
        'uid' : userInfo[player]['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,player)
    resp = session.post(url=intoRoomUrl,data=params,headers=headers)
    try:
        jdata = json.loads(resp.text)
        roomID = jdata.get('data')['roomId']
        print('进入房间成功...')
    except:
        print(resp.text)
        print('进入房间失败...')
        leaveRoom('player1')
        leaveRoom('player2')

def leaveRoom(player):
    params = {
        'roomID' : roomID,
        'uid' : userInfo[player]['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,player)
    resp = session.post(url=leaveRoomUrl,data=params,headers=headers)
    try:
        jdata = json.loads(resp.text)
        if jdata.get('errcode') == 0:
            print(player + ' 退出房间成功...')
    except:
        print(resp.text)
        print(player + ' 退出房间失败...')

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
    try :
        jdata = json.loads(resp.text)
        if jdata.get('errcode') == 0:
            print(player + ' 选择成功...')
            return jdata.get('data')
    except:
        print(player + ' 选择失败...')

def fightResult(player):
    params = {
        'roomID' : roomID,
        'type' : 0,
        'uid' : userInfo[player]['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,player)
    resp = session.post(url=fightResultUrl,data=params,headers=headers)
    try:
        jdata = json.loads(resp.text)
        if jdata.get('errcode') == 0:
            print(player + ' 获取结果成功...')
            return jdata.get('data')
    except:
        print(player + ' 获取结果失败...') 

def genMagic(optionList):
    optionList.sort()
    originStr = optionList[0]+optionList[1]+optionList[2]+optionList[3]
    m = hashlib.md5()   
    m.update(originStr.encode(encoding='utf-8'))
    return m.hexdigest()

def startAnswer():
    for i in range(1,6):
        #请求数据与接收到数据延时
        cfTime = nowTime()
        quizInfo = findQuiz(i)
        cfTime = nowTime() - cfTime
        print(quizInfo)   
        time.sleep(0.5)
        magic = genMagic(quizInfo['options'])
        chooseResult = choose('player1',i,1,cfTime,magic)
        choose('player2',i,2,cfTime+10,magic)
        print(chooseResult)

if __name__ == '__main__':
    intoRoom('player1')
    intoRoom('player2')
    beginFight()
    startAnswer()
    fightResult('player1')
    fightResult('player2')
    leaveRoom('player1')
    leaveRoom('player2')