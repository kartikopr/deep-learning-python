import scrapy
import numpy
import pandas
import re

class WebCrawler(scrapy.Spider):
    name = "comment"
    start_urls = [
        'http://46.166.167.16/threads/panlok-pacar-ttm-binor.1271363/page-2'
    ]
    
    csv = []

    def parse(self, response):
        for comment in response.css('div.messageInfo'):
            if(re.sub(r'(\\[rn]|\s){2,}','',comment.css('blockquote.messageText::text').extract_first()) != ''):
                self.csv.append([re.sub(r'(\\[rn]|\s){2,}','',comment.css('blockquote.messageText::text').extract_first())])
            yield{
                #'comment' : comment.xpath('.//div[@class="messageContent"]/blockquote[@class="messageText"]/text()').extract_first()
                'comment' : re.sub(r'(\\[rn]|\s){2,}','',comment.css('blockquote.messageText::text').extract_first()) #comment.css('blockquote.messageText::text').extract_first()
            }
        next_page = response.css('nav a.text::attr(href)')[1].extract()
        if next_page is not None : 
            yield response.follow(next_page, callback=self.parse)
        data = pandas.DataFrame(self.csv)
        data.to_csv('coba.csv', sep = '\t')
        
            
        