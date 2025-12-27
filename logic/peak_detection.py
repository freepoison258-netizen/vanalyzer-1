import numpy as np
from scipy.signal import find_peaks, peak_prominences
from typing import Dict, Any


def extract_peak(E: np.ndarray, I: np.ndarray, baseline: np.ndarray,
                 height: float = None, distance: int = None, prominence: float = None) -> Dict[str, Any]:
    """
    Extract most relevant peak from I - baseline using scipy.find_peaks.
    Returns dict with E_peak, I_peak, index, prominence, width (where available).
    If no peak found returns I_peak = 0 and E_peak = None.
    """
    signal = I - baseline
    # find_peaks expects 1d array
    peaks, props = find_peaks(signal, height=height, distance=distance, prominence=prominence)

    if peaks.size == 0:
        return {"E_peak": None, "I_peak": 0.0, "index": None, "prominence": 0.0}

    # choose peak with maximum prominence (robust to noise)
    prominences = peak_prominences(signal, peaks)[0]
    best_idx = int(np.argmax(prominences))
    peak_index = int(peaks[best_idx])

    return {
        "E_peak": float(E[peak_index]),
        "I_peak": float(signal[peak_index]),
        "index": peak_index,
        "prominence": float(prominences[best_idx])
    }