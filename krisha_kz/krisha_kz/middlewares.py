# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
from copy import deepcopy

from scrapy import signals
from elasticsearch import Elasticsearch
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class KrishaKzSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class KrishaKzDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# import base64
#
# class MyProxyMiddleware(object):
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def __init__(self, settings):
#         self.user = settings.get('PROXY_USER')
#         self.password = settings.get('PROXY_PASSWORD')
#         self.endpoint = settings.get('PROXY_ENDPOINT')
#         self.port = settings.get('PROXY_PORT')
#
#     def process_request(self, request, spider):
#         user_credentials = '{user}:{passw}'.format(user=self.user, passw=self.password)
#         basic_authentication = 'Basic ' + base64.b64encode(user_credentials.encode()).decode()
#         host = 'http://{endpoint}:{port}'.format(endpoint=self.endpoint, port=self.port)
#         request.meta['proxy'] = host
#         request.headers['Proxy-Authorization'] = basic_authentication


class UploadItems(object):

    def __init__(self):
        self.items = list()

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_closed(self, spider):
        es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
        for i, item in enumerate(self.items):
            es.index(index='developers', id=i, document=json.dumps(item))

    def item_scraped(self, item, spider):
        self.items.append(deepcopy(item))
