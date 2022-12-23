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

    def get_developers(self, response):
        developers = response.xpath(PL_DEVELOPERS).getall()
        return developers

    def get_next_page(self, response):
        next_page = response.xpath(PL_PAGE_NEXT).get(None)
        if not next_page:
            return ''
        url = response.urljoin(next_page)
        return url

    def get_id(self, response=None):
        id = response.xpath(PP_ID).get()
        return {'ID': id}  # 'url': response.url}

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
        'RETRY_TIMES': 10,
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
                yield Request(url=url, callback=self.parse_building, dont_filter=True, cookies=self.cookies,
                              meta={'proxy': 'http://kJ0cQY:7dLgdASzsL@46.8.22.213:3000'})
            next_page = self.get_next_page(response)
            if next_page:
                yield Request(url=next_page, callback=self.parse, dont_filter=True,
                              meta={'proxy': 'http://kJ0cQY:7dLgdASzsL@46.8.22.213:3000'})
        except:
            self.log(f"Last list page: {response.url}")

    def parse_building(self, response):
        result = dict()
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


class KrishaDevelopersSpider(Spider, KrishaKzParser):
    name = 'krisha.kz_developers'
    allowed_domains = ['krisha.kz']
    start_urls = ['https://krisha.kz/zastroyshik/search']
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
            'krisha_kz.pipelines.DropDuplicateItems': 100,
        },
        'UNIQUE_KEYS': ['name', 'logo'],
        # 'EXTENSIONS': {
        #     'krisha_kz.middlewares.UploadItems': 800
        # },
    }

    def parse(self, response):
        try:
            result = dict()
            developers = self.get_developers(response)
            for developer in developers:
                developer = Selector(text=developer)
                url = response.urljoin(developer.xpath(PL_DEVELOPER_URL).get(''))
                result['name'] = self.clear_string(developer.xpath(DP_NAME).get(''))
                yield Request(url=url, callback=self.parse_developer, dont_filter=True,
                              meta={'result': deepcopy(result), 'proxy': 'http://kJ0cQY:7dLgdASzsL@46.8.22.213:3000'})
            next_page = self.get_next_page(response)
            if next_page:
                yield Request(url=next_page, callback=self.parse, dont_filter=True,
                              meta={'proxy': 'http://kJ0cQY:7dLgdASzsL@46.8.22.213:3000'})
        except:
            self.log(f"Last list page: {response.url}")

    def parse_developer(self, response):
        result = response.meta.get('result', {})
        result.update(self.get_dev_logo(response))
        result.update(self.get_foundation_year(response))
        result.update(self.get_rented_qnty(response))
        result.update(self.get_being_built_qnty(response))
        result.update(self.get_dev_description(response))
        yield result
