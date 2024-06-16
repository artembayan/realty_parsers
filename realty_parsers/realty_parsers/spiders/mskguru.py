import json
import re

from copy import deepcopy
from scrapy import Request, Selector, Spider

from .mskguru_constants import *


class MskguruParser:

    def clear_string(self, string):
        if isinstance(string, str):
            string = re.sub(r'\<[^>]*\>', '', string).strip()
            string = re.sub(r'\<[^>]*\>', '', string)
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
        price = response.xpath(PP_PRICE).get('')
        price = re.sub(r'[^\d.]+', '', price)
        price = int(price)
        return {'price': price}

    def get_status(self, response=None):
        status = response.xpath(PP_STATUS).get('')
        status = self.clear_string(status)
        return {'status': status}

    def get_date(self, response=None):
        date = response.xpath(PP_DATE).get('')
        date = self.clear_string(date)
        return {'date': date}

    def get_location(self, response=None):
        location = response.xpath(PP_LOCATION).get('')
        return {'location': location}

    def get_developer(self, response=None):
        developer = response.xpath(PP_DEVELOPER).get('')
        return {'developer': developer}

    def get_images(self, response=None):
        # images = response.xpath(PP_IMAGES).getall()
        images_urls = []
        jo = response.xpath(PP_JSON).get('')
        jo = re.search('(\{.+\})', jo).group(1)
        jo = json.loads(jo)
        images = jo.get('complex', {}).get('photos', {})
        for image in images:
            width = image['w']
            height = image['h']
            url = image['src'].replace('/complex', '')
            #url = url.replace('photo.jpg', f'photo-{width}x{height}.jpg')
            images_urls.append(url)
        return {'images': images_urls}

    def get_parameters(self, response=None):
        parameters = {}
        keys = response.xpath(PP_PROP_KEY).getall()
        values = response.xpath(PP_PROP_VALUE).getall()
        props = list(zip(keys, values))
        parameters.update(props)
        return {'parameters': parameters}

    def get_description(self, response=None):
        description = response.xpath(PP_DESC).getall()
        description = ''.join(description)
        description = self.clear_string(description)
        return {'description': description}

    def get_infrastructure(self, response=None):
        infrastructure = response.xpath(PP_INFRASTRUCTURE).getall()
        return {'infrastructure': infrastructure}

    def get_dev_logo(self, response=None):
        logo = response.xpath(DP_LOGO).get('')
        return {'logo': logo}

    def get_foundation_year(self, response=None):
        foundation_year = response.xpath(DP_FOUNDATION_YEAR).get('')
        return {'year': foundation_year}

    def get_rented_qnty(self, response=None):
        rented_qnty = int(response.xpath(DP_RENTED_QNTY).get(0))
        return {'rented_qnty': rented_qnty}

    def get_being_built_qnty(self, response=None):
        being_built_qnty = int(response.xpath(DP_BEING_BUILT_QNTY).get(0))
        return {'being_built_qnty': being_built_qnty}

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
        'DOWNLOAD_DELAY': 0.7,
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'REFERER_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'RETRY_TIMES': 10,
        # 'DOWNLOADER_CLIENT_TLS_METHOD': 'TLSv1.2',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
        }
    }

    def parse(self, response):
        try:
            urls = self.get_items_urls(response)
            for url in urls:
                yield Request(url=url, callback=self.parse_building, dont_filter=True, headers=HEADERS,
                              meta={'proxy': 'http://217.25.95.220:8443'}
                              )
            if next_page := self.get_next_page(response):
                yield Request(url=next_page, callback=self.parse, dont_filter=True,
                              meta={'proxy': 'http://217.25.95.220:8443'}
                              )
        except:
            self.log(f"Last list page: {response.url}")

    def parse_building(self, response):
        result = dict()
        if response.status != 200:
            g=2
        print(f"Parse {response.url}")
        try:
            result.update(self.get_id(response))
            result.update(self.get_url(response))
            result.update(self.get_title(response))
            result.update(self.get_price(response))
            result.update(self.get_status(response))
            result.update(self.get_date(response))
            result.update(self.get_location(response))
            result.update(self.get_developer(response))
            result.update(self.get_images(response))
            result.update(self.get_parameters(response))
            result.update(self.get_description(response))
            result.update(self.get_infrastructure(response))
            yield result
        except:
            self.log(f'Parse Item Err: DataOut {response.url}')

    def parse_number(self, response):
        result = response.meta['passed_data']
        jo = json.loads(response.text)
        number = jo['phones'][0]
        result.update({'number': number})
        yield result
