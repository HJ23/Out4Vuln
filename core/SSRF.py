from utils.utilities import *
from urllib.parse import parse_qs,urlparse

class SSRF(BaseClass):
    def __init__(self,verbose):
        super().__init__()
        CONFIGS.TIMEOUT=10
        self.headers=["X-Forwarded-From","Location"]
        self.verbose_obj=verbose
        
    def start(self,urls):
        
        perm_headers=self.requester.HEADERS.copy()
        
        for i,url in enumerate(urls):
            
            self.verbose_obj.add(url)    
            
            for header in self.headers:
                temp_header=perm_headers.copy()
                temp_header[header]=CONFIGS.CONST_REFERER
                self.requester.HEADERS=temp_header
                self.requester.sendGET(url)
                self.requester.sendPOST(url)
            
            tmp_urlparse=parse_qs(urlparse(url).query)
            for key in tmp_urlparse:
                if(bool(CONFIGS.REGEX_OBJ_URL.match(tmp_urlparse[key][0]))):
                    url=url.replace(tmp_urlparse[key][0],CONFIGS.CONST_REFERER)
                    self.requester.sendGET(url)
                    self.requester.sendPOST(url)
            
            rand_sleep()
    