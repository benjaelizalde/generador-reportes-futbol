from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "epl_clean.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
INDICE_CRONICAS = REPORTS_DIR / "indice_cronicas.csv"
