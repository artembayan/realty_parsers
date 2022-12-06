from copy import deepcopy
from scrapy import Request, Spider, Selector
from .krisha_constants import *

import json
import re


class KrishaKzParser():

    def clear_string(self, string):
        if isinstance(string, str):
            string = re.sub(r'\<[^>]*\>', '', string).strip()
            string = re.sub(r'\<[^>]*\>', '', string)
            return string
        else:
            return ''

    def get_items_urls(self, response):
        items = [response.urljoin(url) for url in response.xpath(PL_ITEM_URL).getall()]
        return items

    def get_next_page(self, response):
        next_page = response.xpath(PL_PAGE_NEXT).get(None)
        if not next_page:
            return ''
        url = response.urljoin(next_page)
        return url

    def get_id(self, response=None):
        id = response.xpath(PP_ID).get()
        return {'ID': id}  # 'url': response.url}

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

class KrishaSpider(Spider, KrishaKzParser):
    name = 'krisha.kz'
    allowed_domains = ['krisha.kz']
    start_urls = ['https://krisha.kz/complex/search/']
    cookies = dict()
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 60,
        'DOWNLOAD_DELAY': 0.7,
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
        'REFERER_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 50
        }
    }

    def parse(self, response):
        try:
            urls = self.get_items_urls(response)
            for url in urls:
                yield Request(url=url, callback=self.parse_building, dont_filter=True, cookies=self.cookies)
            next_page = self.get_next_page(response)
            if next_page:
                yield Request(url=next_page, callback=self.parse, dont_filter=True)
        except:
            self.log(f"Last list page: {response.url}")

    def parse_building(self, response):
        result = dict()
        try:
            result.update(self.get_id(response))
            result.update(self.get_title(response))
            result.update(self.get_price(response))
            result.update(self.get_status(response))
            result.update(self.get_date(response))
            result.update(self.get_location(response))
            result.update(self.get_developer(response))
            result.update(self.get_parameters(response))
            result.update(self.get_description(response))
            result.update(self.get_infrastructure(response))
            yield result
            # id = response.url.split('/')[-1]
            # ajax_url = 'https://krisha.kz/a/ajaxPhones?id=' + id
            # cookies = response.request.headers.get('Cookie')
            # cookies_list = cookies.decode().split("; ")
            # for cookie in cookies_list:
            #     if cookie.split('=')[0] == 'krssid' or cookie.split('=')[0] == 'krishauid':
            #         self.cookies[cookie.split('=')[0]] = cookie.split('=')[-1]
            # yield Request(url=ajax_url, callback=self.parse_number, dont_filter=True,
            #               cookies=self.cookies, headers=HEADERS,
            #               meta={'passed_data': deepcopy(result)})
        except:
            self.log(f'Parse Item Err: DataOut {response.url}')

    def parse_number(self, response):
        result = response.meta['passed_data']
        jo = json.loads(response.text)
        number = jo['phones'][0]
        result.update({'number': number})
        yield result
