from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import codecs
from pymongo import Connection
#db=Connection('worker.oklahomawatersurvey.org')
#db=Connection('fire.rccc.ou.edu')
#year='2012'
url_template='http://ofmpub.epa.gov/waters10/attains_watershed.control?p_state=OK&p_huc=%s&p_cycle=%s&p_report_type='
urls=[]
for huc in db.ows.watersheds.distinct('properties.HUC_8'):
    urls.append(url_template % (huc,'2006'))
    urls.append(url_template % (huc,'2008'))
    urls.append(url_template % (huc,'2010'))
    urls.append(url_template % (huc,'2012'))
    urls.append(url_template % (huc,'2014'))
#db.ows.impaired_waters.remove()
class iwaters(BaseSpider):
    name="iwaters"
    allowed_domains = ["epa.gov"]
    start_urls = urls 
    def __init__(self):
        #remove old data
        #db.ows.impaired_waters.remove()
    def parse(self, response):
        year = response.url.split("p_cycle=")[-1].replace('&p_report_type=','')
        filename = response.url.split("p_huc=")[-1].replace("&p_cycle=%s&p_report_type=" % (year),'')# + '.html'
        hxs = HtmlXPathSelector(response)
        tables = hxs.select('//div[@class="center"]') #'//table')
        data={'huc':filename,'tmdl_year':year}
        i=1
        for tab in tables:
            data['table' + str(i)]=tab.extract().encode("ascii","ignore")
            i=i+1
        print data
        #db.ows.impaired_waters.save(data)

