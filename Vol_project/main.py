from functions.PNL_Actual import actual_pnl_simulation
from functions.PNL_Actual_backup import actual_pnl_full_simulation
from plot_PNL import simu_on_data


n_simulation = 5
expiry_date: float = 1.
strike: float = 100.
asset_price0: float = strike
actual_vol: float = 0.3
implied_vol: float = 0.2
interest: float = 0.05
dividend: float = 0.
drift: float = 0.5
op_type: str = "call"


if True:
    n_steps_time: int = 250
    actual_pnl_simulation(
        n_simulation, actual_vol, implied_vol, expiry_date, strike,
        interest, dividend, drift, asset_price0, n_steps_time, op_type
    )
    actual_pnl_full_simulation(
        n_simulation, actual_vol, implied_vol, expiry_date, strike,
        interest, dividend, drift, asset_price0, n_steps_time, op_type
    )

if False:
    year: int
    for year in [2001, 2008, 2015, 2018]:
        do_estimation: bool = True
        simu_on_data(
            year, strike, interest, dividend, op_type,
            implied_vol, actual_vol, drift, do_estimation
        )
