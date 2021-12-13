from dataclasses import dataclass
import numpy as np
import json


@dataclass
class Room:
    name: str
    id: int
    building_id: int
    cost_matrix: np.ndarray
    availability_matrix: np.ndarray


def room_factory(file_path: str):
    rooms = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for room in data:
        rooms[room["id"]] = Room(
            name=room["name"],
            id=room["id"],
            building_id=room["building_id"],
            cost_matrix=np.array(room["cost_matrix"]),
            availability_matrix=np.array(room["availability_matrix"]),
        )
    return rooms


if __name__ == "__main__":
    print(room_factory("buildings_data.json"))
