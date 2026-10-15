import { useMemo, useState } from 'react'
import { SAMPLES } from './samples.js'
import { useSolve } from './hooks.js'
import { AlgoPicker, CompareTable, Editor, JsonBox, Kpis, Player, Samples, Verdict, num, usePlayer } from './ui.jsx'

const fromInput = (inp) => ({ items: inp.items.map((x) => ({ ...x })), W: inp.W })

export default function Knap() {
  const [st, setSt] = useState(() => fromInput(SAMPLES.knapsack[0].input))
  const [algo, setAlgo] = useState('greedy')

  const { body, errors } = useMemo(() => {
    const errors = [], n = st.items.length
    if (!n) errors.push('Thêm ít nhất một yêu cầu.')
    if (n > 25) errors.push('Tối đa 25 yêu cầu.')
    st.items.forEach((x, i) => {
      if (!String(x.name).trim()) errors.push(`Dòng ${i + 1}: thiếu tên.`)
      if (!Number.isInteger(x.w) || x.w < 1) errors.push(`${x.name || 'Dòng ' + (i + 1)}: số giờ phải là số nguyên ≥ 1.`)
      if (x.v === '' || x.v < 0) errors.push(`${x.name || 'Dòng ' + (i + 1)}: giá trị phải ≥ 0.`)
    })
    if (!Number.isInteger(st.W) || st.W < 0 || st.W > 200) errors.push('Quỹ giờ phải là số nguyên từ 0 đến 200.')
    else if (n * (st.W + 1) > 2500) errors.push(`Số yêu cầu × (quỹ + 1) = ${n * (st.W + 1)} vượt 2500 ô của bảng quy hoạch động.`)
    return { errors, body: errors.length ? null : { items: st.items.map((x) => ({ ...x, name: x.name.trim() })), W: st.W } }
  }, [st])

  const { res, err, busy, solved } = useSolve('knapsack', body)
  const a = res && res.algos.find((x) => x.key === algo)
  const p = usePlayer(a ? a.steps.length : 1)
  const step = a ? a.steps[p.idx] : { kind: 'info', msg: '' }
  const apply = (inp) => setSt(fromInput(inp))

  // Bảng quy hoạch động dựng lại từ các bước 'cell' tính đến bước hiện tại.
  const table = useMemo(() => {
    if (!a || a.key !== 'dp') return null
    const n = solved.items.length, W = solved.W
    const t = Array.from({ length: n + 1 }, () => Array(W + 1).fill(null))
    for (let j = 0; j <= W; j++) t[0][j] = 0
    for (let k = 1; k <= p.idx; k++) { const s = a.steps[k]; if (s.kind === 'cell') t[s.i][s.j] = s.val }
    return t
  }, [a, p.idx, solved])

  const taken = step.take || (step.kind === 'done' ? a.take : null)
  return (
    <>
      <Samples list={SAMPLES.knapsack} onPick={apply} />
      <div className="main">
        <div className="col">
          <section className="card">
            <div className="card-h"><h2>Yêu cầu tăng ca</h2><span>{st.items.length} yêu cầu</span></div>
            <div className="card-b">
              <Editor max={25} rows={st.items} setRows={(items) => setSt({ ...st, items })}
                cols={[{ key: 'name', label: 'Yêu cầu', w: '1.2fr' }, { key: 'w', label: 'Giờ', type: 'number', step: 1, w: '0.7fr' }, { key: 'v', label: 'Giá trị', type: 'number', w: '0.7fr' }]}
                newRow={(rows) => ({ name: `Y${rows.length + 1}`, w: 5, v: 10 })} />
              <label className="lbl">Quỹ giờ công W<input className="in" type="number" min={0} max={200} value={st.W} onChange={(e) => setSt({ ...st, W: e.target.value === '' ? '' : +e.target.value })} /></label>
              {errors.length > 0 && <div className="alert" role="alert">{errors.map((e) => <div key={e}>{e}</div>)}</div>}
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
              <Kpis items={[['Quỹ còn lại', step.left != null ? step.left + 'h' : '—'], ['Giá trị tạm thời', step.value != null ? num(step.value) : '—'],
                ['Phương án tốt nhất hiện có', step.best != null ? num(step.best) : '—'], ['Kết quả cuối', num(a.value)]]} />
              {a.key === 'dp' ? (
                <section className="card"><div className="card-h"><h2>Bảng quy hoạch động f[i][j]</h2><span>hàng i = số yêu cầu xét, cột j = quỹ giờ</span></div>
                  <div className="card-b scroll"><table className="dp"><thead><tr><th></th>{Array.from({ length: solved.W + 1 }, (_, j) => <th key={j}>{j}</th>)}</tr></thead>
                    <tbody>{table.map((row, i) => (<tr key={i}><th title={i ? solved.items[i - 1].name : ''}>{i === 0 ? '0' : solved.items[i - 1].name}</th>
                      {row.map((v, j) => <td key={j} className={(step.i === i && step.j === j ? 'now ' : '') + (step.kind === 'trace' && step.i === i && step.j === j ? 'tr' : '')}>{v == null ? '' : num(v)}</td>)}</tr>))}</tbody></table></div></section>
              ) : null}
              <section className="card"><div className="card-h"><h2>Các yêu cầu</h2><span>{solved.items.length} yêu cầu, quỹ {solved.W}h</span></div>
                <div className="card-b scroll"><table className="tbl"><thead><tr><th>Yêu cầu</th><th className="num">Giờ</th><th className="num">Giá trị</th><th className="num">Giá trị/giờ</th><th>Trạng thái</th></tr></thead>
                  <tbody>{solved.items.map((x, i) => (<tr key={i} className={step.cur === i ? 'sel' : ''}><td>{x.name}</td><td className="num">{x.w}</td><td className="num">{num(x.v)}</td><td className="num">{(x.v / x.w).toFixed(2)}</td>
                    <td>{taken ? (taken[i] ? <Verdict ok text="Nhận" /> : <Verdict text="Không nhận" />) : '—'}</td></tr>))}</tbody></table>
                  <div className="barwrap" aria-label="Quỹ giờ đã dùng"><div className="barfill" style={{ width: `${solved.W ? ((solved.W - (step.left ?? solved.W)) / solved.W) * 100 : 0}%` }} /></div>
                  <p className="legend">Thanh cho thấy tỉ lệ quỹ giờ đã dùng ở bước hiện tại.</p></div></section>
              <CompareTable selected={algo} head={['Thuật toán', 'Giá trị', 'Số bước', 'Nút', 'ms', 'Đánh giá']}
                foot="Tham lam theo giá trị/giờ có thể sai với cái túi 0/1. Quy hoạch động luôn tối ưu. Quay lui dùng cận trên nới lỏng phân số để bỏ nhánh."
                rows={res.algos.map((x) => ({ key: x.key, cells: [x.name, num(x.value), x.steps.length - 1, x.nodes || '—', x.ms.toFixed(2),
                  <Verdict key="v" ok={x.optimal === true ? true : x.optimal === false ? false : num(x.value) === num(res.algos[1].value) ? true : false}
                    text={x.optimal === true ? 'Tối ưu' : x.optimal === false ? 'Chưa chứng minh tối ưu' : num(x.value) === num(res.algos[1].value) ? 'Trùng tối ưu (do may mắn)' : `Kém tối ưu ${num(res.algos[1].value - x.value)}`} />] }))} />
            </>
          )}
        </div>
      </div>
    </>
  )
}
