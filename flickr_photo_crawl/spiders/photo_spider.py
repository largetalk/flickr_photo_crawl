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
        #self.rules = [
        #        Rule(SgmlLinkExtractor(allow=['/photos/%s/page\d+/' % username])),
        #        Rule(SgmlLinkExtractor(allow=['/photos/%s/\d+/in/photostream' % username]), 'parse_image')
        #]


    def parse_image(self, response):
        hxs = HtmlXPathSelector(response)

        item = FlickrPhotoCrawlItem()
        item['web_url'] = response.url
        flickr_id = re.findall('photos/\w+/(\d+)/in/photostream', response.url)[0]
        item['name'] = hxs.select("//h1[@id='title_div']/text()").extract()
        item['set_name'] = hxs.select("//ul[@id='secondary-contexts']/li/div[2]/a/span/span[3]/text()").extract()
        item['ksize_url'] =  "http://www.flickr.com/photos/%s/%s/sizes/k/in/photostream/" % (self.username, flickr_id)
        item['download_url'] = ''
        return item


                         

