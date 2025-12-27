from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
import hashlib


def stable_color_from_string(s: str):
    """
    Детерминированный радужный цвет из строки (имя файла).
    Цвет НЕ меняется между запусками.
    """
    h = hashlib.sha1(s.encode("utf-8")).hexdigest()
    hue = int(h[:8], 16) / 0xFFFFFFFF  # 0..1
    color = pg.hsvColor(
        hue=hue,
        sat=0.9,
        val=0.95,
        alpha=1.0
    )
    return color


class OverviewTab(QtWidgets.QWidget):
    def __init__(self, curves, parent=None):
        """
        curves: список dict'ов, каждый минимум:
            {
                'file': str,
                'E': np.ndarray,
                'I': np.ndarray,
                'baseline_I': np.ndarray | None,
                'sensor': str,
                'enantiomer': str,
                'conc': float | None,
                'pH': float | None
            }
        """
        super().__init__(parent)
        self.curves = curves
        self.items = []

        self._build_ui()
        self._populate()

    # ---------------- UI ----------------

    def _build_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        # ---- Left panel (list) ----
        self.list = QtWidgets.QListWidget()
        self.list.setMaximumWidth(320)
        self.list.setSpacing(2)
        self.list.itemChanged.connect(self._on_item_changed)

        layout.addWidget(self.list)

        # ---- Plot ----
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot, 1)

        self._setup_plot_style()

    def _setup_plot_style(self):
        self.plot.setBackground((10, 10, 14))
        self.plot.showGrid(x=True, y=True, alpha=0.15)

        self.plot.getAxis("left").setPen(pg.mkPen("#66ffff"))
        self.plot.getAxis("bottom").setPen(pg.mkPen("#66ffff"))

        self.plot.setLabel("left", "Current, A")
        self.plot.setLabel("bottom", "Potential, V")

    # ---------------- Populate ----------------

    def _populate(self):
        self.list.blockSignals(True)

        for idx, curve in enumerate(self.curves):

            # --- нормализация ---
            if isinstance(curve, dict):
                fname = curve.get("file", f"curve_{idx}")
            else:
                continue
            color = stable_color_from_string(fname)


            # --- List item ---
            item = QtWidgets.QListWidgetItem(fname)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)

            tooltip = self._build_tooltip(curve)
            item.setToolTip(tooltip)

            # цветной маркер
            item.setForeground(pg.mkColor(color))

            self.list.addItem(item)

            # --- Plot items ---
            pen_raw = pg.mkPen(color=color, width=1.5)

            raw_curve = self.plot.plot(
                curve["E"],
                curve["I"],
                pen=pen_raw
            )

            # baseline (пока может быть None)
            baseline_curve = None
            if curve.get("baseline_I") is not None:
                pen_bl = pg.mkPen(color=color, width=1.2, style=QtCore.Qt.DashLine)
                baseline_curve = self.plot.plot(
                    curve["E"],
                    curve["baseline_I"],
                    pen=pen_bl
                )
                baseline_curve.setVisible(False)

            self.items.append({
                "item": item,
                "raw": raw_curve,
                "baseline": baseline_curve,
                "has_baseline": baseline_curve is not None
            })

        self.list.blockSignals(False)

    # ---------------- Helpers ----------------

    def _build_tooltip(self, curve):
        def fmt(v):
            return "None" if v is None else str(v)

        return (
            f"File: {curve.get('file')}\n"
            f"Sensor: {curve.get('sensor')}\n"
            f"Enantiomer: {curve.get('enantiomer')}\n"
            f"Conc: {fmt(curve.get('conc'))}\n"
            f"pH: {fmt(curve.get('pH'))}"
        )

    # ---------------- Slots ----------------

    def _on_item_changed(self, item):
        idx = self.list.row(item)
        state = item.checkState() == QtCore.Qt.Checked

        entry = self.items[idx]
        entry["raw"].setVisible(state)

        # baseline пока выключен (логика будет позже)
        if entry["baseline"] is not None:
            entry["baseline"].setVisible(False)

        # визуальная подсветка имени файла
        font = item.font()
        font.setBold(entry["baseline"] is not None)
        item.setFont(font)
