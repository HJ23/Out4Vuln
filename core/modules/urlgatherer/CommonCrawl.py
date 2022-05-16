from core.FinderBase import FinderBase
from utils.utilities import *

class CommonCrawl(FinderBase):
    def __init__(self):
        super().__init__()
        self.URL="http://index.commoncrawl.org/collinfo.json"
    def start(self,domain):
        page_count=0
        results=[]
        uselesses=['"',"{","}",'url',":"]
        try:
            out=self.requester.send_get(self.URL)
            main_url=out.json()[0]["cdx-api"]
            load="?url={domain}/*&output=json&fl=url&page={page}"
            main_url=main_url+load
            while( True ):
                tmp_url=main_url.format(domain=domain,page=str(page_count))
                out=self.requester.send_get(tmp_url)
                if(out is None or "message" in out.text):
                    break
                tmp_out=out.text
                for useless in uselesses:
                    tmp_out=tmp_out.replace(useless,"")
                tmp_results=list(map(lambda x:x.strip(),tmp_out.split("\n")))
                results+=tmp_results
                page_count+=1
        except Exception as e:
            Log.info(e)        
        return self.clean(results,domain)