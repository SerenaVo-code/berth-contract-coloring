import { useMemo, useState } from 'react'
import { SAMPLES } from './samples.js'
import { useSolve, parsePairs, pairsToText } from './hooks.js'
import { CX } from './info.js'
import { AlgoPicker, Cands, CompareTable, Editor, Gantt, Glossary, JsonBox, Kpis, Player, Pseudo, Samples, Verdict, col, num, txt, usePlayer } from './ui.jsx'

const fromInput = (inp) => ({
  ships: inp.ships.map((s) => ({ ...s })), F: inp.F, r: inp.r,
  pairsText: pairsToText(inp.pairs, inp.ships.map((s) => s.name)),
})

export default function Berth() {
  const [st, setSt] = useState(() => fromInput(SAMPLES.berth[0].input))
  const [algo, setAlgo] = useState('greedy')
  const [tab, setTab] = useState('gantt')

  const { body, errors, warns } = useMemo(() => {
    const errors = [], names = new Set()
    st.ships.forEach((s, i) => {
      const nm = String(s.name).trim()
      if (!nm) errors.push(`Dòng ${i + 1}: thiếu tên tàu.`)
      else if (/[-,;]/.test(nm)) errors.push(`Tàu "${nm}": tên không được chứa - , ;`)
      else if (names.has(nm)) errors.push(`Tên "${nm}" bị trùng.`)
      names.add(nm)
      if (s.s === '' || s.e === '' || !(s.e > s.s)) errors.push(`Tàu ${nm || i + 1}: giờ rời phải lớn hơn giờ đến.`)
    })
    if (st.F === '' || st.r === '' || st.F < 0 || st.r < 0) errors.push('F và r phải là số không âm.')
    if (!st.ships.length) errors.push('Thêm ít nhất một tàu.')
    const { pairs, warns } = parsePairs(st.pairsText, st.ships.map((s) => s.name))
    return { errors, warns, body: errors.length ? null : { ships: st.ships.map((s) => ({ name: s.name.trim(), s: s.s, e: s.e })), pairs, F: st.F, r: st.r } }
  }, [st])

  const { res, err, busy, solved } = useSolve('berth', body)
  const a = res && res.algos.find((x) => x.key === algo)
  const p = usePlayer(a ? a.steps.length : 1)
  const step = a ? a.steps[p.idx] : { kind: 'info', msg: '' }
  const apply = (inp) => setSt(fromInput(inp))

  return (
    <>
      <Samples list={SAMPLES.berth} onPick={apply} />
      <div className="main">
        <div className="col">
          <section className="card">
            <div className="card-h"><h2>Danh sách tàu</h2><span>{st.ships.length} tàu</span></div>
            <div className="card-b">
              <Editor max={200} rows={st.ships} setRows={(ships) => setSt({ ...st, ships })}
                cols={[{ key: 'name', label: 'Tàu', w: '1.2fr' }, { key: 's', label: 'Đến (giờ)', type: 'number', step: 0.5, w: '0.9fr' }, { key: 'e', label: 'Rời (giờ)', type: 'number', step: 0.5, w: '0.9fr' }]}
                newRow={(rows) => { const last = rows.length ? rows[rows.length - 1].e : 0; return { name: `T${rows.length + 1}`, s: last || 0, e: (last || 0) + 4 } }} />
            </div>
          </section>
          <section className="card">
            <div className="card-h"><h2>Giá thuê và ràng buộc</h2></div>
            <div className="card-b">
              <div className="two">
                <label className="lbl">Phí cố định F mỗi hợp đồng<input className="in" type="number" min={0} value={st.F} onChange={(e) => setSt({ ...st, F: e.target.value === '' ? '' : +e.target.value })} /></label>
                <label className="lbl">Đơn giá r mỗi giờ<input className="in" type="number" min={0} value={st.r} onChange={(e) => setSt({ ...st, r: e.target.value === '' ? '' : +e.target.value })} /></label>
              </div>
              <p className="hint">Chi phí một hợp đồng = F + r × (giờ rời cuối − giờ đến đầu), tính cả giờ trống giữa các tàu.</p>
              <label className="lbl">Cặp tàu cấm chung hợp đồng (dạng A-B, cách nhau dấu phẩy)
                <textarea className="in" value={st.pairsText} onChange={(e) => setSt({ ...st, pairsText: e.target.value })} placeholder="Ví dụ: T2-T5, T3-T6" /></label>
              {errors.length > 0 && <div className="alert" role="alert">{errors.map((e) => <div key={e}>{e}</div>)}</div>}
              {warns.length > 0 && <div className="alert warn">{warns.map((e) => <div key={e}>{e}</div>)}</div>}
              {err && <div className="alert" role="alert">{err}</div>}
              <JsonBox value={{ ...body }} onApply={apply} />
            </div>
          </section>
        </div>
        <div className="col">
          {!a ? <section className="card empty">{busy ? 'Đang tính…' : 'Sửa các lỗi bên trái để chạy thuật toán.'}</section> : (
            <>
              <AlgoPicker algos={res.algos} value={algo} onChange={setAlgo} />
              <Player p={p} step={step} />
              <Pseudo mod="berth" algo={algo} kind={step.kind} />
              <Kpis items={[
                ['Tổng tạm thời', num(step.cost ?? 0)], ['Phương án tốt nhất hiện có', step.best != null ? num(step.best) : '—'],
                ['Cận dưới', num(res.lb)], ['Hợp đồng đang mở', step.n_contracts ?? 0], ['Kết quả cuối', num(a.cost)],
              ]} />
              <Cands cands={step.cands} picked={step.to} nameOf={(k) => `Hợp đồng ${k + 1}`} unit="chi phí tăng thêm nếu tàu vào hợp đồng đó" />
              <section className="card">
                <div className="tabs inner" role="tablist">
                  {[['gantt', 'Biểu đồ Gantt'], ['graph', 'Đồ thị xung đột'], ['cmp', 'So sánh']].map(([k, n]) => (
                    <button key={k} role="tab" aria-selected={tab === k} onClick={() => setTab(k)}>{n}</button>))}
                </div>
                <div className="card-b">
                  {tab === 'gantt' && <GanttView res={res} a={a} step={step} body={solved} />}
                  {tab === 'graph' && <GraphView body={solved} step={step} />}
                  {tab === 'cmp' && <CompareTable selected={algo} head={['Thuật toán', 'Hợp đồng', 'Tổng chi phí', 'Số bước', 'Nút/lần thử', 'ms', 'Độ phức tạp', 'Đánh giá']}
                    foot={`Cận dưới = ω·F + r·Σ thời gian cập = ${num(res.lb)} (ω = ${res.omega} tàu neo cùng lúc nhiều nhất). Tối ưu nghĩa là bằng cận dưới hoặc quay lui đã duyệt hết.`}
                    rows={res.algos.map((x) => ({ key: x.key, cells: [x.name, x.n_contracts, num(x.cost), x.steps.length - 1, x.nodes || '—', x.ms.toFixed(2), CX.berth[x.key],
                      <Verdict key="v" ok={x.key === 'bt' ? x.optimal : x.optimal ? true : null} text={x.optimal ? 'Tối ưu' : x.key === 'bt' ? 'Chưa chứng minh tối ưu' : 'Chưa chắc tối ưu'} />] }))} />}
                </div>
              </section>
              <Glossary />
            </>
          )}
        </div>
      </div>
    </>
  )
}

