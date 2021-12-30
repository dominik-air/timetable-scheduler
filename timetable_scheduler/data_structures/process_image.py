from __future__ import annotations

import json

import numpy as np
from copy import deepcopy, copy
from dataclasses import dataclass, field
from .course import courses_factory
from .lecturer import lecturer_factory
from .room import room_factory

# paths accessible from the top project layer
ROOMS_DATA_PATH = "timetable_scheduler/data_structures/data/room_data.json"
COURSES_DATA_PATH = "timetable_scheduler/data_structures/data/courses_data.json"
LECTURERS_DATA_PATH = "timetable_scheduler/data_structures/data/lecturer_data.json"


@dataclass
class ProcessImage:
    """The current state of objects a Solution is based on."""

    distance_matrix: np.ndarray
    minimal_break_time: int
    courses: dict = field(default_factory=dict)
    lecturers: dict = field(default_factory=dict)
    rooms: dict = field(default_factory=dict)

    def __deepcopy__(self, memodict={}):
        courses = {course_id: deepcopy(course) for course_id, course in self.courses.items()}
        lecturers = {lecturer_id: deepcopy(lecturer) for lecturer_id, lecturer in self.lecturers.items()}
        rooms = {room_id: deepcopy(room) for room_id, room in self.rooms.items()}
        return ProcessImage(distance_matrix=self.distance_matrix, minimal_break_time=self.minimal_break_time,
                            courses=courses, lecturers=lecturers, rooms=rooms)

    def check_availability(self, object_id: int | str, day: int = None, start: int = None, stop: int = None,
                           time_period: np.ndarray = None) -> bool:
        """
        Checks the availability of a Lecturer or a Room in a given period of time. The period of time can be
        represented by a boolean array of an availability matrix(a number_of_timestamps x number_of_days shaped matrix)
        or by inputting the day and start and stop timestamps.

        Args:
            object_id: id of the object which availability_matrix is checked. The type of object_id
                       determines if we check a lecturer (id of type int) or a room (id of type str).
            day: the day (column) of the availability matrix.
            start: the starting timestamp (first row) of the availability matrix.
            stop: the ending timestamp (last row) of the availability matrix.
            time_period: segment of the availability matrix we're interested in.

        Returns:
            True if the whole period of time is available and False otherwise.

        """

        objects = self._contextualize_input_arguments(object_id, day, start, stop, time_period)

        if time_period is not None:
            return np.all(objects[object_id].availability_matrix[time_period])
        return np.all(objects[object_id].availability_matrix[start:stop, day])

    def reserve_time(self, object_id: int | str, day: int = None, start: int = None, stop: int = None,
                     time_period: np.ndarray = None):
        """
        Reserves time in an object's availability matrix by setting all 1s to 0s in a given time period.
        The period of time can be represented by a boolean array of an availability matrix(a number_of_timestamps
        x number_of_days shaped matrix) or by inputting the day and start and stop timestamps.

        Args:
            object_id: id of the object which availability_matrix is checked. The type of object_id
                       determines if we check a lecturer (id of type int) or a room (id of type str).
            day: the day (column) of the availability matrix.
            start: the starting timestamp (first row) of the availability matrix.
            stop: the ending timestamp (last row) of the availability matrix.
            time_period: segment of the availability matrix we're interested in.

        """

        objects = self._contextualize_input_arguments(object_id, day, start, stop, time_period)

        if time_period is not None:
            objects[object_id].availability_matrix[time_period] = 0
        objects[object_id].availability_matrix[start:stop, day] = 0

    def free_time(self, object_id: int | str, day: int = None, start: int = None, stop: int = None,
                  time_period: np.ndarray = None):
        """
        Frees time in an object's availability matrix by setting all 0s to 1s in a given time period.
        The period of time can be represented by a boolean array of an availability matrix(a number_of_timestamps
        x number_of_days shaped matrix) or by inputting the day and start and stop timestamps.

        Args:
            object_id: id of the object which availability_matrix is checked. The type of object_id
                       determines if we check a lecturer (id of type int) or a room (id of type str).
            day: the day (column) of the availability matrix.
            start: the starting timestamp (first row) of the availability matrix.
            stop: the ending timestamp (last row) of the availability matrix.
            time_period: segment of the availability matrix we're interested in.

        """

        objects = self._contextualize_input_arguments(object_id, day, start, stop, time_period)

        if time_period is not None:
            objects[object_id].availability_matrix[time_period] = 1
        objects[object_id].availability_matrix[start:stop, day] = 1

    def check_travel_time(self, course_A_id: int, course_B_id: int, current_time: int):
        """Checks if travel time between two courses is sufficient.

        Args:
            course_A_id: id of the course students travel from to course_B.
            course_B_id: id of the course students travel to from course_A.
            current_time: break between classes in the timetable.

        Returns:
            True if the break is at least as long as the expected travel time in the distance matrix.
            Otherwise it returns False.

        """

        start_building = self.rooms[self.courses[course_A_id].room_id].building_id
        destination_building = self.rooms[self.courses[course_B_id].room_id].building_id
        min_time = self.distance_matrix[start_building, destination_building]
        return current_time >= min_time

    def _contextualize_input_arguments(self, object_id: int | str, day: int = None, start: int = None, stop: int = None,
                                       time_period: np.ndarray = None) -> dict:
        """Validates the input data and returns objects with respect to the object_id type.

        Args:
            object_id: id of the object which availability_matrix is checked. The type of object_id
                       determines if we check a lecturer (id of type int) or a room (id of type str).
            day: the day (column) of the availability matrix.
            start: the starting timestamp (first row) of the availability matrix.
            stop: the ending timestamp (last row) of the availability matrix.
            time_period: segment of the availability matrix we're interested in.

        """
        if time_period is None and (day is None or start is None or stop is None):
            raise ValueError('You need to provide a slice or the day, start and stop arguments!')

        if type(object_id) == int:
            return self.lecturers
        elif type(object_id) == str:
            return self.rooms
        else:
            raise NotImplementedError('Currently the process image does not include any '
                                      'other objects with availability matrices.')


