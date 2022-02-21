from functions.math_utility import avg


def list_vol_hist(C: [float]) -> [float]:
    """
    C: call prices list
    Return the list of hisctorical volatility
    """
    n: int = len(C)
    avg_C: [float] = [avg(C[:i]) for i in range(1, n+1)]
    C2: [float] = [C[i]**2 for i in range(n)]
    avg_C2: [float] = [
        avg(C2[:i]) for i in range(1, n+1)
    ]
    return [(avg_C2[i] - avg_C[i]**2)**.5 for i in range(n)]
