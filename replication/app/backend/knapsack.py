"""Module 3: quỹ giờ công = cái túi 0/1.

Tham chiếu: [3] Kleinberg-Tardos §6.4 (quy hoạch động), [4] CLRS §16.2 (phân số đúng, 0/1 sai),
[5] Dantzig 1957 (cận trên nới lỏng phân số), [1] khung quy hoạch động và quay lui.
"""
from core import EPS, Budget, Recorder, Timer, fmt, step_cap, MAX_NODES


def prepare(items, W):
    return {"n": len(items), "items": items, "W": W}


def value_of(P, take):
    return sum(P["items"][i]["v"] for i in range(P["n"]) if take[i])


def weight_of(P, take):
    return sum(P["items"][i]["w"] for i in range(P["n"]) if take[i])


def is_valid(P, take):
    return weight_of(P, take) <= P["W"]


def run_greedy(P):
    rec = Recorder(step_cap(P["n"]))
    with Timer() as t:
        it = P["items"]
        order = sorted(range(P["n"]), key=lambda i: (-it[i]["v"] / it[i]["w"], i))
        take = [False] * P["n"]
        left, val = P["W"], 0.0
        rec.add("info", "Xếp yêu cầu theo giá trị/giờ giảm dần, nhận nếu còn đủ giờ. Cách này đúng với cái túi phân số nhưng có thể sai với 0/1.",
                order=order, take=take[:], left=left, value=0)
        for i in order:
            ratio = it[i]["v"] / it[i]["w"]
            if it[i]["w"] <= left:
                take[i] = True
                left -= it[i]["w"]
                val += it[i]["v"]
                rec.add("assign", f"Nhận {it[i]['name']} (giá trị/giờ = {ratio:.2f}, {it[i]['w']}h). Còn {left}h, tổng giá trị {fmt(val)}.",
                        cur=i, take=take[:], left=left, value=val)
            else:
                rec.add("skip", f"Bỏ {it[i]['name']} ({it[i]['w']}h) vì chỉ còn {left}h.", cur=i, take=take[:], left=left, value=val)
        rec.add("done", f"Hoàn tất: giá trị {fmt(val)}, dùng {P['W'] - left}/{P['W']}h.", cur=-1, take=take[:], left=left, value=val)
    return {"key": "greedy", "name": "Tham lam giá trị/giờ", "steps": rec.steps, "take": take, "value": val,
            "optimal": None, "nodes": 0, "truncated": rec.truncated, "ms": t.ms}


def run_dp(P):
    n, W, it = P["n"], P["W"], P["items"]
    rec = Recorder(n * (W + 1) + n + 10)  # đủ chỗ cho mọi ô (n*(W+1) <= 2500)
    with Timer() as t:
        dp = [[0.0] * (W + 1) for _ in range(n + 1)]
        rec.add("info", "f[i][j] = giá trị lớn nhất khi chỉ xét i yêu cầu đầu và quỹ j giờ: "
                        "f[i][j] = max(f[i-1][j], f[i-1][j-w_i] + v_i). Mỗi bước điền một ô.", i=0, j=0)
        for i in range(1, n + 1):
            w, v = it[i - 1]["w"], it[i - 1]["v"]
            for j in range(W + 1):
                skip = dp[i - 1][j]
                if j >= w and dp[i - 1][j - w] + v > skip:
                    dp[i][j] = dp[i - 1][j - w] + v
                    how = "take"
                    msg = f"f[{i}][{j}] = f[{i-1}][{j-w}] + {fmt(v)} = {fmt(dp[i][j])} (nhận {it[i-1]['name']}, hơn bỏ qua = {fmt(skip)})."
                else:
                    dp[i][j] = skip
                    how = "skip"
                    why = "" if j >= w else f" ({w}h > {j}h nên không nhận được)"
                    msg = f"f[{i}][{j}] = f[{i-1}][{j}] = {fmt(skip)} (bỏ qua {it[i-1]['name']}{why})."
                rec.add("cell", msg, i=i, j=j, val=dp[i][j], how=how)
        take = [False] * n
        j = W
        rec.add("info", f"Truy vết từ ô f[{n}][{W}] = {fmt(dp[n][W])}: nếu f[i][j] khác f[i-1][j] thì yêu cầu i được nhận.", i=n, j=j, trace=True)
        for i in range(n, 0, -1):
            if abs(dp[i][j] - dp[i - 1][j]) > EPS:
                take[i - 1] = True
                rec.add("trace", f"f[{i}][{j}] ≠ f[{i-1}][{j}] nên nhận {it[i-1]['name']}, quỹ còn {j - it[i-1]['w']}h.", i=i, j=j, taken=True)
                j -= it[i - 1]["w"]
            else:
                rec.add("trace", f"f[{i}][{j}] = f[{i-1}][{j}] nên không nhận {it[i-1]['name']}.", i=i, j=j, taken=False)
        rec.add("done", f"Hoàn tất: giá trị {fmt(dp[n][W])}, tối ưu theo quy hoạch động.", take=take[:], value=dp[n][W], i=0, j=j)
    return {"key": "dp", "name": "Quy hoạch động", "steps": rec.steps, "take": take, "value": dp[n][W], "optimal": True,
            "nodes": n * (W + 1), "truncated": rec.truncated, "ms": t.ms}


