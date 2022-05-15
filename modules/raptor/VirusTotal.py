from core.FinderBase import *
from utils.utilities import *

class VirusTotal(FinderBase):
    def __init__(self):
        super().__init__()
        self.API_KEY=Configs.ConstAPIKeys["VIRUSTOTAL_API_KEY"]
        self.URL="https://www.virustotal.com/vtapi/v2/domain/report?domain={domain}&apikey={key}"
    @LOGGER("VirusTotal")
    def start(self,domain):
        results=[]
        try:
            tmp_url=self.URL.format(key=self.API_KEY,domain=domain)
            out=self.requester.send_get(tmp_url)
            if(not out is None and out.status_code==200):
                json_out=out.json()
                results+=json_out["subdomains"] if("subdomains" in json_out.keys()) else []
        except Exception as e:
            Log.info(e,"VirusTotal")
        return self.clean(results,domain)