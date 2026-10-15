import glob, json, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import run_testcases as rt

FILES = sorted(glob.glob(str(ROOT / "testcases" / "m*" / "*.json")))


def test_enough_cases():
    assert len(FILES) >= 70


@pytest.mark.parametrize("f", FILES, ids=lambda f: Path(f).stem)
def test_case(f):
    tc = json.load(open(f, encoding="utf-8"))
    r = rt.run_case(tc)
    assert r["pass"], r["notes"]
