from functions.PNL_Actual import actual_pnl_simulation


n_simulation = 5
expiry_date: float = 1.
strike: float = 100.
actual_vol: float = 0.3
implied_vol: float = 0.2
interest: float = 0.05
dividend: float = 0.
drift: float = 0.1

actual_pnl_simulation(
    n_simulation, actual_vol, implied_vol, expiry_date, strike, interest,
    dividend, drift, asset_price0=strike, n_steps_time=1000, op_type="Call"
)
