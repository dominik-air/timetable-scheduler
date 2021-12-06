from typing import List

import numpy as np
import operators


class Solution:
    def __init__(self, matrix: np.ndarray):
        self.matrix: np.ndarray = matrix

    @property
    def cost(self) -> float:
        """Returns the combined cost for the current solution matrix."""
        raise NotImplementedError

    def check_acceptability(self) -> bool:
        """Checks if the solution is acceptable."""
        raise NotImplementedError

    @classmethod
    def from_neighbourhood(cls, ops: List[operators.matrix_operator]):
        raise NotImplementedError
