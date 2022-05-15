from thirdparty.raptor.FinderBase import *
from utils.utilities import *

class Shodan(FinderBaseClass):
    def __init__(self):
        super().__init__()
        self.API_KEY=Configs.ConstAPIKeys["SHODAN_API_KEY"]
        self.URL="https://api.shodan.io/dns/domain/{domain}?key={api_key}"
    @LOGGER("Shodan")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain,api_key=self.API_KEY)
        try:
            out=self.requester.send_get(tmp_url)
            if(not out is None and out.status_code==200):
                json_resp=out.json()
                results+=list(map(lambda x:x+"."+domain,json_resp["subdomains"]))
        except Exception as e:
            Log.info(e,"Shodan")
        return self.clean(results,domain)