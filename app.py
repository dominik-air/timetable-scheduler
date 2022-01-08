#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import gui.main_window as main_window
import gui.loading_window as loading_window
import gui.char_window as char_window
import timetable_scheduler
import timetable_scheduler.simulated_annealing as sa_file
import timetable_scheduler.cost_functions
import numpy as np
import matplotlib.animation as animation
from timetable_scheduler.data_structures import process_image_manager

COOLING_SCHEDULE_MAP = {
    'exponential': sa_file.exponential_cooling_schedule,
    'linear': sa_file.linear_cooling_schedule,
    'logarithmic': sa_file.logarithmic_cooling_schedule,
    'quadratic': sa_file.quadratic_cooling_schedule,
    'bolzmann': sa_file.bolzmann_cooling_schedule,
    'cauchy': sa_file.cauchy_cooling_schedule
}

SIMULATED_ANNEALING_COST_FUNCTIONS = np.array([
    timetable_scheduler.cost_functions.gaps_c_function,
    timetable_scheduler.cost_functions.unbalanced_function,
    timetable_scheduler.cost_functions.lecturer_work_time,
    timetable_scheduler.cost_functions.late_lectures_cost_function,
    timetable_scheduler.cost_functions.early_lectures_cost_function
])

chart_iterations = []
chart_cost_function_values = []

initial_solution_matrix = None
best_solution_matrix = None

min_chart_value = 999999
min_chart_tab = []


def calculate_max_iteration(cooling_schedule: sa_file.CoolingSchedule,
                            Tmax: float, Tmin: float, alpha: float) -> int:
    iter = 0
    T = Tmax
    while T > Tmin:
        iter += 1
        T = cooling_schedule(Tmax, alpha, iter)
    return iter


class GuiSetup(sa_file.AlgorithmSetup):
    def change_in_temperature(self, new_temperature: float):
        load_window.lcdNumber_final_temp.display(new_temperature)
        QCoreApplication.processEvents()

    def change_in_cost_function(self, new_f_cost: float, **kwargs):
        global min_chart_value
        load_window.lcdNumber_final_cost.display(new_f_cost)
        current_iteration = kwargs['n_iter']
        chart_iterations.append(current_iteration)

        percent = current_iteration / main_window.spinBox_iter_max.value() * 100
        load_window.progressBar.setValue(int(percent))

        chart_cost_function_values.append(new_f_cost)

        if new_f_cost < min_chart_value:
            min_chart_value = new_f_cost
        min_chart_tab.append(min_chart_value)

        QCoreApplication.processEvents()

    def initial_cost_function(self, new_f_cost: float, **kwargs):
        # clears the chart every time we run SA algorithm
        global chart_iterations, chart_cost_function_values, min_chart_tab, min_chart_value
        chart_iterations = []
        chart_cost_function_values = []
        min_chart_tab = []
        min_chart_value = 999999

        f_costs = [new_f_cost]
        load_window.lcdNumber_initial_cost.display(f_costs[0])
        QCoreApplication.processEvents()

    def initial_temperature(self, new_temperature: float):
        update_animation()


def update_animation():
    load_window.ani = animation.FuncAnimation(
        load_window.widget_chart_temp, update_axes, update_graph, interval=50, repeat=False)
    load_window.widget_chart_temp.canvas.draw()
    QCoreApplication.processEvents()


def update_graph():
    while True:
        x = chart_iterations
        y = chart_cost_function_values
        y_min = min_chart_tab
        yield x, y, y_min


def update_axes(update):
    x, y, y_min = update[0], update[1], update[2]
    load_window.widget_chart_temp.canvas.axes.clear()
    load_window.widget_chart_temp.canvas.axes.plot(x, y, '-', color='mediumblue')
    load_window.widget_chart_temp.canvas.axes.plot(x, y_min, 'r--')
    load_window.widget_chart_temp.canvas.axes.set_title('cost function')
    load_window.widget_chart_temp.canvas.axes.set_xlabel('iterations')
    load_window.widget_chart_temp.canvas.axes.set_ylabel('value of cost function')
    load_window.widget_chart_temp.canvas.axes.set_xlim(0, main_window.spinBox_iter_max.value())
    load_window.widget_chart_temp.canvas.axes.legend(["neighbourhood", "best"])


