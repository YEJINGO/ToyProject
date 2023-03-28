from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://matjib:ALw2P06QtN3qzY6A@cluster0.j3vhkcc.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.matjib

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
# import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
import hashlib

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/yummy/sign_up', methods=['POST'])
def yummy_sign_up():
    user_id_receive = request.form['user_id_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        'user_id': user_id_receive,
        'pw': password_hash,
    }
    db.user.insert_one(doc)

    return jsonify({'result': '회원 가입 완료!'})

@app.route('/yummy/check_dup', methods=['POST'])
def yummy_check_dup():
    result = ""
    user_id_receive = request.form['user_id_give']
    user = db.user.find_one(user_id_receive)
    if user == user_id_receive:
        result = "again"
    else:
        result = "pass"

    return jsonify({'result':result})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)