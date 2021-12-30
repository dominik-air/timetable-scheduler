from __future__ import annotations

import random
import math

import numpy as np
from dataclasses import dataclass

from abc import abstractmethod, ABC
from typing import Callable

from timetable_scheduler import operators
from timetable_scheduler.quality import OperatorQuality
from .solution import Solution
from .data_structures import process_image_manager


def exponential_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T * (alpha ** k)


def linear_cooling_schedule(T: float, alpha: float, k: int) -> float:
    return T - alpha * k


def logarithmic_cooling_schedule(T: float, alpha: float, k: int) -> float:
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
    operator_quality_measurement: list


class AlgorithmSetup(ABC):
    """Base setup for the simulated annealing algorithm."""

    def __init__(self,
                 Tmax: int | float = 20.0,
                 Tmin: int | float = 5.0,
                 kmax: int = 3,
                 alpha: float = 0.9,
                 max_iterations: int = None,
                 cooling_schedule: Callable[[float, float, int], float] = exponential_cooling_schedule,
                 operator_probabilities: list[float] = None,
                 cost_functions: list[callable] = None
                 ):

        # simulated annealing parameters
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.kmax = kmax
        self.alpha = alpha
        self.cooling_schedule = cooling_schedule

        # Solution parameters
        if operator_probabilities is None:
            operator_probabilities = [0.33, 0.33, 0.34]
        self.operator_probabilities = operator_probabilities

        self.cost_functions = cost_functions

        if max_iterations is None:
            # random huge number
            max_iterations = int(10e9)
        self.max_iterations = max_iterations

        self.operator_quality_measurement = {
            operators.matrix_transposition: OperatorQuality(operator_name='matrix_transposition'),
            operators.matrix_inner_translation: OperatorQuality(operator_name='matrix_inner_translation'),
            operators.matrix_cut_and_paste_translation: OperatorQuality(
                operator_name='matrix_cut_and_paste_translation')
        }

    @abstractmethod
    def change_in_temperature(self, new_temperature: float):
        raise NotImplementedError

    @abstractmethod
    def change_in_cost_function(self, new_f_cost: float, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def initial_cost_function(self, new_f_cost: float):
        raise NotImplementedError

    @abstractmethod
    def initial_temperature(self, new_temperature: float):
        raise NotImplementedError

    def SA(self) -> Results:
        """Simulated annealing algorithm."""
        process_image_manager.reset_process_image()
        x0 = Solution(cost_functions=self.cost_functions)

        initial_solution_resets = 0
        while not x0.check_acceptability():
            initial_solution_resets += 1
            process_image_manager.reset_process_image()
            x0 = Solution(cost_functions=self.cost_functions)
        print(f'zresetowałem początkowe rozwiązanie {initial_solution_resets}-razy')
        process_image_copy = process_image_manager.process_image

        x0_cost = x0.cost
        x_best = x0
        f_best = x0_cost

        n_iter = 0
        T = self.Tmax

        print(f_best)
        self.initial_cost_function(f_best)
        self.initial_temperature(T)

        xc = x0
        while T > self.Tmin and n_iter < self.max_iterations:
            print(T)
            for k in range(self.kmax):
                matrix_operator = np.random.choice([operators.matrix_transposition,
                                                    operators.matrix_inner_translation,
                                                    operators.matrix_cut_and_paste_translation],
                                                   p=self.operator_probabilities)
                xp, operator_iter = xc.from_neighbourhood(matrix_operator)
                new_solution_cost = xp.cost
                delta = new_solution_cost - xc.cost
                # record current matrix operator's quality data
                self.operator_quality_measurement[matrix_operator].add_operator_call_data(iteration_number=n_iter,
                                                                                          n_calls=operator_iter,
                                                                                          f_cost=new_solution_cost,
                                                                                          f_cost_change=delta)
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
                self.change_in_cost_function(new_f_cost=xp.cost, n_iter=n_iter)
                n_iter += 1
            xc = x_best
            process_image_manager.process_image = process_image_copy
            T = self.cooling_schedule(self.Tmax, self.alpha, n_iter)
            self.change_in_temperature(new_temperature=T)

        print(f'Best cost = {f_best}')
        return Results(initial_cost=x0_cost,
                       initial_solution_matrix=x0.matrix,
                       best_cost=f_best,
                       best_solution_matrix=x_best.matrix,
                       operator_quality_measurement=list(self.operator_quality_measurement.values()))


class StatisticalTestsAlgorithmSetup(AlgorithmSetup):
    """Algorithm setup for performing statistical tests."""

    temperatures: list[float] = []
    f_costs: list[float] = []

    def change_in_temperature(self, new_temperature: float):
        self.temperatures.append(new_temperature)

    def change_in_cost_function(self, new_f_cost: float, **kwargs):
        self.f_costs.append(new_f_cost)

    def initial_cost_function(self, new_f_cost: float):
        self.f_costs = [new_f_cost]

    def initial_temperature(self, new_temperature: float):
        self.temperatures = [new_temperature]


if __name__ == '__main__':
    print('xd')
