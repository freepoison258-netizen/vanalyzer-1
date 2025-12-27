import re
import numpy as np
from core.models import Voltammogram
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

FLOAT_RE = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')


def _extract_floats(line: str):
    return [float(x) for x in FLOAT_RE.findall(line)]


def load_voltammogram_txt(path: str) -> Voltammogram:
    """
    Load .txt file and return Voltammogram(E, I).
    Raises ValueError on invalid data.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    data = []
    replaced_chars = False

    # use 'replace' so we can detect but not silently drop chars (was 'ignore')
    with p.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if '\ufffd' in line:
                replaced_chars = True
            nums = _extract_floats(line)
            if len(nums) >= 2:
                data.append((nums[0], nums[1]))

    if replaced_chars:
        logger.warning("File %s contained characters that could not be decoded (replaced)", path)

    if len(data) == 0:
        raise ValueError(f"[VAnalyzer] '{path}': no numeric pairs found")

    arr = np.asarray(data, dtype=float)

    if arr.shape[0] > 5:
        if np.allclose(arr[:, 0], arr[:, 1]):
            raise ValueError(
                f"[VAnalyzer] '{path}': first and second columns match (E == I) — likely wrong format"
            )

    E = arr[:, 0]
    I = arr[:, 1]

    return Voltammogram(E=E, I=I)