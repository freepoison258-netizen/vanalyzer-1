import sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

try:
    from PyQt5.QtWidgets import QApplication
    HAS_QT = True
except Exception:
    HAS_QT = False
    logger.warning("PyQt5 not available; GUI cannot be started in this environment")

from data_io.load_raw_curves import load_raw_curves
from gui.main_window import MainWindow


def main(data_dir: Path = None):
    if data_dir is None:
        data_dir = Path(__file__).parent / "test_data"

    curves = load_raw_curves(data_dir)

    import numpy as np
    for i, c in enumerate(curves[:8]):
        E = np.asarray(c["E"])
        I = np.asarray(c["I"])
        print(f"#{i} {c['file']}: len(E)={E.size}, len(I)={I.size}, dtype(E)={E.dtype}, dtype(I)={I.dtype}")
        print(f"  E: min={E.min():.6g}, max={E.max():.6g}, uniq_head={E[:5]}")
        print(f"  I: min={I.min():.6g}, max={I.max():.6g}, uniq_head={I[:5]}")
        print(f"  any NaN E={np.isnan(E).any()}, any NaN I={np.isnan(I).any()}")
        print(f"  monotonic E? {np.all(np.diff(E) >= 0)}\n")

    if not HAS_QT:
        logger.error("PyQt5 is not installed or cannot be used in this environment")
        return 1

    app = QApplication(sys.argv)
    w = MainWindow(curves)
    w.show()
    return app.exec_()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    exit_code = main()
    sys.exit(exit_code)