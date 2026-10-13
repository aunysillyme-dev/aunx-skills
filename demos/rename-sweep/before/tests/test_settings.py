import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from settings import cargo_delay
config = json.loads((ROOT / "config/settings.json").read_text())
assert cargo_delay(config) == 2
print("PASS: config reader returns the expected delay")
