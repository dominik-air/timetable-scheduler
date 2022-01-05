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


@dataclass
class StatisticalResults(Results):
    temperatures: List[float]
    f_costs: List[float]
    initial_solutions_resets: int
    operator_quality_measurement: List[OperatorQuality]

    def to_json(self):
        json_data = self.__dict__.copy()
        del json_data['initial_solution_matrix']
        del json_data['best_solution_matrix']
        del json_data['temperatures']
        del json_data['f_costs']
        json_data['operator_quality_measurement'] = [op_q.to_json() for op_q in self.operator_quality_measurement]
        return json_data


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
        initial_solution = Solution(cost_functions=self.cost_functions)

        initial_solution_resets = 0
        while not initial_solution.check_acceptability():
            initial_solution_resets += 1
            process_image_manager.reset_process_image()
            initial_solution = Solution(cost_functions=self.cost_functions)
        print(f'zresetowałem początkowe rozwiązanie {initial_solution_resets}-razy')
        process_image_copy = process_image_manager.process_image

        initial_cost = initial_solution.cost
        best_solution = initial_solution
        f_best = initial_cost

        n_iter = 0
        T = self.Tmax

        print(f_best)
        self.initial_cost_function(f_best, resets=initial_solution_resets)
        self.initial_temperature(T)

        current_solution = initial_solution
        while T > self.Tmin and n_iter < self.max_iterations:
            print(T)
            for k in range(self.kmax):
                current_solution_cost = current_solution.cost

                matrix_operator = np.random.choice([matrix_operators.matrix_transposition,
                                                    matrix_operators.matrix_inner_translation,
                                                    matrix_operators.matrix_cut_and_paste_translation],
                                                   p=self.operator_probabilities)
                new_solution, new_process_image, operator_iter = current_solution.from_neighbourhood(matrix_operator)

                process_image_backup = process_image_manager.process_image
                process_image_manager.process_image = new_process_image

                new_solution_cost = new_solution.cost
                delta = new_solution_cost - current_solution_cost

                if delta <= 0:
                    current_solution = new_solution
                    if new_solution_cost <= f_best:
                        f_best = new_solution_cost
                        best_solution = current_solution
                        process_image_copy = process_image_manager.process_image
                else:
                    sigma = random.random()
                    if sigma < math.exp(-delta / T):
                        current_solution = new_solution
                    else:
                        process_image_manager.process_image = process_image_backup

                self.change_in_cost_function(new_f_cost=min(new_solution_cost, current_solution_cost),
                                             n_iter=n_iter,
                                             matrix_operator=matrix_operator,
                                             n_calls=operator_iter,
                                             f_cost_change=delta
                                             )
                n_iter += 1

            T = self.cooling_schedule(self.Tmax, self.alpha, n_iter)
            self.change_in_temperature(new_temperature=T)

        print(f'Best cost = {f_best}')

        return initial_cost, initial_solution.matrix, f_best, best_solution.matrix


class StatisticalTestsAlgorithmSetup(AlgorithmSetup):
    """Algorithm setup for performing statistical tests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_solution_resets: int = 0
        self.temperatures: List[float] = []
        self.f_costs: List[float] = []
        self.best_cost_change: List[float] = []

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
        if new_f_cost < self.best_cost_change[-1]:
            self.best_cost_change.append(new_f_cost)
        else:
            self.best_cost_change.append(self.best_cost_change[-1])

        # record current matrix operator's quality data
        self.operator_quality_measurement[kwargs['matrix_operator']].add_operator_call_data(
            iteration_number=kwargs['n_iter'],
            n_calls=kwargs['n_calls'],
            f_cost=new_f_cost,
            f_cost_change=kwargs['f_cost_change'])

    def initial_cost_function(self, new_f_cost: float, **kwargs):
        self.f_costs = [new_f_cost]
        self.best_cost_change = [new_f_cost]
        self.initial_solution_resets = kwargs['resets']

    def initial_temperature(self, new_temperature: float):
        self.temperatures = [new_temperature]

    def SA(self, *args, **kwargs) -> StatisticalResults:
        """Interface for calling the simulated annealing algorithm."""

        (initial_cost, initial_matrix, f_best, best_matrix), run_time = self._SA(*args, **kwargs)

        return StatisticalResults(initial_cost=initial_cost,
                                  initial_solution_matrix=initial_matrix,
                                  best_cost=f_best,
                                  best_solution_matrix=best_matrix,
                                  elapsed_time=run_time,
                                  initial_solutions_resets=self.initial_solution_resets,
                                  temperatures=self.temperatures,
                                  f_costs=self.f_costs,
                                  operator_quality_measurement=list(self.operator_quality_measurement.values()))


if __name__ == '__main__':
    print('xd')
