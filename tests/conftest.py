# Dodaje folder src/ do cieki import?w, eby testy widziay moduy projektu
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