class ProcessImageManager:
    """Manages the access to the canonical Process Image and tries to prevent its unintended modification."""

    def __init__(self):

        with open("timetable_scheduler/data_structures/data/misc_data.json", "r") as file:
            data = json.load(file)
            distance_matrix = np.array(data['distance_matrix'])
            minimal_break_time = data['minimal_break_time']

        self._process_image = ProcessImage(
            distance_matrix=distance_matrix,
            minimal_break_time=minimal_break_time,
            courses=courses_factory(file_path=COURSES_DATA_PATH),
            lecturers=lecturer_factory(file_path=LECTURERS_DATA_PATH),
            rooms=room_factory(file_path=ROOMS_DATA_PATH))

    @property
    def process_image(self) -> ProcessImage:
        """Returns a deepcopy of the process image so the canonical one stays intact in case of an error."""
        return deepcopy(self._process_image)

    @property
    def process_image_read_only(self) -> ProcessImage:
        """Returns a shallow copy to use when we're only reading from the process image."""
        return copy(self._process_image)

    @process_image.setter
    def process_image(self, new_process_image: ProcessImage):
        """Overwrites the canonical process image with a new one."""
        self._process_image = new_process_image

    def reset_process_image(self):
        """Resets the process image to the initial values read from JSON files.
        It needs to be done for every new test case in order to work on untouched data structures.
        """

        with open("timetable_scheduler/data_structures/data/misc_data.json", "r") as file:
            data = json.load(file)
            distance_matrix = np.array(data['distance_matrix'])
            minimal_break_time = data['minimal_break_time']

        self._process_image = ProcessImage(
            distance_matrix=distance_matrix,
            minimal_break_time=minimal_break_time,
            courses=courses_factory(file_path=COURSES_DATA_PATH),
            lecturers=lecturer_factory(file_path=LECTURERS_DATA_PATH),
            rooms=room_factory(file_path=ROOMS_DATA_PATH))


# ProcessImageManager Singleton exportable to every other module
process_image_manager = ProcessImageManager()

if __name__ == '__main__':
    p_img = process_image_manager.process_image
    print(p_img.check_travel_time(course_A_id=55, course_B_id=88, current_time=0))
