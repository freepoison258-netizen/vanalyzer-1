import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication

from data_io.load_raw_curves import load_raw_curves
from gui.main_window import MainWindow




def main():
    data_dir = Path(__file__).parent / "test_data"
    curves = load_raw_curves(data_dir)

    app = QApplication(sys.argv)
    w = MainWindow(curves)
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

curves = load_raw_curves(DATA_DIR)
DATA_DIR = "test_data"
