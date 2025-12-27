from dataclasses import dataclass
import numpy as np
from typing import Optional


@dataclass
class Voltammogram:
    E: np.ndarray
    I: np.ndarray


@dataclass
class MeasurementMeta:
    analyte: Optional[str]
    analyte_concentration: Optional[float]

    modifier: Optional[str]
    modifier_concentration: Optional[float]

    sensor_type: Optional[str]   # bare / modified / MIP / NIP
    replicate: Optional[int]

    source_file: str


@dataclass
class Measurement:
    voltammogram: Voltammogram
    meta: MeasurementMeta
