import timetable_scheduler

if __name__ == '__main__':
    results = timetable_scheduler.SA()
    results.export_matrix_to_excel()
