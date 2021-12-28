#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
# import process_image_manager
# import simulated_annealing
import main_window
import loading_window
import monday_window


def sa_algorithm(Tmax: int, Tmin: int, kmax: int, alpha: float, cooling_schedule_str: str):
    # if cooling_schedule_str == 'exponential':
    #     simulated_annealing.SA(Tmax, Tmin, kmax, alpha, simulated_annealing.exponential_cooling_schedule)
    # elif cooling_schedule_str == 'linear':
    #     simulated_annealing.SA(Tmax, Tmin, kmax, alpha, simulated_annealing.linear_cooling_schedule)
    # elif cooling_schedule_str == 'logarithmic':
    #     simulated_annealing.SA(Tmax, Tmin, kmax, alpha, simulated_annealing.logarithmic_cooling_schedule)
    # elif cooling_schedule_str == 'quadratic':
    #     simulated_annealing.SA(Tmax, Tmin, kmax, alpha, simulated_annealing.quadratic_cooling_schedule)
    # elif cooling_schedule_str == 'bolzmann':
    #     simulated_annealing.SA(Tmax, Tmin, kmax, alpha, simulated_annealing.bolzmann_cooling_schedule)
    # elif cooling_schedule_str == 'cauchy':
    #     simulated_annealing.SA(Tmax, Tmin, kmax, alpha, simulated_annealing.cauchy_cooling_schedule)
    #
    # process_image_manager.process_image_manager.reset_process_image()
    print('------ SA --------')


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_run.clicked.connect(self.go_to_loading_window)
        self.horizontalSlider_lecturer_availability_2.valueChanged.connect(lambda: self.label_test.setText(str(self.horizontalSlider_lecturer_availability_2.value())))

    def go_to_loading_window(self):
        widget.setCurrentWidget(load_window)
        print(self.spinBox_tmax.value())
        print(self.spinBox_tmin.value())
        print(self.spinBox_kmax.value())
        print(self.horizontalSlider_alpha.value())
        print(self.comboBox_cooling_schedule.currentText())
        tmax = self.spinBox_tmax.value()
        tmin = self.spinBox_tmin.value()
        kmax = self.spinBox_kmax.value()
        alpha = self.horizontalSlider_alpha.value()
        cooling_schedule_str = self.comboBox_cooling_schedule.currentText()
        sa_algorithm(tmax, tmin, kmax, alpha, cooling_schedule_str)


class LoadingWindow(QMainWindow, loading_window.Ui_MainWindow):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_back.clicked.connect(self.go_to_main_window)
        self.pushButton_show_timetable.clicked.connect(self.show_excel)

    def go_to_main_window(self):
        widget.setCurrentWidget(main_window)

    def show_excel(self):
        os.system("start EXCEL.EXE ../ResultSchedule.xlsx")


class MondayWindow(QMainWindow, monday_window.Ui_MainWindow):
    def __init__(self):
        super(MondayWindow, self).__init__()
        self.setupUi(self)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_window = MainWindow()
    widget.addWidget(main_window)
    load_window = LoadingWindow()
    widget.addWidget(load_window)
    monday_window = MondayWindow()
    widget.addWidget(monday_window)
    widget.setFixedSize(800, 550)
    # widget.setFixedHeight(600)
    # widget.setFixedWidth(850)
    widget.show()

    sys.exit(app.exec_())
