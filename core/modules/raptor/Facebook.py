from core.FinderBase import *
from utils.utilities import *


class FacebookCert(FinderBase):
    def __init__(self):
        super().__init__()
        self.API_SECRET=Configs.ConstAPIKeys["FACEBOOK_API_SECRET"]
        self.API_ID=Configs.ConstAPIKeys["FACEBOOK_API_ID"]
        self.GETAUTH="https://graph.facebook.com/oauth/access_token?client_id={Id}&client_secret={secret}&grant_type=client_credentials"
        self.GETDOMAINS="https://graph.facebook.com/certificates?fields=domains&access_token={token}&query=*.{domain}"
        self.TOKEN=self.getAuth()
    def getAuth(self):
        tmp_url=self.GETAUTH.format(Id=self.APP_ID,secret=self.APP_SECRET)
        out=self.requester.send_get(tmp_url)
        json_resp=out.json()
        # assert key not found !
        return json_resp["access_token"] if("access_token" in json_resp) else ""
    @LOGGER("FacebookCert")
    def start(self,domain):
        results=[]
        tmp_url=self.GETDOMAINS.format(domain=domain,token=self.TOKEN)
        try:
            while(tmp_url!=""):
                out=self.requester.send_get(tmp_url)
                json_resp=out.json()
                data=json_resp["data"] if("data" in json_resp.keys()) else []
                for domain_obj in data:
                    results+=domain_obj["domains"]
                time.sleep(1.8)
                if("paging" in json_resp.keys()):  
                    tmp_url=json_resp["paging"]["next"] if("next" in json_resp["paging"]) else ""
                else:
                    tmp_url=""
        except Exception as e:
            Log.info(e,"FacebookCert")
        return self.clean(results, domain)