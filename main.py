import sys
from utils.levels import WorkingMode

from utils.reporter import Reporter
sys.path.append(".")
import argparse
from core.modules.urlgatherer.spider import Spider
from utils.config import reinit_configs

reinit_configs("google.com","https://www.google.com","https://www.google.com",WorkingMode.Aggresive,False,1)

reporter=Reporter("https://google.com")
a=Spider(reporter,10)
a.start(["google.com"])
