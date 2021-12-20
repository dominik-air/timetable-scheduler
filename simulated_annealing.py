import random
import math
import cProfile
from solution import Solution


def SA():
    T = 100
    Tmin = 10
    kmax = 100
    alpha = 0.9

    x0 = Solution()
    x_best = x0
    f_best = x0.cost
    print(f_best)

    xc = x0
    while T > Tmin:
        print(T)
        for k in range(kmax):
            xp = xc.from_neighbourhood()
            delta = xp.cost - xc.cost
            if delta <= 0:
                xc = xp
                if xc.cost < f_best:
                    f_best = xc.cost
                    x_best = xc
            else:
                sigma = random.random()
                if sigma < math.exp(delta / T):
                    xc = xp
        T *= alpha

    print(f'Best cost = {f_best}')


if __name__ == '__main__':
    cProfile.run('SA()')
