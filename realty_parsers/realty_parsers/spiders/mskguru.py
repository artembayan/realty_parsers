import json
import re
from typing import Iterable

from scrapy import Request, Spider

from constants.mskguru import *
from realty_parsers.settings import PROXY_URL


class MskguruParser:

    def clear_string(self, string):
        if isinstance(string, str):
            string = re.sub(r'\<[^>]*\>', '', string).strip()
            string = re.sub(r'\<[^>]*\>', '', string)
            string = string.split()
            string = ' '.join(c.replace(" ", "") for c in string)
            return string
        else:
            return ''

    @staticmethod
    def get_items_urls(response):
        return response.xpath(PL_ITEM_URL).getall()

    @staticmethod
    def get_next_page(response):
        return response.xpath(PL_PAGE_NEXT).get()

    def get_id(self, response=None):
        id = response.xpath(PP_ID).get()
        return {'ID': id}

    def get_url(self, response):
        url = response.url
        return {'url': url}

    def get_title(self, response=None):
        title = response.xpath(PP_TITLE).get('')
        title = self.clear_string(title)
        return {'title': title}

    def get_price(self, response=None):
        price = response.xpath(PP_PRICE).get('').strip()
        if price != 'Цена по запросу':
            price_range = price.split('–')
            price_range = [int(re.sub(r'\D', '', price)) for price in price_range]
            price_min = min(price_range)
            price_max = max(price_range)
        else:
            price_min = price_max = None
        return {'price_min': price_min, 'price_max': price_max}

    def get_price_per_metr(self, response=None):
        price = response.xpath(PP_PRICE_PER_METR).get('').strip()
        if price != 'Узнавайте по телефону':
            price_range = price.split('–')
            price_range = [int(re.sub(r'\D', '', price)) for price in price_range]
            price_min = min(price_range)
            price_max = max(price_range)
        else:
            price_min = price_max = None
        return {'price_per_metr_min': price_min, 'price_per_metr_max': price_max}

    def get_status(self, response=None):
        status = response.xpath(PP_DATE).get('')
        status = self.clear_string(status)
        return {'status': status}

    def get_date(self, response=None):
        date = response.xpath(PP_DATE).get('')
        date = self.clear_string(date)
        return {'date': date}

    def get_location(self, response=None):
        location = response.xpath(PP_LOCATION).get('')
        return {'location': self.clear_string(location)}

    def get_developer(self, response=None):
        developer = response.xpath(PP_DEVELOPER).get('')
        return {'developer': developer}

    def get_images(self, response=None):
        images_urls = response.xpath(PP_IMAGES).getall()
        return {'images': images_urls}

    def get_parameters(self, response=None):
        keys = response.xpath(PP_PROP_KEY).getall()
        values = [self.clear_string(value) for value in response.xpath(PP_PROP_VALUE).getall()]
        parameters = {key: value for key, value in zip(keys, values)}
        return {'parameters': parameters}

    def get_description(self, response=None):
        description = response.xpath(PP_DESC).getall()
        description = ''.join(description)
        description = self.clear_string(description)
        return {'description': description}

    def get_devs_urls(self, response):
        urls = response.xpath(PL_DEVELOPERS).getall()
        return urls

    def get_dev_name(self, response=None):
        name = self.clear_string(response.xpath(DP_NAME).get(''))
        return {'name': name}

    def get_dev_logo(self, response=None):
        logo = response.xpath(DP_LOGO).get('')
        return {'logo': logo}

    def get_dev_foundation_year(self, response=None):
        foundation_year = response.xpath(DP_FOUNDATION_YEAR).get('')
        return {'year': foundation_year}

    def get_dev_rented_qnty(self, response=None):
        rented = response.xpath(DP_RENTED_QNTY).get("0")
        rented_qnty = re.search("(\d+)", rented).group(0)
        return {'rented_qnty': int(rented_qnty)}

    def get_dev_being_built_qnty(self, response=None):
        being_built = response.xpath(DP_BEING_BUILT_QNTY).get("0")
        being_built_qnty = re.search("(\d+)", being_built).group(1)
        return {'being_built_qnty': int(being_built_qnty)}

    def get_dev_description(self, response=None):
        description = response.xpath(DP_DESCRIPTION).getall()
        description = ''.join(description)
        description = self.clear_string(description)
        return {'description': description}


