# installed scrapy local (triton-env)
# installed splash local (triton-env)
# installed scrapypyxlsx

# root: TritonProject/spiders

import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

# import sys to expose the path for Items
from sys import path
path.append('/Users/razvanchirilov/Code Projects/Triton/TritonProject')
from TritonProject.items import TritonprojectItem

# import warnings to ignore Deprecation
import warnings
warnings.filterwarnings("ignore", category=scrapy.exceptions.ScrapyDeprecationWarning)

class VacuumCleanersSpider(scrapy.Spider):
    name = "vacuum_cleaners"
    allowed_domains = ["triton.com.ro"]
    start_urls = [
                 "https://www.triton.com.ro/curatenie-si-climatizare/aspirare-exhaustare/aspiratoare",
                 "https://www.triton.com.ro/curatenie-si-climatizare/aspirare-exhaustare/aparate-spray-extractie", 
                 "https://www.triton.com.ro/curatenie-si-climatizare/aspirare-exhaustare/filtre-aspirator-aspirator-exhaustor",
                 "https://www.triton.com.ro/curatenie-si-climatizare/aspirare-exhaustare/componenete-aspiratoare",
                 "https://www.triton.com.ro/curatenie-si-climatizare/curatare-cu-presiune",
                 "https://www.triton.com.ro/curatenie-si-climatizare/curatare-cu-presiune/curatitoare-cu-presiune-apa-calda",
                 "https://www.triton.com.ro/curatenie-si-climatizare/curatare-cu-presiune/curatitoare-cu-abur"
                 "https://www.triton.com.ro/curatenie-si-climatizare/curatare-cu-presiune/componente-curatitoare-cu-presiune"
                ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1}, endpoint='render.html')

    # extract data from the first page 
    def parse(self, response):
        products = response.xpath('//*[@class="products wrapper grid columns4 products-grid   "]//li')
        for product in products:
            product_title = product.xpath('.//*[@class="product name product-item-name"]/a/text()').get().strip()
            product_price = product.xpath('.//*[@class="price"]/text()').get().strip()
            product_availability = product.xpath('//*[@class="stock unavailable"]/span/text()').get()
            product_link = product.xpath('.//*[@class="product photo product-item-photo"]//a[1]/@href').get()
            
            yield SplashRequest(product_link,
                                callback=self.parse_product_page, 
                                meta= {'product_title': product_title, 
                                       'product_price': product_price, 
                                       'product_availability': product_availability},
                                args= {'wait': 1},     
                                endpoint= 'render.html')
 
        # Process load more products alongside the javascript:void(0) function
        load_more_products = response.xpath('//*[@class="items pages-items"]/li/a/@href').extract()[0:5]
        for links in load_more_products:
            yield SplashRequest(links, callback=self.parse, args={'wait': 1}, endpoint='render.html')          
 
    # extract the data inside each item  
    def parse_product_page(self, response):
        product_code = response.xpath('//*[@class="value"]/text()').get() 
        product_title = response.meta['product_title']
        product_price = response.meta['product_price']
        product_availability = response.meta['product_availability']      
        
        # load items to item loader and yield the values in dict
        l = ItemLoader(item = TritonprojectItem(), selector = response)
        l.add_value('product_code', product_code)
        l.add_value('product_title', product_title)
        l.add_value('product_price', product_price)
        l.add_value('product_availability', product_availability)
        
        yield l.load_item()


# main driver
if __name__ == '__main__': 
    #run spider
    process = CrawlerProcess()
    process.crawl(VacuumCleanersSpider)
    process.start()
