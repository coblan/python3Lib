#!python3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re


class Win(QWidget):
    def __init__(self, *arg):
        super(Win, self).__init__(*arg)
        self.line = QPlainTextEdit()
        self.line.textChanged.connect(self.change)

        self.line2 = QPlainTextEdit()
        self.line2.textChanged.connect(self.change)

        self.lab_lab = QLabel(u'全部')
        self.lab_lab.setMaximumWidth(30)
        self.lab = QLabel()
        lay_1 = QHBoxLayout()
        lay_1.addWidget(self.lab_lab)
        lay_1.addWidget(self.lab)

        self.lab2_lab = QLabel(u'分组')
        self.lab2_lab.setMaximumWidth(30)
        self.lab2 = QLabel()
        lay_2 = QHBoxLayout()
        lay_2.addWidget(self.lab2_lab)
        lay_2.addWidget(self.lab2)

        self.lab.setTextFormat(Qt.PlainText)
        self.lab2.setTextFormat(Qt.PlainText)

        lay = QVBoxLayout()
        lay.addWidget(self.line2)
        lay.addWidget(self.line)
        lay.addLayout(lay_1)
        lay.addLayout(lay_2)
        self.setLayout(lay)
        self.setWindowTitle("正则表达式测试_python")

    def change(self):
        """当任何一个文本框内容变化的时候，调用该函数"""
        mt = ""
        try:
            mt = re.search(self.line.toPlainText(), self.line2.toPlainText(), re.M | re.S)
        except:
            pass
        if mt:
            self.lab.setText("[%s]" % mt.group())
            self.lab2.setText(",".join(["[%s]" % x for x in mt.groups()]))
        else:
            self.lab.clear()
            self.lab2.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())
