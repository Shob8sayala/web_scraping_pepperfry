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
            yield scrapy.Request(url = prod_url, callback=self.parsepage,dont_filter=True,cb_kwargs = dict(item = item))
    
    def parsepage(self, response, item):
        yield dict(
        item = item,
        )
        prod_name = response.css('div.vip-pro-hd-wrap h1::text').get()
        item_path = 'pepperfry/{}/{}'.format(item,prod_name)
        if not os.path.exists(item_path):
            os.makedirs(item_path)
        prod_price = response.css('div.vip-eff-price-wrap span.vip-eff-price-amt::text').get()
        prod_disc = response.css('div.vip-eff-price-wrap span.vip-eff-price-disc::text').get()
        gallery = response.css('div.vipImage__thumb-wrapper ul li')
        img_urls = gallery.css('a::attr(data-img)').getall()
        for index,img_url in enumerate(img_urls):
            data = requests.get(img_url)
            # path = ''
            with open(os.path.join( item_path, "{}.jpg".format(index)),'wb') as f:
                f.write(data.content)
        with open(os.path.join( item_path, "metadata.txt".format(index)),'w',encoding='UTF-8') as f:
            f.write("Product: {}\n".format(prod_name))
            f.write("Price: {}\n".format(prod_price))
            f.write("Discount: {}\n".format(prod_disc))
            table = response.css('div.vip-prod-dtl-wrap')
            for t in table:
                f.write("{}: {}".format(t.css('span.vip-prod-dtl-ttl::text').get(),t.css('span.vip-prod-dtl-subttl::text').get()))
                f.write('\n')

