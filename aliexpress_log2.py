# -*- coding: utf-8 -*-
import scrapy


class AliexpressLog2Spider(scrapy.Spider):
    name = 'aliexpress_log2'
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://fr.aliexpress.com/category/205002365/pens-pencils-writing-supplies.html']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'loginId': 'jean-denis.zafar@insee.fr', 'password': 'INSEE_MK1'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
        nom = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product", " " ))]/text()').extract()
        print(nom)
        prix=response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "price-m", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "value", " " ))]/text()').extract()
        prix=["".join(s.split(" ")[1:]) for s in prix]
        url_image=response.xpath('//img[contains(@class,"picCore")]').extract()
        url_image=[s.split('src="')[1] for s in url_image]
        url_image=[s.split('" alt')[0] for s in url_image]
        url_lien_page=response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product", " " ))]/@href').extract()
        for item in zip(nom,prix,url_image,url_lien_page):
            scraped_info = {
                    'nom' : item[0],
                    'prix' : item[1],
                    'url_image':item[2],
                    'url_lien_page':item[3],
            }
            yield scraped_info
        next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ui-pagination-next", " " ))]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)