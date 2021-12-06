from dataclasses import dataclass, field
from course import courses_factory
from lecturer import lecturer_factory
from building import building_factory


@dataclass
class DatabaseManager:
    courses: dict = field(default_factory=dict)
    lecturers: dict = field(default_factory=dict)
    buildings: dict = field(default_factory=dict)


# DatabaseManager Singleton exportable to every other module
DBManager = DatabaseManager(
    courses=courses_factory(file_path="courses_data.json"),
    lecturers=lecturer_factory(file_path="lecturers_data.json"),
    buildings=building_factory(file_path="buildings_data.json"),
)
