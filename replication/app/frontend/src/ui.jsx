import { useEffect, useRef, useState } from 'react'
import { GLOSS, PSEUDO } from './info.js'

export const PALETTE = ['#024D71', '#F99D20', '#683D99', '#25B570', '#2462B5', '#863376', '#5AA7AD', '#555A61']
export const TEXTC = ['#fff', '#542E00', '#fff', '#0D3F26', '#fff', '#fff', '#032938', '#fff']
export const col = (k) => PALETTE[k % PALETTE.length]
export const txt = (k) => TEXTC[k % TEXTC.length]

export const num = (v) => (Number.isInteger(v) ? String(v) : String(Math.round(v * 100) / 100))

/** Phát lại các bước đã tính sẵn: Tiếp, Lùi, tự động, thanh trượt. */
export function usePlayer(len) {
  const [idx, setIdx] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [speed, setSpeed] = useState(600)
  const last = Math.max(0, len - 1)
  useEffect(() => { setIdx(0); setPlaying(false) }, [len])
  useEffect(() => {
    if (!playing) return
    const t = setInterval(() => setIdx((i) => (i >= last ? i : i + 1)), speed)
    return () => clearInterval(t)
  }, [playing, speed, last])
  useEffect(() => { if (playing && idx >= last) setPlaying(false) }, [idx, last, playing])
  return {
    idx: Math.min(idx, last), last, playing, speed, setSpeed,  // kẹp idx: lần vẽ đầu sau khi đổi thuật toán vẫn dùng idx cũ
    go: (i) => { setPlaying(false); setIdx(Math.max(0, Math.min(last, i))) },
    toggle: () => { if (!playing && idx >= last) setIdx(0); setPlaying((p) => !p) },
  }
}

export function Player({ p, step }) {
  return (
    <section className="card">
      <div className="card-h"><h2>Chạy từng bước</h2><span>{p.idx === 0 ? 'Khởi tạo' : `Bước ${p.idx}/${p.last}`}</span></div>
      <div className="card-b">
        <div className="ctl">
          <button className="btn" onClick={() => p.go(0)} disabled={p.idx === 0}>Về đầu</button>
          <button className="btn" onClick={() => p.go(p.idx - 1)} disabled={p.idx === 0}>Lùi</button>
          <button className="btn primary" onClick={() => p.go(p.idx + 1)} disabled={p.idx >= p.last}>Tiếp</button>
          <button className="btn" onClick={p.toggle}>{p.playing ? 'Dừng' : 'Tự động'}</button>
          <select aria-label="Tốc độ" value={p.speed} onChange={(e) => p.setSpeed(+e.target.value)}>
            <option value={1200}>Chậm</option><option value={600}>Vừa</option><option value={200}>Nhanh</option>
          </select>
          <input type="range" min={0} max={p.last} value={p.idx} aria-label="Bước hiện tại" onChange={(e) => p.go(+e.target.value)} />
        </div>
        <div className="msg" aria-live="polite"><span className={'tag ' + step.kind}>{TAG[step.kind] || step.kind}</span>{step.msg}</div>
      </div>
    </section>
  )
}
const TAG = { info: 'Thông tin', assign: 'Thử', back: 'Quay lui', prune: 'Bỏ nhánh', found: 'Tìm được', done: 'Xong', dead: 'Ngõ cụt', skip: 'Bỏ qua', cell: 'Điền ô', trace: 'Truy vết' }

export function Kpis({ items }) {
  return (
    <div className="kpis">
      {items.map(([l, v, cls]) => (
        <div key={l} className="kpi"><span>{l}</span><b className={cls || ''}>{v}</b></div>
      ))}
    </div>
  )
}

