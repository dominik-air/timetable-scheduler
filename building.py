from dataclasses import dataclass
import numpy as np
import json

@dataclass
class Building:
    name: str
    id: int
    cost_matrix: np.ndarray

def building_factory(file_path: str):
    buildings = []
    with open(file_path, 'r') as file:
        data = json.load(file)
    for building in data:
        buildings.append(Building(building['name'], building['id'], building['cost_matrix']))
    return buildings
if __name__ == "__main__":
    print(building_factory('buildings_data.json'))