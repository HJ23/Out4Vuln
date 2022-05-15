from core.HHI import HHI
from core.Spider import Spider
from core.Raptor import Raptor
from core.DirSearch import DirSearch
from core.Bypass403 import Bypass403
from core.HttProbe import HttProbe
from core.Nuclei import Nuclei
from core.Spider import Spider
from core.SSRF import SSRF
from core.PathTraversal import PathTraversal
from core.CORS import CORS
from core.Bypass403 import Bypass403
from core.Reporter import Reporter
from core.URLGatherer import URLGatherer
from thirdparty.raptor.Chaos import ChaoSubdomainEnum


from utils.utilities import *


class Scanner():
    def __init__(self,args):
        self.args=args
        CONFIGS.VERBOSE_MODE=args.verbose
        CONFIGS.CONST_DOMAIN=args.domain
        CONFIGS.CONST_REFERER=args.referer
        CONFIGS.EXCLUDED_DOMAINS=read_file(CONFIGS.CONST_EXCLUDED_OUT) 
        
        self.reporter=Reporter()
        # problem here
        self.verbose_obj=FILELogger(CONFIGS.CONST_VERBOSE_OUT)
        self.cached_obj=FILELogger(CONFIGS.CONST_CACHED_OUT)
        
        
    def start(self):
        # recon phase
        # subdomain recon
        
        if(self.args.new):
            init_scanner()

        if( (self.args.subf or self.args.all ) and not self.args.chaos):
            Log.success("Recon started successfully  "+":From Server : "+self.args.keyword)
            raptor_obj=Raptor()
            Log.success("Raptor started successfully  "+":From Server : "+self.args.keyword)
            raptor_obj.start(CONFIGS.CONST_DOMAIN)
            Log.success("Raptor finished successfully  "+":From Server : "+self.args.keyword)
        
        if(  self.args.chaos):
            Log.success("Recon started successfully  "+":From Server : "+self.args.keyword)
            chaos_obj=ChaoSubdomainEnum()
            Log.success("Chaos started successfully  "+":From Server : "+self.args.keyword)
            chaos_obj.start(CONFIGS.CONST_DOMAIN)
            Log.success("Chaos finished successfully  "+":From Server : "+self.args.keyword)
        
        
        
        # httprobe
        # should check cache
        if(self.args.httpp or self.args.all):
            
            
            subdomains=read_file(CONFIGS.CONST_SUBFINDER_OUT)
            
            final_sbs=[]
            for subdomain in subdomains:
                if(subdomain in CONFIGS.EXCLUDED_DOMAINS):
                    continue
                final_sbs+=[subdomain]
            
            
            Log.success("HttProbe started successfully  "+":From Server : "+self.args.keyword)
            httprobe_obj=HttProbe(no_load=self.args.noload)
            httprobe_obj.start(final_sbs)
            Log.success("HttProbe finished successfully  "+":From Server : "+self.args.keyword)
                
        # should check cache
        
        if(self.args.dirsearch or self.args.all):
        # dirsearch
            Log.success("Dirsearch started successfully  "+":From Server : "+self.args.keyword)
            clean_subdomains=read_file(CONFIGS.CONST_HTTPROBE_OUT)
            dirsearch_obj=DirSearch()
            dirsearch_obj.start(clean_subdomains)
            Log.success("Dirsearch finished successfully  "+":From Server : "+self.args.keyword)
           
        if(self.args.bypass403 or self.args.all):
            Log.success("Bypass403 started successfully  "+":From Server : "+self.args.keyword)
            dir_403=read_file(CONFIGS.CONST_DIRSEARCH_OUT_403)
            b403_obj=Bypass403(self.reporter)
            b403_obj.start(dir_403)
            Log.success("Bypass403 finished successfully  "+":From Server : "+self.args.keyword)
        
            
            
        # nuclei
        # clean_subdomains + dirsearch_out(200,403)
        if(self.args.nuclei or self.args.all):
            Log.success("Nuclei started successfully  "+":From Server : "+self.args.keyword)
            final_nuclei=read_file(CONFIGS.CONST_HTTPROBE_OUT)
        
            nuclei_obj=Nuclei(self.reporter)
            nuclei_obj.start(final_nuclei)
            Log.success("Nuclei finished successfully  "+":From Server : "+self.args.keyword)
        
        # Spider
        # should check cache
        if(self.args.spider):
            Log.success("Spider started successfully  "+":From Server : "+self.args.keyword)
            subdomains=read_file(CONFIGS.CONST_HTTPROBE_OUT)
            spider_obj=Spider(limit=self.args.limit,reporter=self.reporter)
            spider_obj.start(subdomains)
            classify()
            Log.success("Spider finished successfully  "+":From Server : "+self.args.keyword)
            
            
        if(self.args.urlgather or self.args.all):
            Log.success("URLGatherer started successfully  "+":From Server : "+self.args.keyword)
            subdomains=read_file(CONFIGS.CONST_HTTPROBE_OUT)
            spider_obj=URLGatherer()
            spider_obj.start(subdomains)
            classify()
            Log.success("URLGatherer finished successfully  "+":From Server : "+self.args.keyword)
            
        
            
        # SSRF
        # should check cache
        if(self.args.ssrf or self.args.all):
            Log.success("SSRF started successfully  "+":From Server : "+self.args.keyword)
            subdomains=read_file(CONFIGS.CONST_HTTPROBE_OUT)
            ssrf_obj=SSRF(self.verbose_obj)
            ssrf_obj.start(subdomains)
        
            spider_out=read_file(CONFIGS.CONST_SPIDER_OUT)
            ssrf_obj.start(spider_out)
            Log.success("SSRF finished successfully  "+":From Server : "+self.args.keyword)
        # HHI
        # should check cache
        if(self.args.hhi or self.args.all):
            Log.success("HHI started successfully  "+":From Server : "+self.args.keyword)
            
            
            inputs=read_file(CONFIGS.CONST_HTTPROBE_OUT)
            inputs+=read_file(CONFIGS.CONST_SPIDER_OUT)
            
            hhi_obj=HHI(self.reporter)
            hhi_obj.start(inputs)
        
            Log.success("HHI finished successfully  "+":From Server : "+self.args.keyword)
        
        
        
        if(self.args.pathtraversal or self.args.all):
            Log.success("PathTraversal started successfully  "+":From Server : "+self.args.keyword)
            fileio_out=read_file(CONFIGS.CONST_FILEIO_OUT)
            pt_obj=PathTraversal(self.reporter)
            pt_obj.start(fileio_out)
            
            subdomains=read_file(CONFIGS.CONST_HTTPROBE_OUT)
            pt_obj=PathTraversal(self.reporter)
            pt_obj.start(subdomains)
            
            Log.success("PathTraversal finished successfully  "+":From Server : "+self.args.keyword)
        # CORS
        # should check cache
        if(self.args.cors or self.args.all):
            Log.success("CORS started successfully  "+":From Server : "+self.args.keyword)
            spider_out=read_file(CONFIGS.CONST_SPIDER_OUT)
            cors_obj=CORS(self.reporter)
            cors_obj.start(spider_out)
            Log.success("CORS finished successfully  "+":From Server : "+self.args.keyword)
       
        
        self.verbose_obj.finalize()
        self.reporter.save(finalize=True)
        Log.success("*Whole pipeline finished successfully  "+":From Server : "+self.args.keyword)