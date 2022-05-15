import subprocess
from os.path import expanduser
from utils.utilities import *
import time
from core.Reporter import Reporter

class Nuclei:
    def __init__(self,reporter):
        self.home = expanduser("~")
        self.severities=["info","low","medium","high","critical","leak"]
        self.useless=["\\x1b","\\n","\\t","[","]","'b"]
        self.reporter=reporter

    def start(self,urls):
        
        p1=subprocess.Popen("nuclei -update-templates",shell=True,stdout=subprocess.PIPE)
        if(p1.wait()!=0):
            pass
        
        for i,url in enumerate(urls):
            
            p1=subprocess.Popen(f"nuclei -target {url} -silent -no-color -t ~/nuclei-templates",shell=True,stdout=subprocess.PIPE)
            out=p1.stdout.readlines()
            if(p1.wait()!=0):
                pass
        
            out=str(out)
            for u in self.useless:
                if(u in out):
                    out=out.replace(u, " ")
            outs=out.split(",")
            result=[]
            for out in outs:
                for i,severity in enumerate(self.severities):
                    if(severity in out):
                        result.append(out)
            self.reporter.addRow(url, result)     
            time.sleep(1)
        self.reporter.save()
            
       