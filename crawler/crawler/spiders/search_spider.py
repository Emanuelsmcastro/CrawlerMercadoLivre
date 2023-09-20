from typing import Any, Iterable
from enum import Enum
import scrapy
from scrapy.http import Request, Response
from crawler.items import CrawlerItem
from config import config_db

class Selector(Enum):
    items = '//ol[@class="items_container"]/li[contains(@class, "promotion-item")]'
    link = './/div/a[@class="promotion-item__link-container"]/@href'
    img = '//figure[@class="ui-pdp-gallery__figure"][1]/img/@src'
    currency = '//div[@class="ui-pdp-price__main-container"]/div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__currency-symbol"]/text()'
    price = '//div[@class="ui-pdp-price__main-container"]/div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]/text()'
    seller = '//a[@class="ui-pdp-action-modal__link"]/span/text()'
    title = '//h1[@class="ui-pdp-title"]/text()'
    decimal = '//span[@class="andes-money-amount__cents andes-money-amount__cents--superscript-36"]/text()'
    link_next = '//li[@class="andes-pagination__button andes-pagination__button--next"]/a/@href'


class SearchItemSpider(scrapy.Spider):
    name = 'search'
    url = 'https://www.mercadolivre.com.br/ofertas#c_id=/home/promotions-recommendations&c_uid=d1d68fa7-dbb6-40c4-9dac-34159e9b2634'
    
    def start_requests(self) -> Iterable[Request]:
        config_db.Base.metadata.create_all(config_db.engine)
        yield scrapy.Request(url=self.url, callback=self.parse_itens)
    
    def parse_itens(self, response: Response, **kwargs: Any) -> Any:
        items = response.xpath(Selector.items.value)
        for item in items:
            link = item.xpath(Selector.link.value).get()
            yield response.follow(link, callback=self.parse_item)
        
        link_next = response.xpath(Selector.link_next.value).get()
        if link_next:
            yield response.follow(link_next, callback=self.parse_itens)
    
    def parse_item(self, response: Response, **kawargs: Any) -> Any:
        img = response.xpath(Selector.img.value).get()
        title = response.xpath(Selector.title.value).get()
        currency = response.xpath(Selector.currency.value).get()
        price = response.xpath(Selector.price.value).get()
        seller = response.xpath(Selector.seller.value).get()
        decimal = response.xpath(Selector.decimal.value).get()
        
        data = {
            'link': response.url,
            'title': title,
            'currency': currency,
            'price': price,
            'seller': seller,
            'image': img,
            'decimal': decimal
        }
        
        crawler_item = CrawlerItem(**data)
        yield crawler_item
            