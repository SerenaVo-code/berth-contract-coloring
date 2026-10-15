"""Module 2: phân công đội phục vụ cho từng lượt tàu (gán có ràng buộc, chi phí nhỏ nhất).

Tham chiếu: [1] khung tham lam / quay lui;  [9] Hall 1935 và [10] Kuhn 1955 (khớp hai phía)
cho bước kiểm tra vô nghiệm.  Tự thiết kế: mô hình đội–kỹ năng–đơn giá và cận dưới theo tàu còn lại.
"""
from core import EPS, Budget, Recorder, Timer, fmt, step_cap, MAX_NODES


def prepare(ships, teams, pairs):
    n, m = len(ships), len(teams)
    elig = [[t for t in range(m) if set(ships[i]["need"]) <= set(teams[t]["skills"])] for i in range(n)]
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if ships[i]["s"] < ships[j]["e"] and ships[j]["s"] < ships[i]["e"]:
                adj[i].add(j); adj[j].add(i)
    for a, b in pairs:
        if a != b:
            adj[a].add(b); adj[b].add(a)
    dur = [sh["e"] - sh["s"] for sh in ships]
    return {"n": n, "m": m, "ships": ships, "teams": teams, "elig": elig, "adj": adj, "dur": dur}


def cost_of(P, col):
    return sum(P["teams"][col[i]]["rate"] * P["dur"][i] for i in range(P["n"]))


def is_valid(P, col):
    for i in range(P["n"]):
        t = col[i]
        if t < 0 or t not in P["elig"][i] or any(col[j] == t for j in P["adj"][i]):
            return False
    return True


def hall_violation(P):
    """Điều kiện cần: tại mọi thời điểm, các tàu đang neo phải khớp được với các đội khác nhau
    (đội đủ kỹ năng). Trả None nếu qua được, ngược lại mô tả chỗ vi phạm."""
    for i in range(P["n"]):
        if not P["elig"][i]:
            return {"kind": "no_team", "ships": [i], "time": P["ships"][i]["s"],
                    "msg": f"{P['ships'][i]['name']} không có đội nào đủ kỹ năng."}
    for t in sorted({sh["s"] for sh in P["ships"]}):
        act = [i for i, sh in enumerate(P["ships"]) if sh["s"] <= t < sh["e"]]
        match = {}

        def aug(u, seen):
            for tm in P["elig"][u]:
                if tm in seen:
                    continue
                seen.add(tm)
                if tm not in match or aug(match[tm], seen):
                    match[tm] = u
                    return True
            return False

        for u in act:
            if not aug(u, set()):
                pool = sorted({tm for x in act for tm in P["elig"][x]})
                return {"kind": "hall", "ships": act, "time": t,
                        "msg": f"Lúc {fmt(t)}h có {len(act)} tàu cùng neo nhưng chỉ có {len(pool)} đội đủ kỹ năng "
                               f"cho nhóm này, không thể gán mỗi tàu một đội khác nhau."}
    return None


def cand_table(P, col, v):
    out = []
    for t in range(P["m"]):
        tm = P["teams"][t]
        if t not in P["elig"][v]:
            miss = sorted(set(P["ships"][v]["need"]) - set(tm["skills"]))
            out.append({"k": t, "ok": False, "why": "thiếu kỹ năng " + ", ".join(miss), "delta": None})
            continue
        bl = [u for u in P["adj"][v] if col[u] == t]
        if bl:
            out.append({"k": t, "ok": False, "why": "trùng/cấm với " + ", ".join(P["ships"][u]["name"] for u in sorted(bl)[:3]), "delta": None})
        else:
            out.append({"k": t, "ok": True, "why": "", "delta": tm["rate"] * P["dur"][v]})
    return out


def result(P, key, name, rec, col, status, ms, nodes=0, optimal=None, extra=None):
    done = status in ("ok",)
    out = {"key": key, "name": name, "steps": rec.steps, "col": col, "status": status,
           "cost": cost_of(P, col) if done else None, "optimal": optimal, "nodes": nodes,
           "truncated": rec.truncated, "ms": ms}
    if extra:
        out.update(extra)
    return out


