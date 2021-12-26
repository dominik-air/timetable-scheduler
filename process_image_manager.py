from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from course import courses_factory
from lecturer import lecturer_factory
from room import room_factory, distance_matrix
from copy import deepcopy


@dataclass
class ProcessImage:
    """The current state of objects a Solution is based on."""

    distance_matrix: np.ndarray
    courses: dict = field(default_factory=dict)
    lecturers: dict = field(default_factory=dict)
    rooms: dict = field(default_factory=dict)

    def __deepcopy__(self, memodict={}):
        courses = {course_id: deepcopy(course) for course_id, course in self.courses.items()}
        lecturers = {lecturer_id: deepcopy(lecturer) for lecturer_id, lecturer in self.lecturers.items()}
        rooms = {room_id: deepcopy(room) for room_id, room in self.rooms.items()}
        return ProcessImage(distance_matrix=self.distance_matrix, courses=courses, lecturers=lecturers, rooms=rooms)

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

        if time_period is None and (day is None or start is None or stop is None):
            raise ValueError('You need to provide a slice or the day, start and stop arguments!')

        if type(object_id) == int:
            objects = self.lecturers
        elif type(object_id) == str:
            objects = self.rooms
        else:
            raise NotImplementedError('Currently the process image does not include any '
                                      'other objects with availability matrices.')

        if time_period is not None:
            return np.all(objects[object_id].availability_matrix[time_period])
        return np.all(objects[object_id].availability_matrix[start:stop, day])

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

        if time_period is None and (day is None or start is None or stop is None):
            raise ValueError('You need to provide a slice or the day, start and stop arguments!')

        if type(object_id) == int:
            objects = self.lecturers
        elif type(object_id) == str:
            objects = self.rooms
        else:
            raise NotImplementedError('Currently the process image does not include any '
                                      'other objects with availability matrices.')
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
        if time_period is None and (day is None or start is None or stop is None):
            raise ValueError('You need to provide a slice or the day, start and stop arguments!')

        if type(object_id) == int:
            objects = self.lecturers
        elif type(object_id) == str:
            objects = self.rooms
        else:
            raise NotImplementedError('Currently the process image does not include any '
                                      'other objects with availability matrices.')
        if time_period is not None:
            objects[object_id].availability_matrix[time_period] = 1
        objects[object_id].availability_matrix[start:stop, day] = 1


class ProcessImageManager:
    """Manages the access to the canonical Process Image and tries to prevent it's unintended modification."""

    def __init__(self):
        self._process_image = ProcessImage(
            distance_matrix=distance_matrix,
            courses=courses_factory(file_path="data/courses_data.json"),
            lecturers=lecturer_factory(file_path="data/lecturer_data.json"),
            rooms=room_factory(file_path="data/room_data.json"))

    @property
    def process_image(self) -> ProcessImage:
        """Returns a deepcopy of the process image so the canonical one stays intact in case of an error."""
        return deepcopy(self._process_image)

    @process_image.setter
    def process_image(self, new_process_image: ProcessImage):
        """Overwrites the canonical process image with a new one."""
        self._process_image = new_process_image

    def reset_process_image(self):
        """Resets the process image to the initial values read from JSON files.
        It needs to be done for every new test case in order to work on untouched data structures.
        """

        self._process_image = ProcessImage(
            distance_matrix=distance_matrix,
            courses=courses_factory(file_path="data/courses_data.json"),
            lecturers=lecturer_factory(file_path="data/lecturer_data.json"),
            rooms=room_factory(file_path="data/room_data.json"))


# ProcessImageManager Singleton exportable to every other module
process_image_manager = ProcessImageManager()

if __name__ == '__main__':
    p_img = process_image_manager.process_image
    print(p_img.check_travel_time(55, 88, 0))

