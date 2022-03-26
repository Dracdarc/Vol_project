from functions.playground import OptionMonitoring
from functions.BS_pricing import black_scholes_pricing
from functions.math_utility import generate_GBM

import numpy as np
from matplotlib import pyplot as plt

n_tics: int = 24*365
refresh_rate: int = 12
charges: float = .0

S0: float = 100.
drift: float = 0.02
realized_volatility: float = 0.5
interest: float = 0.02
dividend: float = 0.

maturity: float = 1.
strike: float = 100.


time_line: np.array = np.linspace(0., maturity, n_tics+1)
time_to_ex: np.array = time_line[::-1]
dt: float = time_line[1]

asset_prices: [float] = generate_GBM(
    S0, drift, realized_volatility, time_line
)

option_prices = [
  black_scholes_pricing(
    asset_prices[i], strike, realized_volatility,
    interest, time_line[-1]-time_line[i]
  ) for i in range(n_tics+1)
]

world: OptionMonitoring = OptionMonitoring(
    strike=strike,
    interest=interest
)

world.init(
    time_to_ex=time_to_ex[0],
    underlying_price=asset_prices[0],
    option_price=option_prices[0],
    volatility=realized_volatility
)

for t in range(n_tics+1)[::refresh_rate][1:]:
    world.update(
        time_to_ex=time_to_ex[t],
        underlying_price=asset_prices[t],
        option_price=option_prices[t],
        volatility=abs(realized_volatility + np.random.normal(0., 0.05))
    )

world.end(
    underlying_price=asset_prices[-1],
    option_price=option_prices[-1]
)

world.display(
    full_time_to_ex=time_to_ex,
    full_underlying_prices=asset_prices,
    full_option_prices=option_prices
)
