import re
import numpy as np
from core.models import Voltammogram


FLOAT_RE = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')


def _extract_floats(line: str):
    return [float(x) for x in FLOAT_RE.findall(line)]


def load_voltammogram_txt(path: str) -> Voltammogram:
    """
    Загружает .txt файл и возвращает Voltammogram(E, I).

    Интерфейс СОХРАНЁН.
    Добавлена только валидация данных.
    """

    data = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            nums = _extract_floats(line)
            if len(nums) >= 2:
                data.append((nums[0], nums[1]))

    if len(data) == 0:
        raise ValueError(
            f"[VAnalyzer] '{path}': не найдено ни одной числовой пары"
        )

    arr = np.asarray(data, dtype=float)

    if arr.shape[0] > 5:
        if np.allclose(arr[:, 0], arr[:, 1]):
            raise ValueError(
                f"[VAnalyzer] '{path}': первая и вторая колонки совпадают "
                f"(E == I) — вероятно неверный формат файла"
            )

    E = arr[:, 0]
    I = arr[:, 1]

    return Voltammogram(E=E, I=I)
