import numpy as np
from scipy import stats

def mean_ci(values, alpha=0.05):
    values = np.asarray(values, dtype=float)
    n = len(values)
    mean = np.mean(values)
    sd = np.std(values, ddof=1) if n > 1 else 0.0
    if n > 1:
        t = stats.t.ppf(1 - alpha / 2, n - 1)
        ci = (mean - t * sd / np.sqrt(n), mean + t * sd / np.sqrt(n))
    else:
        ci = (mean, mean)
    return mean, sd, ci

def selectivity_ratio(values_r, values_s):
    if len(values_r) != len(values_s):
        raise ValueError("R and S must have same length")
    ratios = np.asarray(values_r) / np.asarray(values_s)
    mean, sd, ci = mean_ci(ratios)
    rsd = (sd / mean) * 100 if mean != 0 else float("nan")
    return {"alpha": mean, "sd": sd, "rsd": rsd, "ci": ci, "n": len(ratios)}
