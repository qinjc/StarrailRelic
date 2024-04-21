# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RelicMainWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RelicMainWindow(object):
    def setupUi(self, RelicMainWindow):
        RelicMainWindow.setObjectName("RelicMainWindow")
        RelicMainWindow.resize(1600, 610)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RelicMainWindow.sizePolicy().hasHeightForWidth())
        RelicMainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(RelicMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 1250, 511))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setProperty("showDropIndicator", False)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setShowGrid(False)
        self.tableView.setSortingEnabled(False)
        self.tableView.setWordWrap(True)
        self.tableView.setCornerButtonEnabled(True)
        self.tableView.setObjectName("tableView")
        self.checkBox_ignore_full_level = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_ignore_full_level.setGeometry(QtCore.QRect(1120, 530, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_ignore_full_level.setFont(font)
        self.checkBox_ignore_full_level.setObjectName("checkBox_ignore_full_level")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(1270, 10, 321, 511))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lineEdit_suit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_suit.setGeometry(QtCore.QRect(10, 60, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_suit.setFont(font)
        self.lineEdit_suit.setFrame(False)
        self.lineEdit_suit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_suit.setReadOnly(True)
        self.lineEdit_suit.setClearButtonEnabled(False)
        self.lineEdit_suit.setObjectName("lineEdit_suit")
        self.lineEdit_position = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_position.setGeometry(QtCore.QRect(230, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_position.setFont(font)
        self.lineEdit_position.setFrame(False)
        self.lineEdit_position.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_position.setReadOnly(True)
        self.lineEdit_position.setClearButtonEnabled(False)
        self.lineEdit_position.setObjectName("lineEdit_position")
        self.label_title = QtWidgets.QLabel(self.frame)
        self.label_title.setGeometry(QtCore.QRect(80, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.lineEdit_main_entry_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_main_entry_name.setGeometry(QtCore.QRect(10, 220, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_main_entry_name.setFont(font)
        self.lineEdit_main_entry_name.setFrame(False)
        self.lineEdit_main_entry_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_main_entry_name.setReadOnly(True)
        self.lineEdit_main_entry_name.setClearButtonEnabled(False)
        self.lineEdit_main_entry_name.setObjectName("lineEdit_main_entry_name")
        self.lineEdit_main_entry_value = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_main_entry_value.setGeometry(QtCore.QRect(220, 220, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_main_entry_value.setFont(font)
        self.lineEdit_main_entry_value.setFrame(True)
        self.lineEdit_main_entry_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_main_entry_value.setReadOnly(False)
        self.lineEdit_main_entry_value.setClearButtonEnabled(False)
        self.lineEdit_main_entry_value.setObjectName("lineEdit_main_entry_value")
        self.lineEdit_sub_entry_1_value = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_1_value.setGeometry(QtCore.QRect(220, 300, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_1_value.setFont(font)
        self.lineEdit_sub_entry_1_value.setFrame(True)
        self.lineEdit_sub_entry_1_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_1_value.setReadOnly(False)
        self.lineEdit_sub_entry_1_value.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_1_value.setObjectName("lineEdit_sub_entry_1_value")
        self.lineEdit_sub_entry_1_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_1_name.setGeometry(QtCore.QRect(10, 300, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_1_name.setFont(font)
        self.lineEdit_sub_entry_1_name.setFrame(False)
        self.lineEdit_sub_entry_1_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_1_name.setReadOnly(True)
        self.lineEdit_sub_entry_1_name.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_1_name.setObjectName("lineEdit_sub_entry_1_name")
        self.lineEdit_sub_entry_2_value = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_2_value.setGeometry(QtCore.QRect(220, 340, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_2_value.setFont(font)
        self.lineEdit_sub_entry_2_value.setFrame(True)
        self.lineEdit_sub_entry_2_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_2_value.setReadOnly(False)
        self.lineEdit_sub_entry_2_value.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_2_value.setObjectName("lineEdit_sub_entry_2_value")
        self.lineEdit_sub_entry_2_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_2_name.setGeometry(QtCore.QRect(10, 340, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_2_name.setFont(font)
        self.lineEdit_sub_entry_2_name.setFrame(False)
        self.lineEdit_sub_entry_2_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_2_name.setReadOnly(True)
        self.lineEdit_sub_entry_2_name.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_2_name.setObjectName("lineEdit_sub_entry_2_name")
        self.lineEdit_sub_entry_4_value = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_4_value.setGeometry(QtCore.QRect(220, 420, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_4_value.setFont(font)
        self.lineEdit_sub_entry_4_value.setFrame(True)
        self.lineEdit_sub_entry_4_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_4_value.setReadOnly(False)
        self.lineEdit_sub_entry_4_value.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_4_value.setObjectName("lineEdit_sub_entry_4_value")
        self.lineEdit_sub_entry_4_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_4_name.setGeometry(QtCore.QRect(10, 420, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_4_name.setFont(font)
        self.lineEdit_sub_entry_4_name.setFrame(False)
        self.lineEdit_sub_entry_4_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_4_name.setReadOnly(True)
        self.lineEdit_sub_entry_4_name.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_4_name.setObjectName("lineEdit_sub_entry_4_name")
        self.lineEdit_sub_entry_3_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_3_name.setGeometry(QtCore.QRect(10, 380, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_3_name.setFont(font)
        self.lineEdit_sub_entry_3_name.setFrame(False)
        self.lineEdit_sub_entry_3_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_3_name.setReadOnly(True)
        self.lineEdit_sub_entry_3_name.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_3_name.setObjectName("lineEdit_sub_entry_3_name")
        self.lineEdit_sub_entry_3_value = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_sub_entry_3_value.setGeometry(QtCore.QRect(220, 380, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_sub_entry_3_value.setFont(font)
        self.lineEdit_sub_entry_3_value.setFrame(True)
        self.lineEdit_sub_entry_3_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_sub_entry_3_value.setReadOnly(False)
        self.lineEdit_sub_entry_3_value.setClearButtonEnabled(False)
        self.lineEdit_sub_entry_3_value.setObjectName("lineEdit_sub_entry_3_value")
        self.spinBox_level = QtWidgets.QSpinBox(self.frame)
        self.spinBox_level.setGeometry(QtCore.QRect(120, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBox_level.setFont(font)
        self.spinBox_level.setMinimum(0)
        self.spinBox_level.setMaximum(15)
        self.spinBox_level.setProperty("value", 0)
        self.spinBox_level.setObjectName("spinBox_level")
        self.pushButton_modify = QtWidgets.QPushButton(self.frame)
        self.pushButton_modify.setEnabled(False)
        self.pushButton_modify.setGeometry(QtCore.QRect(20, 470, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_modify.setFont(font)
        self.pushButton_modify.setObjectName("pushButton_modify")
        self.pushButton_reset = QtWidgets.QPushButton(self.frame)
        self.pushButton_reset.setEnabled(False)
        self.pushButton_reset.setGeometry(QtCore.QRect(180, 470, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.label_level = QtWidgets.QLabel(self.frame)
        self.label_level.setGeometry(QtCore.QRect(80, 100, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_level.setFont(font)
        self.label_level.setAlignment(QtCore.Qt.AlignCenter)
        self.label_level.setObjectName("label_level")
        self.label_main_entry = QtWidgets.QLabel(self.frame)
        self.label_main_entry.setGeometry(QtCore.QRect(80, 180, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_main_entry.setFont(font)
        self.label_main_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main_entry.setObjectName("label_main_entry")
        self.label_sub_entry = QtWidgets.QLabel(self.frame)
        self.label_sub_entry.setGeometry(QtCore.QRect(80, 260, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_sub_entry.setFont(font)
        self.label_sub_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sub_entry.setObjectName("label_sub_entry")
        self.pushButton_filter = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_filter.setGeometry(QtCore.QRect(1010, 530, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_filter.setFont(font)
        self.pushButton_filter.setObjectName("pushButton_filter")
        self.pushButton_get_relics = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_get_relics.setGeometry(QtCore.QRect(10, 530, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_get_relics.setFont(font)
        self.pushButton_get_relics.setObjectName("pushButton_get_relics")
        RelicMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RelicMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 23))
        self.menubar.setObjectName("menubar")
        RelicMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RelicMainWindow)
        self.statusbar.setObjectName("statusbar")
        RelicMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RelicMainWindow)
        QtCore.QMetaObject.connectSlotsByName(RelicMainWindow)

    def retranslateUi(self, RelicMainWindow):
        _translate = QtCore.QCoreApplication.translate
        RelicMainWindow.setWindowTitle(_translate("RelicMainWindow", "遗器小助手@qinjc"))
        self.checkBox_ignore_full_level.setText(_translate("RelicMainWindow", "忽略满级遗器"))
        self.label_title.setText(_translate("RelicMainWindow", "遗器修改面板"))
        self.pushButton_modify.setText(_translate("RelicMainWindow", "修改"))
        self.pushButton_reset.setText(_translate("RelicMainWindow", "重置"))
        self.label_level.setText(_translate("RelicMainWindow", "等级"))
        self.label_main_entry.setText(_translate("RelicMainWindow", "主词条"))
        self.label_sub_entry.setText(_translate("RelicMainWindow", "副词条"))
        self.pushButton_filter.setText(_translate("RelicMainWindow", "筛选"))
        self.pushButton_get_relics.setText(_translate("RelicMainWindow", "获取"))
