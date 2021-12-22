import json
import pandas as pd
import numpy as np

np.random.seed(0)

term_id = 5
groups = list(range(1, 6))
given_term_courses = []

with open("schedule_5_json", "r") as file:
    data = json.load(file)
    for id, course_data in data.items():
        if course_data["semestr"] == term_id:
            given_term_courses.append(course_data)

# course data mining
courses = []
course_type_keys = ["wyklad", "audytoryjne", "laboratoryjne"]
i = 1
lecturer_counter = 0
# rules
# jest wyklad -> 1 wykladowca
# sa audytoryjne -> 2-4 prow na audy
# sa laby -> 2-4 prow na laby

for given_term_course in given_term_courses:
    for course_type in course_type_keys:
        if given_term_course[course_type] != 0:
            if course_type == "wyklad":
                course = {
                    "id": i,
                    "name": f"{given_term_course['nazwa']} wyklad",
                    "room": given_term_course["sala_wyk"],
                    "lecturer_id": lecturer_counter,
                    "group": "wyklad",
                    "hours_weekly": round(given_term_course[course_type] / 19, 1),
                }
                courses.append(course)
                i += 1
                lecturer_counter += 1
            elif course_type == "audytoryjne":
                for j, group in enumerate(groups):
                    course = {
                        "id": i,
                        "name": f"{given_term_course['nazwa']} {course_type} {group}",
                        "room": given_term_course["sala_aud"],
                        "lecturer_id": lecturer_counter,
                        "group": group,
                        "hours_weekly": round(given_term_course[course_type] / 19, 1),
                    }
                    courses.append(course)
                    i += 1
                    if (j + 1) % 3 == 0:
                        lecturer_counter += 1
                lecturer_counter += 1
            else:
                j = 0
                for group in groups:
                    for subgroup in "AB":
                        course = {
                            "id": i,
                            "name": f"{given_term_course['nazwa']} {course_type} {group}{subgroup}",
                            "room": given_term_course["sala_lab"],
                            "lecturer_id": lecturer_counter,
                            "group": str(group) + subgroup,
                            "hours_weekly": round(
                                given_term_course[course_type] / 19, 1
                            ),
                        }
                        courses.append(course)
                        i += 1
                        j += 1
                        if (j + 1) % 3 == 0:
                            lecturer_counter += 1
                lecturer_counter += 1

with open("courses_data_term_5.json", "w") as file:
    json.dump(courses, file, indent=4)


# def create_availability_matrix(n_rows: int = 144, chance: 0.05) -> list:
#     n_days = np.random.randint(1, 5, size=1)
#     reserved_days = np.random.choice(5, n_days)
#     matrix = np.ones((n_rows, 5), dtype='int')
#     for day in reserved_days:
#         matrix[:round(n_rows / 2), day] = 0
#     return matrix.tolist()

def create_availability_matrix(n_rows: int = 144) -> list:
    matrix = np.ones((n_rows, 5), dtype='int')
    return matrix.tolist()


# creating lecturers data
lecturer_data = []
for lecturer_id in range(lecturer_counter):
    lecturer_json = {"id": lecturer_id,
                     "availability_matrix": create_availability_matrix()}
    lecturer_data.append(lecturer_json)

with open("lecturer_data_term_5.json", "w") as file:
    json.dump(lecturer_data, file, indent=4)

# creating room data
courses_df = pd.DataFrame(courses)
rooms = courses_df["room"].unique()

available_buildings = []
for room_name in rooms:
    building, *_ = room_name.split('-')
    available_buildings.append(building)

unique_buildings = sorted(list(set(available_buildings)))

# distance matrix
# TODO: pseudorandom algorithm is needed for improved scalability
distance_matrix = [
    [0, 8, 6, 5, 3],
    [8, 0, 11, 10, 8],
    [6, 11, 0, 1, 7],
    [5, 10, 1, 0, 8],
    [3, 8, 7, 8, 0],
]

room_data = []
for room_name in rooms:
    for building_id, building in enumerate(unique_buildings):
        if building in room_name:
            room_json = {"id": room_name,
                         "building_id": building_id,
                         "distance_matrix": distance_matrix,
                         "availability_matrix": create_availability_matrix()
                         }
            room_data.append(room_json)

with open("room_data_term_5.json", "w") as file:
    json.dump(room_data, file, indent=4)
