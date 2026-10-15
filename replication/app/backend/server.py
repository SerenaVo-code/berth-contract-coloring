from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import assign as m2
import berth as m1
import binpack as m4
import knapsack as m3

app = FastAPI(title="Điều phối cảng (bản dựng lại)")


def bad(msg):
    raise HTTPException(422, msg)


def check_pairs(pairs, n):
    for p in pairs:
        if len(p) != 2 or not all(0 <= x < n for x in p):
            bad("Cặp ràng buộc không hợp lệ.")


class Ship(BaseModel):
    name: str
    s: float
    e: float


class BerthIn(BaseModel):
    ships: list[Ship]
    pairs: list[list[int]] = Field(default_factory=list)
    F: float = 100
    r: float = 10


@app.post("/api/berth")
def berth(b: BerthIn):
    n = len(b.ships)
    if not 1 <= n <= 200:
        bad("Số tàu phải từ 1 đến 200.")
    if b.F < 0 or b.r < 0:
        bad("F và r phải không âm.")
    for s in b.ships:
        if not s.e > s.s:
            bad(f"{s.name}: giờ rời phải sau giờ đến.")
    check_pairs(b.pairs, n)
    return m1.solve_all([s.model_dump() for s in b.ships], b.pairs, b.F, b.r)


class AShip(Ship):
    need: list[str] = Field(default_factory=list)


class Team(BaseModel):
    name: str
    skills: list[str] = Field(default_factory=list)
    rate: float


class AssignIn(BaseModel):
    ships: list[AShip]
    teams: list[Team]
    pairs: list[list[int]] = Field(default_factory=list)


@app.post("/api/assign")
def assign(b: AssignIn):
    n, m = len(b.ships), len(b.teams)
    if not (1 <= n <= 60 and 1 <= m <= 12):
        bad("Cần 1–60 tàu và 1–12 đội.")
    for s in b.ships:
        if not s.e > s.s:
            bad(f"{s.name}: giờ rời phải sau giờ đến.")
    if any(t.rate < 0 for t in b.teams):
        bad("Đơn giá phải không âm.")
    check_pairs(b.pairs, n)
    return m2.solve_all([s.model_dump() for s in b.ships], [t.model_dump() for t in b.teams], b.pairs)


class KItem(BaseModel):
    name: str
    w: int
    v: float


class KnapIn(BaseModel):
    items: list[KItem]
    W: int


@app.post("/api/knapsack")
def knapsack(b: KnapIn):
    n = len(b.items)
    if not 1 <= n <= 25:
        bad("Cần 1–25 yêu cầu.")
    if not 0 <= b.W <= 200 or n * (b.W + 1) > 2500:
        bad("Quỹ giờ từ 0 đến 200 và số yêu cầu × (quỹ + 1) tối đa 2500 ô.")
    for i in b.items:
        if i.w < 1 or i.v < 0:
            bad(f"{i.name}: số giờ phải nguyên ≥ 1 và giá trị ≥ 0.")
    return m3.solve_all([i.model_dump() for i in b.items], b.W)


class BItem(BaseModel):
    name: str
    w: float


class BinIn(BaseModel):
    items: list[BItem]
    C: float


@app.post("/api/binpack")
def binpack(b: BinIn):
    n = len(b.items)
    if not 1 <= n <= 60:
        bad("Cần 1–60 lô container.")
    if b.C <= 0:
        bad("Tải trọng phải dương.")
    for i in b.items:
        if not 0 < i.w <= b.C:
            bad(f"{i.name}: khối lượng phải trong (0, {b.C}].")
    return m4.solve_all([i.model_dump() for i in b.items], b.C)


_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=_dist, html=True), name="web")
