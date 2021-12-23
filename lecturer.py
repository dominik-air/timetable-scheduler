from dataclasses import dataclass
import json
import numpy as np
from copy import deepcopy


@dataclass
class Lecturer:
    id: int
    availability_matrix: np.ndarray

    @property
    def availability_matrix_copy(self) -> np.ndarray:
        return deepcopy(self.availability_matrix)


def lecturer_factory(file_path: str):
    lecturers = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for lecturer in data:
        lecturers[lecturer["id"]] = Lecturer(
            id=lecturer["id"],
            availability_matrix=np.array(lecturer["availability_matrix"]),
        )
    return lecturers


if __name__ == "__main__":
    print(lecturer_factory("data/lecturer_data_term_5.json"))
