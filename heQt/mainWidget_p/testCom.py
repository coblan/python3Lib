from qt_.qtEven import QSplitter

class testSplitter(QSplitter):
    "测试mainwin的"
    def __init__(self, *args):
        super().__init__( *args)
        self.addWidget(QWidget(self))
        self.addWidget(QPlainTextEdit(self))
    
    def saveItems(self):
        return [(self.restoreGeometry, self.saveGeometry, "splitter/geo"), 
                (self.restoreState, self.saveState, "splitter/state") ]