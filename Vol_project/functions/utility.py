import math as m


SQRT_1_2: float = 1 / m.sqrt(2.)
e: float = m.e


def avg(l_float: [float]) -> float:
    return 0. if not l_float else sum(l_float)/len(l_float)


def normal_cdf(x: float) -> float:
    "Normal cumulative distribution function"
    return .5 * (1. + m.erf(x*SQRT_1_2))


def ln(x: float) -> float:
    return float("inf") if not x else m.log(x)
