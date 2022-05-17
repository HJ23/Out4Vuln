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
        super().__init__()
        self.hiddenfinder=HiddenFinder(reporter)
        self.limit=limit
        self.depth=depth
    def has_link(self,tag):
        return tag.has_attr('href') or tag.has_attr('src') or tag.has_attr('xlink:href') or  tag.has_attr("data-src")
    def check_domains(self,url):
        if(not Configs.ConstDomain in url):
            return True
        for exc_domain in Configs.ConstExcludedDomains:
            if( exc_domain.lower() in url.lower() ):
                return True
        return False
    def check_extensions(self,url):
        for ext in Configs.ConstExcludedExtensions:
            if(url.lower().endswith(ext)):
                return True
        return False
    def start(self,urls):
        results=set()
        already_visited=set()
        for _,url in enumerate(urls):
            url_counter=1
            tmp_queue=[(url,0)]
            already_visited.add(url)

            while(len(tmp_queue)!=0 and url_counter<=self.limit):
                if(url_counter%100==0):
                    save_file({os.path.join(Configs.ConstSpiderOutPath) : list(results)})

                node,counter=tmp_queue.pop(0)
                node=clean_add_prefix(node)
                if(self.check_domains(node)  or self.check_extensions(node)):
                    continue
                
                resp=self.requester.send_get(node)
                if(resp is None or resp.status_code==404):
                    continue  
                else:
                    # add current one and process urls from js , css files
                    node=requests.utils.unquote(node)
                    self.hiddenfinder.check(resp.text) 
                    results.add(node)
                    print("ADDED!!! :",node)
                    tmp_urls=re.compile('https?://[^\s<>"]+|www\.[^\s<>"\']+').findall(resp.text)
                
                # check normal pages for links
                if(not ".js" in node.lower() and not ".css" in node.lower()):
                    soup=BS(resp.text,'lxml')
                    href_tags = soup.find_all(self.has_link)
                    for param in ["href","src","data-src","xlink:href"]:
                        hrefs = [tag.get(param) for tag in href_tags]
                        for href in hrefs:
                            if(href==None or href==""):
                                continue
                            href=correct_url(node,href)
                            
                            if( not (self.check_domains(href) or self.check_extensions(href)) 
                                and (counter+1<self.depth and not href in already_visited) ):
                                already_visited.add(href)
                                tmp_queue.append((href,counter+1))
                # prepare for check links from js, css files        
                for tmp_url in tmp_urls:
                    if( not (self.check_extensions(tmp_url) or self.check_domains(tmp_url)) 
                        and (counter+1<self.depth and not tmp_url in already_visited)):
                        already_visited.add(tmp_url)
                        tmp_queue.append((tmp_url,counter+1))
                rand_sleep()
                url_counter+=1

        save_file({os.path.join(Configs.ConstSpiderOutPath) : list(results)})