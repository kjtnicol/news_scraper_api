from unittest import TestCase
import pandas as pd
from news_collector.dao.mongodb_dao import MongoDbDao
from news_collector import app_config


class TestMongoDbDao(TestCase):
    def test_upload_df(self):
        test_scraped_csv = 'testdata/news_scraped.csv'
        test_df = pd.read_csv(test_scraped_csv)
        dao = MongoDbDao(app_config.db_conn_string)

        dao.upload_df(test_df, app_config.collection_name)

        result = dao.get_items_by_urls(test_df['url'].tolist(), app_config.collection_name)
        result_df = pd.DataFrame(list(result))

        test_df_ordered = test_df.set_index('url').sort_index()
        result_df_ordered = result_df.set_index('url').sort_index()

        dao.delete_items_by_urls(test_df['url'].tolist(), app_config.collection_name)

        self.assertTrue(result_df_ordered.drop('_id', axis=1)[test_df_ordered.columns].equals(test_df_ordered))

    def test_get_items_by_keyword(self):
        dao = MongoDbDao(app_config.db_conn_string)
        keyword = 'Nadal'

        result = dao.get_items_by_keyword(app_config.collection_name, keyword.lower())
        result_df = pd.DataFrame(list(result))

        for article_text in result_df['article_text'].tolist():
            self.assertTrue(keyword in article_text)
