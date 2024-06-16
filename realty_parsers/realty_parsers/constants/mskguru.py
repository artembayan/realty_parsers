PL_ITEM_URL = "//a[@data-id]/@href"
PL_PAGE_NEXT = "//li[@class='next']/a/@href"

HEADERS = {
    # 'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'Te': 'trailers',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

PP_ID = "//a[@class='button callback']/@data-build"
PP_TITLE = "//div[@class='flat_title_block']//h1[@class='flat_title']/text()"
PP_PRICE = "//div[@class='flat_title_block']//div[@class='flat_price']/text()"
PP_DATE = "//table[@id='characteristics']//tr[@class='queue']/td[2]/text()"
PP_LOCATION = "//div[@class='map_block']/p/text()"
PP_DEVELOPER = "//div[@class='flat_right_col']//a[@class='company']/span/text()"
PP_IMAGES = "//div[contains(@class, 'media_tab') and @rel='photo']//ul[@class='gallery']/li/img/@data-src"
PP_DESC = "//div[@class='build_description']//text()"
PP_PROP_KEY = "//table[@id='characteristics']//tr/td[1]/text()"
PP_PROP_VALUE = "//table[@id='characteristics']//tr/td[2]/text()"
