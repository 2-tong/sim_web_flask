# -*- coding: utf-8 -*- #
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import url_for
from flask import redirect
from sqlConnecter import myDB
from CNSegment import CNSegment
import json
import wordSim

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login",methods=["post",'get'])
def login():
    mydb = myDB()
    uid = request.cookies.get('userID')

    if uid == None:
        name=request.form['username']
        psw = request.form['password']

        uid=mydb.checkpsw(name,psw)
    else:
        uid = int(uid)
    if uid==-1:
        worngstr='login failed'
        return render_template('index.html',wrong_info=worngstr)
    else:

        scorelist=mydb.get_all_teacherScore(uid)

        respon = Response(render_template('table.html',scores=scorelist))
        respon.set_cookie("userID",str(uid))

        return respon

@app.route("/form",methods=["post",'get'])
def get_form():

    uid = request.cookies.get('userID')
    if uid == None:
        return redirect(url_for('hello'))

    return  render_template('login.html')

@app.route("/putans",methods=["post",'get'])
def putans():
    uid = request.cookies.get('userID')
    if uid == None:
        return redirect(url_for('hello'))
    uid=int(uid)
    answer = request.form.get('first')
    name = request.form.get('second')

    cutool=CNSegment()
    cutword=cutool.cut(answer)[0]
    db = myDB()
    q_id = db.addQuestion(answer, name, uid)
    redict={"qid":q_id,"wlist":cutword}
    Jstr=json.dumps(redict)

    return Jstr

@app.route("/putwei",methods=["post",'get'])
def putwei():
    str=request.data
    ls=json.loads(str)
    quesid=ls["ques_id"]
    wwLst=ls["wList"]
    db=myDB()
    if db.addWeight(wwLst,quesid):
        return """{"status":"成功"}"""
    else:
        return """{"status":"失败"}"""

@app.route("/stuanswer",methods=["post",'get'])
def getsocre():
    uid = request.cookies.get('userID')
    if uid == None:
        return redirect(url_for('hello'))
    db=myDB()
    queslist=db.getquesbyuid(int(uid))

    return render_template('getscore.html',quesList=queslist)

@app.route("/stuans",methods=["post",'get'])
def putstudentans():
    data=request.data
    j=json.loads(data)

    st=wordSim.put_stu_answer(j['quesid'],j['answers'])
    return """{"status":"%s"}"""%(st)



if __name__=="__main__":
    app.run('127.0.0.1',8080,True)

