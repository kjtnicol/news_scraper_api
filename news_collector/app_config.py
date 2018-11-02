
# General Config
debug_mode = True

# Web Config
host_name = '127.0.0.1'
port = 5000
api_url = '/api/articles/bbc'


# Database Access Config
db_conn_string = 'mongodb+srv://isentia:isentia@cluster0-aoq9j.mongodb.net/admin'
db_name = 'scraped_news'
collection_name = 'bbc_articles'

# News Scraping Config
base_url = 'http://www.bbc.com/'
removing_strings = ['Media playback is unsupported on your device ']
csv_file_name = 'news_scraped.csv'