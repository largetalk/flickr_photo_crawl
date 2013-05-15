# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class FlickrPhotoCrawlItem(Item):
    # define the fields for your item here like:
    # name = Field()
    web_url = Field()
    name = Field()
    set_name = Field()
    ksize_url = Field()
    download_url = Field()
