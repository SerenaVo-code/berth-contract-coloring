"""Đối chiếu hai chiều với bản gốc (thư mục repo gốc truyền vào):
  (A) chạy bộ testcase của BẢN GỐC bằng solver dựng lại, kiểm bằng checker độc lập;
  (B) chạy bộ testcase DỰNG LẠI bằng solver của bản gốc và so kết quả của quay lui.
Dùng:  python tools/cross_check.py <đường dẫn repo gốc>
"""
import glob, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT / "backend"), str(HERE)]
import run_testcases as rt  # noqa: E402

orig = Path(sys.argv[1]).resolve()
rep = ["# Đối chiếu với bản gốc\n"]

# ---- (A)
files = sorted(glob.glob(str(orig / "testcases" / "m*" / "*.json")))
rows = []
for f in files:
    tc = json.load(open(f, encoding="utf-8"))
    r = rt.run_case(tc)
    rows.append(r)
okA = sum(r["pass"] for r in rows)
rep.append(f"## A. Testcase của bản gốc chạy bằng solver dựng lại\n\n**{okA}/{len(rows)}** đạt (kiểm bằng checker độc lập, so với đáp án tham chiếu của bản gốc).\n")
bad = [r for r in rows if not r["pass"]]
for r in bad:
    rep.append(f"- {r['id']} {r['title']}: {r['notes']}")
worse = [r for r in rows if "chưa chạm tối ưu" in r["notes"]]
if worse:
    rep.append("\nCa mà quay lui dựng lại hết ngân sách trước khi chạm tối ưu (không tính là lỗi): " + ", ".join(r["id"] for r in worse))

# ---- (B)
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

sys.path.insert(0, str(orig / "backend"))
o1, o2, o3, o4 = (load("o_" + n, orig / "backend" / f"{n}.py") for n in ("solver", "assign", "knapsack", "binpack"))
import assign, berth, binpack, knapsack  # noqa: E402

def best_of(res, key):
    vals = [a[key] for a in res if a.get(key) is not None]
    return vals

diff = []
n = 0
for f in sorted(glob.glob(str(ROOT / "testcases" / "m*" / "*.json"))):
    tc = json.load(open(f, encoding="utf-8")); i = tc["input"]; m = tc["module"]
    n += 1
    if m == "m1":
        mine = min(a["cost"] for a in berth.solve_all(i["ships"], i["pairs"], i["F"], i["r"])["algos"])
        out = o1.solve_all(i["ships"], i["pairs"], i["F"], i["r"])["results"]
        theirs = min(x["cost"] for x in out.values())
    elif m == "m2":
        a = assign.solve_all(i["ships"], i["teams"], i["pairs"])["algos"]
        mine = min([x["cost"] for x in a if x["cost"] is not None], default=None)
        out = o2.solve_assign(i["ships"], i["teams"], i["pairs"])["results"]
        theirs = min([x["cost"] for x in out.values() if x.get("feasible") and x.get("cost") is not None], default=None)
    elif m == "m3":
        mine = max(a["value"] for a in knapsack.solve_all(i["items"], i["W"])["algos"])
        out = o3.solve_knapsack(i["items"], i["W"])["results"]
        theirs = max(x["value"] for x in out.values())
    else:
        mine = min(a["bins"] for a in binpack.solve_all(i["items"], i["C"])["algos"])
        out = o4.solve_binpack(i["items"], i["C"])["results"]
        theirs = min(x["used"] for x in out.values())
    if (mine is None) != (theirs is None) or (mine is not None and abs(mine - theirs) > 1e-6):
        diff.append((tc["id"], mine, theirs, tc["expect"].get("opt")))
rep.append(f"\n## B. Testcase dựng lại chạy bằng solver bản gốc\n\nSo kết quả tốt nhất của mỗi bên trên {n} ca. **{n - len(diff)}/{n} ca hai bên cho cùng kết quả tốt nhất.**\n")
if diff:
    rep.append("| ID | Dựng lại | Bản gốc | Tham chiếu |\n|---|---|---|---|")
    for d in diff:
        rep.append("| " + " | ".join(str(x) for x in d) + " |")
(ROOT / "CROSS_CHECK.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
print("\n".join(rep))
