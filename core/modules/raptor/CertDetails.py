from core.FinderBase import *
from utils.utilities import *


class CertDetails(FinderBase):
    def __init__(self):
        super().__init__()
        self.URL="https://certificatedetails.com/api/list/{domain}"
    @LOGGER("CertDetails")
    def start(self,domain):
        results=[]
        tmp_url=self.URL.format(domain=domain)
        try:
            out=self.requester.send_get(tmp_url)
            json_resps=out.json()
            for json_resp in json_resps:
                results+=[json_resp["CommonName"]] if("CommonName" in json_resp.keys()) else []
        except Exception as e:
            Log.info(e,"CertDetails")
        return self.clean(results, domain)