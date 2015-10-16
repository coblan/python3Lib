# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Fri Oct 16 08:34:42 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 180)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(300, 180))
        Form.setMaximumSize(QtCore.QSize(300, 180))
        self.btn_login = QtGui.QPushButton(Form)
        self.btn_login.setGeometry(QtCore.QRect(90, 130, 75, 23))
        self.btn_login.setObjectName("btn_login")
        self.btn_quit = QtGui.QPushButton(Form)
        self.btn_quit.setGeometry(QtCore.QRect(200, 130, 75, 23))
        self.btn_quit.setObjectName("btn_quit")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(19, 39, 42, 16))
        self.label.setObjectName("label")
        self.account = QtGui.QLineEdit(Form)
        self.account.setGeometry(QtCore.QRect(80, 30, 191, 30))
        self.account.setObjectName("account")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 48, 16))
        self.label_2.setObjectName("label_2")
        self.passtext = QtGui.QLineEdit(Form)
        self.passtext.setGeometry(QtCore.QRect(80, 70, 191, 30))
        self.passtext.setEchoMode(QtGui.QLineEdit.Password)
        self.passtext.setObjectName("passtext")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_login.setText(QtGui.QApplication.translate("Form", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_quit.setText(QtGui.QApplication.translate("Form", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "password", None, QtGui.QApplication.UnicodeUTF8))