def run_sa(Tmax: int, Tmin: int, kmax: int, alpha: float, cooling_schedule_str: str, cost_functions: np.ndarray):
    term_id = int(main_window.comboBox_term.currentText()[-1])
    lecturer_availability = main_window.horizontalSlider_lecturer_availability.value() / 100
    room_availability = main_window.horizontalSlider_room_availability.value() / 100

    timetable_scheduler.create_dataset(term_id=term_id, lecturer_p=lecturer_availability, room_p=room_availability)

    chosen_cost_functions = np.where(cost_functions, SIMULATED_ANNEALING_COST_FUNCTIONS, 0)
    chosen_cost_functions = chosen_cost_functions[chosen_cost_functions != 0]

    # calculate probabilities for every matrix operator
    transposition_weight = max(main_window.horizontalSlider_matrix_transposition.value(), 0.01)
    translation_weight = max(main_window.horizontalSlider_matrix_inner_translation.value(), 0.01)
    cut_and_paste_weight = max(main_window.horizontalSlider_matrix_cut_and_paste_translation.value(), 0.01)
    weights_summed = transposition_weight + translation_weight + cut_and_paste_weight

    transposition_p = transposition_weight / weights_summed
    translation_p = translation_weight / weights_summed
    cut_and_paste_p = cut_and_paste_weight / weights_summed

    chosen_cooling_schedule = COOLING_SCHEDULE_MAP[cooling_schedule_str]

    max_iterations = min(main_window.spinBox_iter_max.value(),
                         calculate_max_iteration(chosen_cooling_schedule, Tmax, Tmin, alpha))
    main_window.spinBox_iter_max.setValue(max_iterations)

    result = GuiSetup(Tmax, Tmin, kmax, alpha,
                      cooling_schedule=chosen_cooling_schedule,
                      max_iterations=max_iterations,
                      cost_functions=chosen_cost_functions,
                      operator_probabilities=[transposition_p, translation_p, cut_and_paste_p]).SA()

    lecturers_list = [str(lecturer_id) for lecturer_id in
                      process_image_manager.process_image_read_only.lecturers.keys()]
    char_window.comboBox_lecturer.addItems(lecturers_list)
    rooms_list = process_image_manager.process_image_read_only.rooms.keys()
    char_window.comboBox_room.addItems(rooms_list)

    load_window.lcdNumber_final_cost.display(result.best_cost)
    load_window.progressBar.setValue(100)
    global initial_solution_matrix, best_solution_matrix
    initial_solution_matrix = result.initial_solution_matrix
    best_solution_matrix = result.best_solution_matrix


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_apply.clicked.connect(self.go_to_loading_window)
        self.comboBox_cooling_schedule.currentIndexChanged.connect(self.change_parameters)
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
        tmax = self.doubleSpinBox_tmax.value()
        tmin = self.doubleSpinBox_tmin.value()
        kmax = self.spinBox_kmax.value()
        alpha = self.horizontalSlider_alpha.value() / 10000
        cooling_schedule_str = self.comboBox_cooling_schedule.currentText()
        cost_functions = np.array([self.checkBox_unbalanced_function.isChecked(),
                                   self.checkBox_gaps_c_function.isChecked(),
                                   self.checkBox_lecturer_work_time.isChecked(),
                                   self.checkBox_late_lectures_cost_function.isChecked(),
                                   self.checkBox_early_lectures_cost_function.isChecked()])
        if tmax < tmin:
            QMessageBox.about(self, "Wrong inputs", "tmin can't be greater than tmax")
        elif np.sum(cost_functions) == 0:
            QMessageBox.about(self, "Wrong inputs", "choose at least one cost function")
        else:
            widget.setCurrentWidget(load_window)

    def change_parameters(self, index):
        self.doubleSpinBox_tmax.setEnabled(True)
        self.doubleSpinBox_tmin.setEnabled(True)
        self.spinBox_kmax.setEnabled(True)
        self.pushButton_apply.setEnabled(True)
        self.horizontalSlider_alpha.setEnabled(True)
        self.horizontalSlider_alpha.setMinimum(9000)
        self.horizontalSlider_alpha.setMaximum(9999)
        self.horizontalSlider_alpha.setProperty("value", 9900)
        self.horizontalSlider_alpha.setTickInterval(100)
        if index == 0:
            self.doubleSpinBox_tmax.setValue(0.1)
            self.doubleSpinBox_tmin.setValue(0.1)
            self.spinBox_kmax.setValue(1)
            self.doubleSpinBox_tmax.setEnabled(False)
            self.doubleSpinBox_tmin.setEnabled(False)
            self.spinBox_kmax.setEnabled(False)
            self.pushButton_apply.setEnabled(False)
        elif index == 1:
            self.doubleSpinBox_tmax.setValue(20)
            self.doubleSpinBox_tmin.setValue(5)
            self.spinBox_kmax.setValue(5)
        elif index == 2:
            self.doubleSpinBox_tmax.setValue(130)
            self.doubleSpinBox_tmin.setValue(5)
            self.spinBox_kmax.setValue(5)
            self.horizontalSlider_alpha.setMinimum(10000)
            self.horizontalSlider_alpha.setMaximum(100000)
            self.horizontalSlider_alpha.setProperty("value", 20000)
            self.horizontalSlider_alpha.setTickInterval(5000)
        elif index == 3:
            self.doubleSpinBox_tmax.setValue(25)
            self.doubleSpinBox_tmin.setValue(5)
            self.spinBox_kmax.setValue(5)
        elif index == 4:
            self.doubleSpinBox_tmax.setValue(199)
            self.doubleSpinBox_tmin.setValue(0.1)
            self.spinBox_kmax.setValue(1)
        elif index == 5:
            self.horizontalSlider_alpha.setEnabled(False)
            self.doubleSpinBox_tmax.setValue(30)
            self.doubleSpinBox_tmin.setValue(5)
            self.spinBox_kmax.setValue(5)
        elif index == 6:
            self.horizontalSlider_alpha.setEnabled(False)
            self.doubleSpinBox_tmax.setValue(150)
            self.doubleSpinBox_tmin.setValue(1.2)
            self.spinBox_kmax.setValue(1)


