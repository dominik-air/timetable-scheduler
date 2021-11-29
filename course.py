from dataclasses import dataclass
import json

@dataclass
class Course:
    id: int
    building: int
    lecturer_id: int
    group: int
    hours_weekly: float

def courses_factory(file_path: str):
    courses = []
    with open(file_path, 'r') as file:
        data = json.load(file)
    for course in data:
        courses.append(Course(course['id'], course['building'], course['lecturer_id'], course['group'], course['hours_weekly']))
    return courses
if __name__ == "__main__":
    print(courses_factory('courses_data.json'))