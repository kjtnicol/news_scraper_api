from pymongo import MongoClient, TEXT, errors
import json
import re
import pandas as pd
from news_collector import app_config


class MongoDbDao:
    def __init__(self, conn_string, db_name=app_config.db_name):
        self.client = MongoClient(conn_string)
        self.db = self.client[db_name]

    def upload_df(self, df, collection_name):
        records = json.loads(df.T.to_json()).values()
        try:
            self.db[collection_name].insert_many(records, ordered=False)
        except errors.BulkWriteError as e:
            print(e.details['writeErrors'])

        """
        for idx, row in df.iterrows():
            self.db[collection_name].update(
                {'url': row['url']},
                # row.to_dict(),
                json.loads(row.to_json()),
                upsert=True
            )
        """

    def get_items_by_keyword(self, collection_name, keyword):
        rgx = re.compile('.*' + keyword + '.*', re.IGNORECASE)  # compile the regex

        result = self.db[collection_name].find({'article_text': rgx})

        return result

