from functions.PNL_Actual import actual_strategy_pnl
from functions.get_asset_parameters import get_param
from get_SPX_prices import get_data
from matplotlib import pyplot as plt


plt.style.use('ggplot')


def simu_on_data(
    year: int,
    strike: float,
    interest: float,
    dividend: float,
    op_type: str,
    implied_vol: float,
    actual_vol: float,
    drift: float,
    do_estimation: bool = False
) -> None:
    data: [[float]] = get_data(year)
    print("Number of sightings: ", len(data[0]))
    time: [float] = [t - data[0][0] for t in data[0]]
    if do_estimation:
        (drift, actual_vol) = get_param(time, data[1])
        print("Drift: ", drift)
        print("Actual volatility: ", actual_vol)

    pnl_curves: [float] = actual_strategy_pnl(
        data[1], time, actual_vol, implied_vol, strike,
        interest, dividend, drift, op_type
    )

    fig, axs = plt.subplots(2)
    axs[0].plot(data[0], data[1])
    axs[0].set_title("Underlying price")
    axs[1].plot(data[0], pnl_curves)
    axs[1].set_title("""Profit and Loss""")
    for ax in axs.flat:
        ax.set(xlabel="Time in year", ylabel="Price")
        ax.label_outer()
    plt.show()
