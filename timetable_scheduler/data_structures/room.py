from dataclasses import dataclass
import numpy as np
import json

distance_matrix = None
with open("../timetable_scheduler/data_structures/data/room_data.json", "r") as file:
    data = json.load(file)
    for room in data:
        distance_matrix = np.array(room['distance_matrix'])
        break


@dataclass
class Room:
    id: str
    building_id: int
    availability_matrix: np.ndarray

    @property
    def availability_matrix_copy(self) -> np.ndarray:
        return np.copy(self.availability_matrix)

    def __deepcopy__(self, memodict={}):
        return Room(id=self.id, building_id=self.building_id, availability_matrix=self.availability_matrix_copy)


def room_factory(file_path: str):
    rooms = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for room in data:
        rooms[room["id"]] = Room(
            id=room["id"],
            building_id=room["building_id"],
            availability_matrix=np.array(room["availability_matrix"]),
        )
    return rooms


if __name__ == "__main__":
    print(room_factory("data/room_data.json"))
