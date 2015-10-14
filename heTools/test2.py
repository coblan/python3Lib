##from PyQt5.QtWidgets import *
##import pickle
##from heQt.qtPickle import tstWin
##if __name__=='__main__':
##    import sys,os.path
##    app= QApplication(sys.argv)
####    if os.path.exists('d:/try/testwin_pickle'):
####        with open('d:/try/testwin_pickle','br') as f:
####            win=pickle.load(f)
####        win.show()
    
##    win = QTreeView()
##    cd = pickle.dumps(win)
    
##    print(cd)
    
##    ss = pickle.loads(cd)
##    ss.show()
##    sys.exit(app.exec_())

ls= range(0,10)

for i in ls[-1::-1]:
    print(i)