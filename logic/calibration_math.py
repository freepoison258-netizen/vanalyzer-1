import numpy as np
from scipy import stats


def linear_calibration(x, y):
    if len(x) < 3:
        raise RuntimeError("Для градуировки нужно ≥ 3 точек")

    slope, intercept, r, _, _ = stats.linregress(x, y)

    y_fit = slope * x + intercept
    residuals = y - y_fit

    sigma = np.std(residuals, ddof=1)

    lod = 3.3 * sigma / slope
    loq = 10 * sigma / slope

    return {
        "slope": slope,
        "intercept": intercept,
        "r2": r ** 2,
        "LOD": lod,
        "LOQ": loq
    }
