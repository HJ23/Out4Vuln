from utils.utilities import *
from bs4 import BeautifulSoup as BS
from utils.utilities import *
from urllib.parse import urlparse
from core.HiddenFinder import HiddenFinder
import urllib3
urllib3.disable_warnings()

# spider will fetch contents of subdomains limit by subdomain
# limit for each starting point
# depth for limitation for each page

class Spider(BaseClass):
    def __init__(self,depth=5,limit=10000,reporter=None):
        super().__init__()
        CONFIGS.TIMEOUT=5
        
        self.reporter=reporter
        self.hiddenfinder=HiddenFinder(self.reporter)
        self.limit=limit
        self.depth=depth
        
    def has_link(self,tag):
        return tag.has_attr('href') or tag.has_attr('src') or tag.has_attr('xlink:href') or  tag.has_attr("data-src")
  
    def start(self,urls):
        results=set()
        already_visited=set()
            
        for i,url in enumerate(urls):
            url_counter=1    
            
            tmp_queue=[(url,0)]
            already_visited.add(url)
        
            while(len(tmp_queue)!=0 and url_counter<=self.limit):
                if(url_counter%100==0):
                    save_file(list(results),CONFIGS.CONST_SPIDER_OUT)
          
                node,counter=tmp_queue.pop(0)
                
                node=node if("https://" in node or "http://" in node) else "https://"+node
                url_counter+=1
                found=False
                for ext in [".gif",".GIF",".ttf",".png",".jpeg",".jpg",".woff",".css",".pdf",".tiff",".svg",".csv",".ini"\
                    ".TTF",".PNG",".JPEG",".JPG",".WOFF",".CSS",".PDF",".TIFF",".SVG",".CSV",".INI"]:
                    if(ext in node):
                        found=True
                        node=requests.utils.unquote(node)
                        results.add(node)
                        break

                if(found):
                    continue
                
                resp=self.requester.sendGET(node)
                
                if(resp is None):
                    continue
                
                self.hiddenfinder.check(resp.text)
                tmp_urls=CONFIGS.REGEX_OBJ_URL_SPIDER.findall(resp.text)
            
                if(resp.status_code!=404):
                    results.add(node)
            
            
                if(not ".js" in node and not ".JS" in node):
                    soup=BS(resp.text,'lxml')
                    href_tags = soup.find_all(self.has_link)
                    for param in ["href","src","data-src","xlink:href"]:
                        hrefs = [tag.get(param) for tag in href_tags]
                        for href in hrefs:
                            if(href==None or href==""):
                                continue
                            href=correct_url(node,href)
                            
                            if(CONFIGS.CONST_DOMAIN in href):
                                if(counter+1<self.depth and not href in already_visited ):
                                    already_visited.add(href)
                                    tmp_queue.append((href,counter+1))
                    continue
            
            
            
                for tmp_url in tmp_urls:
                    
                    url_check=True
                    if( not CONFIGS.CONST_DOMAIN in tmp_url ):
                        continue
                    for edomain in CONFIGS.EXCLUDED_DOMAINS:
                        if( edomain in tmp_url ):
                            url_check=False
                            break
                    if( url_check and counter+1<self.depth and not tmp_url in already_visited ):
                        already_visited.add(tmp_url)
                        tmp_queue.append((tmp_url,counter+1))
        
                rand_sleep()  
        save_file(list(results),CONFIGS.CONST_SPIDER_OUT)
    