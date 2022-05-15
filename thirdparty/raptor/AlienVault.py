from thirdparty.raptor.FinderBase import *
from utils.utilities import *

class AlienVault(FinderBaseClass):
    def __init__(self):
        super().__init__()
        self.URL="https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    @LOGGER("AlienVault")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain)
        try:
            out=self.requester.send_get(tmp_url)
            json_resp=out.json()
            resps=json_resp["passive_dns"] if("passive_dns" in json_resp.keys()) else [] 
            for resp in resps:
                results.append(resp["hostname"])
        except Exception as e:
            Log.info(e,"AlienVault")
        return self.clean(results, domain)