import os
import yaml

from utils.levels import WorkingMode

def read_yaml(path):
    with open(path,"r") as file:
        configs=yaml.load(file,Loader=yaml.FullLoader)
    return configs

class Configs:
    ConstDomain=""
    ConstReferer=""
    ConstOOBDomain=""
    THREADS=4
    TIMEOUT=10
    ConstVerboseMode=False
    ConstWorkingMode=WorkingMode.Aggresive
    ConstRootPath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
    ConstReportPath=os.path.join(ConstRootPath,"reports")
    ConstOutputPath=os.path.join(ConstRootPath,"output")
    ConstDownloadPath=os.path.join(ConstOutputPath,"zip")
    ConstYAMLPath=os.path.join(ConstRootPath,"configs.yaml")
    ConstAPIKeys=read_yaml(ConstYAMLPath)["API_KEYS"]
    ConstExcludedExtensions=read_yaml(ConstYAMLPath)["EXTENSIONS"]
    ConstExcludedDomains=read_yaml(ConstYAMLPath)["EXCLUDED_DOMAINS"]
    ConstCookiePath=read_yaml(ConstYAMLPath)["COOKIE_PATH"]
    ConstSpiderOutPath=os.path.join(ConstRootPath,"outputs",ConstDomain+"_spider.txt")
    ConstWaybackOutPath=os.path.join(ConstRootPath,"outputs",ConstDomain+"_wayback.txt")
    ConstRaptorOutPath=os.path.join(ConstRootPath,"outputs",ConstDomain+"_raptor.txt")
    ConstSlackWebHook=read_yaml(ConstYAMLPath)["SLACK_WEBHOOK"]
    ConstPayloadsPath=os.path.join(ConstRootPath,"payloads")

def reinit_configs(domain,referrer,oob_domain,verbose_mode,working_mode,threads):
    Configs.ConstDomain=domain
    Configs.ConstReferer=referrer
    Configs.ConstOOBDomain=oob_domain
    Configs.ConstVerboseMode=verbose_mode
    Configs.ConstWorkingMode=working_mode
    Configs.THREADS=threads