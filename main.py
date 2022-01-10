import os
import timetable_scheduler
import matplotlib.pyplot as plt

if __name__ == '__main__':
    timetable_scheduler.create_dataset(term_id=5, lecturer_p=1, room_p=1)
    setup = timetable_scheduler.StatisticalTestsAlgorithmSetup(
        cooling_schedule=timetable_scheduler.simulated_annealing.exponential_cooling_schedule,
        operator_probabilities=[0.33, 0.33, 0.34], Tmax=30, Tmin=0.00133, kmax=30, alpha=0.995)

    results = setup.SA()

    print(f'Time elapsed: {results.elapsed_time}')

    plt.plot(setup.f_costs, 'b--')
    plt.plot(setup.best_cost_change, 'r-')
    plt.show()

