import os
import timetable_scheduler

if __name__ == '__main__':
    results = timetable_scheduler.SA(alpha=0.9)
    timetable_scheduler.export_matrix_to_excel(results.best_solution_matrix)
    # open the Result Schedule in Excel
    os.system("start EXCEL.EXE ResultSchedule.xlsx")
