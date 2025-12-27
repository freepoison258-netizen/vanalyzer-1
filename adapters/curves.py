
from dataclasses import dataclass
import numpy as np

@dataclass
class Curve:
    E: np.ndarray
    I: np.ndarray
    meta: dict

def load_curves_from_experiment(exp):
    """
    exp: iterable of dicts produced by existing pipeline.
    Expected that raw E/I are present under exp[i]['E'], exp[i]['I']
    or exp[i]['raw']['E'], exp[i]['raw']['I'].
    This adapter does NOT modify data, only normalizes access.
    """
    curves = []
    for item in exp:
        if 'E' in item and 'I' in item:
            E = item['E']
            I = item['I']
        elif 'raw' in item and 'E' in item['raw'] and 'I' in item['raw']:
            E = item['raw']['E']
            I = item['raw']['I']
        else:
            # skip entries without raw curves
            continue

        meta = {k: v for k, v in item.items() if k not in ('E', 'I', 'raw')}
        curves.append(Curve(E=E, I=I, meta=meta))

    return curves
