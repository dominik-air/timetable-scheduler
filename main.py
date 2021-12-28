import os
import timetable_scheduler

if __name__ == '__main__':
    results = timetable_scheduler.SA()
    results.export_matrix_to_excel()
    # open the Result Schedule in Excel
    os.system("start EXCEL.EXE ResultSchedule.xlsx")
