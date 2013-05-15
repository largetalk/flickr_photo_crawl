# Scrapy settings for flickr_photo_crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'flickr_photo_crawl'

SPIDER_MODULES = ['flickr_photo_crawl.spiders']
NEWSPIDER_MODULE = 'flickr_photo_crawl.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'flickr_photo_crawl (+http://www.yourdomain.com)'
