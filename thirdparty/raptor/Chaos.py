from distutils.command.clean import clean
from thirdparty.raptor.FinderBase import *
from utils.utilities import *
import os
from zipfile import ZipFile

class ChaoSubdomainEnum(FinderBaseClass):
    def __init__(self):
        super().__init__()
        self.URL="https://chaos-data.projectdiscovery.io/{domain}.zip"
    def clean(self,key,path):
        os.remove(os.path.join(path,key+".zip"))
        for file in os.listdir(path):
            os.remove(os.path.join(path,file))
        os.rmdir(os.path.join(path,key))
    @LOGGER("ChaosSubdomainEnum")
    def start(self,domain):
        results=[]
        key=domain.split(".")[0]
        tmp_url=self.URL.format(domain=key)
        try:
            os.mkdir(os.path.join(Configs.ConstDownloadPath,key))
            path=os.path.join(Configs.ConstDownloadPath,key+".zip")
            file=open(path  ,"wb")
            req=self.requester.send_get(tmp_url)
            file.write(req.content)
            file.close()
            with ZipFile(path, 'r') as zip:
                zip.extractall(path=os.path.join(Configs.ConstDownloadPath,key))
            for file in os.listdir(os.path.join(Configs.ConstDownloadPath,key)):
                if(file.endswith(".txt")):
                    with open(os.path.join(Configs.ConstDownloadPath,key,file),"r") as f:
                        for line in f:
                            results.append(line.strip().replace("\n",""))
            self.clean(key,Configs.ConstDownloadPath)
        except Exception as e:
           Log.info(e,"Chaos")
        return self.clean(results,domain)