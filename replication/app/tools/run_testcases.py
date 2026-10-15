"""Chạy toàn bộ testcase bằng cách gọi thẳng hàm giải, kiểm lại bằng checker độc lập, ghi RESULTS.md."""
import glob, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT / "backend"), str(HERE)]
import assign, berth, binpack, knapsack  # noqa: E402
from checker import check_assign, check_berth, check_bins, check_knap, knap_dp_1d  # noqa: E402

GROUPS = {"thuong": "Thông thường", "nho": "Dữ liệu nhỏ", "bien": "Biên", "dacbiet": "Đặc biệt", "lon": "Dữ liệu lớn"}
MODS = {"m1": "Thuê bến", "m2": "Phân công đội", "m3": "Quỹ giờ công", "m4": "Xếp container"}
EPS = 1e-6


def run_case(tc):
    inp, exp, m = tc["input"], tc["expect"], tc["module"]
    notes, fails, shown = [], [], []
    if m == "m1":
        res = berth.solve_all(inp["ships"], inp["pairs"], inp["F"], inp["r"])
        vals = []
        for a in res["algos"]:
            v, err = check_berth(inp, a["col"])
            if v is None: fails.append(f"{a['name']}: {err}")
            elif abs(v - a["cost"]) > EPS: fails.append(f"{a['name']}: tự báo {a['cost']} ≠ tính lại {v}")
            vals.append(v); shown.append(f"{a['name']} {fmtv(v)}")
        better = min
    elif m == "m2":
        res = assign.solve_all(inp["ships"], inp["teams"], inp["pairs"])
        vals = []
        for a in res["algos"]:
            if a["status"] == "ok":
                v, err = check_assign(inp, a["col"])
                if v is None: fails.append(f"{a['name']}: {err}")
                elif abs(v - a["cost"]) > EPS: fails.append(f"{a['name']}: tự báo ≠ tính lại")
                vals.append(v); shown.append(f"{a['name']} {fmtv(v)}")
            else:
                vals.append(None); shown.append(f"{a['name']} {a['status']}")
        better = min
        if exp.get("feasible") is False:
            if res["algos"][2]["status"] != "infeasible": fails.append("quay lui không kết luận vô nghiệm")
            if any(a["status"] == "ok" for a in res["algos"]): fails.append("có thuật toán báo nghiệm cho bài vô nghiệm")
        if exp.get("hall"):
            if not res["hall"]: fails.append("kiểm tra Hall không bắt được")
            if res["algos"][2]["nodes"] != 0: fails.append("quay lui vẫn duyệt dù Hall đã vi phạm")
    elif m == "m3":
        res = knapsack.solve_all(inp["items"], inp["W"])
        vals = []
        for a in res["algos"]:
            v, err = check_knap(inp, a["take"])
            if v is None: fails.append(f"{a['name']}: {err}")
            elif abs(v - a["value"]) > EPS: fails.append(f"{a['name']}: tự báo ≠ tính lại")
            vals.append(v); shown.append(f"{a['name']} {fmtv(v)}")
        better = max
        ref = knap_dp_1d(inp["items"], inp["W"])
        if abs(res["algos"][1]["value"] - ref) > EPS: fails.append(f"quy hoạch động {res['algos'][1]['value']} ≠ DP một chiều {ref}")
    else:
        res = binpack.solve_all(inp["items"], inp["C"])
        vals = []
        for a in res["algos"]:
            v, err = check_bins(inp, a["bin"])
            if v is None: fails.append(f"{a['name']}: {err}")
            elif v != a["bins"]: fails.append(f"{a['name']}: tự báo {a['bins']} ≠ tính lại {v}")
            vals.append(v); shown.append(f"{a['name']} {v}")
        better = min
        if res["lb"] > min(v for v in vals if v is not None): fails.append("cận dưới lớn hơn một kết quả hợp lệ")
    bt = res["algos"][-1]
    ok_vals = [v for v in vals if v is not None]
    opt = exp.get("opt")
    if opt is not None:
        if any(better(v, opt) != opt and abs(v - opt) > EPS for v in ok_vals):
            fails.append(f"có kết quả {'tốt hơn' } đáp án tham chiếu {opt} (đáp án hoặc checker sai)")
        if bt.get("optimal") and ok_vals and abs(vals[-1] - opt) > EPS:
            fails.append(f"quay lui báo tối ưu nhưng {vals[-1]} ≠ {opt}")
        if not bt.get("optimal"):
            notes.append("quay lui hết ngân sách")
            if vals[-1] is not None and abs(vals[-1] - opt) > EPS: notes.append(f"chưa chạm tối ưu {opt}")
    elif ok_vals and vals[-1] is not None and better(ok_vals) != vals[-1] and abs(better(ok_vals) - vals[-1]) > EPS:
        fails.append("quay lui kém hơn một thuật toán khác")
    if not bt.get("optimal") and opt is None: notes.append("quay lui hết ngân sách (không có đáp án tham chiếu)")
    # tính xác định: chạy lại phải ra y hệt
    again = run_signature(tc)
    if again != signature(res): fails.append("hai lần chạy cho kết quả khác nhau")
    return {"id": tc["id"], "module": m, "group": tc["group"], "title": tc["title"], "size": size_of(tc),
            "opt": opt, "opt_source": exp.get("opt_source"), "shown": "; ".join(shown),
            "max_ms": round(max(a["ms"] for a in res["algos"]), 2), "pass": not fails, "notes": "; ".join(notes + fails)}


