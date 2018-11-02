import flask
from bson.json_util import dumps
from flask import request

from news_collector.dao.mongodb_dao import MongoDbDao
from news_collector import app_config

app = flask.Flask(__name__)
app.config["DEBUG"] = app_config.debug_mode

dao = MongoDbDao(app_config.db_conn_string)

@app.route('/', methods=['GET'])
def home():
    link_string = "http://%s:%s/api/articles/bbc?keyword=Google" % (app_config.host_name, app_config.port)
    return '''<h1>BBC News Article API examples</h1>
<p>You can retrieve article data with a keyword "Google" from the following link.</p>
<a href="%s">%s</a>
''' % (link_string, link_string)

@app.route(app_config.api_url, methods=['GET'])
def api_keyword():
    if 'keyword' in request.args:
        keyword = request.args['keyword']
    else:
        return "Error: No keyword field provided. Please specify a keyword."

    results = dao.get_items_by_keyword(app_config.collection_name, keyword)

    return dumps(results)