def run_greedy(P, hardest):
    key = "greedy_hard" if hardest else "greedy"
    name = "Tham lam tàu khó trước" if hardest else "Tham lam theo giờ đến"
    rec = Recorder(step_cap(P["n"]))
    with Timer() as t:
        n = P["n"]
        col = [-1] * n
        if hardest:
            order = sorted(range(n), key=lambda i: (len(P["elig"][i]), P["ships"][i]["s"], i))
            txt = "Sắp tàu theo số đội đủ kỹ năng tăng dần (tàu khó nhất trước)."
        else:
            order = sorted(range(n), key=lambda i: (P["ships"][i]["s"], P["ships"][i]["e"], i))
            txt = "Sắp tàu theo giờ đến."
        rec.add("info", txt + " Mỗi tàu nhận đội rẻ nhất còn hợp lệ.", order=order, col=col[:], cost=0)
        cost, status = 0.0, "ok"
        for v in order:
            cs = cand_table(P, col, v)
            ok = [c for c in cs if c["ok"]]
            sh = P["ships"][v]
            if not ok:
                rec.add("dead", f"Kẹt: {sh['name']} không còn đội nào hợp lệ. Tham lam không đi tiếp được (chưa chứng minh vô nghiệm).",
                        cur=v, cands=cs, col=col[:], cost=round(cost, 6))
                status = "fail"
                break
            pick = min(ok, key=lambda c: (c["delta"], c["k"]))
            col[v] = pick["k"]
            cost += pick["delta"]
            rec.add("assign", f"{sh['name']} giao cho {P['teams'][pick['k']]['name']}, thêm {fmt(pick['delta'])}.",
                    cur=v, to=pick["k"], cands=cs, col=col[:], cost=round(cost, 6))
        if status == "ok":
            rec.add("done", f"Hoàn tất: tổng {fmt(cost)}.", cur=-1, col=col[:], cost=round(cost, 6))
        else:
            rec.add("done", "Dừng: tham lam không tìm được phân công đầy đủ.", cur=-1, col=col[:], cost=None)
    return result(P, key, name, rec, col, status, t.ms)


