from utils.utilities import *
import os
from concurrent.futures import ThreadPoolExecutor
from termcolor import cprint


class HttProbe(BaseClass):
    def __init__(self,no_load=False):
        super().__init__()
        
        CONFIGS.TIMEOUT=3    
        self.ports=["81","2082", "2087", "2095", "2096", "2480", "3000", "3128", "3333", "4243", "4567", "4711", "4712", "4993", "5000", "5104", "5108", "5800", "6543", "7000", "7396", "7474", "8000", "8001", "8008", "8014", "8042", "8069", "8080", "8081", "8088", "8090", "8091", "8118",  "8880", "8888", "8983", "9000", "9043", "9060", "9080", "9090", "9091", "9200", "9443", "28017","4443"] if(not no_load) else []
        self.subd_count=0
        self.counter=0
        
    def check(self,domain):
        results=[]
        
        for prefix in ["http://","https://"]:
            url=prefix+domain
            req=self.requester.send_get(url)
            if(not req is None):
                results.append(url)                    
            
        
        for prefix in ["http://","https://"]:
            for port in self.ports:
                url=prefix+domain+":"+port
                req=self.requester.send_get(url)
                if(not req is None):
                    results.append(url)                    
        
        self.counter+=1
        if(self.counter%(int(self.subd_count*0.1)+1)==0):
            Log.success(f"* HTTPPROBE { self.counter*100//self.subd_count+1 }% of work completed! ")
        
        return results     
        
    
    def start(self,domains):
        
        self.subd_count=len(domains)
        final=[]
        futures=[]
        
        with ThreadPoolExecutor(CONFIGS.THREADS) as thread:
            for i,domain in enumerate(domains):
                futures.append(thread.submit(self.check,domain=domain))
                
                    
        for future in futures:
            final+=future.result()
        
        save_file(final,CONFIGS.CONST_HTTPROBE_OUT)
