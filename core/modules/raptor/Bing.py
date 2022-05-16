from core.FinderBase import *
from utils.utilities import *

class Bing(FinderBase):
    def __init__(self):
        super().__init__()     
        self.URL='https://api.bing.microsoft.com/v7.0/search'
        self.requester.HEADERS["Ocp-Apim-Subscription-Key"]=Configs.ConstAPIKeys["BING_API_KEY"]
    @LOGGER("Bing")
    def start(self,domain,limit=15):
        results=[]
        params={"q":"","textFormat":"HTML","count":50}
        params["q"]='''"*.'''+domain+'''"'''
        limits=0
        try:
            for _ in range(0,limit):
                params["offset"]=limits
                out=self.requester.send_get(self.URL,params=params)
                if(not out is None and out.status_code==200):
                    json_resp=out.json()
                    for resp in json_resp["webPages"]["value"]:
                        results+=[resp["url"]]
                limits=len(results)
                rand_sleep()
        except Exception as e:
            Log.info(e,"Bing")
        return self.clean(results,domain)