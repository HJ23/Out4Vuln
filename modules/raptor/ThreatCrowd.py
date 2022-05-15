from core.FinderBase import *
from utils.utilities import *

class ThreatCrowd(FinderBase):
    def __init__(self):
        super().__init__()
        self.URL="https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
    @LOGGER("ThreatCrowd")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain)
        try:
            out=self.requester.send_get(tmp_url)
            json_resp=out.json()
            results+=json_resp["subdomains"] if("subdomains" in json_resp.keys()) else []         
        except Exception as e:
            Log.info(e,"ThreadCrowd")
        return self.clean(results,domain)

