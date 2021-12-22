import random
import math
import cProfile
from solution import Solution
from process_image_manager import process_image_manager


# TODO: add other cooling schedules
def exponential_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T*(alpha**k)


def linear_cooling_schedule(T:int, alpha: float, k: int) -> float:
    return T - alpha*k


def logarithmic_cooling_schedule(T: int, alpha: int, k: int) -> float:
    return T/(alpha*math.log(k+1))


def quadratic_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T/(1+alpha*(k**2))


def bolzmann_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T/(1+math.log(k))


def cauchy_cooling_schedule(T: int, alpha: float, k: int) -> float:
    return T/(1+k)


def SA(T: int = 100, Tmin: int = 10, kmax: int = 10, alpha: float = 0.9,
       cooling_schedule: callable = exponential_cooling_schedule):
    """Simulated annealing algorithm.

    Args:
        T: initial system temperature.
        Tmin: minimal temperature (lower bound) of the cooling process.
        kmax: number of iterations in a given temperature.
        alpha: cooling process coefficient.
        cooling_schedule: cooling_schedule

    """
    all_values = []

    x0 = Solution()
    x_best = x0
    f_best = x0.cost
    print(f_best)
    all_values.append(f_best)
    process_image_copy = process_image_manager.process_image
    n_iter = 0

    xc = x0
    while T > Tmin:
        print(T)
        for k in range(kmax):
            xp = xc.from_neighbourhood()
            delta = xp.cost - xc.cost
            if delta <= 0:
                xc = xp
                if xc.cost <= f_best:
                    f_best = xc.cost
                    x_best = xc
                    process_image_copy = process_image_manager.process_image
            else:
                sigma = random.random()
                if sigma < math.exp(-delta / T):
                    xc = xp
            all_values.append(xp.cost)
            n_iter += 1
        xc = x_best
        process_image_manager.process_image = process_image_copy
        T = cooling_schedule(T, alpha, n_iter)

    print(f'Best cost = {f_best}')

    with open('statistics/wyniki_sa_1.txt', 'w') as f:
        f.write(','.join([str(i) for i in all_values]))


if __name__ == '__main__':
    cProfile.run('SA()')

