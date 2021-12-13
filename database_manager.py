import numpy as np
from dataclasses import dataclass, field
from course import courses_factory, Course
from lecturer import lecturer_factory, Lecturer
from room import room_factory, Room


@dataclass
class DatabaseManager:
    courses: dict = field(default_factory=dict)
    lecturers: dict = field(default_factory=dict)
    rooms: dict = field(default_factory=dict)

    def get_lecturer_by_id(self, lecturer_id: int) -> Lecturer:
        return self.lecturers[lecturer_id]

    def get_course_by_id(self, course_id: int) -> Course:
        return self.courses[course_id]

    def get_room_by_id(self, room_id: int) -> Room:
        return self.rooms[room_id]


# DatabaseManager Singleton exportable to every other module
DBManager = DatabaseManager(
    courses=courses_factory(file_path="courses_data_term_5.json"),
    lecturers=lecturer_factory(file_path="lecturer_data_term_5.json"),
    rooms=room_factory(file_path="room_data_term_5.json"),
)


if __name__ == '__main__':
    lecturer = DBManager.get_lecturer_by_id(lecturer_id=1)
    lecturer.availability_matrix = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
