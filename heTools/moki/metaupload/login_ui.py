# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 180)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(300, 180))
        Form.setMaximumSize(QtCore.QSize(300, 180))
        self.btn_login = QtWidgets.QPushButton(Form)
        self.btn_login.setGeometry(QtCore.QRect(90, 130, 75, 23))
        self.btn_login.setObjectName("btn_login")
        self.btn_quit = QtWidgets.QPushButton(Form)
        self.btn_quit.setGeometry(QtCore.QRect(200, 130, 75, 23))
        self.btn_quit.setObjectName("btn_quit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(19, 39, 42, 16))
        self.label.setObjectName("label")
        self.account = QtWidgets.QLineEdit(Form)
        self.account.setGeometry(QtCore.QRect(80, 30, 191, 30))
        self.account.setObjectName("account")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 48, 16))
        self.label_2.setObjectName("label_2")
        self.passtext = QtWidgets.QLineEdit(Form)
        self.passtext.setGeometry(QtCore.QRect(80, 70, 191, 30))
        self.passtext.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passtext.setObjectName("passtext")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_login.setText(_translate("Form", "Login"))
        self.btn_quit.setText(_translate("Form", "Quit"))
        self.label.setText(_translate("Form", "Account"))
        self.label_2.setText(_translate("Form", "password"))

