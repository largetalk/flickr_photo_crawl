#!/usr/bin/env python
# encoding=utf-8

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from flickr_photo_crawl.items import FlickrPhotoCrawlItem
from scrapy import log
import sys
import re
import sqlite3
### Kludge to set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')
 
class FlickrSpider(CrawlSpider):
    name = "flickr"
    allowed_domains = ["www.flickr.com", "staticflickr.com"]
    start_urls = [
            #"http://www.flickr.com/photos/largetalk/"
    ]
    rules = [
            Rule(SgmlLinkExtractor(allow=['/photos/\w+/page\d+/'])),
            Rule(SgmlLinkExtractor(allow=['/photos/\w+/\d+/in/photostream']), 'parse_image')
    ]

    def __init__(self, username='largetalk', *args, **kwargs):
        super(FlickrSpider, self).__init__(*args, **kwargs)
        self.username = username
        self.start_urls = [
                "http://www.flickr.com/photos/%s/" % username
        ]
        self.conn = sqlite3.connect('photo.db')
        self._create_table()

    def _create_table(self):
        sql1 = '''
        drop table if exists photos;
        '''
        sql2 = '''
        create table if not exists photos (
        flickr_id text,
        web_url text,
        name  text,
        set_name text,
        ksize_url text,
        download_url text
        );
        '''
        self.conn.execute(sql1)
        self.conn.execute(sql2)
        self.conn.commit()

        #self.rules = [
        #        Rule(SgmlLinkExtractor(allow=['/photos/%s/page\d+/' % username])),
        #        Rule(SgmlLinkExtractor(allow=['/photos/%s/\d+/in/photostream' % username]), 'parse_image')
        #]


    def parse_image(self, response):
        hxs = HtmlXPathSelector(response)

        item = FlickrPhotoCrawlItem()
        item['web_url'] = response.url
        flickr_id = re.findall('photos/\w+/(\d+)/in/photostream', response.url)[0]
        item['flickr_id'] = flickr_id
        item['name'] = hxs.select("//h1[@id='title_div']/text()").extract()[0]
        item['set_name'] = hxs.select("//ul[@id='secondary-contexts']/li/div[2]/a/span/span[3]/text()").extract()[0]
        item['ksize_url'] =  "http://www.flickr.com/photos/%s/%s/sizes/k/in/photostream/" % (self.username, flickr_id)
        sql = "insert into photos (flickr_id, web_url, name, set_name, ksize_url) values ('%s', '%s', '%s', '%s', '%s')" % (flickr_id, item['web_url'], item['name'], item['set_name'], item['ksize_url'])
        self.conn.execute(sql)
        self.conn.commit()
        

        yield Request(url=item['ksize_url'], callback=self.parse_download)


    def parse_download(self, response):
        hxs = HtmlXPathSelector(response)
        flickr_id = re.findall('/photos/\w+/(\d+)/sizes/k/in/photostream/', response.url)[0]
        download_url = hxs.select("//div[@id='allsizes-photo']/img/@src").extract()[0]
        cu = self.conn.cursor()
        sql = "select flickr_id, web_url, name, set_name, ksize_url from photos where flickr_id = %s" % flickr_id
        cu.execute(sql)
        row = cu.fetchone()

        item = FlickrPhotoCrawlItem()
        item['flickr_id'] = row[0]
        item['web_url'] = row[1]
        item['name'] = row[2]
        item['set_name'] = row[3]
        item['ksize_url'] = row[4]
        item['download_url'] = download_url

        return item

