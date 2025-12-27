import logging
from data_io.load_experiment import load_experiment_folder
from logic.baseline_detection import estimate_baseline
from logic.peak_detection import extract_peak

DATA_DIR = "test_data"


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    exp = load_experiment_folder(DATA_DIR)
    logger.info("Loaded files: %d", len(exp))

    responses = []

    for m in exp:
        curve = m["curve"]

        E = curve.E if hasattr(curve, "E") else curve[:, 0]
        I = curve.I if hasattr(curve, "I") else curve[:, 1]

        baseline = estimate_baseline(I)
        peak = extract_peak(E, I, baseline)

        meta = m["meta"]

        responses.append({
            "file": getattr(meta, "source_file", None),
            "sensor": getattr(meta, "sensor_type", None),
            "enantiomer": getattr(meta, "enantiomer", None),
            "conc": getattr(meta, "analyte_concentration", None),
            "I_peak": peak.get("I_peak")
        })

    logger.info("Example responses (first 10):")
    for r in responses[:10]:
        logger.info(r)


if __name__ == "__main__":
    main()