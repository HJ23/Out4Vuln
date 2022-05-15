"""
                 FinderBase

    This class is the base class for all finders.

"""
from utils.utilities import Requester

class FinderBase:
    def __init__(self):
        self.requester=Requester()
    def start(self):
        raise NotImplemented("Start method not implemented for base class !")
    def clean(self,results,domain)->list:
        final=set()
        for url in results:
            for useless in ["https://","http://",":","\\","*","https:\\\\","http:\\\\"]:
                url=url.replace(useless,"")
            splitted=url.split("/")
            if( splitted[0].endswith("."+domain) and splitted[0][0].isalnum() ):
                final.add(splitted[0])
        return list(final)