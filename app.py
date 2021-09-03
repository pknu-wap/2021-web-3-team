from flask import Flask, redirect,render_template,url_for,request,session
from flask_mail import Mail, Message #설치 필요 pip install Flask-Mail
from DB_handler import DBModule;
from random import *
import datetime
from collections import OrderedDict

DB = DBModule()
app = Flask(__name__)
app.secret_key = 'WAP_003789632145'

mail = Mail(app)  
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'user@gmail.com'  
app.config['MAIL_PASSWORD'] = '*****'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
otp = randint(000000,999999)

#홈
@app.route('/',methods=["GET", "POST"])
def main():
    if 'login' in session:
        id =session['login']
        return render_template('main.html', name = id)
    return render_template('main.html')
    
#회원가입
@app.route('/join', methods=['GET', 'POSt'])
def join():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['password']
        nickname = request.form['nickname']
        university = request.form.get('select1')
        email = session['email']

        DB.nickname_check(nickname)
        # 아이디 중복 방지, 닉네임 중복방지
        if DB.IDcheck(id) or DB.nickname_check(nickname):
            return redirect(url_for('join'))
        else:
            if DB.join(id,pw,nickname,university,email):
                return redirect(url_for('login'))
            else:
                return render_template('join.html')

    return render_template('join.html')

#이메일 인증1 -> @pknu.ac.kr @ks.ac.kr -> javascript에서 특정 단어를 포함하는지 확인
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        per_email = request.form['email']
        if not per_email:
            return render_template('auth.html')
        else:
            msg = Message('DAON OTP 인증번호 발송',sender = 'daon@gmail.com', recipients = [per_email])  
            msg.body = str(otp)  
            mail.send(msg)
            session['email'] = per_email  
            return render_template('verify.html')

    return render_template('auth.html')

#이메일 인증2
@app.route('/validate',methods=['GET', 'POSt'])   
def validate():  
    user_otp = request.form['otp']  
    if otp == int(user_otp):  
        return render_template('join.html')
    return render_template('auth.html')

#로그인
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        
        if DB.login(id, pw):
            session['login'] = id
            session['nickname'] = DB.nickname_get(id)
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

#로그아웃
@app.route("/logout")
def logout():
    session.pop("login", None)
    return redirect(url_for("main"))

# 전체 게시물 목록 보기
@app.route('/post',methods=["GET", "POST"])
def post():
    post_list = DB.post_list()
    if 'login' in session:
        return render_template('post.html', 
        post_list = OrderedDict(sorted(post_list.items(), key=lambda x: x[0], reverse=True)).items()) # 날짜 시간 순서대로
    else:
        return render_template('login.html')

# 내가 작성한 게시물 목록 보기
@app.route('/mypost')
def mypost():
    nickname = session['nickname']
    mypost_list = DB.mypost_list(nickname)
    return render_template('mypost.html', 
    mypost_list=OrderedDict(sorted(mypost_list.items(), key=lambda x: x[1]['Date'], reverse=True)).items()) # 날짜 시간 순서대로

# 게시물 내용 보기
#@app.route('post/<string:nickname><string:title>')
#def post_detail(nickname, title):
    pass

@app.route('/write_page',methods=["GET", "POST"])
def write_page():
    return render_template('writting.html')
    
@app.route('/write',methods=["GET", "POST"])
def write():
    if request.method == 'POST':       
        title=request.form['title']
        content=request.form['content']

        if(DB.write(session['nickname'],title,content)):
            return redirect(url_for('post'))
        else:                    
            return render_template('writtingpage.html')
    return render_template('writtingpage.html')

if __name__ =='__main__':
    app.run(debug=True)