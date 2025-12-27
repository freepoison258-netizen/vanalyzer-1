from pathlib import Path
import numpy as np
import logging
from data_io.voltammogram_loader import load_voltammogram_txt
from data_io.metadata_parser import parse_metadata_from_filename

logger = logging.getLogger(__name__)


def load_raw_curves(folder):
    """
    Load raw voltammograms from folder.
    Returns list of dicts with keys: file, E, I, baseline_I, sensor, enantiomer, conc, pH
    """
    folder = Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    curves = []

    for p in sorted(folder.iterdir()):
        if not p.is_file() or not p.name.lower().endswith(".txt"):
            continue

        try:
            arr = load_voltammogram_txt(p)
            E = arr.E
            I = arr.I
            if E.size == 0 or I.size == 0:
                raise ValueError("empty E or I")
        except Exception as e:
            logger.warning("[SKIP] %s: %s", p.name, e)
            continue

        meta = parse_metadata_from_filename(p.name)

        curve = {
            "file": p.name,
            "E": np.asarray(E),
            "I": np.asarray(I),
            "baseline_I": None,   # will be filled later
            "sensor": getattr(meta, "sensor_type", None),
            "enantiomer": getattr(meta, "enantiomer", None),
            "conc": getattr(meta, "analyte_concentration", None),
            "pH": None,  # could be parsed later
        }

        curves.append(curve)

    logger.info("[RAW] loaded curves: %d", len(curves))
    return curves