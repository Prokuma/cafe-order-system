from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.RnBCafe
order_collection = db.order
auth_collection = db.auth

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/<int:table_num>', methods=['GET', 'POST'])
def select_table(table_num):
    if request.method == 'POST':
        order = {
            "table": table_num,
            "order": request.form.getlist('order')
        }
        order_id = str(order_collection.insert(order))
        return render_template('done.html', order_id=order_id)
    else:
        return render_template('table.html', num=table_num) #table page

@app.route('/management')
def management():
    #if not logined, login page, if logined management page
    return ""

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        auth = auth_collection.find_one({'id': request.form.get('id')})
        if auth['password'] == request.form.get('password'):
            session['id'] = request.form.get('id')
            return redirect(url_for('management'))
        else:
            return '아이디 또는 비밀번호가 틀립니다'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

app.secret_key = 'SDJFPASHVAJDPFNASV0934ursdfnfasz=@#$@%#@$%'