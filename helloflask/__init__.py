from flask import Flask,g, request, Response, make_response
#g= 접속자 수, 방문자 수 처리. 점진적 증가
#g의 값을 바꾸면서 정보 변경 가능
from datetime import datetime, date, timedelta
from flask import session

app=Flask(__name__)
app.debug=True #오류 알려줌


@app.route('/rc')
def rc():
    key=request.args.get('key')#token
    val=request.cookies.get(key)
    return "cookie["+key+"]="+val
#cookie[token]=abc

@app.route('/wc')
def wc():
    key=request.args.get('key')
    val=request.args.get('val')
    res=Response("SET COOKIE")
    res.set_cookie(key,val)
    return make_response(res)
#http://localhost:5000/wc?key=token&val=abc
#set cookie 출력.

def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str,fmt)
    return trans

@app.route("/dt")
def dt():
    datestr=request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)
#localhost:5000/dt?date=2019-05-2 우리나라 시간 형식: 2019-05-02 00:00:00
#localhost:5000/dt 우리나라 시간 형식: 2019-02-11
#default->date.today()


app.config['SERVER_NAME']='local.com:5000'
@app.route('/sd')
def helloworld_local():
    return "Hello Local.com!"
#local.com:5000/sd

@app.route('/sd',subdomain='g')
def helloworld3():
    return "Hello G.Local.com!"
#g.local.com:5000/sd

@app.route('/rp')
def rp():
    q=request.args.get('q')
    return "q= %s" %str(q)
#localhost:5000/rp?q=123 입력시 q=123출력

@app.route('/rp1')
def rp1():
    q=request.args.getlist('q')
    return "q=%s" %str(q)
#localhost:5000/rp?q=한글&q=eng 입력시 q=['한글','eng']

#response 정석의 방법
@app.route('/res1')
def res1():
    custom_res=Response("custom response",200,{'test':'ttt'})#response, ?, 헤더
    return make_response(custom_res)


@app.before_request#리퀘스트 요청 처리하기 전에 처리되는 것
def before_request():
    print("before_request!!")
    g.str="한글"
    #세션=한 유저. 브라우저 다르면 다른 유저로 인식
    #application context=접속하는 모든 사람들이 공유하는 공간
    #session context=한 유저에 대한 브라우저 영역(나만 사용. 나의 로그인 정보 등. 나의 정보)

@app.route("/gg")
def helloword2():
    return("helloworld! "+getattr(g,'str','111'))#사용할 문자 전달. '111'default

@app.route("/")#아무것도 안주는 것. 처음 시랭
def helloworld():
    return "hi python"

if __name__=="__main__":
    app.run()

#flask가 메모리와 프로세스로 떠있음. 네트워크 포트에서 요청 받음
#해당 포트를 플라스크가 지켜보고 있음(기본:5000번)
#라우터 모델 찾고 띄우는 놈이 필요함=start_helloflask.py
