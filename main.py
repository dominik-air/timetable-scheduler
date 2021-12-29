import os
import timetable_scheduler

if __name__ == '__main__':
    setup = timetable_scheduler.StatisticalTestsAlgorithmSetup(cooling_schedule=timetable_scheduler.simulated_annealing.exponential_cooling_schedule, alpha=0.9)
    results = setup.SA()
    timetable_scheduler.export_matrix_to_excel(results.best_solution_matrix)
    timetable_scheduler.export_availability_to_excel(export_type='lecturer', id=1, filename='lecturer_availability')
    timetable_scheduler.export_availability_to_excel(export_type='room', id='B1-121', filename='room_availability')
    # open the Result Schedule in Excel
    os.system("start EXCEL.EXE lecturer_availability.xlsx")
    os.system("start EXCEL.EXE room_availability.xlsx")
    # os.system("start EXCEL.EXE ResultSchedule.xlsx")
