from thirdparty.raptor.FinderBase import *
from utils.utilities import *

class DNSDumpster(FinderBaseClass):
    def __init__(self):
        super().__init__()
        
        self.URL="https://dnsdumpster.com"
        self.CSRF_REGEX=re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">', re.S)
        self.TABLE_REGEX=re.compile('<a name="hostanchor"><\/a>Host Records.*?<table.*?>(.*?)</table>', re.S)
        self.URL_REGEX=re.compile('<td class="col-md-4">(.*?)<br>', re.S)
    def extract(self,resp):
        results = []
        try:
            table = self.TABLE_REGEX.findall(resp)[0]
        except IndexError:
            table = ''
        results = self.URL_REGEX.findall(table)
        results = list(set(results))
        for i,link in enumerate(results):
            results[i]= link.strip()
        return results    
    def getToken(self,resp):
        token = self.CSRF_REGEX.findall(resp)[0]
        return token.strip()
    
    @LOGGER("DNSDumpster")
    def start(self,domain):
        results=[]
        self.requester.HEADERS['Referer'] = 'https://dnsdumpster.com'
        try:
            out=self.requester.send_get(self.URL)
            if(not out is None and out.status_code==200):
                resp=out.text
                token=self.getToken(resp)
                params = {'csrfmiddlewaretoken': token, 'targetip': domain}
                post_resp = self.requester.send_post( self.URL, params=params).text
                results=self.extract(post_resp)
        except Exception as e:
            Log.info(e,"DNSDumpster") 
        return self.clean(results,domain)
