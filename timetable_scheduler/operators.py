from __future__ import annotations

import numpy as np
from copy import deepcopy
from .data_structures import process_image_manager, ProcessImage, group_map


def get_time_period_for_course(matrix: np.ndarray) -> np.ndarray:
    """Slices solution matrix into a availability_matrix shape used by Lecturer and Room objects.

    Args:
        matrix: current solution matrix (of shape 5x144x10)

    Returns:

    """
    number_of_groups = matrix.shape[2]
    for group in range(number_of_groups):
        if np.any(matrix[:, :, group]):
            return matrix[:, :, group].T


def matrix_transposition(matrix: np.ndarray) -> tuple[np.ndarray, ProcessImage]:
    """Swaps two random courses of the same type with each other.

    Args:
        matrix: current solution matrix.

    Returns:
        New solution matrix and process image after changes made by the operator.

    """
    process_image = process_image_manager.process_image
    matrix = deepcopy(matrix)

    auditoriums = []
    labs = []
    for course in process_image.courses.values():
        if 'wyklad' in course.name:
            continue
        elif 'laboratoryjne' in course.name:
            labs.append(course)
        else:
            auditoriums.append(course)

    if auditoriums and labs:
        courses = np.random.choice(np.array([auditoriums, labs], dtype='object'), p=[0.3, 0.7])
    elif labs:
        courses = labs
    elif auditoriums:
        courses = auditoriums
    else:
        raise ValueError('No courses to swap!')

    while True:

        course_A = np.random.choice(courses, size=1)[0]
        current_place_A = matrix == course_A.id
        time_period_A = get_time_period_for_course(current_place_A)
        courses.remove(course_A)

        if not courses:
            # if we run out of courses we just return the input solution matrix and process image
            return matrix, process_image_manager.process_image

        swap_candidates = [course for course in courses if course.group == course_A.group]
        for course_B in np.random.permutation(swap_candidates):

            current_place_B = matrix == course_B.id
            time_period_B = get_time_period_for_course(current_place_B)

            if np.sum(time_period_A) != np.sum(time_period_B):
                # we can only swap courses of the same length(as for now)
                continue

            # make copies for possible backup restoration
            room_A_old_availability_matrix = process_image.rooms[course_A.room_id].availability_matrix_copy
            lecturer_A_old_availability_matrix = process_image.lecturers[course_A.lecturer_id].availability_matrix_copy
            room_B_old_availability_matrix = process_image.rooms[course_B.room_id].availability_matrix_copy
            lecturer_B_old_availability_matrix = process_image.lecturers[course_B.lecturer_id].availability_matrix_copy

            # without time freeing operations the availability check would always fail
            # course A would block course B and vice versa

            # frees time in the rooms' availability matrices
            process_image.free_time(object_id=course_A.room_id, time_period=time_period_A)
            process_image.free_time(object_id=course_B.room_id, time_period=time_period_B)
            # frees time in the lecturer's availability matrices
            process_image.free_time(object_id=course_A.lecturer_id, time_period=time_period_A)
            process_image.free_time(object_id=course_B.lecturer_id, time_period=time_period_B)

            if process_image.check_availability(object_id=course_A.room_id, time_period=time_period_B) and \
                    process_image.check_availability(object_id=course_B.room_id, time_period=time_period_A) and \
                    process_image.check_availability(object_id=course_A.lecturer_id, time_period=time_period_B) and \
                    process_image.check_availability(object_id=course_B.lecturer_id, time_period=time_period_A):

                # swap we two courses in the timetable matrix
                matrix[current_place_A] = course_B.id
                matrix[current_place_B] = course_A.id

                # reserve time in the rooms' availability matrices
                process_image.reserve_time(object_id=course_A.room_id, time_period=time_period_B)
                process_image.reserve_time(object_id=course_B.room_id, time_period=time_period_A)
                # frees time in the lecturer's availability matrices
                process_image.reserve_time(object_id=course_A.lecturer_id, time_period=time_period_B)
                process_image.reserve_time(object_id=course_B.lecturer_id, time_period=time_period_A)

                return matrix, process_image
            else:
                # we need to revert changes made by freeing space in availability matrices
                process_image.rooms[course_A.room_id].availability_matrix = room_A_old_availability_matrix
                process_image.lecturers[course_A.lecturer_id].availability_matrix = lecturer_A_old_availability_matrix
                process_image.rooms[course_B.room_id].availability_matrix = room_B_old_availability_matrix
                process_image.lecturers[course_B.lecturer_id].availability_matrix = lecturer_B_old_availability_matrix


