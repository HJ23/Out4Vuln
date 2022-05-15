import sys
sys.path.append(".")
import argparse
from core.Scanner import Scanner
from utils.utilities import *

parser = argparse.ArgumentParser()
parser.add_argument('--domain',"-d",help='Domain name',required=False)
parser.add_argument('--domains',help='Domain name file',required=False,type=str,default="")
parser.add_argument('--keyword',help='Keyword that indicate server',required=False,default="1",type=str)
parser.add_argument('--threads',"-t",help='Thread',required=False,default=4,type=int)
parser.add_argument('--referer',"-r",help='Referer',required=False,default="www.google.com")
parser.add_argument('--limit',"-l",help='Limit for spider',required=False,default=10000)
parser.add_argument('--verbose',"-v",help='Verbose mode',required=False,default=False,action="store_true")
parser.add_argument('--all',default=False,help='*Run whole pipeline.',action='store_true')
parser.add_argument('--noload',default=False,help='*No load to httpprobe.',action='store_true')
parser.add_argument('--new',default=False,help='*New scope for target.',action='store_true')
parser.add_argument('--httpp',default=False,help='*HTTPPROBE.',action='store_true')
parser.add_argument('--urlgather',default=False,help='*URLGatherer.',action='store_true')
parser.add_argument('--hhi',default=False,help='*Nuclei check.',action='store_true')
parser.add_argument('--spider',default=False,help='*Spider crawler.',action='store_true')
parser.add_argument('--ssrf',default=False,help='*SSRF.',action='store_true')
parser.add_argument('--cors',default=False,help='*CORS.',action='store_true')
parser.add_argument('--pathtraversal',default=False,help='*Pathtraversal.',action='store_true')
parser.add_argument('--subf',default=False,help='*Raptor subdomain enumeration.',action='store_true')
parser.add_argument('--nuclei',default=False,help='*Nuclei engine.',action='store_true')
parser.add_argument('--dirsearch',default=False,help='*Dirsearch engine.',action='store_true')
parser.add_argument('--bypass403',default=False,help='*Bypass403.',action='store_true')
parser.add_argument('--chaos',default=False,help='*Instead normal subdomain enum. user chaos modules to gather all',action='store_true')


args=parser.parse_args()

if __name__=="__main__":
    
    if(args.domains!=""):
        init_scanner()
        
        domains=read_file(args.domains)
        for domain in domains:
            Log.success(f"### ATTACKS FOR {domain} HAS STARTED SUCCESFULLY")
            obj=Scanner(args)
            CONFIGS.CONST_DOMAIN=domain
            re_init() # reinitialize names of files etc.
            obj.start()
            Log.success(f"### ATTACKS FOR {domain} HAS FINISHED SUCCESFULLY")
            Log.success(f"### CHECK OUT REPORT & OUTPUTS FOR MORE DETAILS")
            
    else:
        
        Log.success(f"### ATTACKS FOR {args.domain} HAS STARTED SUCCESFULLY")
        obj=Scanner(args)
        re_init()  # reinitialize names of files etc.
        obj.start()
        Log.success(f"### ATTACKS FOR {args.domain} HAS FINISHED SUCCESFULLY")
        Log.success(f"### CHECK OUT REPORT & OUTPUTS FOR MORE DETAILS")
        
