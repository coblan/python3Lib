##import itertools

##for x,y in itertools.product(range(10),range(2)):
##    print(x,y)

# ------------------------------------
# class kiss(object):
#     def __init__(self,*args):
#         #print( super().__class__ )
#         print( super().__getattribute__('__class__').__bases__ )
#
#
# def foo():
#     cc = kiss()
#     c2 = kiss()
#
#
# foo()
#-------logging ---------------------
# import logging
#
# log=logging.getLogger()
#
# hand=logging.StreamHandler()
# log.addHandler(hand)
# log.setLevel(logging.DEBUG)
# log.debug("fuck")

from heQt.qtPickle import QtPickle
from PyQt5.QtWidgets import *
from heStruct.cls import add_component
import pickle
class fuck(QtPickle):
    def real_reduce(self):
        self.pickle_dict['fuck']='春天'

    def __setstate__(self,state):
        if isinstance(self,QWidget):
            self.setWindowTitle(state['fuck'])

add_component(QtPickle.components,fuck)

if __name__ =='__main__':
    import  sys
    app=QApplication(sys.argv)
    win=QWidget()
    win.show()

    ss =pickle.dumps(win)
    print(ss)
    cd= pickle.loads(ss)

    cd.show()

    sys.exit(app.exec_())