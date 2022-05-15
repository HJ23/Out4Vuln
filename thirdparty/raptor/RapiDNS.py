from thirdparty.raptor.FinderBase import *
from utils.utilities import *
import re

class RapiDNS(FinderBaseClass):
    def __init__(self):
        super().__init__()        
        self.URL="https://rapiddns.io/subdomain/{domain}"
        self.REGEX_URL=re.compile('<a href="(.*?)"')
    @LOGGER("RapidDNS")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain)
        try:
            out=self.requester.send_get(tmp_url)
            if(not out is None and out.status_code==200):
                urls=self.REGEX_URL.findall(out.text)
                results+=urls
        except Exception as e:
            Log.info(e,"RapiDNS")
        return FinderBaseClass.clean(results, domain)