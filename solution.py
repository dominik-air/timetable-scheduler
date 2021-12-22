from __future__ import annotations

import numpy as np
import operators
from process_image_manager import process_image_manager
from cost_functions import unbalanced_function, gaps_c_function, lecturer_work_time
from data_creator import group_map


class Solution:
    def __init__(self, matrix: np.ndarray = None):
        if matrix is not None:
            self.matrix: np.ndarray = matrix
        else:
            process_image = process_image_manager.process_image
            matrix = np.zeros((5, 144, 10), dtype='int')

            lectures = []
            auditoriums = []
            labs = []
            for course in process_image.courses.values():
                if 'wyklad' in course.name:
                    lectures.append(course)
                elif 'laboratoryjne' in course.name:
                    labs.append(course)
                else:
                    auditoriums.append(course)
            courses = np.concatenate((np.random.permutation(lectures),
                                      np.random.permutation(auditoriums),
                                      np.random.permutation(labs)))
            for i, course in enumerate(courses):
                length = int(course.hours_weekly * (60 / 5))
                inserted = False

                while not inserted:
                    day = i % 5
                    for j in range(matrix.shape[1]):

                        if j + length + 1 > matrix.shape[1]:
                            # FIXME: to może być problematyczne
                            i += 1
                            if i > 200:
                                raise ValueError("Infinite loop")
                            break
                        # max(0, j-3) myk do robienia przerwy 15 minut
                        if np.all(matrix[day, max(0, j-3):j + length, group_map[course.group]] == 0) and \
                                process_image.check_lecturer_availability(course.lecturer_id, day, max(0, j-3),
                                                                          j + length) and \
                                process_image.check_room_availability(course.room_id, day, max(0, j-3), j + length):
                            matrix[day, j:j + length, group_map[course.group]] = course.id
                            process_image.reserve_lecturer_time(course.lecturer_id, day, j, j + length)
                            process_image.reserve_room_time(course.room_id, day, j, j + length)
                            inserted = True
                            break
            self.matrix = matrix
            # comment the line below for initial solution statistics tests(the image process can't be overwritten
            # since it would block the creation of other initial solutions)
            process_image_manager.process_image = process_image

    @property
    def cost(self) -> float:
        """Returns the combined cost for the current solution matrix."""
        return gaps_c_function(self.matrix, 1) + unbalanced_function(self.matrix, 1) + lecturer_work_time(20.0)

    def check_acceptability(self) -> bool:
        """Checks if the solution is acceptable."""
        # check the number of hours per week
        for course in process_image_manager.process_image.courses.values():
            expected = int(course.hours_weekly * (60/5) * len(group_map[course.group]))
            actual = (self.matrix == course.id).sum()
            if expected != actual:
                return False
        # check travel times
        for day in range(self.matrix.shape[0]):
            for group in range(self.matrix.shape[2]):
                current_course_id = None
                window_length = 0
                for timestamp in range(self.matrix.shape[1]):
                    if current_course_id is None and self.matrix[day, timestamp, group] != 0:
                        current_course_id = self.matrix[day, timestamp, group]
                    elif self.matrix[day, timestamp, group] == 0 and current_course_id is not None:
                        window_length += 1
                    elif self.matrix[day, timestamp, group] != current_course_id and current_course_id is not None:
                        if not process_image_manager.process_image.check_travel_time(course_A_id=current_course_id,
                                                                                     course_B_id=self.matrix[day, timestamp, group],
                                                                                     current_time=window_length*5):
                            return False
                        current_course_id = self.matrix[day, timestamp, group]
                        window_length = 0
        return True

    def from_neighbourhood(self, iter_limit: int = 5) -> Solution:
        """Create new Solution from a Solution's neighbourhood. A neighbourhood is defined as Solutions
        different by one operation from the origin."""
        while i := 0 < iter_limit:
            matrix_operator = np.random.choice([operators.matrix_transposition,
                                                operators.matrix_inner_translation,
                                                operators.matrix_cut_and_paste_translation],
                                               p=[0.1, 0.1, 0.8])
            new_solution_matrix, new_process_image = matrix_operator(self.matrix)
            new_solution = Solution(new_solution_matrix)
            if new_solution.check_acceptability():
                process_image_manager.process_image = new_process_image
                return new_solution
            i += 1
        raise ValueError('Iteration limit exceeded!')


if __name__ == '__main__':
    np.random.seed(10)
    solution = Solution()
    solution.from_neighbourhood()
    solution.check_acceptability()
