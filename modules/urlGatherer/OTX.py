from core.FinderBase import FinderBase
from utils.utilities import *

class OTX(FinderBase):
    def __init__(self):
        super().__init__()
        self.URL="https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list?limit=100&page={page}"
    def start(self,domain):
        page_count=0
        results=[]
        try:
            while( True ):
                tmp_url=self.URL.format(domain=domain,page=str(page_count))
                out=self.requester.send_get(tmp_url)
                json_out=out.json()
                
                for result in json_out["url_list"]:
                    results+=[result["url"]]
                if(not json_out["has_next"]):
                    break
                page_count+=1
        except Exception as e:
            Log.info(e)        
        return self.clean(results,domain)