function conflicts(body) {
  const sh = body.ships, adj = sh.map(() => new Set())
  sh.forEach((x, i) => sh.forEach((y, j) => { if (i < j && x.s < y.e && y.s < x.e) { adj[i].add(j); adj[j].add(i) } }))
  body.pairs.forEach(([a, b]) => { if (a !== b) { adj[a].add(b); adj[b].add(a) } })
  return adj
}

function GanttView({ res, a, step, body }) {
  const sh = body.ships
  const adj = useMemo(() => conflicts(body), [body])
  const rows = Math.max(1, ...a.steps.map((s) => s.n_contracts || 0), a.n_contracts)
  const hl = (step.kind === 'assign' || step.kind === 'prune') && step.cur >= 0 ? adj[step.cur] : null
  const bars = []
  step.col.forEach((k, i) => { if (k >= 0) bars.push({ row: k, s: sh[i].s, e: sh[i].e, label: sh[i].name, cls: i === step.cur ? 'cur' : hl && hl.has(i) ? 'conf' : '' }) })
  const un = step.col.map((k, i) => (k < 0 ? i : -1)).filter((i) => i >= 0)
  return (
    <>
      <Gantt rows={Array.from({ length: rows }, (_, i) => `Hợp đồng ${i + 1}`)} bars={bars} hlRow={step.to}
        tmin={Math.floor(Math.min(...sh.map((x) => x.s)))} tmax={Math.ceil(Math.max(...sh.map((x) => x.e)))}
        band={step.cur >= 0 ? { s: sh[step.cur].s, e: sh[step.cur].e } : null} />
      <div className="chips"><span className="cl">Chưa xếp ({un.length}):</span>{un.map((i) => <span key={i} className={'chip' + (i === step.cur ? ' cur' : '')}>{sh[i].name}</span>)}</div>
      <p className="legend">Hàng là hợp đồng, thanh là tàu. Khung nét đứt xanh là khoảng giờ của tàu đang xét; viền đỏ là tàu đã xếp nhưng xung đột với nó.</p>
    </>
  )
}

