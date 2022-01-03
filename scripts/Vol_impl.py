import math as m


# Brouillon !!

def vol_impl(
    C: [float],
    S: [float],
    E: float,
    r: float,
    t: [float]
) -> [float]:
    """
    C: call prices list
    S: asset prices list
    E: stike
    r: asset drift
    t: times list // t[-1]: expiry date
    Return the list of implicit volatility
    """
    vol_impl_list: [float] = [0. for _ in t]
    ksi: [float] = [0. for _ in t]
    E_ksi: [float] = [0. for _ in t]
    dS: float

    for i in range(1, len(t)-1):
        dS = S[i+1]-S[i-1]
        ksi[i] = 4*(C[i+1] + C[i-1] - 2*C[i])/(dS*dS) - (C[i+1]-C[i-1])/dS
    ksi[-1] = ksi[-2]

    for i in range(1, len(t)-1):
        E_ksi[i] = m.log(abs(ksi(i+1)*S[i-1]/(ksi[i+1]/S[i-1])))
    E_ksi[-1] = E_ksi[-2]

    for i in range(1, len(t)-1):
        vol_impl_list[i] = (m.log(E/S[i]) - r*(t[-1]-t[i])) /
        ((t[-1]-t[i]) * (E_ksi[i]))
    vol_impl_list[-1] = vol_impl_list[-2]

    return vol_impl_list
