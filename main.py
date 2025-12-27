from data_io.load_experiment import load_experiment_folder
from logic.baseline_detection import estimate_baseline
from logic.peak_detection import extract_peak

DATA_DIR = "test_data"

exp = load_experiment_folder(DATA_DIR)
print(f"Загружено файлов: {len(exp)}")

responses = []

for m in exp:
    curve = m["curve"]

    E = curve[:, 0]
    I = curve[:, 1]

    baseline = estimate_baseline(I)
    peak = extract_peak(E, I, baseline)

    meta = m["meta"]

    responses.append({
        "file": meta.source_file,
        "sensor": meta.sensor_type,
        "enantiomer": meta.enantiomer,
        "conc": meta.analyte_concentration,   # может быть None — и это ок
        "I_peak": peak["I_peak"]
    })

print("Пример:")
for r in responses[:66]:
    print(r)
