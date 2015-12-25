#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import datetime
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

#메뉴
menu = {
        '메뉴1'.decode('utf-8'): 3000,
        '메뉴2'.decode('utf-8'): 5000,
        '메뉴3'.decode('utf-8'): 6000
       }

#DB연결 등
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.RnBCafe
order_collection = db.order
auth_collection = db.auth

#메인 페이지
@app.route('/')
def index():
    return render_template('main.html')

#GET:테이블별 주문 화면, POST:주문처리
@app.route('/table/<int:table_num>', methods=['GET', 'POST'])
def select_table(table_num):

    if request.method == 'POST':
        price = 0
        for i in request.form.getlist('order'):
            price = price + menu[i]

        order = {
            "table": table_num,
            "order": request.form.getlist('order'),
            "price": price,
            "time": datetime.datetime.utcnow()
        }
        order_id = str(order_collection.insert(order))
        return render_template('done.html', order_id=order_id)
    else:
        return render_template('table.html', num=table_num, menu=menu)

#관리 화면
@app.route('/management')
def management():
    if not ('id' in session):
        return redirect(url_for('login'))
    else:
        return render_template('management.html')

#REST API
#GET:주문관련 정보 얻어오기
#DELETE:주문 관련 정보 삭제
"""
Parameter 안내

1.요청
GET:
{'new': Bool, 'page': Int}
new:새로운 정보 하나만 얻어올것 인지, 그렇지 않을 것인지 설정
page:페이지. 처음은 1페이지, 20개 뛰어넘고 보는게 2페이지같은 형식으로 됨
DELETE:
{'order_id': String}
order_id:주문번호

2.응답
GET:
{'err': Bool, 'data': Array or Dictionary, 'msg': String, 'page': Int}
err:에러 유무
data:데이터, new가 True일경우 Dictionary로, False경우는 Array로 보내짐
msg:메시지
page:페이지
DELETE:
{'err': Bool, 'msg' :String, 'data': Bool}
err:에러유무
msg:메시지
data:없음을 표시하기 위해서 Bool로 False를 표시함
"""
@app.route('/management/order', methods=['GET','DELETE'])
def order_info():
    if 'id' in session:
        if request.method == 'GET':
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
        elif request.method == 'DELETE':
            if 'order_id' in request.get_json().keys():
                order_collection.delete_one({'_id': ObjectId(request.get_json()['order_id'])})
                return jsonify(
                    success=True,
                    data={
                        'err': False,
                        'data': False,
                        'msg': 'Successfully Deleted'
                    }
                )
            else:
                return jsonify(
                    success=True,
                    data={
                        'err': True,
                        'msg': 'Parameter Error'
                    }
                )
        else:
            return jsonify(
                    success=True,
                    data={
                        'err': True,
                        'msg': 'Not Support Method Type'
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

#GET:로그인 페이지, POST:로그인 처리
@app.route('/login', methods=['GET','POST'])
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

#로그아웃 처리
@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

#404페이지
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', msg='404 Not Found. 페이지를 찾을 수 없습니다.'.decode('utf-8')), 404

#500페이지
@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', msg='500 Internal Server Error. 서버오류로 인해 사용 할 수 없습니다.'.decode('utf-8')), 500


if __name__ == '__main__':
    #app.debug = True
    app.run()

#세션 암호화 키
app.secret_key = 'Secret Key'