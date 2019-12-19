"""Run: $ scrapy runspider main.py"""
import os
import re

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

        filename = "quotes.html"
        with open(filename, 'a') as f:
            #memeing filtered_row
            filtered_row = [re.sub(r'\<.*\>', ',', res) for res in response.css("span[id*='quote_display_content']").getall()]
            print(filtered_row)
            for r in filtered_row:
                print(r)
                f.write(r)


        self.log(f"Saved file {filename}")
        
        # # TODO fix the dumb
        # self.clean(filename) 


        # identify next page and recurse
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    

    # def clean(self, filename):
    #     with open(filename, 'a') as f:
    #         f.write(re.sub(r'\<.*\>', '', res))
            