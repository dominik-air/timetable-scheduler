import json

groups = list(range(1, 6))
zajecia_5_semestr = []

with open('schedule_json', 'r') as file:
    data = json.load(file)
    for id, course_data in data.items():
        if course_data['semestr'] == 1:
            zajecia_5_semestr.append(course_data)

courses = []
course_type_keys = ['wyklad', 'audytoryjne', 'laboratoryjne']
i = 1

for zajecia in zajecia_5_semestr:
    for course_type in course_type_keys:
        if zajecia[course_type] != 0:
            if course_type == 'wyklad':
                course = {'id': i,
                          'name': f"{zajecia['nazwa']} wyklad",
                          'building_id': i % 5 + 1,
                          'lecturer_id': i % 10 + 1,
                          'group': 'wyklad',
                          'hours_weekly': round(zajecia[course_type] / 19, 1)}
                courses.append(course)
                i += 1
            elif course_type == 'audytoryjne':
                for group in groups:
                    course = {'id': i,
                              'name': f"{zajecia['nazwa']} {course_type} {group}",
                              'building_id': i % 5 + 1,
                              'lecturer_id': i % 10 + 1,
                              'group': group,
                              'hours_weekly': round(zajecia[course_type] / 19, 1)}
                    courses.append(course)
                    i += 1
            else:
                for group in groups:
                    for subgroup in 'AB':
                        course = {'id': i,
                                  'name': f"{zajecia['nazwa']} {course_type} {group}{subgroup}",
                                  'building_id': i % 5 + 1,
                                  'lecturer_id': i % 10 + 1,
                                  'group': str(group)+subgroup,
                                  'hours_weekly': round(zajecia[course_type] / 19, 1)}
                        courses.append(course)
                        i += 1

with open('testowe_dane_przedmiotow.json', 'w') as file:
    json.dump(courses, file, indent=4)
