#-*- coding: utf-8 -*-
import hashlib
import getpass
from pymongo import MongoClient

id = raw_input("등록할 아이디를 입력하세요: ")
pw = getpass.getpass("등록할 비밀번호를 입력하세요(입력하는 것은 보이지 않습니다): ")

client = MongoClient('localhost', 27017)
db = client.RnBCafe
member_collection = db.member

if member_collection.find_one({'id': id}) is None:
    member_collection.insert({'id': id, 'password': hashlib.sha512(pw).hexdigest()})
    print "성공적으로 등록이 완료되었습니다!"
else:
    print "이미 있는 아이디입니다."