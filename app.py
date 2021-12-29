#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
import gui.main_window as main_window
import gui.loading_window as loading_window
import gui.char_window as char_window
import timetable_scheduler.simulated_annealing as sa_file

import time
import numpy as np
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import gui.mplwidget
import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.animation as animation


class GuiSetup(sa_file.AlgorithmSetup):
    def change_in_temperature(self, new_temperature: float):
        procent = (new_temperature - self.Tmin) / (self.Tmax - self.Tmin) * 100
        load_window.progressBar.setValue(int(100 - procent))
        load_window.lcdNumber_final_temp.display(new_temperature)
        QCoreApplication.processEvents()

    def change_in_cost_function(self, new_f_cost: float):
        load_window.lcdNumber_final_cost.display(new_f_cost)
        QCoreApplication.processEvents()

    def initial_cost_function(self, new_f_cost: float):
        f_costs = [new_f_cost]
        load_window.lcdNumber_initial_cost.display(f_costs[0])
        QCoreApplication.processEvents()

    def initial_temperature(self, new_temperature: float):
        pass


def update_animation(chart):
    load_window.ani = animation.FuncAnimation(load_window.widget_chart_temp, update_axes, update_graph, interval=500, repeat=False)
    load_window.widget_chart_temp.canvas.draw()
    QCoreApplication.processEvents()

def update_graph():
    y = []
    for point in range(1, 101):
        x = range(point)
        y.append(random.random())

        yield x, y

def update_axes(update):
    x, y = update[0], update[1]
    load_window.widget_chart_temp.canvas.axes.clear()
    load_window.widget_chart_temp.canvas.axes.plot(x, y, '-*')
    load_window.widget_chart_temp.canvas.axes.set_xlim(0, 100)
    load_window.widget_chart_temp.canvas.axes.set_ylim(0, 1)


def run_sa(Tmax: int, Tmin: int, kmax: int, alpha: float, cooling_schedule_str: str, cost_functions: np.ndarray):
    # li = np.array([first, second, third, fourth])
    # cost_functions = np.array([True, False, False, True])
    # i = np.where(cost_functions, li, 0)
    # i = i[i != 0]

    update_animation(load_window.widget_chart_temp)
    if cooling_schedule_str == 'exponential':
        result = GuiSetup(Tmax, Tmin, kmax, alpha, sa_file.exponential_cooling_schedule).SA()
    elif cooling_schedule_str == 'linear':
        result = GuiSetup(Tmax, Tmin, kmax, alpha, sa_file.linear_cooling_schedule).SA()
    elif cooling_schedule_str == 'logarithmic':
        result = GuiSetup(Tmax, Tmin, kmax, alpha, sa_file.logarithmic_cooling_schedule).SA()
    elif cooling_schedule_str == 'quadratic':
        result = GuiSetup(Tmax, Tmin, kmax, alpha, sa_file.quadratic_cooling_schedule).SA()
    elif cooling_schedule_str == 'bolzmann':
        result = GuiSetup(Tmax, Tmin, kmax, alpha, sa_file.bolzmann_cooling_schedule).SA()
    elif cooling_schedule_str == 'cauchy':
        result = GuiSetup(Tmax, Tmin, kmax, alpha, sa_file.cauchy_cooling_schedule).SA()

    load_window.lcdNumber_final_cost.display(result.best_cost)


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_apply.clicked.connect(self.go_to_loading_window)
        self.horizontalSlider_alpha.valueChanged.connect(
            lambda: self.label_alpha_procent.setText(str(self.horizontalSlider_alpha.value() / 10000)))
        self.horizontalSlider_lecturer_availability.valueChanged.connect(
            lambda: self.label_lecturer_availability_procent.setText(
                str(self.horizontalSlider_lecturer_availability.value()) + ' %'))
        self.horizontalSlider_room_availability.valueChanged.connect(
            lambda: self.label_room_availability_procent.setText(
                str(self.horizontalSlider_room_availability.value()) + ' %'))
        self.horizontalSlider_matrix_transposition.valueChanged.connect(
            lambda: self.label_matrix_transposition_procent.setText(
                str(self.horizontalSlider_matrix_transposition.value()) + ' %'))
        self.horizontalSlider_matrix_inner_translation.valueChanged.connect(
            lambda: self.label_matrix_inner_translation_procent.setText(
                str(self.horizontalSlider_matrix_inner_translation.value()) + ' %'))
        self.horizontalSlider_matrix_cut_and_paste_translation.valueChanged.connect(
            lambda: self.label_matrix_cut_and_paste_translation_procent.setText(
                str(self.horizontalSlider_matrix_cut_and_paste_translation.value()) + ' %'))

    def go_to_loading_window(self):
        global tmax, tmin, kmax, alpha, cooling_schedule_str, cost_functions
        widget.setCurrentWidget(load_window)
        tmax = self.spinBox_tmax.value()
        tmin = self.spinBox_tmin.value()
        kmax = self.spinBox_kmax.value()
        alpha = self.horizontalSlider_alpha.value() / 10000
        cooling_schedule_str = self.comboBox_cooling_schedule.currentText()
        cost_functions = np.array([self.checkBox_unbalanced_function.isChecked(),
                                   self.checkBox_gaps_c_function.isChecked(),
                                   self.checkBox_lecturer_work_time.isChecked(),
                                   self.checkBox_late_lectures_cost_function.isChecked()])

