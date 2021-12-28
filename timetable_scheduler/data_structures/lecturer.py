from dataclasses import dataclass
import json
import numpy as np


@dataclass
class Lecturer:
    id: int
    availability_matrix: np.ndarray

    @property
    def availability_matrix_copy(self) -> np.ndarray:
        return np.copy(self.availability_matrix)

    def __deepcopy__(self, memodict={}):
        return Lecturer(id=self.id, availability_matrix=self.availability_matrix_copy)


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
    print(lecturer_factory("data/lecturer_data.json"))
