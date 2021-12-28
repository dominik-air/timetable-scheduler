from __future__ import annotations

import numpy as np
import operators
from data_structures import process_image_manager, group_map
from cost_functions import unbalanced_function, gaps_c_function, lecturer_work_time, late_lectures_cost_function


class Solution:
    """Represents """
    def __init__(self,
                 matrix: np.ndarray = None,
                 cost_functions: list[callable] = None,
                 weights: list[float] = None,
                 operator_probabilities: list[float] = None):

        if cost_functions is None:
            cost_functions = [unbalanced_function,
                              gaps_c_function,
                              lecturer_work_time,
                              late_lectures_cost_function]
        self.cost_functions = cost_functions

        if weights is None:
            weights = [1.0, 1.0, 20.0, 5.0]
        self.weights = weights

        if operator_probabilities is None:
            operator_probabilities = [0.1, 0.1, 0.8]
        self.operator_probabilities = operator_probabilities

        if matrix is not None:
            self.matrix: np.ndarray = matrix
        else:
            # initial solution construction algorithm
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
                recursive_return = False

                while not inserted:
                    day = i % 5
                    for j in range(matrix.shape[1]):

                        if j + length + 1 > matrix.shape[1]:
                            i += 1
                            if i > 2 * len(courses):
                                # evil python hacking
                                # in case that the algorithm gets stuck it recursively starts again from the start
                                matrix = Solution().matrix
                                inserted = True
                                recursive_return = True
                            break
                        # max(0, j-3) myk do robienia przerwy 15 minut
                        if np.all(matrix[day, max(0, j - 3):j + length, group_map[course.group]] == 0) and \
                                process_image.check_availability(course.lecturer_id, day, max(0, j - 3),
                                                                 j + length) and \
                                process_image.check_availability(course.room_id, day, max(0, j - 3), j + length):
                            matrix[day, j:j + length, group_map[course.group]] = course.id
                            process_image.reserve_time(course.lecturer_id, day, j, j + length)
                            process_image.reserve_time(course.room_id, day, j, j + length)
                            inserted = True
                            break
                if recursive_return:
                    break
            self.matrix = matrix
            process_image_manager.process_image = process_image

    @property
    def cost(self) -> float:
        """Returns the combined cost for the current solution matrix."""
        return sum([cost_function(self.matrix, w) for cost_function, w in zip(self.cost_functions, self.weights)])

    def check_acceptability(self) -> bool:
        """Returns True if the solution is acceptable, False otherwise."""
        # we're only accessing process image's objects to check stuff so we can work on a non-deep copy
        process_image = process_image_manager.process_image_read_only
        # check the number of hours per week
        for course in process_image.courses.values():
            expected = int(course.hours_weekly * (60 / 5) * len(group_map[course.group]))
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
                        if not process_image.check_travel_time(course_A_id=current_course_id,
                                                               course_B_id=self.matrix[
                                                                   day, timestamp, group],
                                                               current_time=window_length * 5):
                            return False
                        current_course_id = self.matrix[day, timestamp, group]
                        window_length = 0
        return True

    def from_neighbourhood(self) -> Solution:
        """Create new Solution from a Solution's neighbourhood.
        A neighbourhood is defined as Solutions different by one operation from the original Solution.
        """
        while True:
            matrix_operator = np.random.choice([operators.matrix_transposition,
                                                operators.matrix_inner_translation,
                                                operators.matrix_cut_and_paste_translation],
                                               p=self.operator_probabilities)
            new_solution_matrix, new_process_image = matrix_operator(self.matrix)
            new_solution = Solution(new_solution_matrix)
            if new_solution.check_acceptability():
                process_image_manager.process_image = new_process_image
                return new_solution


if __name__ == '__main__':
    np.random.seed(10)
    solution = Solution()
    solution.from_neighbourhood()
    solution.check_acceptability()
