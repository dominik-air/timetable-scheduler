import numpy as np
from typing import Tuple
from process_image_manager import process_image_manager, ProcessImage
from copy import deepcopy

matrix_operator = callable


def get_group_slice_for_course(matrix: np.ndarray) -> np.ndarray:
    for group in range(10):
        if np.any(matrix[:, :, group]):
            return matrix[:, :, group].T


def matrix_transposition(matrix: np.ndarray) -> Tuple[np.ndarray, ProcessImage]:
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

    while True:
        courses = np.random.choice(np.array([auditoriums, labs], dtype='object'), p=[0.3, 0.7])

        course_A = np.random.choice(courses, size=1)[0]
        current_place_A = matrix == course_A.id
        slice_A = get_group_slice_for_course(current_place_A)
        courses.remove(course_A)

        swap_candidates = [course for course in courses if course.group == course_A.group]
        for course_B in np.random.permutation(swap_candidates):

            current_place_B = matrix == course_B.id
            slice_B = get_group_slice_for_course(current_place_B)

            if np.sum(slice_A) != np.sum(slice_B):
                continue

            process_image.free_room_time(room_id=course_A.room_id, slice=slice_A)
            process_image.free_room_time(room_id=course_B.room_id, slice=slice_B)
            process_image.free_lecturer_time(lecturer_id=course_A.lecturer_id, slice=slice_A)
            process_image.free_lecturer_time(lecturer_id=course_B.lecturer_id, slice=slice_B)

            if process_image.check_room_availability(room_id=course_A.room_id, slice=slice_B) and \
                    process_image.check_room_availability(room_id=course_B.room_id, slice=slice_A) and \
                    process_image.check_lecturer_availability(lecturer_id=course_A.lecturer_id, slice=slice_B) and \
                    process_image.check_lecturer_availability(lecturer_id=course_B.lecturer_id, slice=slice_A):

                matrix[current_place_A] = course_B.id
                matrix[current_place_B] = course_A.id
                process_image.reserve_room_time(room_id=course_A.room_id, slice=slice_B)
                process_image.reserve_room_time(room_id=course_B.room_id, slice=slice_A)
                process_image.reserve_lecturer_time(lecturer_id=course_A.lecturer_id, slice=slice_B)
                process_image.reserve_lecturer_time(lecturer_id=course_B.lecturer_id, slice=slice_A)

                return matrix, process_image
            else:
                process_image = process_image_manager.process_image


