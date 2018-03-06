from mitmproxy import http
import pymongo
import json

def response(flow: http.HTTPFlow) -> None:
    global quizInfo

    conn = pymongo.MongoClient('localhost',27017)
    quizSet = conn.zhdtw.quizs
    option = requestUrl.split('/')[-1]
    resp = flow.response.get_content()
    #print(option)
    if option == 'findQuiz':
        try:
            jdata = json.loads(resp.decode('utf-8'))
            quiz = jdata['data']['quiz']
            if quiz :
                quizResult = quizSet.find_one({'quiz':quiz},{'answer':1,'_id':0})
                print(quiz)
                if quizResult:
                    print('答案: ' + quizResult['answer'])
                    quizInfo = {}
                else:
                    print('本地库没有答案')
                    quizInfo = jdata['data']
        except Exception as e:
            print(str(e))
            conn.close()
            
    elif option == 'login':
        try:    
            jdata = json.loads(resp.decode('utf-8'))
            print('token : ' + jdata['data']['token'])
            print('uid : ' + str(jdata['data']['uid']))
        except:
            #print(resp)
            print('登录数据获取失败')
    elif option == 'choose' and quizInfo:
        print('保存题目')
        try:
            jdata = json.loads(resp.decode('utf-8'))
            answer = jdata['data']['answer']
            quizModel = {}
            quizModel['quiz'] = quizInfo['quiz']
            quizModel['options'] = quizInfo['options']
            quizModel['school'] = quizInfo['school']
            quizModel['type'] = quizInfo['type']
            quizModel['typeID'] = quizInfo['typeID']
            quizModel['contributor'] = quizInfo['contributor']
            quizModel['answer'] = quizModel['options'][answer-1]
            print(quizModel)
            quizSet.insert_one(quizModel)
        except Exception as e:
            print(str(e))
            conn.close()
    conn.close()

def request(flow: http.HTTPFlow) -> None:
    global requestUrl
    requestUrl = flow.request.path