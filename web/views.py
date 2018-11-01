import calendar
from flask_appbuilder import expose, has_access
from flask import url_for, make_response, Response, g
from flask_appbuilder import ModelView
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_babel import lazy_gettext as _
from news_collector.web import appbuilder
from .models import BbcArticles


class BbcArticlesView(ModelView):
    datamodel = MongoEngineInterface(BbcArticles)
    list_columns = ['title', 'url', 'created_time', 'tag_text', 'tag_url', 'article_text']


appbuilder.add_view(BbcArticlesView, "List Articles", icon = "fa-folder-open-o",category = "Contacts",
                category_icon = "fa-envelope")