def fmtv(v): return "—" if v is None else (str(int(v)) if float(v).is_integer() else f"{v:g}")


def size_of(tc):
    i = tc["input"]
    return f"{len(i['ships']) if 'ships' in i else len(i['items'])} " + ("tàu" if "ships" in i else "mục")


def signature(res):
    return [(a["name"], len(a["steps"]), a.get("cost", a.get("value", a.get("bins"))), a.get("nodes")) for a in res["algos"]]


def run_signature(tc):
    i, m = tc["input"], tc["module"]
    if m == "m1": return signature(berth.solve_all(i["ships"], i["pairs"], i["F"], i["r"]))
    if m == "m2": return signature(assign.solve_all(i["ships"], i["teams"], i["pairs"]))
    if m == "m3": return signature(knapsack.solve_all(i["items"], i["W"]))
    return signature(binpack.solve_all(i["items"], i["C"]))


def main():
    tcs = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(str(ROOT / "testcases" / "m*" / "*.json")))]
    rows = [run_case(tc) for tc in tcs]
    (ROOT / "testcases" / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(r["pass"] for r in rows)
    out = [f"# Kết quả chạy bộ testcase (bản dựng lại)\n", f"Tổng: **{ok}/{len(rows)}** testcase đạt. Sinh bởi `tools/run_testcases.py`.\n",
           "Đáp án tham chiếu đến từ vét cạn, công thức, instance dựng sẵn hoặc DP một chiều viết riêng, không lấy từ solver. Kết quả mỗi thuật toán đã được `tools/checker.py` tính lại độc lập.\n"]
    for m, mn in MODS.items():
        out.append(f"\n## {mn}\n\n| Nhóm | Số ca | Đạt |\n|---|---|---|")
        for g, gn in GROUPS.items():
            sub = [r for r in rows if r["module"] == m and r["group"] == g]
            out.append(f"| {gn} | {len(sub)} | {sum(r['pass'] for r in sub)} |")
        out.append("\n| ID | Nhóm | Cỡ | Tiêu đề | Tham chiếu | Kết quả từng thuật toán | ms | Đạt | Ghi chú |\n|---|---|---|---|---|---|---|---|---|")
        for r in (x for x in rows if x["module"] == m):
            ref = "—" if r["opt"] is None else f"{fmtv(r['opt'])} ({r['opt_source']})"
            out.append(f"| {r['id']} | {GROUPS[r['group']]} | {r['size']} | {r['title']} | {ref} | {r['shown']} | {r['max_ms']} | {'✔' if r['pass'] else '✘'} | {r['notes']} |")
    (ROOT / "testcases" / "RESULTS.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{ok}/{len(rows)} đạt")
    for r in rows:
        if not r["pass"]: print("FAIL", r["id"], r["notes"])
    return 0 if ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
