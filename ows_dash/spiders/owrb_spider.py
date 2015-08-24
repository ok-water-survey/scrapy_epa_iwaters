from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from BeautifulSoup import BeautifulSoup
from datetime import datetime
#import codecs
from pymongo import Connection
# DB Collection Host
Host = 'worker.oklahomawatersurvey.org'
database = 'ows'
site_collection = 'owrb_water_sites' #'owrb_monitor_sites'
data_collection = 'owrb_water_wells' #'owrb_monitoring_wells'
#mongo Connection
db=Connection(Host)


siteids=[]#'85152','85182','85190','85191','85192','85193','86266']
for row in db[database][site_collection].find():
    siteids.append(row['WELL_ID'])
# setup list of urls to crawl
url_template='http://www.owrb.ok.gov/wd/search_test/water_levels.php?siteid=%s'
urls=[]
for huc in siteids: 
    urls.append(url_template % (huc))
#setup colums to insert into mongo
cols={'1':'observed_date','2':'value','3':'status','4':'project'}
#remove old data
#db.ows.owrb_monitoring_wells.remove()
class owrb(BaseSpider):
    name="owrb"
    allowed_domains = ["owrb.ok.gov"]
    start_urls = urls 
    def __init__(self):
        #remove old data
        try:
            now = datetime.now()
            collection_backup = "%s_%s" % (data_collection, now.strftime("%Y_%m_%d_%H%M%S") )
            db[database][data_collection].rename(collection_backup) #.ows.owrb_monitoring_wells.remove()
        except:
            pass
    def parse(self, response):
        #db=Connection(Host)
        now=datetime.now()
        site_id=response.url.split("=")[-1]
        hxs = HtmlXPathSelector(response)
        tables = hxs.select('//tr')
        #print tables
        for tab in tables:
            data={'site':site_id,'source':response.url,'unit':'ft','unit_description':'feet from land surface','scrape_date':now}
            soup=BeautifulSoup(tab.extract().encode("ascii","ignore"))
            i=1
            for col in soup.findAll(name='td'):
                try:
                    if i==1:
                        temp=col.contents[0].strip(' \t\n\r')
                        data['sort_date']=datetime.strptime(temp, '%m/%d/%Y %I:%M %p')
                    data[cols[str(i)]]= col.contents[0].strip(' \t\n\r')
                    i=i+1
                except:
                    pass
                    #print data
            #print data
            if len(data.keys())>5:
                #print database,data_collection, data    
                db[database][data_collection].save(data)

