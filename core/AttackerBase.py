"""
             AttackerBaseClass
    This class is the base class for all attacker modules.

"""
from utils.utilities import Requester
from utils.levels import ImportanceLevel

class AttackerBase:
    def __init__(self,reporter):
        self.requester=Requester()
        self.reporter=reporter
    def report(self,results,module_name,ImportanceLevel=ImportanceLevel.LOW):
        for i,(url,payload) in enumerate(zip(results["url"],results["payload"])):
            if(i==0):
                self.reporter.createBlock(module_name)
            self.reporter.addRow(url,payload)
        self.reporter.save()
    def start(self,domain):
        raise NotImplementedError("BaseClass start not implemented!")
