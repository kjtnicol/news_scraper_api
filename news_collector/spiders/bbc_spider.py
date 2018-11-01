# -*- coding: utf-8 -*-
from datetime import datetime

import pandas as pd
import requests
import scrapy
from bs4 import BeautifulSoup
from readability import Document

from news_collector.dao.mongodb_dao import MongoDbDao
from news_collector import app_config


class BbcSpiderSpider(scrapy.Spider):
    name = 'bbc_spider'
    allowed_domains = ['www.bbc.com/']
    start_urls = [app_config.base_url]
    db_dao = MongoDbDao(app_config.db_conn_string)

    # Part of the URL list doesn't have base URL string, and the others have.
    # Thus, we need to make things all the same with this method.
    def reconcile_url_base(self, raw_urls):
        base_added_urls = [(self.start_urls[0] + x) if x[:4]!='http' else x for x in raw_urls ]

        return base_added_urls

    @staticmethod
    def clean_article_text(raw_text):
        cleaned = raw_text
        for del_str in app_config.removing_strings:
            cleaned = cleaned.replace(del_str, '')

        return cleaned

    def save_to_db(self, df):
        self.db_dao.upload_df(df, app_config.collection_name)

    def parse(self, response):
        # Extracting the content using css selectors
        urls = response.css('.media__link::attr(href)').extract()
        tag_texts = response.css('.media__tag::text').extract()
        tag_urls = response.css('.media__tag::attr(href)').extract()

        urls_cleansed = self.reconcile_url_base(urls)
        tag_urls_cleansed = self.reconcile_url_base(tag_urls)

        if len(urls_cleansed) != len(tag_urls_cleansed):
            raise Exception('Length Mismatch between article urls and tag urls')

        article_info_list = []

        for item in zip(urls_cleansed, tag_urls_cleansed, tag_texts):
            url = item[0]
            tag_url = item[1]
            tag_text = item[2]
            url_response = requests.get(url)
            doc = Document(url_response.text)
            soup = BeautifulSoup(url_response.text)
            date_info = soup.find('div', attrs={'class': 'date date--v2'})
            if date_info:
                created_time_epoch = int(date_info['data-seconds'])
                created_time_datetime = datetime.fromtimestamp(created_time_epoch)
            else:
                created_time_datetime = None

            title = doc.title()
            cleansed_body = doc.summary()
            body_soup = BeautifulSoup(cleansed_body)
            cleansed_article_text = ' '.join([x.get_text().replace('\n', ' ') for x in body_soup.find_all('p')])
            cleansed_article_text = self.clean_article_text(cleansed_article_text)

            scraped_info = {
                'title': title,
                'url': url,
                'created_time': created_time_datetime,
                'tag_url': tag_url,
                'tag_text': tag_text,
                'article_text': cleansed_article_text
            }

            article_info_list.append(scraped_info)

        article_info_df = pd.DataFrame(article_info_list)
        article_info_df = article_info_df[['title', 'url', 'created_time', 'tag_text', 'tag_url', 'article_text']]
        article_info_df = article_info_df.drop_duplicates(subset=['url'])
        article_info_df = article_info_df
        article_info_df.to_csv(app_config.csv_file_name)

        self.save_to_db(article_info_df)

