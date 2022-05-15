from utils.utilities import *

class CORS(BaseClass):
    def __init__(self,reporter):
        super().__init__()
        CONFIGS.TIMEOUT=10
        self.reporter=reporter
    def start(self,urls):
        results={"url":[],"header":[]}
        origin_headers=[CONFIGS.CONST_DOMAIN+"@"+"test.com",CONFIGS.CONST_DOMAIN+".test.com","null"]
        self.reporter.createBlock("CORS")
        for url in urls:
            
            
            for origin in origin_headers:
                tmp_headers=self.requester.HEADERS
                tmp_headers["Origin"]=origin
                
                resp=self.requester.sendGET(url)
                if("Access-Control-Allow-Origin" in resp.headers.keys()\
                   or "test.com" in resp.text):
                    results["url"].append(url)
                    results["header"].append(origin)
                    break
            rand_sleep()
        
        for x,y in zip(results["url"],results["header"]):
            self.reporter.addRow(x,y)
        self.reporter.save()
        
   