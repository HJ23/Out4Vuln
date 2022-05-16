from core.AttackerBase import AttackerBase
from core.FinderBase import FinderBase
from utils.utilities import *
from bs4 import BeautifulSoup as BS
from utils.utilities import *
from urllib.parse import urlparse
from core.modules.vulnerability.HiddenFinder import HiddenFinder

# spider will fetch contents of subdomains limit by subdomain
# limit for each starting point
# depth for limitation for each page

class Spider(FinderBase):
    def __init__(self,reporter,depth=5,limit=200):
        super().__init__(reporter)
        self.hiddenfinder=HiddenFinder(self.reporter)
        self.limit=limit
        self.depth=depth
    def has_link(self,tag):
        return tag.has_attr('href') or tag.has_attr('src') or tag.has_attr('xlink:href') or  tag.has_attr("data-src")
    def start(self,urls):
        results=set()
        already_visited=set()
        for _,url in enumerate(urls):
            url_counter=1
            tmp_queue=[(url,0)]
            already_visited.add(url)
            while(len(tmp_queue)!=0 and url_counter<=self.limit):
                if(url_counter%100==0):
                    save_file({os.path.join(Configs.ConstOutputPath,Configs.ConstDomain+"_spider.txt") : list(results)},Configs.ConstSpiderOutPath)
                node,counter=tmp_queue.pop(0)
                node=add_prefix(node)
                url_counter+=1
                found=False
                for ext in Configs.ConstExcludedExtensions:
                    if(ext in node.lower()):
                        found=True
                        break
                if(found):
                    continue
                resp=self.requester.send_get(node)
                if(resp is None or resp.status_code==404):
                    continue
                node=requests.utils.unquote(node)
                results.add(node)
                self.hiddenfinder.check(resp.text,)    
                tmp_urls=re.compile('https?://[^\s<>"]+|www\.[^\s<>"\']+').findall(resp.text)
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
    