# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 713)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(410, 10, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(QtCore.Qt.AutoText)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.label_tmax = QtWidgets.QLabel(self.centralwidget)
        self.label_tmax.setGeometry(QtCore.QRect(100, 230, 55, 16))
        self.label_tmax.setScaledContents(False)
        self.label_tmax.setObjectName("label_tmax")
        self.label_tmin = QtWidgets.QLabel(self.centralwidget)
        self.label_tmin.setGeometry(QtCore.QRect(100, 290, 55, 16))
        self.label_tmin.setObjectName("label_tmin")
        self.label_kmax = QtWidgets.QLabel(self.centralwidget)
        self.label_kmax.setGeometry(QtCore.QRect(100, 350, 55, 16))
        self.label_kmax.setObjectName("label_kmax")
        self.label_alpha = QtWidgets.QLabel(self.centralwidget)
        self.label_alpha.setGeometry(QtCore.QRect(100, 490, 55, 16))
        self.label_alpha.setObjectName("label_alpha")
        self.label_cooling_schedule = QtWidgets.QLabel(self.centralwidget)
        self.label_cooling_schedule.setGeometry(QtCore.QRect(100, 110, 101, 16))
        self.label_cooling_schedule.setObjectName("label_cooling_schedule")
        self.label_term = QtWidgets.QLabel(self.centralwidget)
        self.label_term.setGeometry(QtCore.QRect(100, 170, 31, 16))
        self.label_term.setObjectName("label_term")
        self.comboBox_term = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_term.setGeometry(QtCore.QRect(100, 190, 73, 22))
        self.comboBox_term.setObjectName("comboBox_term")
        self.comboBox_term.addItem("")
        self.comboBox_term.addItem("")
        self.comboBox_term.addItem("")
        self.comboBox_term.addItem("")
        self.comboBox_term.addItem("")
        self.comboBox_term.addItem("")
        self.comboBox_term.addItem("")
        self.horizontalSlider_alpha = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_alpha.setEnabled(True)
        self.horizontalSlider_alpha.setGeometry(QtCore.QRect(100, 510, 160, 22))
        self.horizontalSlider_alpha.setMinimum(9000)
        self.horizontalSlider_alpha.setMaximum(9999)
        self.horizontalSlider_alpha.setProperty("value", 9900)
        self.horizontalSlider_alpha.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_alpha.setInvertedAppearance(False)
        self.horizontalSlider_alpha.setInvertedControls(False)
        self.horizontalSlider_alpha.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_alpha.setTickInterval(100)
        self.horizontalSlider_alpha.setObjectName("horizontalSlider_alpha")
        self.comboBox_cooling_schedule = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cooling_schedule.setGeometry(QtCore.QRect(100, 130, 101, 21))
        self.comboBox_cooling_schedule.setObjectName("comboBox_cooling_schedule")
        self.comboBox_cooling_schedule.addItem("")
        self.comboBox_cooling_schedule.addItem("")
        self.comboBox_cooling_schedule.addItem("")
        self.comboBox_cooling_schedule.addItem("")
        self.comboBox_cooling_schedule.addItem("")
        self.comboBox_cooling_schedule.addItem("")
        self.comboBox_cooling_schedule.addItem("")
        self.label_lecturer_availability = QtWidgets.QLabel(self.centralwidget)
        self.label_lecturer_availability.setGeometry(QtCore.QRect(390, 110, 121, 16))
        self.label_lecturer_availability.setObjectName("label_lecturer_availability")
        self.horizontalSlider_lecturer_availability = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_lecturer_availability.setGeometry(QtCore.QRect(390, 130, 160, 22))
        self.horizontalSlider_lecturer_availability.setMaximum(100)
        self.horizontalSlider_lecturer_availability.setProperty("value", 50)
        self.horizontalSlider_lecturer_availability.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_lecturer_availability.setInvertedAppearance(False)
        self.horizontalSlider_lecturer_availability.setInvertedControls(False)
        self.horizontalSlider_lecturer_availability.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_lecturer_availability.setTickInterval(10)
        self.horizontalSlider_lecturer_availability.setObjectName("horizontalSlider_lecturer_availability")
        self.label_room_availability = QtWidgets.QLabel(self.centralwidget)
        self.label_room_availability.setGeometry(QtCore.QRect(390, 170, 101, 16))
        self.label_room_availability.setObjectName("label_room_availability")
        self.horizontalSlider_room_availability = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_room_availability.setGeometry(QtCore.QRect(390, 190, 160, 22))
        self.horizontalSlider_room_availability.setMaximum(100)
        self.horizontalSlider_room_availability.setProperty("value", 50)
        self.horizontalSlider_room_availability.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_room_availability.setInvertedAppearance(False)
        self.horizontalSlider_room_availability.setInvertedControls(False)
        self.horizontalSlider_room_availability.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_room_availability.setTickInterval(10)
        self.horizontalSlider_room_availability.setObjectName("horizontalSlider_room_availability")
        self.horizontalSlider_matrix_transposition = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_matrix_transposition.setGeometry(QtCore.QRect(390, 300, 160, 22))
        self.horizontalSlider_matrix_transposition.setMaximum(100)
        self.horizontalSlider_matrix_transposition.setProperty("value", 10)
        self.horizontalSlider_matrix_transposition.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_matrix_transposition.setInvertedAppearance(False)
        self.horizontalSlider_matrix_transposition.setInvertedControls(False)
        self.horizontalSlider_matrix_transposition.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_matrix_transposition.setTickInterval(10)
        self.horizontalSlider_matrix_transposition.setObjectName("horizontalSlider_matrix_transposition")
        self.horizontalSlider_matrix_inner_translation = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_matrix_inner_translation.setGeometry(QtCore.QRect(390, 360, 160, 22))
        self.horizontalSlider_matrix_inner_translation.setMaximum(100)
        self.horizontalSlider_matrix_inner_translation.setProperty("value", 10)
        self.horizontalSlider_matrix_inner_translation.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_matrix_inner_translation.setInvertedAppearance(False)
        self.horizontalSlider_matrix_inner_translation.setInvertedControls(False)
        self.horizontalSlider_matrix_inner_translation.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_matrix_inner_translation.setTickInterval(10)
        self.horizontalSlider_matrix_inner_translation.setObjectName("horizontalSlider_matrix_inner_translation")
        self.label_matrix_inner_translation = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix_inner_translation.setGeometry(QtCore.QRect(390, 340, 141, 16))
        self.label_matrix_inner_translation.setObjectName("label_matrix_inner_translation")
        self.label_matrix_transposition = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix_transposition.setGeometry(QtCore.QRect(390, 280, 121, 16))
        self.label_matrix_transposition.setObjectName("label_matrix_transposition")
        self.label_matrix_cut_and_paste_translation = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix_cut_and_paste_translation.setGeometry(QtCore.QRect(390, 400, 181, 16))
        self.label_matrix_cut_and_paste_translation.setAutoFillBackground(False)
        self.label_matrix_cut_and_paste_translation.setScaledContents(False)
        self.label_matrix_cut_and_paste_translation.setObjectName("label_matrix_cut_and_paste_translation")
        self.horizontalSlider_matrix_cut_and_paste_translation = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_matrix_cut_and_paste_translation.setGeometry(QtCore.QRect(390, 420, 160, 22))
        self.horizontalSlider_matrix_cut_and_paste_translation.setMaximum(100)
        self.horizontalSlider_matrix_cut_and_paste_translation.setProperty("value", 80)
        self.horizontalSlider_matrix_cut_and_paste_translation.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_matrix_cut_and_paste_translation.setInvertedAppearance(False)
        self.horizontalSlider_matrix_cut_and_paste_translation.setInvertedControls(False)
        self.horizontalSlider_matrix_cut_and_paste_translation.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_matrix_cut_and_paste_translation.setTickInterval(10)
        self.horizontalSlider_matrix_cut_and_paste_translation.setObjectName("horizontalSlider_matrix_cut_and_paste_translation")
        self.pushButton_apply = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_apply.setEnabled(False)
        self.pushButton_apply.setGeometry(QtCore.QRect(890, 500, 121, 101))
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.spinBox_kmax = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_kmax.setEnabled(False)
        self.spinBox_kmax.setGeometry(QtCore.QRect(100, 370, 101, 31))
        self.spinBox_kmax.setMinimum(1)
        self.spinBox_kmax.setMaximum(200)
        self.spinBox_kmax.setProperty("value", 1)
        self.spinBox_kmax.setDisplayIntegerBase(10)
        self.spinBox_kmax.setObjectName("spinBox_kmax")
        self.spinBox_iter_max = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_iter_max.setGeometry(QtCore.QRect(100, 440, 101, 31))
        self.spinBox_iter_max.setMaximum(1000000)
        self.spinBox_iter_max.setProperty("value", 1000)
        self.spinBox_iter_max.setObjectName("spinBox_iter_max")
        self.label_iter_max = QtWidgets.QLabel(self.centralwidget)
        self.label_iter_max.setGeometry(QtCore.QRect(100, 420, 55, 16))
        self.label_iter_max.setObjectName("label_iter_max")
        self.label_cost = QtWidgets.QLabel(self.centralwidget)
        self.label_cost.setGeometry(QtCore.QRect(710, 110, 81, 16))
        self.label_cost.setObjectName("label_cost")
        self.checkBox_unbalanced_function = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_unbalanced_function.setGeometry(QtCore.QRect(710, 130, 231, 20))
        self.checkBox_unbalanced_function.setChecked(True)
        self.checkBox_unbalanced_function.setTristate(False)
        self.checkBox_unbalanced_function.setObjectName("checkBox_unbalanced_function")
        self.checkBox_gaps_c_function = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_gaps_c_function.setGeometry(QtCore.QRect(710, 160, 211, 20))
        self.checkBox_gaps_c_function.setChecked(True)
        self.checkBox_gaps_c_function.setObjectName("checkBox_gaps_c_function")
        self.checkBox_lecturer_work_time = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_lecturer_work_time.setGeometry(QtCore.QRect(710, 190, 261, 20))
        self.checkBox_lecturer_work_time.setChecked(True)
        self.checkBox_lecturer_work_time.setObjectName("checkBox_lecturer_work_time")
        self.checkBox_late_lectures_cost_function = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_late_lectures_cost_function.setGeometry(QtCore.QRect(710, 220, 261, 20))
        self.checkBox_late_lectures_cost_function.setChecked(True)
        self.checkBox_late_lectures_cost_function.setObjectName("checkBox_late_lectures_cost_function")
        self.label_alpha_procent = QtWidgets.QLabel(self.centralwidget)
        self.label_alpha_procent.setEnabled(True)
        self.label_alpha_procent.setGeometry(QtCore.QRect(270, 510, 51, 21))
        self.label_alpha_procent.setObjectName("label_alpha_procent")
        self.label_matrix_cut_and_paste_translation_procent = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix_cut_and_paste_translation_procent.setGeometry(QtCore.QRect(560, 420, 51, 21))
        self.label_matrix_cut_and_paste_translation_procent.setObjectName("label_matrix_cut_and_paste_translation_procent")
        self.label_matrix_inner_translation_procent = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix_inner_translation_procent.setGeometry(QtCore.QRect(560, 360, 51, 21))
        self.label_matrix_inner_translation_procent.setObjectName("label_matrix_inner_translation_procent")
        self.label_matrix_transposition_procent = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix_transposition_procent.setGeometry(QtCore.QRect(560, 300, 51, 21))
        self.label_matrix_transposition_procent.setObjectName("label_matrix_transposition_procent")
        self.label_room_availability_procent = QtWidgets.QLabel(self.centralwidget)
        self.label_room_availability_procent.setGeometry(QtCore.QRect(560, 190, 51, 21))
        self.label_room_availability_procent.setObjectName("label_room_availability_procent")
        self.label_lecturer_availability_procent = QtWidgets.QLabel(self.centralwidget)
        self.label_lecturer_availability_procent.setGeometry(QtCore.QRect(560, 130, 51, 21))
        self.label_lecturer_availability_procent.setObjectName("label_lecturer_availability_procent")
        self.checkBox_early_lectures_cost_function = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_early_lectures_cost_function.setGeometry(QtCore.QRect(710, 250, 251, 20))
        self.checkBox_early_lectures_cost_function.setChecked(True)
        self.checkBox_early_lectures_cost_function.setObjectName("checkBox_early_lectures_cost_function")
        self.doubleSpinBox_tmax = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_tmax.setEnabled(False)
        self.doubleSpinBox_tmax.setGeometry(QtCore.QRect(100, 250, 101, 31))
        self.doubleSpinBox_tmax.setReadOnly(False)
        self.doubleSpinBox_tmax.setDecimals(1)
        self.doubleSpinBox_tmax.setMinimum(0.1)
        self.doubleSpinBox_tmax.setMaximum(200.0)
        self.doubleSpinBox_tmax.setSingleStep(0.1)
        self.doubleSpinBox_tmax.setProperty("value", 0.1)
        self.doubleSpinBox_tmax.setObjectName("doubleSpinBox_tmax")
        self.doubleSpinBox_tmin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_tmin.setEnabled(False)
        self.doubleSpinBox_tmin.setGeometry(QtCore.QRect(100, 310, 101, 31))
        self.doubleSpinBox_tmin.setDecimals(1)
        self.doubleSpinBox_tmin.setMinimum(0.1)
        self.doubleSpinBox_tmin.setMaximum(200.0)
        self.doubleSpinBox_tmin.setSingleStep(0.1)
        self.doubleSpinBox_tmin.setProperty("value", 0.1)
        self.doubleSpinBox_tmin.setObjectName("doubleSpinBox_tmin")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1088, 26))
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
        self.label_title.setText(_translate("MainWindow", "Timetable Scheduler"))
        self.label_tmax.setText(_translate("MainWindow", "Tmax"))
        self.label_tmin.setText(_translate("MainWindow", "Tmin"))
        self.label_kmax.setText(_translate("MainWindow", "kmax"))
        self.label_alpha.setText(_translate("MainWindow", "alpha"))
        self.label_cooling_schedule.setText(_translate("MainWindow", "cooling schedule"))
        self.label_term.setText(_translate("MainWindow", "term"))
        self.comboBox_term.setItemText(0, _translate("MainWindow", "term 1"))
        self.comboBox_term.setItemText(1, _translate("MainWindow", "term 2"))
        self.comboBox_term.setItemText(2, _translate("MainWindow", "term 3"))
        self.comboBox_term.setItemText(3, _translate("MainWindow", "term 4"))
        self.comboBox_term.setItemText(4, _translate("MainWindow", "term 5"))
        self.comboBox_term.setItemText(5, _translate("MainWindow", "term 6"))
        self.comboBox_term.setItemText(6, _translate("MainWindow", "term 7"))
        self.comboBox_cooling_schedule.setCurrentText(_translate("MainWindow", "---- wybierz ----"))
        self.comboBox_cooling_schedule.setItemText(0, _translate("MainWindow", "---- wybierz ----"))
        self.comboBox_cooling_schedule.setItemText(1, _translate("MainWindow", "exponential"))
        self.comboBox_cooling_schedule.setItemText(2, _translate("MainWindow", "linear"))
        self.comboBox_cooling_schedule.setItemText(3, _translate("MainWindow", "logarithmic"))
        self.comboBox_cooling_schedule.setItemText(4, _translate("MainWindow", "quadratic"))
        self.comboBox_cooling_schedule.setItemText(5, _translate("MainWindow", "bolzmann"))
        self.comboBox_cooling_schedule.setItemText(6, _translate("MainWindow", "cauchy"))
        self.label_lecturer_availability.setText(_translate("MainWindow", "lecturer availability"))
        self.label_room_availability.setText(_translate("MainWindow", "room availability"))
        self.label_matrix_inner_translation.setText(_translate("MainWindow", "matrix inner translation"))
        self.label_matrix_transposition.setText(_translate("MainWindow", "matrix transposition"))
        self.label_matrix_cut_and_paste_translation.setText(_translate("MainWindow", "matrix cut and paste translation"))
        self.pushButton_apply.setText(_translate("MainWindow", "APPLY"))
        self.label_iter_max.setText(_translate("MainWindow", "iter max"))
        self.label_cost.setText(_translate("MainWindow", "cost function"))
        self.checkBox_unbalanced_function.setText(_translate("MainWindow", "unbalanced cost function"))
        self.checkBox_gaps_c_function.setText(_translate("MainWindow", "gaps cost function"))
        self.checkBox_lecturer_work_time.setText(_translate("MainWindow", "lecturer work time cost function"))
        self.checkBox_late_lectures_cost_function.setText(_translate("MainWindow", "late lectures cost function"))
        self.label_alpha_procent.setText(_translate("MainWindow", "0.99"))
        self.label_matrix_cut_and_paste_translation_procent.setText(_translate("MainWindow", "80 %"))
        self.label_matrix_inner_translation_procent.setText(_translate("MainWindow", "10 %"))
        self.label_matrix_transposition_procent.setText(_translate("MainWindow", "10 %"))
        self.label_room_availability_procent.setText(_translate("MainWindow", "50 %"))
        self.label_lecturer_availability_procent.setText(_translate("MainWindow", "50 %"))
        self.checkBox_early_lectures_cost_function.setText(_translate("MainWindow", "early lectures cost function"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
