import numpy as np

s = np.array([[[0, 2, 3],
               [1, 0, 6],
               [2, 3, 5]],

              [[3, 2, 1],
               [6, 0, 4],
               [0, 4, 1]]])


def gaps_c_function(x: np.ndarray, w1: float) -> float:
    function_cost = 0
    ind = {}
    for n, day in enumerate(x):
        for group in range(day.shape[1]):
            ind[n, group] = []
            for hour in range(day.shape[0]):
                if day[hour, group] != 0:
                    ind[n, group].append(hour)
                    break
            for hour in range(day.shape[0]):
                if day[day.shape[0] - 1 - hour, group] != 0:
                    ind[n, group].append(day.shape[0] - 1 - hour)
                    break
    for n, day in enumerate(x):
        for group in range(day.shape[1]):
            # print(ind[n, group])
            slice = day[ind[n, group][0]: ind[n, group][1] + 1, group]
            # print(slice)
            # znajdz okienka w wycinku zajec
            zeros = len(slice) - np.count_nonzero(slice)
            # print(zeros)
            function_cost += zeros * w1

    return function_cost


def unbalanced_function(x: np.ndarray, w2: float) -> float:
    cost_function = 0
    H = np.count_nonzero(x)
    for n, day in enumerate(x):
        sum_group = 0
        for group in range(day.shape[1]):
            h = np.count_nonzero(day[:, group])
            sum_group += np.abs(H/(len(x)*day.shape[1])-h)
        cost_function += w2*sum_group
    return cost_function


# print(unbalanced_function(s, 1))
# x = gaps_c_function(s, 2)
# print(x)
