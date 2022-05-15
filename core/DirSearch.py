from concurrent.futures import ThreadPoolExecutor
from utils.utilities import *
from difflib import SequenceMatcher
from thirdparty.sqlmap.DynamicContentParser import DynamicContentParser
import urllib3
urllib3.disable_warnings()

class DirSearch(BaseClass):

    def __init__(self,reporter=None,chunked=100):
        super().__init__()
        CONFIGS.TIMEOUT=5
        
        self.chunked=chunked
        self.reporter=reporter
        
        self.payloads=read_file(CONFIGS.CONST_ALL_DICT)
        self.results_200=FILELogger(CONFIGS.CONST_DIRSEARCH_OUT_200)
        self.results_403=FILELogger(CONFIGS.CONST_DIRSEARCH_OUT_403)
        self.results_xxx=FILELogger(CONFIGS.CONST_DIRSEARCH_OUT_XXX)
        
    def ratio(self,l1,l2):   # ratio of dissimilarity lower:similar 
        s_obj=SequenceMatcher(None,l1,l2)
        return s_obj.ratio()
    
    def requester_func(self,subdomain):
        subdomain=add_prefix(subdomain)
        dynamicParser=None
        resp=self.requester.sendGET(subdomain)
        if(resp is None):
            return
        tmp_resp1=self.requester.sendGET(subdomain+"/fullbackupx1.sql")
        tmp_resp2=self.requester.sendGET(subdomain+"/admin_panel_123.php")                               
        dynamicParser = DynamicContentParser(tmp_resp1.text,tmp_resp2.text)
        
        for payload in self.payloads:
            subdomain_payload=subdomain+"/"+payload
            
            resp=self.requester.sendGET(subdomain_payload)
            
            if(payload in resp.url and resp.status_code==200 and dynamicParser.compareTo(resp.text)<0.9):
                self.results_200.add(subdomain_payload)
                    
            elif(payload in resp.url and resp.status_code==403 and dynamicParser.compareTo(resp.text)<0.9):
                self.results_403.add(subdomain_payload)
                
            elif(resp.status_code!=404):
                self.results_xxx.add(subdomain_payload)
            
        return None

    def start(self,domains):
        
        
        with ThreadPoolExecutor(CONFIGS.THREADS) as threads:
            for i,subdomain in enumerate(domains):
                threads.submit(self.requester_func, subdomain)
                
        if(self.reporter!=None):
            self.reporter.createBlock("### DIRSEARCH 200")
            for x in self.results_200:
                self.reporter.addRow(x,"200")
        
        self.results_200.finalize()
        self.results_403.finalize()
        self.results_xxx.finalize()
        
        