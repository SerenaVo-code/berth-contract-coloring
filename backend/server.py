from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from solver import solve_all

app = FastAPI(title="Berth contract coloring demo")
MAX_SHIPS = 200


class Ship(BaseModel):
    name: str
    s: float
    e: float


class SolveIn(BaseModel):
    ships: list[Ship]
    pairs: list[list[int]] = Field(default_factory=list)
    F: float = 100
    r: float = 10


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/solve")
def solve(body: SolveIn):
    n = len(body.ships)
    if not 1 <= n <= MAX_SHIPS:
        raise HTTPException(422, f"Số tàu phải từ 1 đến {MAX_SHIPS}.")
    if body.F < 0 or body.r < 0:
        raise HTTPException(422, "F và r phải không âm.")
    for sh in body.ships:
        if not sh.e > sh.s:
            raise HTTPException(422, f"{sh.name}: giờ rời phải sau giờ đến.")
    for p in body.pairs:
        if len(p) != 2 or not all(0 <= x < n for x in p):
            raise HTTPException(422, "Cặp ràng buộc không hợp lệ.")
    return solve_all([s.model_dump() for s in body.ships], body.pairs, body.F, body.r)


# Chế độ một cổng: nếu đã build frontend (npm run build) thì phục vụ luôn tại "/"
_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=_dist, html=True), name="web")
