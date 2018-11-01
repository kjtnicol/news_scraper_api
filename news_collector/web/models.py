from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField


class BbcArticles(Document):
    title = StringField(required=True, unique=True)
    url = StringField(required=True, unique=True)
    created_time = DateTimeField()
    tag_text = StringField()
    tag_url = StringField()
    article_text = StringField()

