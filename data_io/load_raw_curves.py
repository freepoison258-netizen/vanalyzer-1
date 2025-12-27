import os
import numpy as np

from data_io.voltammogram_loader import load_voltammogram_txt
from data_io.metadata_parser import parse_metadata_from_filename


def load_raw_curves(folder):
    """
    Загружает СЫРЫЕ вольтамперограммы.
    НИКАКОГО анализа.
    """

    curves = []

    for fname in sorted(os.listdir(folder)):
        if not fname.lower().endswith(".txt"):
            continue

        path = os.path.join(folder, fname)

        try:
            arr = load_voltammogram_txt(path)
            if arr.shape[1] < 2:
                raise ValueError("меньше двух колонок")
            E = arr[:, 0]
            I = arr[:, 1]
        except Exception as e:
            print(f"[SKIP] {fname}: {e}")
            continue

        meta = parse_metadata_from_filename(fname)

        curve = {
            "file": fname,
            "E": np.asarray(E),
            "I": np.asarray(I),
            "baseline_I": None,   # будет позже
            "sensor": getattr(meta, "sensor_type", None),
            "enantiomer": getattr(meta, "enantiomer", None),
            "conc": getattr(meta, "analyte_concentration", None),
            "pH": None,  # позже можно вытащить из имени
        }

        curves.append(curve)

    print(f"[RAW] загружено кривых: {len(curves)}")
    return curves
