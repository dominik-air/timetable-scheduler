import random
import math
import cProfile
from solution import Solution
from process_image_manager import process_image_manager


def SA():
    T = 1000
    Tmin = 100
    kmax = 10
    alpha = 0.9
    all_values = []

    x0 = Solution()
    x_best = x0
    f_best = x0.cost
    print(f_best)
    all_values.append(f_best)
    process_image_copy = process_image_manager.process_image

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
        xc = x_best
        process_image_manager.process_image = process_image_copy
        T *= alpha

    print(f'Best cost = {f_best}')

    with open('statistics/wyniki_sa_1.txt', 'w') as f:
        f.write(','.join([str(i) for i in all_values]))


if __name__ == '__main__':
    cProfile.run('SA()')

