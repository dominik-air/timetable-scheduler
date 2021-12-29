import os
import timetable_scheduler

if __name__ == '__main__':
    setup = timetable_scheduler.StatisticalTestsAlgorithmSetup(
        cooling_schedule=timetable_scheduler.simulated_annealing.exponential_cooling_schedule, alpha=0.999)
    results = setup.SA()
    timetable_scheduler.export_matrix_to_excel(results.best_solution_matrix)
    # open the Result Schedule in Excel
    os.system("start EXCEL.EXE ResultSchedule.xlsx")
