import os
from data_io.voltammogram_loader import load_voltammogram_txt
from data_io.metadata_parser import parse_metadata_from_filename

def load_experiment_folder(path: str):
    results = []

    for fname in sorted(os.listdir(path)):
        if not fname.lower().endswith('.txt'):
            continue

        full = os.path.join(path, fname)

        try:
            curve = load_voltammogram_txt(full)
            meta = parse_metadata_from_filename(fname)

            results.append({
                "meta": meta,
                "curve": curve
            })

        except Exception as e:
            print(f"[SKIP] {fname}: {e}")

    print(f"\nИТОГО загружено: {len(results)} файлов\n")
    return results
