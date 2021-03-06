from core.FinderBase import *
from utils.utilities import *

class CertSpotter(FinderBase):
    def __init__(self):
        super().__init__()
        
        self.URL="https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
    
    @LOGGER("CertSpotter")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain)
        try:
            out=self.requester.send_get(tmp_url)
            if(not out is None and out.status_code==200):
                json_resp=out.json()
                for resp in json_resp:
                    results+=resp["dns_names"]
        except Exception as e:
            Log.info(e,"CertSpotter")
        return self.clean(results, domain)

