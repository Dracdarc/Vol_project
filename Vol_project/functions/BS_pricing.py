from functions.utility import normal_cdf, ln, e


def black_scholes_pricing(
    underlying_price: float,
    strike: float,
    volatility: float,
    interest: float,
    maturity: float,
    option_type: str = "call"
) -> float:
    alpha: float = volatility * maturity**.5
    d1: float = (ln(underlying_price / strike)
                 + (interest+volatility**2/2)*maturity) / alpha
    d2: float = d1 - alpha
    if option_type.lower() == "call":
        return (underlying_price*normal_cdf(d1)
                - strike*normal_cdf(d2)*e**(-interest*maturity))
    elif option_type.lower() == "put":
        return (strike*normal_cdf(-d2)*e**(-interest*maturity)
                - underlying_price*normal_cdf(-d1))
    else:
        return -1.
