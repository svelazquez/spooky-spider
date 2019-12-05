"""Run: $ scrapy runspider main.py"""
import scrapy

class SpiderKun(scrapy.Spider):
    name = 'spiderkun' # identifies the spider. must be unique per spider. 
    def start_requests(self):
        url = 'https://www.twitchquotes.com/copypastas/labels/weebs'
        yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        try:
            page = response.url.split("/")[-2] 
        except KeyError as e:
            print(f"{e}: Cannot split url into pages. Check url.")

        filename = 'quotes-%s.html' % page
        # TODO truncate file if not empty and is first iteration. 
        with open(filename, 'a') as f:
            stuff = [f.write(res) for res in response.css(f'span#quote_display_content').getall()]
            print(f"Got this stuff for you: {stuff}")
            # wtf is this stuff? id's? 
            # stuff = [76, 32, 59, 17, 75, 30, 73, 31, 73, 31, 63, 19, 78, 33, 62, 
            # 20, 69, 29, 82, 38, 74, 29, 98, 69, 74, 23, 51, 33, 41, 68, 
            # 65, 53, 40, 310, 106, 46, 53, 40, 166, 103, 46, 53, 40, 436,
            #  103, 46, 53, 40, 508, 103, 46, 53, 40, 553, 103, 46, 53, 40, 
            # 390, 101, 46, 53, 40, 198, 101, 46, 53, 40, 832, 101, 46, 53, 
            # 40, 521, 101, 46, 53, 40, 521, 101, 46, 53, 40, 253, 101, 46, 
            # 53, 40, 232, 101, 46, 53, 40, 301, 101, 46, 53, 40, 419, 101, 
            # 46, 53, 40, 489, 101, 46, 53, 40, 355, 100, 46, 53, 40, 423, 
            # 100, 46, 53, 40, 461, 100, 46, 53, 40, 2159, 100, 46, 53, 40, 
            # 625, 100, 46, 35]
        self.log('Saved file %s' % filename)
        # identify next page and recurse
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)