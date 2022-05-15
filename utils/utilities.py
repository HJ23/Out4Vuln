import os
import time
import random
import re
import requests
from termcolor import cprint
from functools import wraps
from datetime import datetime
from urllib.parse import parse_qs,urlparse
from utils.slack import Slack
from utils.config import Configs 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Log:
    @staticmethod
    def info(arg,name=""):
        if(Configs.VERBOSE_MODE):
            if(isinstance(arg,str)):
                cprint("# [INFO] "+arg,"blue")
            else:
                cprint("# [INFO] "+str(arg)+" : "+name,"red")
        return
    @staticmethod
    def success(arg):
        Slack.send(msg=arg)
        cprint(arg,"green")
        return

class Requester:
    def __init__(self):
        # add host and origin
        self.HEADERS={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Referer":Configs.ConstReferer,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8",
            "Accept-Encoding": "gzip",
            }
        self.SESSION=requests.Session()
    def set_cookies(self,cookies):
        self.SESSION.cookies.update(cookies)
    def get_cookies(self):
        return self.SESSION.cookies.get_dict()
    def send_post(self,url,data,auth,json):
        try:
            return self.SESSION.post(url,auth=auth,data=data,json=json,headers=self.HEADERS,verify=False,timeout=Configs.TIMEOUT)
        except Exception as e:
            Log.info(e)
    def send_get(self,url,params):
        try:
            return self.SESSION.get(url=url,allow_redirects=True,headers=self.HEADERS,verify=False,timeout=Configs.TIMEOUT,params=params)
        except Exception as e:
            Log.info(e)
        

# logging decorator
def LOGGER(name):
    def wrapper(func):
        @wraps(func)
        def run(*args,**kwargs):
            Log.info(f"* {name} just started !")
            out=func(*args,**kwargs)
            Log.info(f"* {name} just finished ! {len(out)} subdomains found !")
            return out
        return run
    return wrapper

def rand_sleep():
    time.sleep(random.randint(1,4))
    return

def cache_check(headers):
    headers={ a.lower():b.lower() for a,b in zip(headers.keys(),headers.values())  }
    for header_val,header in zip(headers.values(),headers.keys()):
        header=header.lower()
        header_val=header_val.lower()
        if("cache" in header and not ("no-cache" in header_val or "max-age=0" in header_val ) or ("hit" in header_val or "miss" in header_val)):
            return True
    return False

def save_file(**files_urls_dict):
    for file_name,urls in files_urls_dict.items():
        with open(file_name,"w") as file:
            file.writelines(urls)
    return

def read_file(filename):
    if(not os.path.exists(filename)):
        return []
    with open(filename,"r") as file:
      results=file.readlines()
      results=list(map(lambda x:x.split("\n")[0],results))
    return results

def add_prefix(url):
    if(url!="" and not "http://" in url and not "https://" in url and url[0]!="/" and url[0]!="\\" ):
      url="https://"+url
    return url

def correct_url(abs_url,url):
    if((len(url)>4 and url[0:4]=="http")):
        return url
    path=abs_url.split("/")[2]
    url=url.split("#")[0] if("#" in url) else url
    path=path+url if(len(url)!=0 and (url[0]=="/" or url[0]=="\\")) else path+"/"+url
    return path

def get_date_and_time():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

# classify and clean urls gathered from open-source resources. 
def classify_urls(domain_name):
    url_matcher=re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    parameterized_urls=[]
    redirect_urls=[]
    fileio_urls=[]
    api_urls=[]
    normal_urls=[]
    urls=[]
    urls+=read_file(Configs.ConstSpiderOutPath)
    urls+=read_file(Configs.ConstWaybackOutPath)
    urls+=read_file(Configs.ConstRaptorOutPath)

    for url in urls:
        url=requests.utils.unquote(url)
        if(not domain_name in url):
          continue
        tmp_urlparse=parse_qs(urlparse(url).query)
        if(len(tmp_urlparse)!=0):
          for key in tmp_urlparse.keys():
            if(bool(url_matcher.match(tmp_urlparse[key][0]))):
              redirect_urls.append(url)
          parameterized_urls.append(url)
          continue
        if("/api/" in url):
          api_urls.append(url)
          continue
        for keyw in Configs.CONST_EXTENSION:
          if(keyw in url):
            fileio_urls.append(url)
            continue
        normal_urls.append(url)
      
    urls={Configs.ConstDomain+"_redirect_urls.txt":redirect_urls,Configs.ConstDomain+"_parameterized_urls.txt":parameterized_urls,Configs.ConstDomain+"_fileio_urls.txt":fileio_urls,Configs.ConstDomain+"_api_urls.txt":api_urls,Configs.ConstDomain+"_normal_urls.txt":normal_urls}
    return urls
