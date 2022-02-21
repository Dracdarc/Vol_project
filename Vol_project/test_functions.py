from functions import (
    math_utility,
    BS_pricing,
    Vol_hist,
    Vol_impl
)


N_TEST: int = 2
EPSILON: float = 1e-2

print("Beginning of the tests: ")


# utility
print("\n----> utility: ")

if abs(math_utility.SQRT_1_2 - 0.70710678119) < EPSILON:
    print("math_utility -> SQRT_1_2: No problem")
else:
    print("math_utility -> SQRT_1_2: ERROR!")

if abs(math_utility.exp(1.) - 2.71828182846) < EPSILON:
    print("math_utility -> exp: No problem")
else:
    print("math_utility -> exp: ERROR!")


# BS_pricing

print("\n----> BS_pricing: ")

underlying_price: [float] = [100., 50.]
strike: [float] = [100., 75.]
volatility: [float] = [.2, .5]
interest: [float] = [.2, .4]
maturity: [float] = [1., .5]
option_type: [str] = ["call", "put"]

prices: [float] = [
    BS_pricing.black_scholes_pricing(
        underlying_price[i],
        strike[i],
        volatility[i],
        interest[i],
        maturity[i],
        option_type[i]
    ) for i in range(N_TEST)
]

real_prices: [float] = [19.6299, 14.7834]

if False in [abs(prices[i] - real_prices[i]) < EPSILON for i in range(N_TEST)]:
    print("BS_pricing -> black_scholes_pricing: ERROR!")
else:
    print("BS_pricing -> black_scholes_pricing: No problem")


# Vol_hist

print("\n----> Vol_hist: ")

list_vol: [float] = Vol_hist.list_vol_hist(
    [1., 2., 3., 4., 5., 6.]
)
real_list_vol: [float] = [
    0.0, 0.5, 0.8164965, 1.1180339, 1.4142135, 1.7078251
]
if sum([abs(list_vol[i] - real_list_vol[i])
        for i in range(len(list_vol))]) < EPSILON:
    print("Vol_hist -> list_vol_hist: No problem")
else:
    print("Vol_hist -> list_vol_hist: ERROR!")


# Vol_impl

print("\n----> Vol_impl: ")

list_vol = [
    Vol_impl.vol_impl(
        prices[i],
        underlying_price[i],
        strike[i],
        interest[i],
        maturity[i],
        option_type[i]
    ) for i in range(N_TEST)
]

if False in [abs(volatility[i] - list_vol[i]) < EPSILON
             for i in range(N_TEST)]:
    print("Vol_impl -> vol_impl: ERROR!")
else:
    print("Vol_impl -> vol_impl: No problem")
