import json
import pandas as pd
import numpy as np

# FIXME: the group map is supposed to be based on input data
group_map = {'wyklad': list(range(0, 10))}
j = 0
for i in range(5):
    group_map[i + 1] = [j, j + 1]
    j += 2
j = 0
for i in range(5):
    for subgroup in 'AB':
        group_map[f'{i + 1}{subgroup}'] = [j]
        j += 1

hours_per_term_to_per_week = {
    28: 1.5,
    14: 0.75,
    42: 2.25,
    56: 3,
    15: 0.75,
    45: 2.25,
    32: 1.5,
    30: 1.5,
    60: 3,
}


def create_dataset(term_id: int, lecturer_p: float, room_p: float):
    groups = list(range(1, 6))
    given_term_courses = []

    with open(f"timetable_scheduler/data_structures/data/schedule_{term_id}_json", "r") as file:
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
                        "hours_weekly": hours_per_term_to_per_week[given_term_course[course_type]],
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
                            "hours_weekly": hours_per_term_to_per_week[given_term_course[course_type]],
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
                                "hours_weekly": hours_per_term_to_per_week[given_term_course[course_type]],
                            }
                            courses.append(course)
                            i += 1
                            j += 1
                            if (j + 1) % 3 == 0:
                                lecturer_counter += 1
                    lecturer_counter += 1

    with open(f"timetable_scheduler/data_structures/data/courses_data.json", "w") as file:
        json.dump(courses, file, indent=4)

    def create_availability_matrix(n_rows: int = 144, chance: float = 0.5) -> list:
        matrix = np.ones((n_rows, 5), dtype='int')

        for day in range(matrix.shape[1]):
            hours = set(range(n_rows - 18))
            while True:
                if np.squeeze(np.random.choice([0, 1], 1, p=[1 - chance, chance])) or len(hours) == 0:
                    break
                where = np.squeeze(np.random.choice(np.array(list(hours)), 1))
                matrix[where:where + 18, day] = 0
                hours -= set(range(where - 18, where + 18))

        return matrix.tolist()

    # def create_availability_matrix(n_rows: int = 144) -> list:
    #     matrix = np.ones((n_rows, 5), dtype='int')
    #     return matrix.tolist()

    # creating lecturers data
    lecturer_data = []
    for lecturer_id in range(lecturer_counter):
        lecturer_json = {"id": lecturer_id,
                         "availability_matrix": create_availability_matrix(chance=lecturer_p)}
        lecturer_data.append(lecturer_json)

    with open(f"timetable_scheduler/data_structures/data/lecturer_data.json", "w") as file:
        json.dump(lecturer_data, file, indent=4)

    # creating room data
    courses_df = pd.DataFrame(courses)
    rooms = courses_df["room"].unique()

    available_buildings = []
    for room_name in rooms:
        building, *_ = room_name.split('-')
        if building not in available_buildings:
            available_buildings.append(building)

    # distance matrix
    df = pd.read_csv('timetable_scheduler/data_structures/data/distances.csv', delimiter=';')
    df.drop(df.columns[0], axis=1, inplace=True)
    distance_matrix = df.to_numpy().tolist()
    unique_buildings = df.columns

    room_data = []
    for room_name in rooms:
        for building_id, building in enumerate(unique_buildings):
            room_building, *_ = room_name.split('-')
            if building == room_building:
                room_json = {"id": room_name,
                             "building_id": building_id,
                             "availability_matrix": create_availability_matrix(chance=room_p)
                             }
                room_data.append(room_json)
                break

    with open(f"timetable_scheduler/data_structures/data/room_data.json", "w") as file:
        json.dump(room_data, file, indent=4)

    #  miscellaneous data
    distance_matrix = np.array(distance_matrix)
    available_buildings_ids = np.squeeze(np.argwhere(np.isin(unique_buildings.to_numpy(), available_buildings))).tolist()
    temp = distance_matrix[available_buildings_ids, :]
    minimal_break_time = np.max(temp[:, available_buildings_ids])
    # round it up to the nearest multiple of 5
    minimal_break_time = int(np.ceil(minimal_break_time / 5) * 5)

    misc_data = {
        'distance_matrix': distance_matrix.tolist(),
        'minimal_break_time': minimal_break_time
    }

    with open(f"timetable_scheduler/data_structures/data/misc_data.json", "w") as file:
        json.dump(misc_data, file, indent=4)
