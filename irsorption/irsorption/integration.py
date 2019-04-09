import scipy.integrate
from scipy.interpolate import InterpolatedUnivariateSpline
import pandas as pd

def integrate(data, extrema="max"):
    reduced = data - data.min()
    if extrema=="max":
        reduced = data - data.min()
    elif extrema=="min":
        reduced = -data + data.max()
    interpf = InterpolatedUnivariateSpline(reduced.index, reduced)
    return scipy.integrate.quad(interpf, reduced.index[0], reduced.index[-1])

def integrate_function(data, extrema="max"):
    reduced = data - data.min()
    if extrema=="max":
        reduced = data - data.min()
    elif extrema=="min":
        reduced = -data + data.max()

    interpf = InterpolatedUnivariateSpline(reduced.index, reduced)

    integral = pd.DataFrame(index=reduced.index)
    integral_tuple = [0]
    for i in range(1, len(reduced.index)):
        value = scipy.integrate.quad(interpf, reduced.index[i-1], reduced.index[i])[0]
        integral_tuple.append(integral_tuple[i-1] + value)
    integral["Integral"] = integral_tuple
    return integral
