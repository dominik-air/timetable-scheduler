import os
import timetable_scheduler

if __name__ == '__main__':
    timetable_scheduler.create_dataset(term_id=3, lecturer_p=1, room_p=1)
    setup = timetable_scheduler.StatisticalTestsAlgorithmSetup(
        cooling_schedule=timetable_scheduler.simulated_annealing.exponential_cooling_schedule, alpha=0.99)
    results = setup.SA()

    print(f'Time elapsed: {results.elapsed_time}')

    timetable_scheduler.export_matrix_to_excel(results.best_solution_matrix, filename='results/best_solution')
    timetable_scheduler.export_availability_to_excel(export_type='lecturer',
                                                     id=1, filename='results/lecturer_availability')
    timetable_scheduler.export_availability_to_excel(export_type='room',
                                                     id='SWFIS-1', filename='results/room_availability')
    # open the Result Schedule in Excel
    os.system("start EXCEL.EXE results/lecturer_availability.xlsx")
    os.system("start EXCEL.EXE results/room_availability")
    os.system("start EXCEL.EXE results/best_solution.xlsx")
