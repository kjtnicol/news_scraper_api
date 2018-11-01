import flask
from bson.json_util import dumps
from flask import request

from news_collector.dao.mongodb_dao import MongoDbDao
from news_collector import app_config

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dao = MongoDbDao(app_config.db_conn_string)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>BBC News Article API examples</h1>
<p></p>'''

@app.route('/api/articles/bbc', methods=['GET'])
def api_keyword():
    if 'keyword' in request.args:
        keyword = request.args['keyword']
    else:
        return "Error: No keyword field provided. Please specify a keyword."

    results = dao.get_items_by_keyword('bbc_articles', keyword)

    return dumps(results)

