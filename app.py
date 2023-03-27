from flask import Flask, render_template, request, jsonify
from bson.objectid import ObjectId
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.wmg0vlp.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('post.html')


@app.route("/yummy/search", methods=['POST'])
def yummy_search():
    searching_value = request.form['searching_value']
    all_yummies = list(db.yummy.find({'title': {'$regex': searching_value}}))
    for i, _ in enumerate(all_yummies):
        all_yummies[i]['_id'] = str(all_yummies[i]['_id'])
    return jsonify({'result':all_yummies})


    
    

@app.route("/yummy/post", methods=["POST"])
def yummy_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.find('h1', 'restaurant-details__heading--title').get_text()
    og_description = soup.find('div', 'restaurant-details__description--text').get_text()
    address = soup.find('li','restaurant-details__heading--address').get_text()
    country = address.split(',')[-1]
    city = address.split(',')[-2]
    address = address.split(',')[:-2]

   
    doc = {
        'title':title,
        'desc' : og_description,
        'image' : og_image,
        'address' : address,
        'country' : country,
        'city' : city,
        'comment' : comment_receive,
        'star' : star_receive
    }
    
    db.yummy.insert_one(doc)


    return jsonify({'msg':'저장 완료!'})

@app.route("/yummy", methods=["GET"])
def yummy_get():
    all_yummies = list(db.yummy.find({}))
    for i, _ in enumerate(all_yummies):
        all_yummies[i]['_id'] = str(all_yummies[i]['_id'])

    return jsonify({'result':all_yummies})

@app.route("/movie/delete/<id>", methods=["DELETE"])
def movie_delete(id):
    db.yummy.delete_one({'_id': ObjectId(id)})

    return jsonify({'msg': '삭제되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)