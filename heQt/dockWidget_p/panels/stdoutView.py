from qt_.widget.stdoutView import StdoutView
from struct_.pickleInterface import IPickle
import sys
from .base import Base
class StdoutPage(Base, StdoutView):
    def __init__(self):
        super().__init__()
    
    def initState(self):
        sys.stderr = self
        sys.stdout = self
        super().initState() 

    def uninstall(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        super().uninstall( )