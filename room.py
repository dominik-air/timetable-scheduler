from dataclasses import dataclass
import numpy as np
import json


@dataclass
class Room:
    id: str
    building_id: int
    distance_matrix: np.ndarray
    availability_matrix: np.ndarray


def room_factory(file_path: str):
    rooms = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for room in data:
        rooms[room["id"]] = Room(
            id=room["id"],
            building_id=room["building_id"],
            distance_matrix=np.array(room["distance_matrix"]),
            availability_matrix=np.array(room["availability_matrix"]),
        )
    return rooms


if __name__ == "__main__":
    print(room_factory("room_data_term_5.json"))