class MskguruSpider(Spider, MskguruParser):
    name = 'mskguru.ru'
    allowed_domains = ['mskguru.ru']
    start_urls = ['https://mskguru.ru/novostroyki']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 60,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'REFERER_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_TIMES': 10,
        'DEFAULT_REQUEST_HEADERS': HEADERS,
        # 'DOWNLOADER_CLIENT_TLS_METHOD': 'TLSv1.2',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
        },
        # 'EXTENSIONS': {
        #     'realty_parsers.middlewares.UploadItems': 800
        # },
    }

    def start_requests(self) -> Iterable[Request]:
        yield Request(
            url=self.start_urls[0],
            callback=self.parse,
            dont_filter=True,
            meta={'proxy': PROXY_URL}
        )

    def parse(self, response) -> Iterable[Request]:
        urls = self.get_items_urls(response)
        for url in urls:
            yield Request(
                url=url,
                callback=self.parse_building,
                dont_filter=True,
                meta={'proxy': PROXY_URL}
            )
        if next_page := self.get_next_page(response):
            yield Request(
                url=next_page,
                callback=self.parse,
                dont_filter=True,
                meta={'proxy': PROXY_URL}
            )

    def parse_building(self, response):
        result = dict()
        self.log(f"Parse {response.url}")
        try:
            result.update(self.get_id(response))
            result.update(self.get_url(response))
            result.update(self.get_title(response))
            result.update(self.get_price(response))
            result.update(self.get_price_per_metr(response))
            result.update(self.get_status(response))
            result.update(self.get_date(response))
            result.update(self.get_location(response))
            result.update(self.get_developer(response))
            result.update(self.get_images(response))
            result.update(self.get_parameters(response))
            result.update(self.get_description(response))
            yield result
        except Exception as e:
            self.log(f'Parse Item Err: DataOut {response.url}')


class MskgurDevelopersSpider(Spider, MskguruParser):
    name = 'mskguru.ru_developers'
    allowed_domains = ['mskguru.ru']
    start_urls = ['https://mskguru.ru/companies']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 60,
        'DOWNLOAD_DELAY': 0.7,
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'REFERER_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_TIMES': 10,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
        },
        'ITEM_PIPELINES': {
            'realty_parsers.pipelines.DropDuplicateItems': 100,
        },
        'UNIQUE_KEYS': ['name', 'logo'],
        # 'EXTENSIONS': {
        #     'realty_parsers.middlewares.UploadItems': 800
        # },
    }

    def parse(self, response):
        try:
            urls = self.get_devs_urls(response)
            self.log(f"Got {len(urls)} urls from {response.url}")
            for url in urls:
                yield Request(url=url, callback=self.parse_developer, dont_filter=True,
                              meta={'proxy': PROXY_URL})
            next_page = self.get_next_page(response)
            if next_page:
                yield Request(url=next_page, callback=self.parse, dont_filter=True,
                              meta={'proxy': PROXY_URL})
        except:
            self.log(f"Last list page: {response.url}")

    def parse_developer(self, response):
        result = {}
        try:
            result.update(self.get_dev_name(response))
            result.update(self.get_dev_logo(response))
            result.update(self.get_dev_foundation_year(response))
            result.update(self.get_dev_rented_qnty(response))
            result.update(self.get_dev_being_built_qnty(response))
            result.update(self.get_dev_description(response))
        except Exception as e:
            self.log(f'Parse Item Err: DataOut {response.url}')
        yield result
