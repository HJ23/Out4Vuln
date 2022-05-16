from core.FinderBase import *
from utils.utilities import *

class HackerTarget(FinderBase):
    def __init__(self):
        super().__init__()
        
        self.URL="https://api.hackertarget.com/hostsearch/?q={domain}"
    @LOGGER("HackerTarget")
    def start(self,domain):
        tmp_url=self.URL.format(domain=domain)
        results=[]
        try:
            out=self.requester.send_get(tmp_url)
            if(not out is None and out.status_code==200):
                resp=out.text                        
                for result in resp.split("\n"):
                    if(len(result.split(","))==2):
                        results.append(result.split(",")[0])
        except Exception as e:
            Log.info(e,"HackerTarget")
        return self.clean(results,domain)