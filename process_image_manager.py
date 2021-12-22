import numpy as np
from dataclasses import dataclass, field
from course import courses_factory, Course
from lecturer import lecturer_factory, Lecturer
from room import room_factory, Room, distance_matrix
from copy import deepcopy, copy


@dataclass
class ProcessImage:
    """The current state of objects a Solution is based on."""

    distance_matrix: np.ndarray
    courses: dict = field(default_factory=dict)
    lecturers: dict = field(default_factory=dict)
    rooms: dict = field(default_factory=dict)

    def get_lecturer_by_id(self, lecturer_id: int) -> Lecturer:
        return self.lecturers[lecturer_id]

    def get_course_by_id(self, course_id: int) -> Course:
        return self.courses[course_id]

    def get_room_by_id(self, room_id: int) -> Room:
        return self.rooms[room_id]

    def check_lecturer_availability(self, lecturer_id: int, day: int = None, start: int = None, stop: int = None,
                                    slice: np.ndarray = None) -> bool:
        if slice is not None:
            return np.all(self.lecturers[lecturer_id].availability_matrix[slice])
        return np.all(self.lecturers[lecturer_id].availability_matrix[start:stop, day])

    def check_room_availability(self, room_id: int, day: int = None, start: int = None, stop: int = None,
                                slice: np.ndarray = None) -> bool:
        if slice is not None:
            return np.all(self.rooms[room_id].availability_matrix[slice])
        return np.all(self.rooms[room_id].availability_matrix[start:stop, day])

    def check_travel_time(self, course_A_id: int, course_B_id: int, current_time: int):
        start_building = self.rooms[self.courses[course_A_id].room_id].building_id
        destination_building = self.rooms[self.courses[course_B_id].room_id].building_id
        min_time = self.distance_matrix[start_building, destination_building]
        return current_time >= min_time

    def reserve_lecturer_time(self, lecturer_id: int, day: int = None, start: int = None, stop: int = None,
                              slice: np.ndarray = None):
        if slice is not None:
            self.lecturers[lecturer_id].availability_matrix[slice] = 0
        self.lecturers[lecturer_id].availability_matrix[start:stop, day] = 0

    def reserve_room_time(self, room_id: int, day: int = None, start: int = None, stop: int = None,
                          slice: np.ndarray = None):
        if slice is not None:
            self.rooms[room_id].availability_matrix[slice] = 0
        self.rooms[room_id].availability_matrix[start:stop, day] = 0

    def free_lecturer_time(self, lecturer_id: int, day: int = None, start: int = None, stop: int = None,
                              slice: np.ndarray = None):
        if slice is not None:
            self.lecturers[lecturer_id].availability_matrix[slice] = 1
        self.lecturers[lecturer_id].availability_matrix[start:stop, day] = 1

    def free_room_time(self, room_id: int, day: int = None, start: int = None, stop: int = None,
                          slice: np.ndarray = None):
        if slice is not None:
            self.rooms[room_id].availability_matrix[slice] = 1
        self.rooms[room_id].availability_matrix[start:stop, day] = 1


class ProcessImageManager:
    """Manages the access to the current Process Image and tries to prevent it's unintended modification."""

    def __init__(self):
        self._process_image = ProcessImage(
            distance_matrix=distance_matrix,
            courses=courses_factory(file_path="data/courses_data_term_5.json"),
            lecturers=lecturer_factory(file_path="data/lecturer_data_term_5.json"),
            rooms=room_factory(file_path="data/room_data_term_5.json"))

    @property
    def process_image(self) -> ProcessImage:
        return deepcopy(self._process_image)

    @process_image.setter
    def process_image(self, new_process_image: ProcessImage):
        self._process_image = new_process_image


# ProcessImageManager Singleton exportable to every other module
process_image_manager = ProcessImageManager()

if __name__ == '__main__':
    p_img = process_image_manager.process_image
    print(p_img.check_travel_time(55, 88, 10))

