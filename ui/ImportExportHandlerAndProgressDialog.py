# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\ImportExportHandlerAndProgressDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportExportHandlerAndProgressDialog(object):
    def setupUi(self, ImportExportHandlerAndProgressDialog):
        ImportExportHandlerAndProgressDialog.setObjectName("ImportExportHandlerAndProgressDialog")
        ImportExportHandlerAndProgressDialog.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ImportExportHandlerAndProgressDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.txtLog = QtWidgets.QTextEdit(ImportExportHandlerAndProgressDialog)
        self.txtLog.setReadOnly(True)
        self.txtLog.setObjectName("txtLog")
        self.verticalLayout_2.addWidget(self.txtLog)

        self.retranslateUi(ImportExportHandlerAndProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ImportExportHandlerAndProgressDialog)

    def retranslateUi(self, ImportExportHandlerAndProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ImportExportHandlerAndProgressDialog.setWindowTitle(_translate("ImportExportHandlerAndProgressDialog", "Import/Export action log"))
