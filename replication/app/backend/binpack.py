"""Module 4: xếp lô container lên tàu = bài toán đóng thùng (bin packing).

Tham chiếu: [7] Johnson và cộng sự 1974 (First-Fit, First-Fit Decreasing), [6] Martello-Toth 1990
(cận dưới ⌈Σw/C⌉), [8] Garey-Johnson 1979 (NP-khó), [1] khung quay lui.
"""
import math
from core import EPS, Budget, Recorder, Timer, fmt, step_cap, MAX_NODES_BIN as MAX_NODES


def prepare(items, C):
    return {"n": len(items), "items": items, "C": C, "lb": math.ceil(sum(i["w"] for i in items) / C - EPS)}


def loads_of(P, assign):
    k = (max(assign) + 1) if assign else 0
    ld = [0.0] * k
    for i, b in enumerate(assign):
        ld[b] += P["items"][i]["w"]
    return ld


def is_valid(P, assign):
    return all(b >= 0 for b in assign) and all(x <= P["C"] + EPS for x in loads_of(P, assign))


def snapshot(assign, loads):
    return {"bin": assign[:], "loads": [round(x, 6) for x in loads], "n_bins": len(loads)}


def run_fit(P, key, name, decreasing, best_fit):
    it, C = P["items"], P["C"]
    rec = Recorder(step_cap(P["n"]))
    with Timer() as t:
        order = sorted(range(P["n"]), key=lambda i: (-it[i]["w"], i)) if decreasing else list(range(P["n"]))
        assign, loads = [-1] * P["n"], []
        how = "vào tàu vừa khít nhất (còn trống ít nhất nhưng đủ chỗ)" if best_fit else "vào tàu đầu tiên còn đủ chỗ"
        rec.add("info", ("Sắp lô theo khối lượng giảm dần. " if decreasing else "Giữ nguyên thứ tự nhập. ") + f"Mỗi lô được xếp {how}; không có thì mở tàu mới. Cận dưới {P['lb']} tàu.",
                order=order, **snapshot(assign, loads))
        for v in order:
            w = it[v]["w"]
            fits = [b for b in range(len(loads)) if loads[b] + w <= C + EPS]
            if fits:
                b = min(fits, key=lambda x: (C - loads[x] - w, x)) if best_fit else fits[0]
                new = False
            else:
                b, new = len(loads), True
                loads.append(0.0)
            loads[b] += w
            assign[v] = b
            rec.add("assign", f"{it[v]['name']} ({fmt(w)}) " + (f"không vừa tàu nào, mở tàu {b + 1}." if new else f"vào tàu {b + 1}, còn trống {fmt(C - loads[b])}."),
                    cur=v, to=b, new=new, fits=fits, **snapshot(assign, loads))
        rec.add("done", f"Hoàn tất: {len(loads)} tàu (cận dưới {P['lb']}).", cur=-1, **snapshot(assign, loads))
    return {"key": key, "name": name, "steps": rec.steps, "bin": assign, "bins": len(loads),
            "optimal": len(loads) <= P["lb"] or None, "nodes": 0, "truncated": rec.truncated, "ms": t.ms}


def run_bt(P, seed_assign, max_nodes=MAX_NODES):
    it, C, n = P["items"], P["C"], P["n"]
    rec = Recorder(step_cap(n))
    bud = Budget(max_nodes)
    with Timer() as t:
        order = sorted(range(n), key=lambda i: (-it[i]["w"], i))
        rest = [0.0] * (n + 1)
        for idx in range(n - 1, -1, -1):
            rest[idx] = rest[idx + 1] + it[order[idx]]["w"]
        best_assign = seed_assign[:]
        best = max(seed_assign) + 1
        assign, loads = [-1] * n, []
        stop = [best <= P["lb"]]
        rec.add("info", f"Quay lui: lô nặng trước, mỗi lô thử vào từng tàu đang mở (bỏ qua tàu có cùng mức tải đã thử) rồi thử mở tàu mới. "
                        f"Phương án tốt nhất hiện có bắt đầu từ First-Fit giảm dần: {best} tàu. Cận dưới {P['lb']}.",
                best=best, depth=0, **snapshot(assign, loads))

        def go(idx):
            nonlocal best, best_assign
            if stop[0] or not bud.tick():
                stop[0] = True
                return
            if idx == n:
                if len(loads) < best:
                    best, best_assign = len(loads), assign[:]
                    rec.add("found", f"Tìm được phương án {best} tàu, ghi nhận là phương án tốt nhất hiện có.",
                            best=best, depth=idx, **snapshot(assign, loads))
                    if best <= P["lb"]:
                        stop[0] = True
                return
            v = order[idx]
            w = it[v]["w"]
            tried = []
            for b in range(len(loads) + 1):
                new = b == len(loads)
                if not new:
                    if loads[b] + w > C + EPS or any(abs(loads[b] - x) < EPS for x in tried):
                        continue
                    tried.append(loads[b])
                    loads[b] += w
                else:
                    if len(loads) + 1 >= best:
                        rec.add("prune", f"Bỏ nhánh: mở tàu {b + 1} cho {it[v]['name']} thì ≥ {best} tàu, không hơn phương án tốt nhất hiện có.",
                                cur=v, to=b, best=best, depth=idx + 1, **snapshot(assign, loads))
                        continue
                    loads.append(w)
                assign[v] = b
                free = sum(C - x for x in loads)
                bound = len(loads) + max(0, math.ceil((rest[idx + 1] - free) / C - EPS))
                if bound >= best:
                    rec.add("prune", f"Bỏ nhánh: {it[v]['name']} vào tàu {b + 1}, cận {bound} ≥ {best} (phương án tốt nhất hiện có).",
                            cur=v, to=b, best=best, depth=idx + 1, **snapshot(assign, loads))
                else:
                    rec.add("assign", f"Thử {it[v]['name']} ({fmt(w)}) vào tàu {b + 1}{' (mới)' if new else ''}, cận {bound}.",
                            cur=v, to=b, new=new, best=best, depth=idx + 1, **snapshot(assign, loads))
                    go(idx + 1)
                assign[v] = -1
                if new:
                    loads.pop()
                else:
                    loads[b] -= w
                if stop[0]:
                    return

        go(0)
        tail = f" Dừng vì hết ngân sách {bud.max_nodes} nút, chưa chắc tối ưu." if bud.exhausted else ""
        rec.add("done", f"Hoàn tất: {best} tàu (cận dưới {P['lb']}).{tail}", cur=-1, best=best,
                bin=best_assign[:], loads=[round(x, 6) for x in loads_of(P, best_assign)], n_bins=best)
    return {"key": "bt", "name": "Quay lui + bỏ nhánh", "steps": rec.steps, "bin": best_assign, "bins": best,
            "optimal": best <= P["lb"] or not bud.exhausted, "nodes": bud.nodes, "truncated": rec.truncated, "ms": t.ms}


def solve_all(items, C, max_nodes=MAX_NODES):
    P = prepare(items, C)
    ff = run_fit(P, "ff", "First-Fit", False, False)
    ffd = run_fit(P, "ffd", "First-Fit giảm dần", True, False)
    bfd = run_fit(P, "bfd", "Best-Fit giảm dần", True, True)
    seed = min([ff, ffd, bfd], key=lambda a: a["bins"])["bin"]
    bt = run_bt(P, seed, max_nodes)
    return {"n": P["n"], "C": C, "lb": P["lb"], "algos": [ff, ffd, bfd, bt]}
