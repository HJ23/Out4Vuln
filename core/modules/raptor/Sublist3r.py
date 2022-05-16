from core.FinderBase import *
from utils.utilities import *

class Sublist3r(FinderBase):
    def __init__(self):
        super().__init__()        
        self.URL="https://api.sublist3r.com/search.php?domain={domain}"
    @LOGGER("Sublist3r")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain)
        try:
            out=self.requester.send_get(tmp_url)
            if(not out is None and out.status_code==200):
                resp=out.json()                        
                results+=resp if(not resp is None) else []
        except Exception as e:
            Log.info(e,"Sublist3r")
        return self.clean(results,domain)
