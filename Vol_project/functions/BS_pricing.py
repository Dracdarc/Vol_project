from functions.math_utility import normal_cdf, exp, ln


def black_scholes_pricing(
    underlying_price: float,
    strike: float,
    volatility: float,
    interest: float,
    maturity: float,
    option_type: str = "call"
) -> float:
    """
    Price an option with the Black Scholes model.
    """
    alpha: float = volatility * maturity**.5
    d1: float = (ln(underlying_price / strike)
                 + (interest+volatility**2/2)*maturity) / alpha
    d2: float = d1 - alpha
    if option_type.lower() == "call":
        return (underlying_price*normal_cdf(d1)
                - strike*normal_cdf(d2)*exp(-interest*maturity))
    elif option_type.lower() == "put":
        return (strike*normal_cdf(-d2)*exp(-interest*maturity)
                - underlying_price*normal_cdf(-d1))
    else:
        return -1.
