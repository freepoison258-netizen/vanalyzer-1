import numpy as np
from scipy.signal import savgol_filter


def estimate_baseline(I: np.ndarray, window: int = 51, poly: int = 3):
    if window >= len(I):
        window = len(I) // 2 * 2 + 1
    return savgol_filter(I, window_length=window, polyorder=poly)
