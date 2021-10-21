import scrapy


class TinySpider(scrapy.Spider):
    name = 'tiny'
    allowed_domains = ['cigabuy.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath('//div[@class="r_b_c"]/div[@class="p_box_wrapper"]/div'):
            yield{
                'Title': product.xpath('.//a/text()').get(),
                'URL': product.xpath('.//a/@href').get(),
                'Special_Price': product.xpath('.//div[@class="p_box_price cf"]/span[1]/text()').get(),
                'Normal_Price': product.xpath('.//div[@class="p_box_price cf"]/span[2]/text()').get(),
                'User-Agent': response.request.headers['User-Agent']
            }
        
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        })