import os
import time
from utils.utilities import *

class Reporter:
    def __init__(self):
        self.html_skeleton=f'''
                           <html>
                           <style type="text/css">
                           table, th, td {{
                                  border: 1px solid black;
                                  border-collapse: collapse;
                                         }}
                           th, td {{
                                  padding: 5px;
                                  text-align: left;    
                                  }}
                           
                    
                          table tr#low      {{background-color:blue; color:black;}}
                          table tr#medium   {{background-color:yellow;color:black;}}
                          table tr#critical {{background-color:red; color:black;}}
                          table tr#high {{background-color:red; color:black;}}
                          table tr#leak {{background-color:red; color:black;}}
                          
                                                     
                           </style>
                           <body>
                           <h2>Report for : {CONFIGS.CONST_DOMAIN} </h2>
                           <p>This report includes recon & attack results</p>
                           <p>Report created : {get_date_and_time()}. </p>
                           
                           <br>
                           <table style="width:100%">
                           
        '''
        
        self.counter=0
        self.ucounter=1
        self.chunked=10
        self.createBlock(CONFIGS.CONST_DOMAIN)
    
    def createBlock(self,name):  
        self.html_skeleton+=f'''
                            <tr id="medium">
                            <th>{name}</th>
                            <th>{get_date_and_time()}</th>                         
                            </tr>
                            '''
    # placeholder can be anything : nuclei output,payload etc.
    
    def addRow(self,url,placeholder=""):
        
        if(type(placeholder) is list):
            placeholder="<ul>"+"".join([ "<li>"+x+"</li>" for x in placeholder  ])+"</ul>"
        
        if("low" in placeholder or "info" in placeholder):
            self.html_skeleton+=" <tr id=low>"
        elif("medium" in placeholder):
            self.html_skeleton+=" <tr id=medium>"
        elif("high" in placeholder):
            self.html_skeleton+=" <tr id=high>"
        elif("critical" in placeholder):
            self.html_skeleton+=" <tr id=critical>"
        elif("leak" in placeholder):
            self.html_skeleton+=" <tr id=leak>"
        else:
            self.html_skeleton+=" <tr>"
            
        
        
        
        self.html_skeleton+=f'''
                                  <td>{self.ucounter}</td>
                                  <td><a href={url}>{url}</a> </td>
                                  <td>{placeholder}</td>
                                  <td>{get_date_and_time()}</td>
                                  </tr>'''
        
        
        
        
        self.counter+=1
        self.ucounter+=1
        if(self.counter>=self.chunked):
            self.html_skeleton+=f"<th>{get_date_and_time()}</th>"
            self.save(finalize=False)
            self.counter=0
            self.html_skeleton=""
        
            
        
    
    def save(self,finalize=True):
        if(finalize):
            self.html_skeleton+='''
                            </table>
                            </body>
                            </html>
                            '''
        with open(os.path.join(CONFIGS.CONST_REPORT_IO,CONFIGS.CONST_DOMAIN+"_REPORT.html"),"a") as file:
            file.writelines(self.html_skeleton)
        self.html_skeleton=""
        self.counter=0
        

