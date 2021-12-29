# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(799, 600)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_sa = QtWidgets.QLabel(self.centralwidget)
        self.label_sa.setGeometry(QtCore.QRect(220, 0, 421, 61))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_sa.setFont(font)
        self.label_sa.setObjectName("label_sa")
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(10, 500, 81, 31))
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_result_timetable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_result_timetable.setGeometry(QtCore.QRect(0, 30, 71, 31))
        self.pushButton_result_timetable.setObjectName("pushButton_result_timetable")
        self.pushButton_initial_timetable = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_initial_timetable.setGeometry(QtCore.QRect(0, 0, 71, 31))
        self.pushButton_initial_timetable.setObjectName("pushButton_initial_timetable")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(90, 110, 441, 81))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.lcdNumber_initial_cost = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_initial_cost.setGeometry(QtCore.QRect(90, 60, 81, 41))
        self.lcdNumber_initial_cost.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_initial_cost.setProperty("intValue", 71830)
        self.lcdNumber_initial_cost.setObjectName("lcdNumber_initial_cost")
        self.lcdNumber_final_cost = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_final_cost.setGeometry(QtCore.QRect(540, 90, 81, 41))
        self.lcdNumber_final_cost.setSmallDecimalPoint(False)
        self.lcdNumber_final_cost.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcdNumber_final_cost.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_final_cost.setProperty("value", 71830.0)
        self.lcdNumber_final_cost.setProperty("intValue", 71830)
        self.lcdNumber_final_cost.setObjectName("lcdNumber_final_cost")
        self.pushButton_next = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_next.setGeometry(QtCore.QRect(710, 500, 71, 31))
        self.pushButton_next.setObjectName("pushButton_next")
        self.pushButton_run = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_run.setGeometry(QtCore.QRect(660, 10, 131, 121))
        self.pushButton_run.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 0, 0, 255), stop:0.479904 rgba(255, 0, 0, 255), stop:0.522685 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.pushButton_run.setObjectName("pushButton_run")
        self.lcdNumber_final_temp = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_final_temp.setGeometry(QtCore.QRect(530, 40, 81, 41))
        self.lcdNumber_final_temp.setSmallDecimalPoint(False)
        self.lcdNumber_final_temp.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcdNumber_final_temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_final_temp.setProperty("value", 71830.0)
        self.lcdNumber_final_temp.setProperty("intValue", 71830)
        self.lcdNumber_final_temp.setObjectName("lcdNumber_final_temp")
        self.widget_chart_cost = MplWidget(self.centralwidget)
        self.widget_chart_cost.setGeometry(QtCore.QRect(0, 360, 781, 131))
        self.widget_chart_cost.setObjectName("widget_chart_cost")
        self.widget_chart_temp = MplWidget(self.centralwidget)
        self.widget_chart_temp.setGeometry(QtCore.QRect(0, 220, 781, 131))
        self.widget_chart_temp.setObjectName("widget_chart_temp")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_sa.setText(_translate("MainWindow", "simulated annealing"))
        self.pushButton_back.setText(_translate("MainWindow", "BACK"))
        self.pushButton_result_timetable.setText(_translate("MainWindow", "result timetable"))
        self.pushButton_initial_timetable.setText(_translate("MainWindow", "initial timetable"))
        self.pushButton_next.setText(_translate("MainWindow", "next"))
        self.pushButton_run.setText(_translate("MainWindow", "RUN"))
from gui.mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
