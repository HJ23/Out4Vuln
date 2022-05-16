from core.FinderBase import *
from utils.utilities import *

class Censys(FinderBase):
    def __init__(self):
        super().__init__()
        self.URL="https://www.censys.io/api/v1/search/certificates"
        self.API_KEY=Configs.ConstAPIKeys["CENSYS_API_KEY"]
        self.SECRET=Configs.ConstAPIKeys["CENSYS_SECRET"]
    @LOGGER("Censys")
    def start(self,domain,limit=10):
        json_query={"query":f"{domain}", "page":1, "fields":["parsed.names","parsed.extensions.subject_alt_name.dns_names"], "flatten":True}
        results=[]
        page=0
        while(page<limit):
            page+=1
            time.sleep(1)
            try:
                json_query={"query":f"{domain}", "page":page, "fields":["parsed.names","parsed.extensions.subject_alt_name.dns_names"], "flatten":True}
                out=self.requester.send_post(self.URL,auth=(self.API_KEY,self.SECRET),json=json_query)
                if(not out is None and out.status_code==200):
                    json_resp=out.json()
                    limit=json_resp["metadata"]["pages"] if(limit>json_resp["metadata"]["pages"]) else limit  
                    for result in json_resp["results"]:
                        if("parsed.names" in result):
                            results+=result["parsed.names"]
                        if("parsed.extensions.subject_alt_name.dns_names" in result):
                            results+=result["parsed.extensions.subject_alt_name.dns_names"]
            except Exception as e:
                print(e)
                Log.info(e,"Censys")
        return self.clean(results, domain)