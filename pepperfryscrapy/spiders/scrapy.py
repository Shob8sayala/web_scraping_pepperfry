import scrapy
import os
import requests


class pepperfryScrapy(scrapy.Spider):
    name = "pepperfry"

    def start_requests(self):
        base_url = "https://www.pepperfry.com/site_product/search?q="
        items = ["two seater sofa",
                 "bench",
                 "book case",
                 "coffee table",
                 "dining set",
                 "arm chair",
                 "chest drawer",
                 "garden seating",
                 "bean bag",
                 "king bed"
                 ]
        for item in items:
            itemList = item.split(' ')
            itemList = "+".join(itemList)
            url = base_url
            for str in itemList:
                url = url + str
        #     yield scrapy.Request(url=url, callback=self.parse(item))
            yield scrapy.Request(url=url, callback=self.parse ,dont_filter=True,cb_kwargs = dict(item = item))

    def parse(self, response,item):
        yield dict(
        item_name = item,
        )
        itempath = 'pepperfry/{}'.format(item)
        if not os.path.exists(itempath):
            os.makedirs(itempath)
        prod_urls = response.css('div.clipCard__wrapper input::attr(data-product-url)').getall()[0:5]
        for prod_url in prod_urls:
            # print(product)
            # print(prod_link)
            yield scrapy.Request(url = prod_url, callback=self.parsepage,dont_filter=True,cb_kwargs = dict(item = item))
    
    def parsepage(self, response, item):
        yield dict(
        item = item,
        )
        prod_name = response.css('div.vip-pro-hd-wrap h1::text').get()
        item_path = 'pepperfry/{}/{}'.format(item,prod_name)
        if not os.path.exists(item_path):
            os.makedirs(item_path)
        prod_price = response.css('div.vip-eff-price-wrap span::text').get()
        gallery = response.css('div.vipImage__thumb-wrapper ul li')
        img_urls = gallery.css('a::attr(data-img)').getall()
        print('\n\n\n\n\n')
        for index,img_url in enumerate(img_urls):
            print(index,img_url)
            data = requests.get(img_url)
            # path = ''
            with open(os.path.join( item_path, "{}.jpg".format(index)),'wb') as f:
                f.write(data.content)
        
