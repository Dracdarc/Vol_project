from functions.math_BS_pricing import black_scholes_pricing


ITERATION_NUM: int = 10


def vol_impl(
    option_price: float,
    underlying_price: float,
    strike: float,
    interest: float,
    maturity: float,
    option_type: str = "call"
) -> float:

    def f(x: float) -> float:
        return float("inf") if x == 1. else x/(1-x)

    anti_sigma_0: float = 0.
    anti_sigma_1: float = 1.
    anti_sigma_d: float
    black_scholes_price: float

    for _ in range(ITERATION_NUM):
        anti_sigma_d = .5 * (anti_sigma_0 + anti_sigma_1)
        black_scholes_price = black_scholes_pricing(
            underlying_price, strike, f(anti_sigma_d),
            interest, maturity, option_type
        )
        if option_price > black_scholes_price:
            anti_sigma_0 = anti_sigma_d
        else:
            anti_sigma_1 = anti_sigma_d
    return f(.5 * (anti_sigma_0 + anti_sigma_1))
