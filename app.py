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
        
        # 아이디 & 닉네임 중복 방지
        if DB.IDcheck(id) or DB.nickname_check(nickname):
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
            session['nickname'] = DB.nickname_get(id)
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop("login", None)
    return redirect(url_for("main"))

# @app.route("/post_list")
# def post_list():
#     post_list = DB.post_list()

#     return render_template("post_list.html", post_list = post_list)

if __name__ =='__main__':
    app.run(debug=True)