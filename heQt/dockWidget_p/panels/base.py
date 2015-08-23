from qt_.qtEven import * 
from struct_.objs import findSister
from struct_.pickleInterface import IPickle
import sys
class Base(IPickle):
    """
    sys.state:
             menuPanel : 包含action的菜单。这些action是checkable的，反映了该page是否开启
                         注意action的名字必须是act_xxx的形式，必须以该menuPanel为parent
    """
    def initState(self):
        try:
            menu = sys.state["menuPanel"] 
            act = findSister(self, "act", QAction, menu)
            act.setChecked(True)
        except Exception as e:
            print("初始化面板BASE，寻找对应QAction出现问题，下面是具体错误")
            print(e)  
    
    def uninstall(self):
        self.setParent(None)
        try:
            menu = sys.state["menuPanel"] 
            act = findSister(self, "act", QAction, menu)
            act.setChecked(False)
        except Exception as e:
            print("卸载面板BASE，寻找对应QAction出现问题，下面是具体错误")
            print(e)    
    def __reduce__(self):
        self.pickleDict["obj_name"] = self.objectName()
        return super().__reduce__()
    
    def __setstate__(self, state):
        self.setObjectName(state["obj_name"])