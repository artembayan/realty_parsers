# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, NotConfigured


class KrishaKzPipeline:
    def process_item(self, item, spider):
        return item


class DropDuplicateItems(object):

    def __init__(self, keys):
        self.keys = keys
        self.collected_values = set()

    @classmethod
    def from_crawler(cls, crawler):
        keys = crawler.spider.custom_settings.get('UNIQUE_KEYS')
        if not keys:
            raise NotConfigured()
        return cls(keys=keys)

    def process_item(self, item, spider):
        value = "_".join([str(item.get(key, '')) for key in self.keys])
        if value in self.collected_values:
            raise DropItem()
        self.collected_values.add(value)
        return item