export function AlgoPicker({ algos, value, onChange }) {
  return (
    <div className="band">
      <span className="cap">Thuật toán</span>
      <div className="segm" role="radiogroup" aria-label="Thuật toán">
        {algos.map((a) => (
          <label key={a.key}>
            <input type="radio" name="algo" checked={a.key === value} onChange={() => onChange(a.key)} />
            <span>{a.name}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

/** rows: [{name, cells: [..], ok, note}] */
export function CompareTable({ head, rows, selected, foot }) {
  return (
    <section className="card">
      <div className="card-h"><h2>So sánh các thuật toán</h2></div>
      <div className="card-b scroll">
        <table className="tbl">
          <thead><tr>{head.map((h) => <th key={h}>{h}</th>)}</tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.key} className={r.key === selected ? 'sel' : ''}>
                {r.cells.map((c, i) => <td key={i} className={typeof c === 'number' || (typeof c === 'string' && /^[\d.,—\-]+$/.test(c)) ? 'num' : ''}>{c}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
        {foot && <p className="legend">{foot}</p>}
      </div>
    </section>
  )
}

export function Verdict({ ok, text }) {
  const cls = ok === true ? 'ok' : ok === false ? 'warn' : 'idle'
  return <span className={'pill ' + cls}>{text}</span>
}

export function JsonBox({ value, onApply }) {
  const [open, setOpen] = useState(false)
  const [text, setText] = useState('')
  const [err, setErr] = useState('')
  const ref = useRef()
  useEffect(() => { if (open) setText(JSON.stringify(value, null, 1)) }, [open]) // eslint-disable-line
  return (
    <div className="jsonbox">
      <button className="btn" onClick={() => setOpen(!open)}>{open ? 'Đóng JSON' : 'Nhập/xuất JSON'}</button>
      {open && (
        <>
          <p className="hint">Định dạng giống phần <code>input</code> của file trong <code>testcases/</code>: dán vào rồi bấm Áp dụng.</p>
          <textarea ref={ref} className="in" rows={10} value={text} onChange={(e) => setText(e.target.value)} aria-label="JSON dữ liệu" />
          <div className="row">
            <button className="btn primary" onClick={() => { try { onApply(JSON.parse(text)); setErr('') } catch (e) { setErr('JSON không hợp lệ: ' + e.message) } }}>Áp dụng</button>
          </div>
          {err && <div className="alert">{err}</div>}
        </>
      )}
    </div>
  )
}

export function Samples({ list, onPick }) {
  return (
    <div className="band">
      <span className="cap">Dữ liệu mẫu</span>
      {list.map((s) => <button key={s.id} className="btn" onClick={() => onPick(s.input)} title={s.id}>{s.label}</button>)}
    </div>
  )
}

/** Gantt dùng chung: rows = nhãn hàng, bars = [{row, s, e, label, cls, fill, color}] */
export function Gantt({ rows, bars, tmin, tmax, hlRow, band }) {
  const R = Math.max(1, rows.length)
  const span = Math.max(1, tmax - tmin)
  const W = 760, L = 96, Rr = 14, top = 28, rowH = 32, barH = 22, H = top + R * rowH + 6
  const X = (t) => L + ((t - tmin) / span) * (W - L - Rr)
  const tick = [1, 2, 5, 10, 20, 50, 100, 200].find((s) => span / s <= 12) || 500
  const ticks = []
  for (let t = Math.ceil(tmin / tick) * tick; t <= tmax; t += tick) ticks.push(t)
  return (
    <div className="scroll">
      <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Biểu đồ Gantt">
        {hlRow != null && hlRow >= 0 && hlRow < R && <rect className="g-rowhl" x={L} y={top + hlRow * rowH} width={W - L - Rr} height={rowH} />}
        {ticks.map((t) => (<g key={t}><line className="g-grid" x1={X(t)} x2={X(t)} y1={top - 6} y2={top + R * rowH} /><text className="g-tick" x={X(t)} y={top - 12}>{t}h</text></g>))}
        {rows.map((r, i) => (
          <g key={i}>
            <line className="g-sep" x1={L} x2={W - Rr} y1={top + (i + 1) * rowH} y2={top + (i + 1) * rowH} />
            <rect x={6} y={top + i * rowH + rowH / 2 - 6} width={12} height={12} rx={2} fill={col(i)} />
            <text className="g-lbl" x={24} y={top + i * rowH + rowH / 2 + 4}>{r}</text>
          </g>
        ))}
        {band && <rect className="g-band" x={X(band.s)} y={top - 4} width={Math.max(2, X(band.e) - X(band.s))} height={R * rowH + 4} rx={2} />}
        {bars.map((b, i) => {
          const x = X(b.s), w = Math.max(2, X(b.e) - X(b.s)), y = top + b.row * rowH + (rowH - barH) / 2
          return (
            <g key={i}>
              <title>{`${b.label}: ${num(b.s)}h–${num(b.e)}h`}</title>
              <rect className={'g-bar ' + (b.cls || '')} x={x} y={y} width={w} height={barH} rx={4} fill={col(b.row)} />
              {w >= b.label.length * 6.8 + 10 && <text className="g-bt" x={x + 6} y={y + barH / 2 + 4} fill={txt(b.row)}>{b.label}</text>}
            </g>
          )
        })}
      </svg>
    </div>
  )
}

export function Cands({ cands, picked, nameOf, unit }) {
  if (!cands) return null
  return (
    <section className="card">
      <div className="card-h"><h2>Các lựa chọn của bước này</h2><span>{unit}</span></div>
      <div className="card-b scroll">
        <table className="tbl">
          <thead><tr><th>Lựa chọn</th><th>Hợp lệ</th><th className="num">Chi phí tăng thêm</th><th>Lý do</th></tr></thead>
          <tbody>
            {cands.map((c) => (
              <tr key={c.k} className={c.k === picked ? 'sel' : ''}>
                <td>{nameOf(c.k)}{c.k === picked ? ' ←' : ''}</td>
                <td>{c.ok ? <Verdict ok text="Được" /> : <Verdict ok={false} text="Loại" />}</td>
                <td className="num">{c.delta == null ? '—' : num(c.delta)}</td>
                <td>{c.why}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

/** Hàng cố định phía trên: bảng dữ liệu nhập. cols = [{key, label, type, w}] */
export function Editor({ rows, setRows, cols, newRow, max }) {
  const set = (i, k, v) => setRows(rows.map((r, j) => (j === i ? { ...r, [k]: v } : r)))
  return (
    <div>
      <div className="edit-head" style={{ gridTemplateColumns: gridOf(cols) }}>{cols.map((c) => <span key={c.key}>{c.label}</span>)}<span /></div>
      <div className="edit-body">
        {rows.map((r, i) => (
          <div className="edit-row" key={i} style={{ gridTemplateColumns: gridOf(cols) }}>
            {cols.map((c) => (
              <input key={c.key} className="in" aria-label={`${c.label} dòng ${i + 1}`} type={c.type === 'number' ? 'number' : 'text'} step={c.step || 'any'}
                value={c.list ? (r[c.key] || []).join(', ') : r[c.key] ?? ''}
                onChange={(e) => set(i, c.key, c.list ? e.target.value.split(',').map((x) => x.trim()).filter(Boolean) : c.type === 'number' ? (e.target.value === '' ? '' : +e.target.value) : e.target.value)} />
            ))}
            <button className="x" aria-label={`Xóa dòng ${i + 1}`} onClick={() => setRows(rows.filter((_, j) => j !== i))}>×</button>
          </div>
        ))}
      </div>
      <button className="btn" disabled={rows.length >= max} onClick={() => setRows([...rows, newRow(rows)])}>Thêm dòng</button>
    </div>
  )
}
const gridOf = (cols) => cols.map((c) => c.w || '1fr').join(' ') + ' 28px'

/** Mã giả của thuật toán đang chọn, dòng đang chạy được tô sáng theo loại bước. */
export function Pseudo({ mod, algo, kind }) {
  const ps = PSEUDO[mod] && PSEUDO[mod][algo]
  if (!ps) return null
  const on = ps.map[kind]
  return (
    <section className="card">
      <div className="card-h"><h2>Mã giả đang chạy</h2><span>dòng sáng là bước hiện tại</span></div>
      <pre className="pseudo" aria-label="Mã giả">{ps.lines.map((l, i) => <div key={i} className={i === on ? 'pl on' : 'pl'}>{l || ' '}</div>)}</pre>
    </section>
  )
}

export function Glossary() {
  return (
    <details className="card gloss">
      <summary>Giải thích thuật ngữ</summary>
      <dl>{GLOSS.map(([t, d]) => (<div key={t}><dt>{t}</dt><dd>{d}</dd></div>))}</dl>
    </details>
  )
}
