import os
import yaml

def read_yaml(path):
    with open(path,"r") as file:
        configs=yaml.load(file,Loader=yaml.FullLoader)
    return configs

class Configs:
    ConstDomain=""
    ConstReferer=""
    THREADS=4
    TIMEOUT=10
    ConstRootPath=os.path.dirname(os.path.abspath(__file__),"..")
    ConstReportPath=os.path.join(ConstRootPath,"reports")
    ConstDownloadPath=os.path.join(ConstRootPath,"outputs","ZIP")
    ConstYAMLPath=os.path.join(ConstRootPath,"config.yaml")
    ConstAPIKeys=read_yaml(ConstYAMLPath)["API_KEYS"]
    ConstExcludedExtensions=read_yaml(ConstYAMLPath)["EXTENSIONS"]
    ConstExcludedDomains=read_yaml(ConstYAMLPath)["EXCLUDED_DOMAINS"]
    ConstCookiePath=read_yaml(ConstYAMLPath)["COOKIE_PATH"]
    ConstSpiderOutPath=os.path.join(ConstRootPath,"outputs",ConstDomain+"_spider.txt")
    ConstWaybackOutPath=os.path.join(ConstRootPath,"outputs",ConstDomain+"_wayback.txt")
    ConstRaptorOutPath=os.path.join(ConstRootPath,"outputs",ConstDomain+"_raptor.txt")
    ConstSlackWebHook=read_yaml(ConstYAMLPath)["SLACK_WEBHOOK"]
    
    
    REGEX_OBJ_URL=re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    
    REGEX_OBJ_URL_SPIDER=re.compile('https?://[^\s<>"]+|www\.[^\s<>"\']+') #"(?P<url>https?://[^\s]+)+[^<>)'#-]")

    CONST_PATH_TRAVERSAL_PAYLOADS={"..%2f":"%2f","../":"/","%2e%2e%2f":"%2f","%2e%2e/":"/","%2e%2e%5c":"%5c","%2e%2e\\":"\\","..%5c":"%5c"}
