import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class MeasurementMeta:
    analyte: Optional[str]
    analyte_concentration: Optional[float]
    modifier: Optional[str]
    modifier_concentration: Optional[float]
    sensor_type: str
    enantiomer: Optional[str]
    source_file: str


FLOAT = r'(\d+(?:[.,]\d+)?)'

def parse_metadata_from_filename(fname: str) -> MeasurementMeta:
    name = fname.lower()

    def grab(pattern):
        m = re.search(pattern, name)
        return float(m.group(1).replace(',', '.')) if m else None

    analyte_conc = grab(FLOAT + r'\s*(?:мг|mg|мм|mm|мкм|µm)')
    modifier_conc = grab(r'модификатор\s*' + FLOAT)

    enantiomer = None
    for tag in ['d', 'l', 'r', 's', 'rac', 'racemat', 'рац', 'рацемат']:
        if tag in name:
            enantiomer = tag
            break

    if 'mip' in name:
        sensor = 'MIP'
    elif 'nip' in name:
        sensor = 'NIP'
    elif 'модификатор' in name:
        sensor = 'modified'
    else:
        sensor = 'bare'

    return MeasurementMeta(
        analyte=None,  # честно: из имени часто не вытащить
        analyte_concentration=analyte_conc,
        modifier='yes' if 'модификатор' in name else None,
        modifier_concentration=modifier_conc,
        sensor_type=sensor,
        enantiomer=enantiomer,
        source_file=fname
    )
