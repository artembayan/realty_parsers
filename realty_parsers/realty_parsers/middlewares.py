import logging
from copy import deepcopy

from scrapy import signals
from elasticsearch import Elasticsearch, helpers
from realty_parsers.settings import EL_HOST, EL_PORT, EL_USER, EL_PASS

logger = logging.getLogger(__name__)


class UploadItems(object):

    def __init__(self):
        self.items = list()

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        return ext

    def spider_closed(self, spider):
        es = Elasticsearch(
            [
                {
                    'host': EL_HOST,
                    'port': int(EL_PORT),
                    'scheme': 'http',
                }
            ],
            http_auth=(EL_USER, EL_PASS)
        )

        actions = [
            {
                "_op_type": "index",
                "_index": spider.index,
                "_id": str(i),
                "_source": item
            }
            for i, item in enumerate(self.items)
        ]

        helpers.bulk(es, actions)

    def item_scraped(self, item, spider):
        self.items.append(deepcopy(item))
