from core.Raptor_Modules.Facebook import FacebookCert
from core.Raptor_Modules.RapiDNS import RapiDNS
from core.Raptor_Modules.BufferOverDNS import BufferOverDNS
from core.Raptor_Modules.HackerTarget import HackerTarget
from core.Raptor_Modules.NetCraft import NetCraft
from core.Raptor_Modules.DNSDumpster import DNSDumpster
from core.Raptor_Modules.VirusTotal import VirusTotal
from core.Raptor_Modules.BinaryEdge import BinaryEdge
from core.Raptor_Modules.ThreatCrowd import ThreatCrowd
from core.Raptor_Modules.Sublist3r import Sublist3r
from core.Raptor_Modules.ThreatMiner import ThreatMiner
from core.Raptor_Modules.CertSpotter import CertSpotter 
from core.Raptor_Modules.Bing import Bing
from core.Raptor_Modules.AlienVault import AlienVault
from core.Raptor_Modules.Google import Google
from core.Raptor_Modules.Shodan import Shodan
from core.Raptor_Modules.Crobat import Crobat
from core.Raptor_Modules.SiteDossier import SiteDossier
from core.Raptor_Modules.UrlScan import UrlScan
from core.Raptor_Modules.Censys import Censys
from core.Raptor_Modules.GoogleCert import GoogleCert


from concurrent.futures import ThreadPoolExecutor
from utils.utilities import *

class Raptor:
    def __init__(self):
        self.modules=[FacebookCert(),RapiDNS(),BufferOverDNS(),HackerTarget(),NetCraft(),
                      DNSDumpster(),VirusTotal(),BinaryEdge(),ThreatCrowd(),ThreatMiner(),GoogleCert(),
                      Censys(),UrlScan(),Sublist3r(),CertSpotter(),Bing(),SiteDossier(),AlienVault(),Google(),Shodan(),Crobat()]
        
        
    def save_out(self,results):

        
        final=list(map(lambda x:x+"\n",results))
        with open(CONFIGS.CONST_SUBFINDER_OUT,"w") as file:
            file.writelines(final)
        return 
               
    
    def start(self,domain):
        final=[]
        futures=[]
        with ThreadPoolExecutor(CONFIGS.THREADS) as thread:
            for module in self.modules:
                futures.append(thread.submit(module.start,domain=domain))
        
        for future in futures:
            final+=future.result()        

        self.save_out(list(set(final)))
        return
        
