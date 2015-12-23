#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import datetime
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.RnBCafe
order_collection = db.order
auth_collection = db.auth

@app.errorhandler(404)
def page_not_found(error):
    return render_template(error.html, msg='404 Not Found')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/<int:table_num>', methods=['GET', 'POST'])
def select_table(table_num):
    if request.method == 'POST':
        order = {
            "table": table_num,
            "order": request.form.getlist('order'),
            "time": datetime.datetime.utcnow()
        }
        order_id = str(order_collection.insert(order))
        return render_template('done.html', order_id=order_id)
    else:
        return render_template('table.html', num=table_num)

@app.route('/management')
def management():
    if session['id'] is None:
        return redirect(url_for('login'))
    else:
        return render_template('management.html')

@app.route('/management/order')
def order_info():
    if session['id'] is not None:
        if request.get_json()['new']:
            order = order_collection.find().limit(1).sort('_id', pymongo.DESCENDING)[0]
            return jsonify(
                success=True,
                data={
                    'err': False,
                    'data': order,
                    'msg': 'Successfully respond'
                }
            )
        else:
            orders = order_collection.find().limit(20).skip((int(request.get_json()['page']-1))*20)
            return jsonify(
                success=True,
                data={
                    'err': False,
                    'data': orders,
                    'page': int(request.get_json()['page']),
                    'msg': 'Successfully respond '
                }
            )
    else:
        return jsonify(
            success=True,
            data={
                'err': True,
                'msg': 'Not Permission'
            }
        )

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        auth = auth_collection.find_one({'id': request.form.get('id')})
        if auth['password'] == request.form.get('password'):
            session['id'] = request.form.get('id')
            return redirect(url_for('management'))
        else:
            return render_template('error.html', msg='ID또는 암호가 일치하지 않습니다.')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

app.secret_key = 'Secret Key'