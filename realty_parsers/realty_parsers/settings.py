import os

from dotenv import load_dotenv


load_dotenv()

BOT_NAME = 'realty_parsers'
SPIDER_MODULES = ['realty_parsers.spiders']
NEWSPIDER_MODULE = 'realty_parsers.spiders'

ROBOTSTXT_OBEY = True
PROXY_URL = os.getenv('PROXY_URL')
EL_HOST = os.getenv('EL_HOST')
EL_PORT = os.getenv('EL_PORT')
EL_USER = os.getenv('EL_USER')
EL_PASS = os.getenv('EL_PASS')

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

DOWNLOADER_MIDDLEWARES_BASE = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
}
