class Measurement:
    def __init__(self, voltammogram, meta: dict):
        self.voltammogram = voltammogram
        self.meta = meta  # conc, enantio, modifier, etc


class Experiment:
    def __init__(self, measurements: list[Measurement]):
        self.measurements = measurements

    def filter(self, **conditions):
        out = []
        for m in self.measurements:
            if all(m.meta.get(k) == v for k, v in conditions.items()):
                out.append(m)
        return out
