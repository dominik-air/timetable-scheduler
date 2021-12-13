from dataclasses import dataclass
import json


@dataclass
class Course:
    id: int
    name: str
    room_id: int
    lecturer_id: int
    groups: tuple
    hours_weekly: float


def courses_factory(file_path: str):
    courses = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for course in data:
        courses[course["id"]] = Course(
            id=course["id"],
            name=course["name"],
            room_id=course["building_id"],
            lecturer_id=course["lecturer_id"],
            groups=course["group"],
            hours_weekly=course["hours_weekly"],
        )
    return courses


if __name__ == "__main__":
    print(courses_factory("courses_data.json"))
