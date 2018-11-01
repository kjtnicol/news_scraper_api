from pymongo import MongoClient
import json
import re
import pandas as pd


class MongoDbDao:
    def __init__(self, conn_string, db_name='scraped_news'):
        self.client = MongoClient(conn_string)
        self.db = self.client[db_name]

    def upload_df(self, df, collection_name):
        records = json.loads(df.T.to_json()).values()
        self.db[collection_name].insert_many(records)

    def get_items_by_keyword(self, collection_name, keyword):
        rgx = re.compile('.*' + keyword + '.*', re.IGNORECASE)  # compile the regex

        result = self.db[collection_name].find({'article_text': rgx})

        return result

if __name__ == "__main__":
    dao = MongoDbDao('mongodb+srv://isentia:isentia@cluster0-aoq9j.mongodb.net/admin')
    df = pd.read_csv('scraped_news.csv')
    dao.upload_df(df)