import numpy as np


def extract_peak(E, I, baseline):
    idx = np.argmax(I - baseline)
    return {
        "E_peak": E[idx],
        "I_peak": I[idx] - baseline[idx]
    }
