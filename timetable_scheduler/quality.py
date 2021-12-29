from dataclasses import dataclass, field
from typing import List


@dataclass
class OperatorCallData:
    iteration_number: int
    f_cost: float
    f_cost_change: float


@dataclass
class OperatorQuality:
    operator_name: str
    n_calls: int = 0  # liczba realizacji
    n_acceptable_solutions: int = 0  # liczba rozwiązań dopuszczalnych
    f_cost_improvements: int = 0  # liczba popraw funkcji celu
    f_cost_aggravations: int = 0  # liczba pogorszeń funkcji celu
    f_cost_constants: int = 0  # liczba braku zmian funkcji celu
    operator_calls: List[OperatorCallData] = field(default_factory=list)  # następstwo

    def add_operator_call_data(self, iteration_number: int, n_calls: int, f_cost: float, f_cost_change: float):
        if f_cost_change < 0:
            self.f_cost_improvements += 1
        elif f_cost_change > 0:
            self.f_cost_aggravations += 1
        else:
            self.f_cost_constants += 1

        self.n_calls += n_calls
        self.n_acceptable_solutions += 1
        self.operator_calls.append(OperatorCallData(iteration_number, f_cost, f_cost_change))

