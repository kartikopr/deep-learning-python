import scrapy
import numpy
import pandas
import re

class WebCrawler(scrapy.Spider):
    name = "comment"
    start_urls = [
        'http://ahaporno.com/'
    ]
    
    csv = []

    def parse(self, response):
        for judul in response.css("div.ktz-box-content"):

            self.csv.append(re.sub(r'(\\[rn]|\s){2,}','',judul.css('a::text').extract_first()))

            yield{'judul' : re.sub(r'(\\[rn]|\s){2,}','',judul.css('a::text').extract_first())}
        next_page = response.css('ul.pagination li a::attr(href)')[-1].extract()
        if next_page is not None : 
            yield response.follow(next_page, callback=self.parse) 
        data = pandas.DataFrame(self.csv)
        data.to_csv('ahaporno.csv', sep = '\t')           