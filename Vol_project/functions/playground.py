from functions.math_utility import ln, exp, normal_cdf
from matplotlib import pyplot as plt


plt.style.use('ggplot')


class OptionMonitoring:

    def __init__(
        self,
        maturity: float,
        strike: float,
        interest: float,
        charges=lambda move_cash, move_asset: 0.
    ) -> None:
        self.maturity: float = maturity
        self.strike: float = strike
        self.interest: float = interest
        self.charges = charges

        self.time_line: [float] = []
        self.underlying_prices: [float] = []
        self.option_prices: [float] = []
        self.volatilities: [float] = []

        self.cash: [float] = []
        self.deltas: [float] = []
        self.pnl: [float] = []
        self.portfolio_value: [float] = []

        self.end_flag: bool = False
        self.init_flag: bool = False

    def init(
        self,
        underlying_price: float,
        option_price: float,
        volatility: float
    ) -> None:
        if not self.end_flag:
            self.time_line.append(0.)
            self.underlying_prices.append(underlying_price)
            self.option_prices.append(option_price)
            self.volatilities.append(volatility)
            self.deltas.append(self.get_delta())
            self.cash.append(option_price - self.deltas[-1]*underlying_price)
            self.pnl.append(
                option_price - self.charges(
                    self.cash[-1], self.deltas[-1]*underlying_price
                )
            )
            self.portfolio_value.append(option_price)
            self.init_flag = True

    def update(
        self,
        time: float,
        underlying_price: float,
        option_price: float,
        volatility: float
    ) -> None:
        if (
            self.init_flag
            and not self.end_flag
            and self.time_line[-1] < time <= self.maturity
        ):
            self.time_line.append(time)
            self.underlying_prices.append(underlying_price)
            self.option_prices.append(option_price)
            self.volatilities.append(volatility)
            self.deltas.append(self.get_delta())

            dt: float = self.time_line[-1] - self.time_line[-2]
            d_delta: float = self.deltas[-1] - self.deltas[-2]
            self.cash.append(self.cash[-1]*exp(self.interest*dt))
            new_cash: float = option_price - self.deltas[-1]*underlying_price
            self.pnl.append(
                self.pnl[-1] + self.cash[-1]
                - new_cash - d_delta*underlying_price
                - self.charges(
                    self.cash[-1]-new_cash, d_delta*underlying_price
                )
            )
            self.cash[-1] = new_cash

            self.portfolio_value.append(
                self.cash[-1] + self.deltas[-1]*self.underlying_prices[-1]
            )

    def end(
        self,
        underlying_price: float,
        option_price: float
    ) -> None:
        if not self.end_flag:
            if self.maturity != self.time_line[-1]:
                self.update(
                    self.maturity,
                    underlying_price,
                    option_price,
                    0.
                )
            if underlying_price > self.strike:
                self.pnl[-1] += self.strike
            self.pnl[-1] += self.cash[-1]
            self.cash[-1] = 0.
            self.end_flag = True

    def get_delta(self) -> None:
        tau: float = self.maturity - self.time_line[-1]
        alpha: float = self.volatilities[-1] * tau**.5
        if alpha == 0.:
            alpha = 1e-10
        d1: float = (
            ln(self.underlying_prices[-1] / self.strike)
            + (self.interest + (self.volatilities[-1]**2)/2.) * tau
        ) / alpha
        return normal_cdf(d1)

    def display(
        self,
        full_time_line: [float] = [],
        full_underlying_prices: [float] = [],
        full_option_prices: [float] = []
    ) -> bool:
        fig, axs = plt.subplots(6, figsize=(20, 14), dpi=100)
        color: str = "Red"
        if self.underlying_prices[-1] > self.strike:
            color = "Green"
        if full_underlying_prices:
            axs[0].plot(
                full_time_line,
                full_underlying_prices,
                linewidth=0.7, color=color
            )
        else:
            axs[0].plot(
                self.time_line,
                self.underlying_prices,
                linewidth=0.7, color=color
            )
        axs[0].hlines(self.strike, 0., self.maturity, linewidth=0.7)
        if full_option_prices:
            axs[1].plot(
                full_time_line,
                full_option_prices,
                label="Option price", linewidth=1.
            )
        axs[1].plot(
            self.time_line,
            self.portfolio_value,
            label="Portfolio value", linewidth=0.7, marker='.'
        )
        axs[2].plot(self.time_line, self.deltas, drawstyle='steps-post')
        if self.underlying_prices[-1] > self.strike:
            axs[2].hlines(1., 0., self.maturity, linewidth=0.7)
        else:
            axs[2].hlines(0., 0., self.maturity, linewidth=0.7)
        axs[3].plot(self.time_line, self.pnl, drawstyle='steps-post')
        axs[4].plot(
            self.time_line[:-1], self.volatilities[:-1],
            drawstyle='steps-post'
        )
        axs[5].plot(self.time_line, self.cash, drawstyle='steps-post')
        axs[0].set_title("Underlying price")
        axs[1].set_title("Strategy")
        axs[2].set_title("Hedge ratio")
        axs[3].set_title("P&L")
        axs[4].set_title("Volatility")
        axs[5].set_title("Cash")
        for ax in axs.flat:
            ax.set(xlabel="Time in year", ylabel="Price")
            ax.label_outer()
        axs[1].legend()
        axs.flat[2].set(ylabel="")
        axs.flat[4].set(ylabel="")
        plt.show()
