# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    currency= scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    image = scrapy.Field()
    decimal = scrapy.Field()
