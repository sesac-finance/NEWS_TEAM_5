# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSocialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_date = scrapy.Field()
    news_dir = scrapy.Field()
    pass
