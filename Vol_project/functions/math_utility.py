import math as m
import numpy as np

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


def generate_GBM(
    S0: float,
    mu: float,
    sigma: float,
    time: [float]
) -> [float]:
    gbm: [float] = [S0]
    dt: float
    for i in range(len(time)-1):
        dt = time[i+1] - time[i]
        gbm.append(
            gbm[-1]*(1 + mu*dt + sigma*np.random.normal(0., m.sqrt(dt)))
        )
    return gbm