class LoadingWindow(QMainWindow, loading_window.Ui_MainWindow):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_back.clicked.connect(self.go_to_main_window)
        self.pushButton_initial_timetable.clicked.connect(lambda: self.show_excel('initial'))
        self.pushButton_result_timetable.clicked.connect(lambda: self.show_excel('result'))
        self.pushButton_next.clicked.connect(self.go_to_next_window)
        self.pushButton_run.clicked.connect(
            lambda: run_sa(tmax, tmin, kmax, alpha, cooling_schedule_str, cost_functions))
        # self.lcdNumber_initial_cost.display(56)

    def go_to_main_window(self):
        widget.setCurrentWidget(main_window)

    def show_excel(self, which: str):
        if which == 'initial':
            # TODO
            # os.system("start EXCEL.EXE ../ResultSchedule.xlsx")
            pass
        elif which == 'result':
            os.system("start EXCEL.EXE ../ResultSchedule.xlsx")

    def go_to_next_window(self):
        widget.setCurrentWidget(char_window)


class CharWindow(QMainWindow, char_window.Ui_MainWindow):
    def __init__(self):
        super(CharWindow, self).__init__()
        self.setupUi(self)
        self.addToolBar(NavigationToolbar(self.widget_char.canvas, self))
        # self.pushButton_show.clicked.connect(self.update_animation)


    # def show_chart(self):
    #     x = range(100)
    #     y = [random.random() for _ in range(100)]
    #
    #     self.widget_char.canvas.axes.clear()
    #     self.widget_char.canvas.axes.plot(x, y, '-o')
    #     self.widget_char.canvas.axes.set_xlim(0, 100)
    #     self.widget_char.canvas.draw()

    # def update_animation(self):
    #     self.ani = animation.FuncAnimation(self.widget_char, self.update_axes, self.update_graph, interval=500,
    #                                        repeat=False)
    #     self.widget_char.canvas.draw()
    #
    # def update_graph(self):
    #     y = []
    #     for point in range(1, 101):
    #         x = range(point)
    #         y.append(random.random())
    #
    #         yield x, y
    #
    # def update_axes(self, update):
    #     x, y = update[0], update[1]
    #     self.widget_char.canvas.axes.clear()
    #     self.widget_char.canvas.axes.plot(x, y, '-*')
    #     self.widget_char.canvas.axes.set_xlim(0, 100)
    #     self.widget_char.canvas.axes.set_ylim(0, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_window = MainWindow()
    widget.addWidget(main_window)
    load_window = LoadingWindow()
    widget.addWidget(load_window)
    char_window = CharWindow()
    widget.addWidget(char_window)
    widget.setFixedSize(800, 550)
    # widget.setFixedHeight(600)
    # widget.setFixedWidth(850)
    widget.show()

    sys.exit(app.exec_())
