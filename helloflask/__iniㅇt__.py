from flask import Flask

app = Flask(__name__)
app.debug=True #오류 알려줌

@app.route("/")#아무것도 안주는 것. 처음 시랭
def helloworld():
    return "hi python"

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True)