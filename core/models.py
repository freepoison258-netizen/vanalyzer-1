from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Voltammogram:
    E: np.ndarray
    I: np.ndarray


@dataclass
class MeasurementMeta:
    analyte: Optional[str] = None
    analyte_concentration: Optional[float] = None

    modifier: Optional[str] = None
    modifier_concentration: Optional[float] = None

    sensor_type: Optional[str] = None  # 'bare' / 'modified' / 'MIP' / 'NIP'
    enantiomer: Optional[str] = None
    replicate: Optional[int] = None

    source_file: Optional[str] = None


@dataclass
class Measurement:
    voltammogram: Voltammogram
    meta: MeasurementMeta