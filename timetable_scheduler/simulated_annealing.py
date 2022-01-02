import random
import math

import numpy as np
from dataclasses import dataclass

from abc import abstractmethod, ABC
from typing import Callable, List, Union, Tuple

from timetable_scheduler import matrix_operators
from timetable_scheduler.cost_functions import CostFunction
from timetable_scheduler.quality import OperatorQuality, timing
from .solution import Solution
from .data_structures import process_image_manager

# cooling schedules type hint and implementations
CoolingSchedule = Callable[[float, float, int], float]


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
    elapsed_time: float


class AlgorithmSetup(ABC):
    """Base setup for the simulated annealing algorithm."""

    def __init__(self,
                 Tmax: Union[int, float] = 20.0,
                 Tmin: Union[int, float] = 5.0,
                 kmax: int = 3,
                 alpha: float = 0.9,
                 max_iterations: int = None,
                 cooling_schedule: CoolingSchedule = exponential_cooling_schedule,
                 operator_probabilities: List[float] = None,
                 cost_functions: List[CostFunction] = None
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

    @abstractmethod
    def change_in_temperature(self, new_temperature: float):
        raise NotImplementedError

    @abstractmethod
    def change_in_cost_function(self, new_f_cost: float, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def initial_cost_function(self, new_f_cost: float, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def initial_temperature(self, new_temperature: float):
        raise NotImplementedError

    def SA(self, *args, **kwargs) -> Results:
        """Interface for calling the simulated annealing algorithm."""

        (initial_cost, initial_matrix, f_best, best_matrix), run_time = self._SA(*args, **kwargs)

        return Results(initial_cost=initial_cost,
                       initial_solution_matrix=initial_matrix,
                       best_cost=f_best,
                       best_solution_matrix=best_matrix,
                       elapsed_time=run_time)

    @timing
    def _SA(self) -> Tuple[float, np.ndarray, float, np.ndarray]:
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
        self.initial_cost_function(f_best, resets=initial_solution_resets)
        self.initial_temperature(T)

        xc = x0
        while T > self.Tmin and n_iter < self.max_iterations:
            print(T)
            for k in range(self.kmax):
                matrix_operator = np.random.choice([matrix_operators.matrix_transposition,
                                                    matrix_operators.matrix_inner_translation,
                                                    matrix_operators.matrix_cut_and_paste_translation],
                                                   p=self.operator_probabilities)
                xp, operator_iter, operator_elapsed_time = xc.from_neighbourhood(matrix_operator)
                new_solution_cost = xp.cost
                delta = new_solution_cost - xc.cost

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

                self.change_in_cost_function(new_f_cost=xp.cost,
                                             n_iter=n_iter,
                                             matrix_operator=matrix_operator,
                                             n_calls=operator_iter,
                                             f_cost=new_solution_cost,
                                             f_cost_change=delta,
                                             run_time=operator_elapsed_time
                                             )
                n_iter += 1
            xc = x_best
            process_image_manager.process_image = process_image_copy
            T = self.cooling_schedule(self.Tmax, self.alpha, n_iter)
            self.change_in_temperature(new_temperature=T)

        print(f'Best cost = {f_best}')

        return x0_cost, x0.matrix, f_best, x_best.matrix


class StatisticalTestsAlgorithmSetup(AlgorithmSetup):
    """Algorithm setup for performing statistical tests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_solution_resets: int = 0
        self.temperatures: List[float] = []
        self.f_costs: List[float] = []

        self.operator_quality_measurement = {
            matrix_operators.matrix_transposition: OperatorQuality(operator_name='matrix_transposition'),
            matrix_operators.matrix_inner_translation: OperatorQuality(operator_name='matrix_inner_translation'),
            matrix_operators.matrix_cut_and_paste_translation: OperatorQuality(
                operator_name='matrix_cut_and_paste_translation')
        }

    def change_in_temperature(self, new_temperature: float):
        self.temperatures.append(new_temperature)

    def change_in_cost_function(self, new_f_cost: float, **kwargs):
        self.f_costs.append(new_f_cost)

        # record current matrix operator's quality data
        self.operator_quality_measurement[kwargs['matrix_operator']].add_operator_call_data(
            iteration_number=kwargs['n_iter'],
            n_calls=kwargs['n_calls'],
            f_cost=kwargs['f_cost'],
            f_cost_change=kwargs['f_cost_change'],
            run_time=kwargs['run_time'])

    def initial_cost_function(self, new_f_cost: float, **kwargs):
        self.f_costs = [new_f_cost]
        self.initial_solution_resets = kwargs['resets']

    def initial_temperature(self, new_temperature: float):
        self.temperatures = [new_temperature]


if __name__ == '__main__':
    print('xd')
