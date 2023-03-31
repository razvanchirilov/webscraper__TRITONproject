# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def remove_whitespace(value):
    return value.strip()


def remove_curency(value):
    return value.replace('Lei', '')

class TritonprojectItem(scrapy.Item):

    product_code = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=TakeFirst()
    )
    product_title = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=TakeFirst()
    )
    product_price = scrapy.Field(
        input_processor=MapCompose(remove_whitespace, remove_curency),
        output_processor=TakeFirst()
    )
    product_availability = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=TakeFirst()
    )
