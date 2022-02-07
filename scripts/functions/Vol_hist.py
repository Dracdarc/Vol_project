
# Brouillon !!

def vol_hist(C: [float]) -> float:
    """
    C: call prices list
    Return the list of hisctorical volatility
    """

    def avg(l_float: [float]) -> float:
        return 0. if not l_float else sum(l_float)/len(l_float)

    n: int = len(C)
    avg_C: [float] = [avg(C[:i]) for i in range(1, n+1)]
    C2: [float] = [C[i]**2 for i in range(n)]
    avg_C2: [float] = [
        avg(C2[:i]) for i in range(1, n+1)
    ]
    return [(avg_C2[i] - avg_C[i]**2)**.5 for i in range(n)]
