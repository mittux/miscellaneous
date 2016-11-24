# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from top_imdb_250.TopIMDb250DB import TopIMDb250DataBase


class TopImdb250DBPipeline(object):

    def open_spider(self, spider):
        self.db = TopIMDb250DataBase()
        self.db.removeAllTitles()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        forward_item_to_feed = item.copy()
        self.db.insertTitle(item) # this function alters 'item'
        return forward_item_to_feed


class OmdbInfoPipeline(object):

    def __init__(self):
        self.url = 'http://www.omdbapi.com/?'

    def process_item(self, item, spider):
        payload = { 'i' : item['id'], 'plot' : 'full', 'r' : 'json'}
        try:
            resp = requests.get(self.url, params=payload)
        except Exception as e:
            print(e)
        return resp.json() if resp else item