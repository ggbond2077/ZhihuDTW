import requests
import hashlib
import time
import json
from pymongo import MongoClient

headers = {
    'content-type': 'application/x-www-form-urlencoded',
}

userInfo = {
    'player1':{
        'uid': '玩家1号的uid',
        'token': '玩家1号的token'
    },
    'player2':{
        'uid': '玩家2号的uid',
        'token': '玩家2号的token'
    }
}

session = requests.session()
roomID = -1
#命中题库次数
successTime = 0
#时间戳生成
nowTime = lambda:int(round(time.time() * 1000))

#mongodb
conn = MongoClient('localhost',27017)
quizSet = conn.zhdtw.quizs

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
        print(player + ' 进入房间成功...')
    except:
        print(resp.text)
        print(player + ' 进入房间失败...')
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
    try:
        jdata = json.loads(resp.text)
        if jdata.get('errcode') == 0:
            print('开始好友对战...')
    except:
        print(resp.text)

def findQuiz(quizNum):
    params = {
        'roomID' : roomID,
        'quizNum' : quizNum,
        'uid' : userInfo['player1']['uid'],
        't' : nowTime()
    }
    params['sign'] = genSign(params,'player1')
    resp = session.post(url=findQuizUrl,data=params,headers=headers)
    try:
        jdata = json.loads(resp.text)
        if jdata.get('errcode') == 0:
            print('获取题目成功...')
            return jdata.get('data')
        else:
            print('获取题目失败')
    except:
        print(resp.text)
    
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
        print(resp.text)

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
        print(resp.text)

def genMagic(optionList):
    optionList.sort()
    originStr = optionList[0]+optionList[1]+optionList[2]+optionList[3]
    m = hashlib.md5()   
    m.update(originStr.encode(encoding='utf-8'))
    return m.hexdigest()

def startAnswer():
    global successTime
    for i in range(1,6):
        #请求数据与接收到数据延时
        cfTime = nowTime()
        quizInfo = findQuiz(i)
        cfTime = nowTime() - cfTime

        time.sleep(0.1)

        optionList = quizInfo['options']
        quiz = quizInfo['quiz']
        option = 1
        #题库查找题目
        #print(quiz)
        localQuiz = quizSet.find_one('quiz',quiz)
        if localQuiz:
            successTime += 1
            for i in range(0,4):
                if(optionList[i] == localQuiz['answer']):
                    option = i+1
                    break

        magic = genMagic(optionList.copy())
        chooseResult = choose('player1',i,option,cfTime,magic)
        choose('player2',i,2,cfTime+10,magic)
        if not localQuiz:
            quizModel = {}
            quizModel['quiz'] = quiz
            quizModel['options'] = optionList
            quizModel['school'] = quizInfo['school']
            quizModel['type'] = quizInfo['type']
            quizModel['typeID'] = quizInfo['typeID']
            quizModel['contributor'] = quizInfo['contributor']
            quizModel['answer'] = optionList[chooseResult['answer']-1]
            quizSet.insert_one(quizModel)
        #print(optionList[chooseResult['answer']-1]) 
if __name__ == '__main__':
    #自行修改开房对战次数 i
    i = 100
    gameTime = 0
    while(i > 0):
        roomID = -1
        intoRoom('player1')
        intoRoom('player2')
        beginFight()
        startAnswer()
        fightResult('player1')
        fightResult('player2')
        leaveRoom('player1')
        leaveRoom('player2')
        gameTime += 1
        print('游戏次数 %d /命中题库次数 %d ' % (gameTime,successTime))
        time.sleep(1)
        i = i - 1
    conn.close()