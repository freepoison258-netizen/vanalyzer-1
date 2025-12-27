from pathlib import Path
from data_io.voltammogram_loader import load_voltammogram_txt
from data_io.metadata_parser import parse_metadata_from_filename
import logging

logger = logging.getLogger(__name__)


def load_experiment_folder(path: str):
    """
    Loads all .txt in folder and returns list of dicts {'meta': MeasurementMeta, 'curve': Voltammogram}
    """
    folder = Path(path)
    results = []

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    for p in sorted(folder.iterdir()):
        if not p.is_file() or not p.name.lower().endswith('.txt'):
            continue

        try:
            curve = load_voltammogram_txt(p)
            meta = parse_metadata_from_filename(p.name)
            results.append({
                "meta": meta,
                "curve": curve
            })
        except (ValueError, FileNotFoundError) as e:
            logger.warning("[SKIP] %s: %s", p.name, e)
        except Exception:
            # unexpected error: keep full traceback in logs for debugging
            logger.exception("[ERROR] while loading %s", p.name)

    logger.info("TOTAL loaded: %d files", len(results))
    return results