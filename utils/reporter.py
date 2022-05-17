from ast import Import
import os
from flask import Config
from utils.utilities import *
from utils.levels import ImportanceLevel

class Reporter:
    def __init__(self,domain):
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
                           <h2>Report for : {domain} </h2>
                           <p>This report includes recon & attack results</p>
                           <p>Report created : {get_date_and_time()}. </p>
                           
                           <br>
                           <table style="width:100%">
                           
        '''
        
        self.counter=0
        self.ucounter=1
        self.chunked=10
    
    # Create heading for task type
    def create_block(self,name):  
        self.html_skeleton+=f'''
                            <tr id="medium">
                            <th>{name}</th>
                            <th>{get_date_and_time()}</th>                         
                            </tr>
                            '''
    def add_row(self,url,payload,level):
        if(level==ImportanceLevel.INFO):
            self.html_skeleton+=" <tr id=low>"
        elif(level==ImportanceLevel.MEDIUM):
            self.html_skeleton+=" <tr id=medium>"
        elif(level==ImportanceLevel.CRITICAL):
            self.html_skeleton+=" <tr id=high>"
        else:
            self.html_skeleton+=" <tr>"
        self.html_skeleton+=f'''
                                  <td>{self.ucounter}</td>
                                  <td><a href={url}>{url}</a> </td>
                                  <td>{payload}</td>
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
        else:
            self.html_skeleton=""
            self.counter=0
        with open(os.path.join(Configs.ConstReportPath,Configs.ConstDomain+"_report.html"),"a") as file:
            file.writelines(self.html_skeleton)