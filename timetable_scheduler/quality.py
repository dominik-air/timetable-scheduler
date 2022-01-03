from dataclasses import dataclass, field
from typing import List, Tuple, Any, Callable
from functools import wraps
from time import time


def timing(f) -> Callable[[Any], Tuple[Any, float]]:
    @wraps(f)
    def wrap(*args, **kwargs) -> Tuple[Any, float]:
        start_time = time()
        result = f(*args, **kwargs)
        end_time = time()
        return result, end_time - start_time
    return wrap


@dataclass
class OperatorCallData:
    """Structure for holding data about an matrix operator's call.

    Attributes:
        iteration_number: the algorithms' iteration in which the matrix operator was called.
        f_cost: the function cost of the solution created by the matrix operator.
        f_cost_change: the change in the cost function after the operator call.

    """

    iteration_number: int
    f_cost: float
    f_cost_change: float
    run_time: float

    def to_json(self):
        return self.__dict__.copy()


@dataclass
class OperatorQuality:
    """Stores general information about the efficiency of a matrix operator.

    Attributes:
        operator_name: name of the matrix operator.
        n_calls: number of times the matrix operators was called.
        n_acceptable_solutions: the number of times the matrix operator returned an acceptable solution.
        f_cost_improvements: the number of times the matrix operator lowered the current solution's cost.
        f_cost_aggravations: the number of times the matrix operator decreased the current solution's cost.
        f_cost_constants: the number of times the matrix operator didn't change the current solution's cost.
        operator_calls: list of more detailed information about specific call of the matrix operator.

    """
    operator_name: str
    n_calls: int = 0  # liczba realizacji
    n_acceptable_solutions: int = 0  # liczba rozwiązań dopuszczalnych
    f_cost_improvements: int = 0  # liczba popraw funkcji celu
    f_cost_aggravations: int = 0  # liczba pogorszeń funkcji celu
    f_cost_constants: int = 0  # liczba braku zmian funkcji celu
    operator_calls: List[OperatorCallData] = field(default_factory=list)  # następstwo

    def add_operator_call_data(self, iteration_number: int,
                               n_calls: int,
                               f_cost: float,
                               f_cost_change: float,
                               run_time: float):
        if f_cost_change < 0:
            self.f_cost_improvements += 1
        elif f_cost_change > 0:
            self.f_cost_aggravations += 1
        else:
            self.f_cost_constants += 1

        self.n_calls += n_calls
        self.n_acceptable_solutions += 1
        self.operator_calls.append(OperatorCallData(iteration_number, f_cost, f_cost_change, run_time))

    def to_json(self):
        json_data = self.__dict__.copy()
        operator_calls_data = [operator_call.to_json() for operator_call in self.operator_calls]
        json_data['operator_calls'] = operator_calls_data
        return json_data

    def get_f_cost_data(self):
        iterations = []
        f_costs = []
        for call in self.operator_calls:
            iterations.append(call.iteration_number)
            f_costs.append(call.f_cost)
        return iterations, f_costs

    def get_f_cost_change_data(self):
        iterations = []
        f_cost_changes = []
        for call in self.operator_calls:
            iterations.append(call.iteration_number)
            f_cost_changes.append(call.f_cost_change)
        return iterations, f_cost_changes

    def get_run_time_data(self):
        iterations = []
        run_times = []
        for call in self.operator_calls:
            iterations.append(call.iteration_number)
            run_times.append(call.run_time)
        return iterations, run_times
