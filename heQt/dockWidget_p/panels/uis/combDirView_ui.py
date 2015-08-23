# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'combDirView.ui'
#
# Created: Sat Jan 31 22:49:06 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(309, 541)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comb = QtGui.QComboBox(Form)
        self.comb.setObjectName("comb")
        self.horizontalLayout.addWidget(self.comb)
        self.plus = QtGui.QToolButton(Form)
        self.plus.setObjectName("plus")
        self.horizontalLayout.addWidget(self.plus)
        self.minus = QtGui.QToolButton(Form)
        self.minus.setObjectName("minus")
        self.horizontalLayout.addWidget(self.minus)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.dirView = DirView(Form)
        self.dirView.setObjectName("dirView")
        self.gridLayout.addWidget(self.dirView, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.plus.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.minus.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))

from qt_.view_.modelView_.dirView import DirView