def matrix_inner_translation(matrix: np.ndarray) -> tuple[np.ndarray, ProcessImage]:
    """Moves a given course up or down the timetable's timeline in hope of finding an acceptable solution.

    Args:
        matrix: current solution matrix.

    Returns:
        New solution matrix and process image after changes made by the operator.

    """
    process_image = process_image_manager.process_image
    matrix = deepcopy(matrix)

    while True:
        course = np.random.choice(list(process_image.courses.values()), size=1)[0]
        current_place = matrix == course.id
        time_period = get_time_period_for_course(matrix=current_place)

        # algorithm tries to move a course up or down the timetable 'i' timestamps
        # it starts arbitrarily from 10 for the biggest impact on the cost function
        max_move_size = 10
        for i in reversed(range(1, max_move_size)):
            for j in [1, -1]:
                current_place_shifted = np.roll(current_place, j * i, axis=1)
                time_period_shifted = np.roll(time_period, j * i, axis=0)

                # make copies for possible backup restoration
                room_old_availability_matrix = process_image.rooms[course.room_id].availability_matrix_copy
                lecturer_old_availability_matrix = process_image.lecturers[course.lecturer_id].availability_matrix_copy

                process_image.free_time(object_id=course.room_id, time_period=time_period)
                process_image.free_time(object_id=course.lecturer_id, time_period=time_period)

                if np.all(np.logical_or(matrix[current_place_shifted] == 0,
                                        matrix[current_place_shifted] == course.id)) and \
                        process_image.check_availability(object_id=course.room_id, time_period=time_period_shifted) and \
                        process_image.check_availability(object_id=course.lecturer_id, time_period=time_period_shifted):

                    matrix[current_place] = 0
                    matrix[current_place_shifted] = course.id
                    process_image.reserve_time(object_id=course.room_id, time_period=time_period_shifted)
                    process_image.reserve_time(object_id=course.lecturer_id, time_period=time_period_shifted)
                    return matrix, process_image
                else:
                    # we need to revert changes made by freeing space in availability matrices
                    process_image.rooms[course.room_id].availability_matrix = room_old_availability_matrix
                    process_image.lecturers[course.lecturer_id].availability_matrix = lecturer_old_availability_matrix


def matrix_cut_and_paste_translation(matrix: np.ndarray) -> tuple[np.ndarray, ProcessImage]:
    """Cuts and pastes a course into a free space in the timetable.

    Args:
        matrix: current solution matrix.

    Returns:
        New solution matrix and process image after changes made by the operator.

    """
    process_image = process_image_manager.process_image
    matrix = deepcopy(matrix)

    while True:
        course = np.random.choice(list(process_image.courses.values()), size=1)[0]
        current_place = matrix == course.id
        time_period = get_time_period_for_course(matrix=current_place)
        course_length = int(course.hours_weekly * (60 / 5))  # 60 minutes / 5 minutes = 12 timestamps per hour
        group = group_map[course.group]

        number_of_days = matrix.shape[0]
        number_of_timestamps = matrix.shape[1]
        for day in np.random.choice(list(range(number_of_days)), size=5):
            for timestamp in range(number_of_timestamps):
                if np.all(matrix[day, timestamp:timestamp + course_length, group] == 0) and \
                        process_image.check_availability(object_id=course.room_id, start=timestamp,
                                                         stop=timestamp + course_length, day=day) and \
                        process_image.check_availability(object_id=course.lecturer_id,
                                                         start=timestamp, stop=timestamp + course_length, day=day):

                    process_image.free_time(object_id=course.room_id, time_period=time_period)
                    process_image.free_time(object_id=course.lecturer_id, time_period=time_period)
                    process_image.reserve_time(object_id=course.room_id, start=timestamp,
                                               stop=timestamp + course_length, day=day)
                    process_image.reserve_time(object_id=course.lecturer_id, start=timestamp,
                                               stop=timestamp + course_length, day=day)

                    matrix[day, timestamp:timestamp + course_length, group] = course.id
                    matrix[current_place] = 0
                    return matrix, process_image
