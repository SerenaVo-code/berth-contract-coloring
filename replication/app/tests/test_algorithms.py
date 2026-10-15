import random
import pytest
import assign as m2, berth as m1, binpack as m4, knapsack as m3
from oracles import assign_opt, berth_opt, bins_opt, knap_opt

EPS = 1e-6


def rnd_ships(rng, n, span=20):
    out = []
    for i in range(n):
        s = rng.randint(0, span * 2) / 2
        out.append({"name": f"T{i+1}", "s": s, "e": s + rng.randint(1, 8) / 2})
    return out


# ---------------- module 1
@pytest.mark.parametrize("seed", range(30))
def test_berth_vs_bruteforce(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 8)
    ships = rnd_ships(rng, n)
    pairs = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 3))]
    F, r = rng.choice([0, 50, 300]), rng.choice([0, 5, 40])
    res = m1.solve_all(ships, pairs, F, r)
    opt = berth_opt(ships, pairs, F, r)
    P = m1.prepare(ships, pairs, F, r)
    for a in res["algos"]:
        assert m1.is_valid(P, a["col"])
        assert abs(a["cost"] - m1.total_cost(P, a["col"])) < EPS   # số tự báo = số tính lại
        assert a["cost"] >= opt - EPS
    bt = res["algos"][3]
    assert bt["optimal"] and abs(bt["cost"] - opt) < EPS
    assert res["lb"] <= opt + EPS


def test_berth_known_example():
    t = [(17.5, 21.5), (10, 15.5), (18.5, 22.5), (13.5, 17), (14.5, 18.5), (6, 10.5), (16, 20.5), (11, 13.5)]
    ships = [{"name": f"T{i}", "s": a, "e": b} for i, (a, b) in enumerate(t)]
    res = m1.solve_all(ships, [[0, 5], [6, 0]], 500, 40)
    assert [round(a["cost"]) for a in res["algos"]] == [3400, 3340, 3000, 2900]


def test_berth_deterministic():
    rng = random.Random(5)
    ships = rnd_ships(rng, 40)
    a = m1.solve_all(ships, [], 100, 10, max_nodes=3000)
    b = m1.solve_all(ships, [], 100, 10, max_nodes=3000)
    assert [x["cost"] for x in a["algos"]] == [x["cost"] for x in b["algos"]]
    assert [len(x["steps"]) for x in a["algos"]] == [len(x["steps"]) for x in b["algos"]]


def test_berth_touching_ends_do_not_conflict():
    ships = [{"name": "A", "s": 0, "e": 2}, {"name": "B", "s": 2, "e": 4}]
    P = m1.prepare(ships, [], 100, 10)
    assert P["omega"] == 1 and 1 not in P["adj"][0]


# ---------------- module 2
def rnd_assign(rng):
    n, m = rng.randint(1, 6), rng.randint(1, 4)
    sk = ["cẩu", "buộc", "lạnh"]
    ships = [{**s, "need": rng.sample(sk, rng.randint(0, 2))} for s in rnd_ships(rng, n, 8)]
    teams = [{"name": f"Đ{i+1}", "skills": rng.sample(sk, rng.randint(1, 3)), "rate": rng.randint(5, 30)} for i in range(m)]
    pairs = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 2))]
    return ships, teams, pairs


@pytest.mark.parametrize("seed", range(40))
def test_assign_vs_bruteforce(seed):
    ships, teams, pairs = rnd_assign(random.Random(seed))
    res = m2.solve_all(ships, teams, pairs)
    opt = assign_opt(ships, teams, pairs)
    P = m2.prepare(ships, teams, pairs)
    g1, g2, bt = res["algos"]
    if opt is None:
        assert bt["status"] == "infeasible"          # quay lui phải kết luận vô nghiệm
        for g in (g1, g2):
            assert g["status"] == "fail"             # tham lam không thể "tìm ra" nghiệm không tồn tại
        return
    assert bt["status"] == "ok" and bt["optimal"]
    assert abs(bt["cost"] - opt) < EPS
    assert m2.is_valid(P, bt["col"])
    for g in (g1, g2):
        if g["status"] == "ok":
            assert m2.is_valid(P, g["col"]) and g["cost"] >= opt - EPS


def test_assign_hall_detects_without_search():
    ships = [{"name": f"S{i}", "s": 0, "e": 5, "need": ["cẩu"]} for i in range(3)]
    teams = [{"name": "A", "skills": ["cẩu"], "rate": 10}, {"name": "B", "skills": ["cẩu"], "rate": 10}]
    res = m2.solve_all(ships, teams, [])
    assert res["hall"]["kind"] == "hall"
    assert res["algos"][2]["status"] == "infeasible" and res["algos"][2]["nodes"] == 0


# ---------------- module 3
@pytest.mark.parametrize("seed", range(40))
def test_knapsack_vs_bruteforce(seed):
    rng = random.Random(seed)
    items = [{"name": f"Y{i}", "w": rng.randint(1, 15), "v": rng.randint(0, 40)} for i in range(rng.randint(1, 10))]
    W = rng.randint(0, 40)
    res = m3.solve_all(items, W)
    opt = knap_opt(items, W)
    P = m3.prepare(items, W)
    g, dp, bt = res["algos"]
    for a in (g, dp, bt):
        assert m3.is_valid(P, a["take"])
        assert abs(a["value"] - m3.value_of(P, a["take"])) < EPS
        assert a["value"] <= opt + EPS
    assert abs(dp["value"] - opt) < EPS and abs(bt["value"] - opt) < EPS and bt["optimal"]


def test_knapsack_greedy_is_wrong_on_classic():
    items = [{"name": "A", "w": 10, "v": 60}, {"name": "B", "w": 20, "v": 100}, {"name": "C", "w": 30, "v": 120}]
    g, dp, bt = m3.solve_all(items, 50)["algos"]
    assert (g["value"], dp["value"], bt["value"]) == (160, 220, 220)


def test_knapsack_dp_steps_one_per_cell():
    items = [{"name": "A", "w": 2, "v": 3}, {"name": "B", "w": 3, "v": 4}]
    dp = m3.solve_all(items, 5)["algos"][1]
    assert sum(1 for s in dp["steps"] if s["kind"] == "cell") == 2 * 6


# ---------------- module 4
@pytest.mark.parametrize("seed", range(40))
def test_binpack_vs_bruteforce(seed):
    rng = random.Random(seed)
    C = rng.choice([10, 20, 100])
    items = [{"name": f"L{i}", "w": rng.randint(1, C)} for i in range(rng.randint(1, 9))]
    res = m4.solve_all(items, C)
    opt = bins_opt(items, C)
    P = m4.prepare(items, C)
    assert res["lb"] <= opt
    for a in res["algos"]:
        assert m4.is_valid(P, a["bin"])
        assert a["bins"] >= opt
        assert a["bins"] == max(a["bin"]) + 1
    bt = res["algos"][3]
    assert bt["bins"] == opt and bt["optimal"]


def test_binpack_ffd_beats_ff():
    items = [{"name": f"L{i}", "w": w} for i, w in enumerate([3, 7, 3, 7, 4, 6, 4, 6])]  # C=10: tối ưu 4
    r = m4.solve_all(items, 10)
    ff, ffd = r["algos"][0], r["algos"][1]
    assert ffd["bins"] <= ff["bins"]
