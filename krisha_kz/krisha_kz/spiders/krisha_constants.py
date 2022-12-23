PL_ITEM_URL = "//a[contains(@class, 'complex-card__main-block')]/@href"
PL_PAGE_NEXT = "//a[@class='paginator__btn paginator__btn--next']/@href"

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Te': 'trailers'
}

PP_ID = "//button[contains(@class, 'offer__favorite')]/@data-id"
PP_TITLE = "//div[@class='offer__advert-title']/h1/text()"
PP_PRICE = "//div[@class='offer__price']/text()"
PP_STATUS = "//div[@data-name='home.state']/p/text()"
PP_DATE = "//div[@data-name='deadline']/p/text()"
PP_LOCATION = "//div[span[@class='complex__sidebar-info-icon fi-location']]/following-sibling::p/text()"
PP_DEVELOPER = "//div[span[@class='complex__sidebar-info-icon fi-bag']]/following-sibling::p/text()"
PP_IMAGES = "//li[@class='gallery__thumb']/div/@data-href"
PP_JSON = "//script[@id='jsdata']/text()"
PP_DESC = "//div[@class='offer__description']"
PP_DESC_KEY = "//div[@class='offer__description']//p/strong/text()"
PP_DESC_VALUE = ""
PP_PROPS = "//div[@id='parameters']"
PP_PROP_KEY = "//dt[@class='complex-parameters__block-title']/text()"
PP_PROP_VALUE = "//dd[@class='complex-parameters__block-text']/text()"
PP_INFRASTRUCTURE = "//dd[contains(@class, 'complex-parameters__block-text--infrastructure')]/text()"


PL_DEVELOPERS = "//article[@class='builder-card']"
PL_DEVELOPER_URL = "//header[@class='builder-card__header']/a/@href"

DP_NAME = "//header[@class='builder-card__header']/a/text()"
DP_LOGO = "//section[@id='about-the-developer']//img[@class='builder-dev-briefing__image']/@src"
DP_FOUNDATION_YEAR = "//section[@id='about-the-developer']//p[@class='builder-about__text' and contains(text(), 'Год основания')]/span/text()"
DP_RENTED_QNTY = "//section[@id='about-the-developer']//p[@class='builder-about__text' and contains(text(), 'Сдано объектов')]/span/text()"
DP_BEING_BUILT_QNTY = "//section[@id='about-the-developer']//p[@class='builder-about__text' and contains(text(), 'Строится')]/span/text()"
DP_DESCRIPTION = "//section[@id='about-the-developer']//div[@class='builder-about__description-text']"
