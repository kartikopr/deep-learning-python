import scrapy
import numpy
import pandas
import re

class WebCrawler(scrapy.Spider):
    name = "comment"
    start_urls = [
        'http://bokepsedarah1.getxid.com/page/2.html'
    ]
    
    csv = []

    def parse(self, response):
        for judul in response.css("div.post"):

            self.csv.append(re.sub(r'(\\[rn]|\s){2,}','',judul.css('a::text').extract_first()))

            yield{'judul' : re.sub(r'(\\[rn]|\s){2,}','',judul.css('a::text').extract_first())}
        next_page = response.css('div.pager li a::attr(href)')[5].extract()
        if next_page is not None : 
            yield response.follow(next_page, callback=self.parse) 
        data = pandas.DataFrame(self.csv)
        data.to_csv('judul.csv', sep = '\t')           