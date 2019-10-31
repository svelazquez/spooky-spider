import scrapy

class SpiderKun(scrapy.Spider):
    name = 'spiderkun' # identifies the spider. must be unique per spider. 
    def start_requests(self):
        url = 'https://www.twitchquotes.com/copypastas/labels/weebs'
        yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        page = response.url.split("/")[-2] # wtf is this hackery. 
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.xpath('//*[@id="quote_display_content_3"]/text()').getall()) # just gets one. need 2 iterate
        self.log('Saved file %s' % filename)