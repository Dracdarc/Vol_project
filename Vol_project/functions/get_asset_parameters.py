from functions.math_utility import ln, avg


def get_param(time: [float], asset_values: [float]) -> (float):
    """
    return a tuple with the drift then the realized volatility
    """
    n_step: int = len(time) - 1
    dt: [float] = [time[i+1] - time[i] for i in range(n_step)]
    dt_avg: float = avg(dt)
    log_values: [float] = [ln(value) for value in asset_values]
    d_log_values: [float] = [
        log_values[i+1] - log_values[i] for i in range(n_step)
    ]
    alpha: float = avg(d_log_values)
    center_2_dlog: [float] = [(value - alpha)**2 for value in d_log_values]
    sigma_2: float = avg(center_2_dlog) * (n_step-1)/(n_step-2) / dt_avg
    return (alpha/dt_avg + .5*sigma_2, sigma_2**.5)
