from utils.utilities import *


class WaybackMachine(BaseClass):
    def __init__(self):
        super().__init__()
        
        self.URL="https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&collapse=urlkey&fl=original&page={page}"
    def start(self,domain):
        page_count=0
        results=[]
        
        try:
            while( True ):
                tmp_url=self.URL.format(domain=domain,page=str(page_count))
                out=self.requester.sendGET(tmp_url)
                if(out.text==""):
                    break
                
                for result in out.json()[1:]:
                    results+=result
                page_count+=1
        except Exception as e:
            Log.info(e)
        return list(set(results))
