from flask import Flask, redirect,render_template,url_for,request,session
from DB_handler import DBModule;

DB = DBModule()
app = Flask(__name__)
app.secret_key = 'WAP_003789632145'

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
        confirm = request.form['confirm-pw']
        
        # 아이디 중복 방지
        if DB.IDcheck(id) :
            return redirect(url_for('join'))
        else:
            if DB.join(id,pw,nickname,university):
                return redirect(url_for('login'))
            else:
                return render_template('join.html')

    return render_template('join.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        
        if DB.login(id, pw):
            session['login'] = id
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop("login", None)
    return redirect(url_for("main"))

if __name__ =='__main__':
    app.run(debug=True)