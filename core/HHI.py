from utils.utilities import *
import urllib3
urllib3.disable_warnings()

class HHI(BaseClass):
  
  def __init__(self,reporter):
      super().__init__()
      CONFIGS.TIMEOUT=10
      self.headers=["Host","X-Forwarded-For","X-Forwarded-Host","X-Forwarded-Proto",\
               "X-Forwarded-Server","X-Host","Forwarded","X-HTTP-Host-Override","X-Rewrite-Url",
               "X-Originating-IP","X-Remote-IP","X-Remote-Addr","X-Client-IP","X-Original-Url"]
      self.reporter=reporter
      self.cached_resps=FILELogger(CONFIGS.CONST_CACHED_OUT)
      
  def start(self,urls):
      
      self.reporter.createBlock("HHI")
      
      perm_headers=self.requester.HEADERS

      
      for url in urls:
          found=False
          for header in self.headers:
              temp_headers=perm_headers.copy()
              temp_headers[header]=CONFIGS.CONST_DOMAIN+".test.com"
              self.requester.HEADERS=temp_headers
              resp=self.requester.sendGET(url)
              
              
              if(not resp is None):
                  
                  if(not found and cache_check(resp.headers)):
                      self.cached_resps.add(url)
                      found=True
                  if("test.com" in resp.text ):
                      self.reporter.addRow(url,[header,"Cached : "+str(cache_check(resp.headers))])
                      
          rand_sleep()
      self.reporter.save()
      self.cached_resps.finalize()
      
          