function GraphView({ body, step }) {
  const n = body.ships.length
  const adj = useMemo(() => conflicts(body), [body])
  if (n > 40) return <p className="legend">Có {n} tàu nên không vẽ đồ thị (giới hạn 40 tàu để dễ nhìn).</p>
  const S = 380, rad = S / 2 - 32, nr = n > 24 ? 11 : n > 14 ? 13 : 16
  const pos = body.ships.map((_, i) => { const t = -Math.PI / 2 + (2 * Math.PI * i) / n; return [S / 2 + rad * Math.cos(t), S / 2 + rad * Math.sin(t)] })
  const edges = []
  adj.forEach((set, i) => set.forEach((j) => { if (i < j) edges.push([i, j]) }))
  return (
    <>
      <svg className="graph" viewBox={`0 0 ${S} ${S}`} role="img" aria-label="Đồ thị xung đột">
        {edges.map(([i, j]) => <line key={i + '-' + j} className={'gedge' + (step.cur === i || step.cur === j ? ' hl' : '')} x1={pos[i][0]} y1={pos[i][1]} x2={pos[j][0]} y2={pos[j][1]} />)}
        {body.ships.map((s, i) => { const c = step.col[i]; return (
          <g key={i}>
            <circle className="gnode" cx={pos[i][0]} cy={pos[i][1]} r={nr} style={c >= 0 ? { fill: col(c), stroke: 'none' } : null}><title>{s.name}{c >= 0 ? ` (hợp đồng ${c + 1})` : ' (chưa xếp)'}</title></circle>
            <text className="gnode-t" x={pos[i][0]} y={pos[i][1]} fill={c >= 0 ? txt(c) : undefined}>{s.name.slice(0, 4)}</text>
          </g>) })}
        {step.cur >= 0 && <circle className="gring" cx={pos[step.cur][0]} cy={pos[step.cur][1]} r={nr + 4} />}
      </svg>
      <p className="legend">Màu đỉnh là hợp đồng. Nét xanh đậm là các cạnh của tàu đang xét. Cạnh gồm cả xung đột giờ và cặp cấm.</p>
    </>
  )
}
