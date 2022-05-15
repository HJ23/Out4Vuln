"""
             AttackerBaseClass
    This class is the base class for all attacker modules.

"""
from utils.utilities import Requester

class AttackerBase:
    def __init__(self):
        self.requester=Requester()
    def start(self,domain):
        raise NotImplementedError("BaseClass start not implemented!")
