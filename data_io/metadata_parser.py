import re
from typing import Optional
from core.models import MeasurementMeta

# FLOAT matches integers or floats with optional comma or dot
FLOAT_RE = r'(\d+(?:[.,]\d+)?)'

# Units that may follow numeric concentration (common variants)
UNITS_RE = r'(?:\s*(?:мг|mg|мм|mm|мкм|µm|μM|uM)\b)?'

ENANTIOMER_TAGS = r'\b(?:d|l|r|s|rac|racemat|рац|рацемат)\b'


def _to_float_or_none(s: Optional[str]) -> Optional[float]:
    if s is None:
        return None
    return float(s.replace(',', '.'))


def parse_metadata_from_filename(fname: str) -> MeasurementMeta:
    """
    Robust filename parser. Returns MeasurementMeta with fields filled when found.
    Uses word boundaries to reduce false positives (e.g. single letters inside words).
    """
    name = fname.lower()

    # analyte concentration like '10 mg' or '10mg' or '10,5 mm'
    m = re.search(FLOAT_RE + UNITS_RE, name)
    analyte_conc = _to_float_or_none(m.group(1)) if m else None

    # modifier concentration: e.g. 'modifier 5' or 'модификатор5'
    m2 = re.search(r'(?:modifier|модификатор)[\s:_-]*' + FLOAT_RE, name)
    modifier_conc = _to_float_or_none(m2.group(1)) if m2 else None

    # enantiomer tag using word boundaries
    m3 = re.search(ENANTIOMER_TAGS, name)
    enantiomer = m3.group(0) if m3 else None

    # sensor type detection
    if 'mip' in name:
        sensor = 'MIP'
    elif 'nip' in name:
        sensor = 'NIP'
    elif 'модификатор' in name or 'modifier' in name or 'modified' in name:
        sensor = 'modified'
    else:
        sensor = 'bare'

    modifier_flag = 'yes' if ('модификатор' in name or 'modifier' in name or 'modified' in name) else None

    return MeasurementMeta(
        analyte=None,  # often not recoverable from filename
        analyte_concentration=analyte_conc,
        modifier=modifier_flag,
        modifier_concentration=modifier_conc,
        sensor_type=sensor,
        enantiomer=enantiomer,
        source_file=fname
    )