# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:17:49 2017

@author: NHNBYB
"""

# -*- coding: utf-8 -*-
import scrapy
#from scrapy.crawler import CrawlerProcess


class ZalandoSpider(scrapy.Spider):
    AUTOTHROTTLE_ENABLED = True
    AUTOTHROTTLE_START_DELAY = 10
    AUTOTHROTTLE_MAX_DELAY = 0
    DOWNLOAD_DELAY = 5
    name = 'zalando'
    allowed_domains = ['zalando.fr/']
    start_urls = ['https://www.zalando.fr/manteaux-homme/']
    def parse(self, response):
        nom = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "z-nvg-cognac_articleName--arFp", " " ))]/text()').extract()
        marque = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "z-nvg-cognac_brandName-2XZRz", " " ))]/text()').extract()
        prix=response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "z-nvg-cognac_originalPrice-2Oy4G", " " ))]/text()').extract()
#        url_lien_page=response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "z-nvg-cognac_infoDetail"))]/@href').extract()
        url_lien_page=prix
        page=[response.url for _ in range(len(nom))]
        for item in zip(nom,prix,marque,url_lien_page,page):
            scraped_info = {
                    'page' : item[4],
                    'nom' : item[0],
                    'marque':item[1],
                    'prix' : item[2],
                    'url_lien_page':item[3],
            }
            yield scraped_info

        dom='https://www.zalando.fr/'
        next_page = dom+(response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "z-nvg-cognac_link-8qswi"))]/@href').extract()[1])[1:]
        next_page=next_page.encode('ascii','ignore')
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse,dont_filter=True)
#            yield response.follow(next_page, callback=self.parse)

##process = CrawlerProcess()
##process.crawl(ZalandoSpider)