class LoadingWindow(QMainWindow, loading_window.Ui_MainWindow):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        self.setWindowTitle('Simulated annealing')
        self.setupUi(self)
        self.pushButton_back.clicked.connect(self.go_to_main_window)
        self.pushButton_excel.clicked.connect(self.go_to_next_window)
        self.pushButton_run.clicked.connect(
            lambda: run_sa(tmax, tmin, kmax, alpha, cooling_schedule_str, cost_functions))

    def go_to_main_window(self):
        widget.setCurrentWidget(main_window)

    def go_to_next_window(self):
        widget.setCurrentWidget(char_window)


class CharWindow(QMainWindow, char_window.Ui_MainWindow):
    def __init__(self):
        super(CharWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_back.clicked.connect(self.go_to_loading_window)
        self.pushButton_initial_timetable.clicked.connect(lambda: self.show_excel('initial'))
        self.pushButton_result_timetable.clicked.connect(lambda: self.show_excel('result'))
        self.pushButton_lecturer_excel.clicked.connect(lambda: self.show_excel('lecturer'))
        self.pushButton_room_excel.clicked.connect(lambda: self.show_excel('room'))

    def go_to_loading_window(self):
        widget.setCurrentWidget(load_window)

    def show_excel(self, which: str):
        if which == 'initial' and initial_solution_matrix is not None:
            timetable_scheduler.export_matrix_to_excel(matrix=initial_solution_matrix,
                                                       filename='results/initial_solution')
            os.system("start EXCEL.EXE results/initial_solution.xlsx")
        elif which == 'result' and best_solution_matrix is not None:
            timetable_scheduler.export_matrix_to_excel(matrix=best_solution_matrix,
                                                       filename='results/best_solution')
            os.system("start EXCEL.EXE results/best_solution.xlsx")
        elif which == 'lecturer':
            lecturer_id = int(self.comboBox_lecturer.currentText())
            timetable_scheduler.export_availability_to_excel(export_type='lecturer', id=lecturer_id,
                                                             filename='results/lecturer_availability')
            os.system("start EXCEL.EXE results/lecturer_availability.xlsx")
        elif which == 'room':
            room_id = self.comboBox_room.currentText()
            timetable_scheduler.export_availability_to_excel(export_type='room', id=room_id,
                                                             filename='results/room_availability')
            os.system("start EXCEL.EXE results/room_availability.xlsx")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setWindowTitle('Simulated annealing')
    main_window = MainWindow()
    widget.addWidget(main_window)
    load_window = LoadingWindow()
    widget.addWidget(load_window)
    char_window = CharWindow()
    widget.addWidget(char_window)
    widget.setFixedSize(1100, 700)
    widget.show()

    sys.exit(app.exec_())
