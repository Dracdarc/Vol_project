import math as m

pi: float = m.pi
SQRT_1_2: float = 1 / m.sqrt(2.)
SQRT_1_2pi: float = 1 / m.sqrt(2*pi)


def avg(l_float: [float]) -> float:
    return 0. if not l_float else sum(l_float)/len(l_float)


def normal_df(x: float) -> float:
    "Normal distribution function"
    return SQRT_1_2pi * m.exp(-.5*x**2)


def normal_cdf(x: float) -> float:
    "Normal cumulative distribution function"
    return .5 * (1. + m.erf(x*SQRT_1_2))


def exp(x: float) -> float:
    return m.exp(x)


def ln(x: float) -> float:
    return float("inf") if not x > 0 else m.log(x)
