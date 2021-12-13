from dataclasses import dataclass
import json
import numpy as np


@dataclass
class Lecturer:
    name: str
    id: int
    availability_matrix: np.ndarray


def lecturer_factory(file_path: str):
    lecturers = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for lecturer in data:
        lecturers[lecturer["id"]] = Lecturer(
            name=lecturer["name"],
            id=lecturer["id"],
            availability_matrix=np.array(lecturer["matrix"]),
        )
    return lecturers


if __name__ == "__main__":
    print(lecturer_factory("lecturers_data.json"))
