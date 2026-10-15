"""Đáp án tham chiếu độc lập với solver: vét cạn và công thức."""
import itertools, math


def set_partitions(n):
    """Mọi cách chia {0..n-1} thành các nhóm (restricted growth string)."""
    def rec(i, a, m):
        if i == n:
            yield a[:]
            return
        for k in range(m + 1):
            a.append(k)
            yield from rec(i + 1, a, max(m, k + 1))
            a.pop()
    yield from rec(0, [], 0)


def berth_opt(ships, pairs, F, r):
    n = len(ships)
    bad = {(min(a, b), max(a, b)) for a, b in pairs if a != b}
    best = None
    for col in set_partitions(n):
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                if col[i] == col[j] and ((ships[i]["s"] < ships[j]["e"] and ships[j]["s"] < ships[i]["e"]) or (i, j) in bad):
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        span = {}
        for i, k in enumerate(col):
            lo, hi = span.get(k, (ships[i]["s"], ships[i]["e"]))
            span[k] = (min(lo, ships[i]["s"]), max(hi, ships[i]["e"]))
        c = sum(F + r * (hi - lo) for lo, hi in span.values())
        if best is None or c < best:
            best = c
    return best


def assign_opt(ships, teams, pairs):
    n, m = len(ships), len(teams)
    bad = {(min(a, b), max(a, b)) for a, b in pairs if a != b}
    best = None
    elig = [[t for t in range(m) if set(ships[i]["need"]) <= set(teams[t]["skills"])] for i in range(n)]
    for col in itertools.product(*elig):
        ok = all(not (col[i] == col[j] and ((ships[i]["s"] < ships[j]["e"] and ships[j]["s"] < ships[i]["e"]) or (i, j) in bad))
                 for i in range(n) for j in range(i + 1, n))
        if ok:
            c = sum(teams[col[i]]["rate"] * (ships[i]["e"] - ships[i]["s"]) for i in range(n))
            best = c if best is None else min(best, c)
    return best


def knap_opt(items, W):
    best = 0
    for mask in range(1 << len(items)):
        w = sum(items[i]["w"] for i in range(len(items)) if mask >> i & 1)
        if w <= W:
            best = max(best, sum(items[i]["v"] for i in range(len(items)) if mask >> i & 1))
    return best


def bins_opt(items, C):
    n = len(items)
    for k in range(1, n + 1):
        loads = [0.0] * k
        def rec(i):
            if i == n:
                return True
            seen = set()
            for b in range(k):
                if loads[b] in seen or loads[b] + items[i]["w"] > C + 1e-9:
                    continue
                seen.add(loads[b])
                loads[b] += items[i]["w"]
                if rec(i + 1):
                    loads[b] -= items[i]["w"]
                    return True
                loads[b] -= items[i]["w"]
            return False
        if rec(0):
            return k
    return n
