from core.FinderBase import *
from utils.utilities import *
from bs4 import BeautifulSoup 

class SiteDossier(FinderBase):
    def __init__(self):
        super().__init__()
        self.URL="http://www.sitedossier.com/parentdomain/{domain}"   
    @LOGGER("SiteDossier")
    def start(self,domain):
        tmp_url=self.URL.format(domain=domain)
        results=[]
        try:
            out=self.requester.send_get(tmp_url)
            bs=BeautifulSoup(out.text,"lxml")
            results=list(map(lambda x:x.text,bs.find_all('a',href=True)))
        except Exception as e:
            Log.info(e)
        return self.clean(results,domain)