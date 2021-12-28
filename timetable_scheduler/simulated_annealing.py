import random
import math
import cProfile
import numpy as np
from dataclasses import dataclass

from typing import List

from .solution import Solution
from .data_structures import process_image_manager


@dataclass
class Results:
    initial_solution_matrix: np.ndarray
    best_solution_matrix: np.ndarray
    initial_cost: float
    best_cost: float
    f_cost_changes: List[float]
    temperature_changes: List[float]


def exponential_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T * (alpha ** k)


def linear_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T - alpha * k


def logarithmic_cooling_schedule(T: int, alpha: int, k: int) -> float:
    return T / (alpha * math.log(k + 1))


def quadratic_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T / (1 + alpha * (k ** 2))


def bolzmann_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T / (1 + math.log(k))


def cauchy_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T / (1 + k)


def SA(Tmax: int = 20, Tmin: int = 5, kmax: int = 5, alpha: float = 0.99,
       cooling_schedule: callable = exponential_cooling_schedule):
    """Simulated annealing algorithm.

    Args:
        Tmax: initial system temperature.
        Tmin: minimal temperature (lower bound) of the cooling process.
        kmax: number of iterations in a given temperature.
        alpha: cooling process coefficient.
        cooling_schedule: cooling_schedule

    """

    x0 = Solution()
    process_image_copy = process_image_manager.process_image

    x0_cost = x0.cost
    x_best = x0
    f_best = x0_cost

    n_iter = 0
    T = Tmax

    print(f_best)
    f_costs: list[float] = [f_best]
    temperatures: list[float] = [T]

    xc = x0
    while T > Tmin:
        print(T)
        for k in range(kmax):
            xp = xc.from_neighbourhood()
            delta = xp.cost - xc.cost
            if delta <= 0:
                xc = xp
                if xc.cost <= f_best:
                    f_best = xc.cost
                    x_best = xc
                    process_image_copy = process_image_manager.process_image
            else:
                sigma = random.random()
                if sigma < math.exp(-delta / T):
                    xc = xp
            f_costs.append(xp.cost)
        n_iter += 1
        xc = x_best
        process_image_manager.process_image = process_image_copy
        T = cooling_schedule(Tmax, alpha, n_iter)
        temperatures.append(T)

    print(f'Best cost = {f_best}')
    return Results(initial_cost=x0_cost,
                   initial_solution_matrix=x0.matrix,
                   best_cost=f_best,
                   best_solution_matrix=x_best.matrix,
                   f_cost_changes=f_costs,
                   temperature_changes=temperatures)


def test_SA(cooling_schedule=exponential_cooling_schedule):
    SA(cooling_schedule=cooling_schedule)
    process_image_manager.reset_process_image()


if __name__ == '__main__':
    test_SA(cooling_schedule=exponential_cooling_schedule)
