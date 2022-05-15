from core.URLGatherer_Modules.CommonCrawl import CommonCrawl
from core.URLGatherer_Modules.Wayback import WaybackMachine
from core.URLGatherer_Modules.OTX import OTX
from utils.utilities import *

class URLGatherer:
    def __init__(self):
        CONFIGS.TIMEOUT=30
        self.modules=[OTX(),CommonCrawl(),WaybackMachine()]
    
    def start(self,domains):
        final_results=[]
        
        for domain in domains:
            for module in self.modules:
                final_results+=module.start(domain)
                
        save_file(list(set(final_results)),CONFIGS.CONST_SPIDER_OUT)
    
