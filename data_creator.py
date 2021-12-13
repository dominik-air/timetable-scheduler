import json

term_id = 1
groups = list(range(1, 6))
available_buildings = ['B1', 'B5', 'C2', 'C3', 'D2']
given_term_courses = []

with open('schedule_json', 'r') as file:
    data = json.load(file)
    for id, course_data in data.items():
        if course_data['semestr'] == term_id:
            given_term_courses.append(course_data)

courses = []
course_type_keys = ['wyklad', 'audytoryjne', 'laboratoryjne']
i = 1

for given_term_course in given_term_courses:
    for course_type in course_type_keys:
        if given_term_course[course_type] != 0:
            if course_type == 'wyklad':
                course = {'id': i,
                          'name': f"{given_term_course['nazwa']} wyklad",
                          'building_id': i % 5 + 1,
                          'lecturer_id': i % 10 + 1,
                          'group': 'wyklad',
                          'hours_weekly': round(given_term_course[course_type] / 19, 1)}
                courses.append(course)
                i += 1
            elif course_type == 'audytoryjne':
                for group in groups:
                    course = {'id': i,
                              'name': f"{given_term_course['nazwa']} {course_type} {group}",
                              'building_id': i % 5 + 1,
                              'lecturer_id': i % 10 + 1,
                              'group': group,
                              'hours_weekly': round(given_term_course[course_type] / 19, 1)}
                    courses.append(course)
                    i += 1
            else:
                for group in groups:
                    for subgroup in 'AB':
                        course = {'id': i,
                                  'name': f"{given_term_course['nazwa']} {course_type} {group}{subgroup}",
                                  'building_id': i % 5 + 1,
                                  'lecturer_id': i % 10 + 1,
                                  'group': str(group)+subgroup,
                                  'hours_weekly': round(given_term_course[course_type] / 19, 1)}
                        courses.append(course)
                        i += 1

with open('testowe_dane_przedmiotow.json', 'w') as file:
    json.dump(courses, file, indent=4)
