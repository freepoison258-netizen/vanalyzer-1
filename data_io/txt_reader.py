import numpy as np


def read_txt_file(path: str) -> np.ndarray:
    """
    Reads voltammetry txt file.
    Returns ndarray of shape (N, 2): [E, I]
    """

    # пробуем самые частые варианты
    for delimiter in (None, ",", ";", "\t"):
        try:
            data = np.loadtxt(path, delimiter=delimiter)
            if data.ndim == 2 and data.shape[1] >= 2:
                return data[:, :2]
        except Exception:
            continue

    raise ValueError(f"Cannot parse txt file: {path}")