def run_bt(P, seed, max_nodes=MAX_NODES):
    n = P["n"]
    rec = Recorder(step_cap(n))
    bud = Budget(max_nodes)
    with Timer() as t:
        viol = hall_violation(P)
        col = [-1] * n
        if viol:
            rec.add("dead", "Kiểm tra trước: " + viol["msg"] + " Kết luận vô nghiệm, không cần quay lui.",
                    cur=viol["ships"][0], ships=viol["ships"], col=col[:], cost=None)
            rec.add("done", "Vô nghiệm (đã chứng minh).", cur=-1, col=col[:], cost=None)
            return result(P, "bt", "Quay lui", rec, col, "infeasible", t.ms, optimal=True, extra={"reason": viol["msg"]})
        order = sorted(range(n), key=lambda i: (P["ships"][i]["s"], P["ships"][i]["e"], i))  # theo giờ đến: thử nghiệm cho thấy tốt hơn "tàu khó trước" trên bài lớn
        minrate = [min(P["teams"][tm]["rate"] for tm in P["elig"][i]) * P["dur"][i] for i in range(n)]
        suffix = [0.0] * (n + 1)
        for idx in range(n - 1, -1, -1):
            suffix[idx] = suffix[idx + 1] + minrate[order[idx]]
        best, best_col = float("inf"), None
        if seed is not None:
            best, best_col = cost_of(P, seed), seed[:]
        rec.add("info", "Quay lui: duyệt tàu theo giờ đến, thử các đội đủ kỹ năng từ rẻ đến đắt. "
                        "Cận = chi phí hiện tại + chi phí rẻ nhất có thể của các tàu còn lại. "
                        + (f"Phương án tốt nhất hiện có bắt đầu từ tham lam: {fmt(best)}." if seed is not None else "Chưa có phương án nào."),
                col=col[:], cost=0, best=None if seed is None else round(best, 6), depth=0)
        cur = [0.0]
        used = [0] * P['m']  # số tàu đã giao cho mỗi đội (để biết đội còn trống)
        stop = [False]

        def go(idx):
            nonlocal best, best_col
            if stop[0] or not bud.tick():
                stop[0] = True
                return
            if idx == n:
                if cur[0] < best - EPS:
                    best, best_col = cur[0], col[:]
                    rec.add("found", f"Tìm được phương án rẻ hơn: {fmt(best)}.", cur=-1, col=col[:], cost=round(cur[0], 6), best=round(best, 6), depth=idx)
                return
            v = order[idx]
            cs = cand_table(P, col, v)
            ok = sorted([c for c in cs if c["ok"]], key=lambda c: (c["delta"], c["k"]))
            if not ok:
                rec.add("dead", f"Ngõ cụt: {P['ships'][v]['name']} không còn đội hợp lệ. Quay lui.",
                        cur=v, cands=cs, col=col[:], cost=round(cur[0], 6), best=None if best == float("inf") else round(best, 6), depth=idx)
                return
            seen_empty = set()
            for c in ok:
                tm = c["k"]
                sig = (tuple(sorted(P["teams"][tm]["skills"])), P["teams"][tm]["rate"])
                if used[tm] == 0:
                    if sig in seen_empty:
                        continue  # hai đội giống hệt và đều chưa có việc: thử một đội là đủ
                    seen_empty.add(sig)
                col[v] = tm
                used[tm] += 1
                cur[0] += c["delta"]
                bound = cur[0] + suffix[idx + 1]
                nm = P["ships"][v]["name"]
                bst = None if best == float("inf") else round(best, 6)
                if bound >= best - EPS:
                    rec.add("prune", f"Bỏ nhánh: {nm} cho {P['teams'][tm]['name']} có cận {fmt(bound)} ≥ {fmt(best)} (phương án tốt nhất hiện có).",
                            cur=v, to=tm, col=col[:], cost=round(cur[0], 6), best=bst, depth=idx + 1)
                else:
                    rec.add("assign", f"Thử {nm} cho {P['teams'][tm]['name']}, tổng tạm {fmt(cur[0])}, cận {fmt(bound)}.",
                            cur=v, to=tm, cands=cs, col=col[:], cost=round(cur[0], 6), best=bst, depth=idx + 1)
                    go(idx + 1)
                cur[0] -= c["delta"]
                used[tm] -= 1
                col[v] = -1
                if stop[0]:
                    return

        go(0)
        tail = f" Dừng vì hết ngân sách {bud.max_nodes} nút." if bud.exhausted else ""
        if best_col is None:
            status = "unknown" if bud.exhausted else "infeasible"
            rec.add("done", ("Chưa tìm được phân công nào" + tail) if bud.exhausted else "Đã duyệt hết mà không có phân công hợp lệ: vô nghiệm.",
                    cur=-1, col=[-1] * n, cost=None)
            return result(P, "bt", "Quay lui", rec, [-1] * n, status, t.ms, bud.nodes, optimal=not bud.exhausted)
        rec.add("done", f"Hoàn tất: tổng {fmt(best)}.{tail}", cur=-1, col=best_col[:], cost=round(best, 6), best=round(best, 6))
    return result(P, "bt", "Quay lui", rec, best_col, "ok", t.ms, bud.nodes, optimal=not bud.exhausted)


def solve_all(ships, teams, pairs, max_nodes=MAX_NODES):
    P = prepare(ships, teams, pairs)
    g1, g2 = run_greedy(P, False), run_greedy(P, True)
    seeds = [g for g in (g1, g2) if g["status"] == "ok"]
    seed = min(seeds, key=lambda g: g["cost"])["col"] if seeds else None
    bt = run_bt(P, seed, max_nodes)
    viol = hall_violation(P)
    return {"n": P["n"], "m": P["m"], "hall": viol, "algos": [g1, g2, bt]}
