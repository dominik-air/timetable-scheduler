from dataclasses import dataclass
import json


@dataclass
class Course:
    id: int
    name: str
    room_id: str
    lecturer_id: int
    group: str
    hours_weekly: float

    def __deepcopy__(self, memodict={}):
        return self


def courses_factory(file_path: str):
    courses = {}
    with open(file_path, "r") as file:
        data = json.load(file)
    for course in data:
        courses[course["id"]] = Course(
            id=course["id"],
            name=course["name"],
            room_id=course["room"],
            lecturer_id=course["lecturer_id"],
            group=course["group"],
            hours_weekly=course["hours_weekly"],
        )
    return courses


if __name__ == "__main__":
    print(courses_factory("data/courses_data.json"))
