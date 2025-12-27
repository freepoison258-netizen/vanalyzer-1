import numpy as np
from scipy.signal import savgol_filter
import logging

logger = logging.getLogger(__name__)


def estimate_baseline(I: np.ndarray, window: int = 51, poly: int = 3) -> np.ndarray:
    """
    Estimate baseline using Savitzky-Golay filter with safe parameter selection.
    For very short arrays returns a copy of I.
    """
    n = len(I)
    if n == 0:
        raise ValueError("Empty signal")

    # polyorder must be < window_length and window_length must be odd and >= 3
    if n <= poly:
        logger.debug("Signal too short for polyorder: returning copy")
        return I.copy()

    # maximum allowed odd window <= n
    max_window = n if n % 2 == 1 else n - 1
    # choose min between requested window and max_window
    window = min(window, max_window)
    # ensure window > poly
    if window <= poly:
        window = poly + 1
        if window % 2 == 0:
            window += 1
        if window > max_window:
            logger.debug("Adjusted window exceeds max_window for length %d: returning copy", n)
            return I.copy()

    return savgol_filter(I, window_length=window, polyorder=poly)