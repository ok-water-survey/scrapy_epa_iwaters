# Scrapy settings for ows_dash project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'ows_dash'

SPIDER_MODULES = ['ows_dash.spiders']
NEWSPIDER_MODULE = 'ows_dash.spiders'
DOWNLOAD_TIMEOUT = 360
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ows_dash (+http://www.yourdomain.com)'
