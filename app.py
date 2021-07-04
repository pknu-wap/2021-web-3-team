from flask import Flask, redirect,render_template,url_for,request,session
from DB_handler import DBModule;
from flask_mail import *
from random import *  

DB = DBModule()
app = Flask(__name__)
app.secret_key = 'WAP_003789632145'

mail = Mail(app)  
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'username@gmail.com'  
app.config['MAIL_PASSWORD'] = '*************'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
otp = randint(000000,999999)   

@app.route('/',methods=["GET", "POST"])
def main():
    if 'login' in session:
        id =session['login']
        return render_template('main.html', name = id)
    return render_template('main.html')


@app.route('/join', methods=['GET', 'POSt'])
def join():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['password']
        nickname = request.form['nickname']
        university = request.form.get('select1')

        DB.nickname_check(nickname)
        # 아이디 중복 방지, 닉네임 중복방지
        if DB.IDcheck(id) or DB.nickname_check(nickname):
            return redirect(url_for('join'))
        else:
            if DB.join(id,pw,nickname,university):
                return redirect(url_for('login'))
            else:
                return render_template('join.html')

    return render_template('join.html')

#이메일 인증1 -> @pknu.ac.kr @ks.ac.kr -> javascript에서 특정 단어를 포함하는지 확인
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form['email']
        if not email:
            return render_template('auth.html')
        else:
            return render_template('verify.html')

    return render_template('auth.html')

#이메일 인증2
@app.route('/verify', methods=['GET', 'POSt'])
def verify():
    email = request.form["email"]   
    msg = Message('OTP',sender = 'username@gmail.com', recipients = [email])  
    msg.body = str(otp)  
    mail.send(msg)  
    return render_template('verify.html')

#이메일 인증3
@app.route('/validate',methods=['GET', 'POSt'])   
def validate():  
    user_otp = request.form['otp']  
    if otp == int(user_otp):  
        return render_template('join.html')
    return render_template('auth.html')

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

@app.route("/logout")
def logout():
    session.pop("login", None)
    return redirect(url_for("main"))

@app.route('/post',methods=["GET", "POST"])
def post():
    if 'login' in session:
        post_list = DB.post_list()
        
        return render_template('post.html', post_list=post_list.items())
    else:
        return render_template('login.html')

# 게시물 내용 보기
@app.route('post/<string:nickname><string:title>')
def post_detail(nickname, title):
    pass


@app.route('/write_page',methods=["GET", "POST"])
def write_page():
    return render_template('write.html')
    

@app.route('/write',methods=["GET", "POST"])
def write():
    if request.method == 'POST':       
        title=request.form['title']
        contents=request.form['contents']

        if(DB.write(session['nickname'],title,contents)):
            return redirect(url_for('post'))
        else:
            return redirect(url_for('write'))

@app.route('/mypage',methods=["GET", "POST"])
def mypage():
    return render_template('mypage.html')

if __name__ =='__main__':
    app.run(debug=True)