from dataclasses import dataclass
import numpy as np
import json


@dataclass
class Building:
    name: str
    id: int
    cost_matrix: np.ndarray
    availability_matrix: np.ndarray


def building_factory(file_path: str):
    buildings = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for building in data:
        buildings[building["id"]] = Building(
            name=building["name"],
            id=building["id"],
            cost_matrix=building["cost_matrix"],
            availability_matrix=building["availability_matrix"],
        )
    return buildings


if __name__ == "__main__":
    print(building_factory("buildings_data.json"))
