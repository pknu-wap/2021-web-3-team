from flask import Flask, redirect,render_template,url_for,request,session, flash
from DB_handler import DBModule

DB = DBModule()
app = Flask(__name__)
app.secret_key = 'WAP_003'

@app.route('/',methods=["GET", "POST"])
def main():
    return render_template('main.html')

@app.route('/home')
def home():
    id =session['login_S']
    return render_template('home.html', name = id)

@app.route('/register', methods=['GET', 'POSt'])
def register():
    if request.method == 'POST':
        id = request.form['regi_id']
        pw = request.form['regi_pw']
        if not id or not pw:
            return redirect(url_for('register'))
        else:
            if DB.register(id,pw):
                return redirect(url_for('register'))
            else:
                return redirect(url_for('main'))

    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['username']
        pw = request.form['password']
        if not id or not pw:
           return redirect(url_for('login'))
        else: 
            if DB.login(id, pw):
                session['login_S'] = id
                return redirect(url_for('home'))
            else:
                flash("아이디가 없거나 비밀번호가 틀립니다.")
                return redirect(url_for('login'))

    return render_template('login.html')

if __name__ =='__main__':
    app.run(debug=True)
