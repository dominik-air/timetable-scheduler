from __future__ import annotations

import random
import math

import numpy as np
from dataclasses import dataclass

from abc import abstractmethod, ABC
from typing import Callable

from .solution import Solution
from .data_structures import process_image_manager


def exponential_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T * (alpha ** k)


def linear_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T - alpha * k


def logarithmic_cooling_schedule(T: float, alpha: int, k: int) -> float:
    return T / (alpha * math.log(k + 1))


def quadratic_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T / (1 + alpha * (k ** 2))


def bolzmann_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T / (1 + math.log(k))


def cauchy_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T / (1 + k)


@dataclass
class Results:
    initial_solution_matrix: np.ndarray
    best_solution_matrix: np.ndarray
    initial_cost: float
    best_cost: float


class AlgorithmSetup(ABC):
    """Base setup for the simulated annealing algorithm."""

    def __init__(self,
                 Tmax: int | float = 20.0,
                 Tmin: int | float = 5.0,
                 kmax: int = 3,
                 alpha: float = 0.9,
                 cooling_schedule: Callable[[float, float, int], float] = exponential_cooling_schedule):

        self.Tmax = Tmax
        self.Tmin = Tmin
        self.kmax = kmax
        self.alpha = alpha
        self.cooling_schedule = cooling_schedule

        # TODO: add Solution parameters

        self.temperatures: list[float] = []
        self.f_costs: list[float] = []

    @abstractmethod
    def change_in_temperature(self, new_temperature: float):
        raise NotImplementedError

    @abstractmethod
    def change_in_cost_function(self, new_f_cost: float):
        raise NotImplementedError

    def SA(self) -> Results:
        """Simulated annealing algorithm."""

        x0 = Solution()
        process_image_copy = process_image_manager.process_image

        x0_cost = x0.cost
        x_best = x0
        f_best = x0_cost

        n_iter = 0
        T = self.Tmax

        print(f_best)
        self.f_costs = [f_best]
        self.temperatures = [T]

        xc = x0
        while T > self.Tmin:
            print(T)
            for k in range(self.kmax):
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
                self.change_in_cost_function(new_f_cost=xp.cost)
            n_iter += 1
            xc = x_best
            process_image_manager.process_image = process_image_copy
            T = self.cooling_schedule(self.Tmax, self.alpha, n_iter)
            self.change_in_temperature(new_temperature=T)

        print(f'Best cost = {f_best}')
        return Results(initial_cost=x0_cost,
                       initial_solution_matrix=x0.matrix,
                       best_cost=f_best,
                       best_solution_matrix=x_best.matrix)


class StatisticalTestsAlgorithmSetup(AlgorithmSetup):
    """Algorithm setup for performing statistical tests."""

    def change_in_temperature(self, new_temperature: float):
        self.temperatures.append(new_temperature)

    def change_in_cost_function(self, new_f_cost: float):
        self.f_costs.append(new_f_cost)


if __name__ == '__main__':
    print('xd')
