from typing import List

import numpy as np
import operators
from process_image_manager import process_image_manager
from cost_functions import unbalanced_function, gaps_c_function


# FIXME: XD
group_map = {'wyklad': list(range(0, 10))}
j = 0
for i in range(5):
    group_map[i + 1] = [j, j + 1]
    j += 2
j = 0
for i in range(5):
    for subgroup in 'AB':
        group_map[f'{i + 1}{subgroup}'] = j
        j += 1


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
                            break

                        if np.all(matrix[day, j:j + length + 1, group_map[course.group]] == 0) and \
                                process_image.check_lecturer_availability(course.lecturer_id, day, j,
                                                                          j + length + 1) and \
                                process_image.check_room_availability(course.room_id, day, j, j + length + 1):
                            matrix[day, j:j + length + 1, group_map[course.group]] = course.id
                            process_image.reserve_lecturer_time(course.lecturer_id, day, j, j + length + 1)
                            process_image.reserve_room_time(course.room_id, day, j, j + length + 1)
                            inserted = True
                            break
            self.matrix = matrix
            process_image_manager.process_image = process_image

    @property
    def cost(self) -> float:
        """Returns the combined cost for the current solution matrix."""
        return gaps_c_function(self.matrix, 1) + unbalanced_function(self.matrix, 1)

    def check_acceptability(self) -> bool:
        """Checks if the solution is acceptable."""
        raise NotImplementedError

    @classmethod
    def from_neighbourhood(cls, ops: List[operators.matrix_operator]):
        raise NotImplementedError


if __name__ == '__main__':
    test_solution = Solution()
    print(test_solution.cost)
