#
# to run:
# scrapy runspider top_imdb_250_spider.py -o top250.json
# alternatively from top-level dir: scrapy crawl top250 -o top250.json
#

import scrapy

class TopImdb250(scrapy.Spider):
    name = "top250"

    start_urls = ['http://www.imdb.com/chart/top?sort=rk,asc&mode=simple']

    def parse(self, response):
        for each in response.css('td.titleColumn'):
            yield { 'id' : each.css('a::attr(href)').re(r'/title/([\d\w]*)/?.*').pop() }
