import { useMemo, useState } from 'react'
import { SAMPLES } from './samples.js'
import { useSolve } from './hooks.js'
import { AlgoPicker, CompareTable, Editor, JsonBox, Kpis, Player, Samples, Verdict, col, num, txt, usePlayer } from './ui.jsx'

const fromInput = (inp) => ({ items: inp.items.map((x) => ({ ...x })), C: inp.C })

export default function Bins() {
  const [st, setSt] = useState(() => fromInput(SAMPLES.binpack[0].input))
  const [algo, setAlgo] = useState('ff')

  const { body, errors } = useMemo(() => {
    const errors = []
    if (!st.items.length) errors.push('Thêm ít nhất một lô.')
    if (st.C === '' || !(st.C > 0)) errors.push('Tải trọng một tàu phải dương.')
    st.items.forEach((x, i) => {
      if (!String(x.name).trim()) errors.push(`Dòng ${i + 1}: thiếu tên.`)
      if (x.w === '' || !(x.w > 0) || x.w > st.C) errors.push(`${x.name || 'Dòng ' + (i + 1)}: khối lượng phải trong (0, ${st.C}].`)
    })
    return { errors, body: errors.length ? null : { items: st.items.map((x) => ({ ...x, name: x.name.trim() })), C: st.C } }
  }, [st])

  const { res, err, busy, solved } = useSolve('binpack', body)
  const a = res && res.algos.find((x) => x.key === algo)
  const p = usePlayer(a ? a.steps.length : 1)
  const step = a ? a.steps[p.idx] : { kind: 'info', msg: '' }
  const apply = (inp) => setSt(fromInput(inp))
  const assign = step.bin || (a ? a.bin : [])
  const nb = Math.max(step.n_bins || 0, ...assign.map((b) => b + 1), 1)
  const un = assign.map((b, i) => (b < 0 ? i : -1)).filter((i) => i >= 0)

  return (
    <>
      <Samples list={SAMPLES.binpack} onPick={apply} />
      <div className="main">
        <div className="col">
          <section className="card">
            <div className="card-h"><h2>Các lô container</h2><span>{st.items.length} lô</span></div>
            <div className="card-b">
              <Editor max={60} rows={st.items} setRows={(items) => setSt({ ...st, items })}
                cols={[{ key: 'name', label: 'Lô', w: '1.2fr' }, { key: 'w', label: 'Khối lượng', type: 'number', w: '1fr' }]}
                newRow={(rows) => ({ name: `L${rows.length + 1}`, w: 10 })} />
              <label className="lbl">Tải trọng một tàu C<input className="in" type="number" min={0} value={st.C} onChange={(e) => setSt({ ...st, C: e.target.value === '' ? '' : +e.target.value })} /></label>
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
              <Kpis items={[['Tàu đang dùng', step.n_bins ?? 0], ['Phương án tốt nhất hiện có', step.best ?? '—'], ['Cận dưới ⌈Σw/C⌉', res.lb], ['Kết quả cuối', a.bins]]} />
              <section className="card"><div className="card-h"><h2>Các tàu</h2><span>tải trọng {num(solved.C)}</span></div>
                <div className="card-b">
                  <div className="bins">
                    {Array.from({ length: nb }, (_, b) => {
                      const mem = assign.map((x, i) => (x === b ? i : -1)).filter((i) => i >= 0)
                      const load = mem.reduce((s, i) => s + solved.items[i].w, 0)
                      return (
                        <div className={'bin' + (step.to === b ? ' on' : '')} key={b}>
                          <div className="binbox">
                            {mem.map((i) => (<div key={i} className={'binitem' + (i === step.cur ? ' cur' : '')} title={solved.items[i].name}
                              style={{ height: `${(solved.items[i].w / solved.C) * 100}%`, background: col(b), color: txt(b) }}>{solved.items[i].name}</div>))}
                          </div>
                          <div className="binlbl">Tàu {b + 1}<br /><span>{num(load)}/{num(solved.C)}</span></div>
                        </div>)
                    })}
                  </div>
                  <div className="chips"><span className="cl">Chưa xếp ({un.length}):</span>{un.map((i) => <span key={i} className={'chip' + (i === step.cur ? ' cur' : '')}>{solved.items[i].name} ({num(solved.items[i].w)})</span>)}</div>
                  <p className="legend">Mỗi cột là một tàu, chiều cao khối tỉ lệ với khối lượng. Khối viền đen là lô đang xét.</p>
                </div></section>
              <CompareTable selected={algo} head={['Thuật toán', 'Số tàu', 'Số bước', 'Nút', 'ms', 'Đánh giá']}
                foot={`Cận dưới ⌈Σw/C⌉ = ${res.lb} tàu. Tối ưu nghĩa là bằng cận dưới hoặc quay lui đã duyệt hết.`}
                rows={res.algos.map((x) => ({ key: x.key, cells: [x.name, x.bins, x.steps.length - 1, x.nodes || '—', x.ms.toFixed(2),
                  <Verdict key="v" ok={x.optimal === true ? true : x.key === 'bt' ? false : null} text={x.optimal === true ? 'Tối ưu' : x.key === 'bt' ? 'Chưa chứng minh tối ưu' : 'Chưa chắc tối ưu'} />] }))} />
            </>
          )}
        </div>
      </div>
    </>
  )
}
