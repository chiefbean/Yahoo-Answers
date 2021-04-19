from flask import Flask, render_template, request
from flask.json import JSONEncoder
import pymongo
from bson import json_util, ObjectId
import json

app = Flask(__name__)

database = pymongo.MongoClient("mongodb://localhost:27017/")
table = database["yahoo"]["qs"]

class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)

app.json_encoder = MongoJSONEncoder

cats = [
    'Arts & Humanities',
    'Beauty & Style',
    'Business & Finance',
    'Cars & Transportation',
    'Computers & Internet',
    'Consumer Electronics',
    'Dining Out',
    'Education & Reference',
    'Entertainment & Music',
    'Environment',
    'Family & Relationships',
    'Food & Drink',
    'Games & Recreation',
    'Health',
    'Home & Garden',
    'Local Businesses',
    'News & Events',
    'Pets',
    'Politics & Government',
    'Pregnancy & Parenting',
    'Science & Mathematics',
    'Social Science',
    'Society & Culture',
    'Sports',
    'Travel',
    'Yahoo Products'
]

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/category')
def category(page=1):
    cat = cats[int(request.args.get('c'))]
    data = table.find({"category": cat})
    return render_template('category.html', category=cat, data=data)

@app.route('/question')
def question():
    quuid = request.args.get('q')
    question = table.find_one({"_id": ObjectId(quuid)})
    return render_template('question.html', question=question, num=len(question['answers']), cat=cats.index(question['category']))

@app.route('/search')
def search():
    search = request.args.get('q')
    data = table.find({"$or": [{"title": {'$regex': str(search), '$options': 'i'}}, {"question": {'$regex': search, '$options': 'i'}}]})
    return render_template('search.html', search=search, data=data)

if __name__ == '__main__':
    app.run()