def frac_bound(items, order, idx, left, val):
    """Cận trên: nhận lần lượt theo giá trị/giờ, phần cuối lấy theo tỉ lệ (Dantzig)."""
    b = val
    for k in range(idx, len(order)):
        it = items[order[k]]
        if it["w"] <= left:
            left -= it["w"]; b += it["v"]
        else:
            b += it["v"] * left / it["w"]
            break
    return b


def run_bt(P, seed_val, max_nodes=MAX_NODES):
    n, W, it = P["n"], P["W"], P["items"]
    rec = Recorder(step_cap(n))
    bud = Budget(max_nodes)
    with Timer() as t:
        order = sorted(range(n), key=lambda i: (-it[i]["v"] / it[i]["w"], i))
        take = [False] * n
        best, best_take = seed_val, None
        rec.add("info", "Quay lui: với mỗi yêu cầu (đã xếp theo giá trị/giờ) thử nhận rồi thử bỏ. "
                        "Cận trên = giá trị hiện tại + nhận tiếp theo tỉ lệ (cho phép nhận một phần). Bỏ nhánh khi cận ≤ phương án tốt nhất hiện có "
                        f"({fmt(best)}, bắt đầu từ tham lam).", take=take[:], left=W, value=0, best=best, depth=0)
        stop = [False]

        def go(idx, left, val):
            nonlocal best, best_take
            if stop[0] or not bud.tick():
                stop[0] = True
                return
            if val > best + EPS:
                best, best_take = val, take[:]
                rec.add("found", f"Phương án tốt hơn: giá trị {fmt(val)}.", take=take[:], left=left, value=val, best=best, depth=idx)
            if idx == n:
                return
            ub = frac_bound(it, order, idx, left, val)
            i = order[idx]
            if ub <= best + EPS:
                rec.add("prune", f"Bỏ nhánh tại {it[i]['name']}: cận trên {fmt(ub)} ≤ {fmt(best)} (phương án tốt nhất hiện có).",
                        cur=i, take=take[:], left=left, value=val, best=best, depth=idx, ub=ub)
                return
            if it[i]["w"] <= left:
                take[i] = True
                rec.add("assign", f"Thử nhận {it[i]['name']} ({it[i]['w']}h, +{fmt(it[i]['v'])}). Cận trên {fmt(ub)}.",
                        cur=i, take=take[:], left=left - it[i]["w"], value=val + it[i]["v"], best=best, depth=idx + 1, ub=ub)
                go(idx + 1, left - it[i]["w"], val + it[i]["v"])
                take[i] = False
                if stop[0]:
                    return
                rec.add("back", f"Quay lui: bỏ {it[i]['name']}, thử không nhận.", cur=i, take=take[:], left=left, value=val, best=best, depth=idx)
            rec.add("assign", f"Thử không nhận {it[i]['name']}.", cur=i, take=take[:], left=left, value=val, best=best, depth=idx + 1, ub=ub, skipped=True)
            go(idx + 1, left, val)

        go(0, W, 0.0)
        tail = f" Dừng vì hết ngân sách {bud.max_nodes} nút, chưa chắc tối ưu." if bud.exhausted else ""
        if best_take is None:
            best_take = P["seed_take"][:]
        rec.add("done", f"Hoàn tất: giá trị {fmt(best)}.{tail}", cur=-1, take=best_take[:], value=best, best=best)
    return {"key": "bt", "name": "Quay lui + cận trên", "steps": rec.steps, "take": best_take, "value": best,
            "optimal": not bud.exhausted, "nodes": bud.nodes, "truncated": rec.truncated, "ms": t.ms}


def solve_all(items, W, max_nodes=MAX_NODES):
    P = prepare(items, W)
    g = run_greedy(P)
    P["seed_take"] = g["take"]
    d = run_dp(P)
    b = run_bt(P, g["value"], max_nodes)
    return {"n": P["n"], "W": W, "algos": [g, d, b]}
