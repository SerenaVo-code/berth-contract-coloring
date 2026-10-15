import { useMemo, useState } from 'react'
import { SAMPLES } from './samples.js'
import { useSolve, parsePairs, pairsToText } from './hooks.js'
import { CX } from './info.js'
import { AlgoPicker, Cands, CompareTable, Editor, Gantt, Glossary, JsonBox, Kpis, Player, Pseudo, Samples, Verdict, num, usePlayer } from './ui.jsx'

const fromInput = (inp) => ({
  ships: inp.ships.map((s) => ({ ...s, need: [...s.need] })), teams: inp.teams.map((t) => ({ ...t, skills: [...t.skills] })),
  pairsText: pairsToText(inp.pairs, inp.ships.map((s) => s.name)),
})
const STATUS = { ok: 'Có phân công', fail: 'Kẹt (chưa chứng minh vô nghiệm)', infeasible: 'Vô nghiệm', unknown: 'Chưa kết luận' }

export default function Assign() {
  const [st, setSt] = useState(() => fromInput(SAMPLES.assign[0].input))
  const [algo, setAlgo] = useState('greedy')

  const { body, errors, warns } = useMemo(() => {
    const errors = [], seen = new Set()
    st.ships.forEach((s, i) => {
      const nm = String(s.name).trim()
      if (!nm) errors.push(`Tàu dòng ${i + 1}: thiếu tên.`)
      else if (/[-,;]/.test(nm)) errors.push(`Tàu "${nm}": tên không được chứa - , ;`)
      else if (seen.has(nm)) errors.push(`Tên tàu "${nm}" bị trùng.`)
      seen.add(nm)
      if (s.s === '' || s.e === '' || !(s.e > s.s)) errors.push(`Tàu ${nm || i + 1}: giờ rời phải lớn hơn giờ đến.`)
    })
    st.teams.forEach((t, i) => { if (!String(t.name).trim()) errors.push(`Đội dòng ${i + 1}: thiếu tên.`); if (t.rate === '' || t.rate < 0) errors.push(`Đội ${t.name || i + 1}: đơn giá phải không âm.`) })
    if (!st.ships.length) errors.push('Thêm ít nhất một tàu.')
    if (!st.teams.length) errors.push('Thêm ít nhất một đội.')
    const { pairs, warns } = parsePairs(st.pairsText, st.ships.map((s) => s.name))
    return { errors, warns, body: errors.length ? null : { ships: st.ships.map((s) => ({ ...s, name: s.name.trim() })), teams: st.teams, pairs } }
  }, [st])

  const { res, err, busy, solved } = useSolve('assign', body)
  const a = res && res.algos.find((x) => x.key === algo)
  const p = usePlayer(a ? a.steps.length : 1)
  const step = a ? a.steps[p.idx] : { kind: 'info', msg: '' }
  const apply = (inp) => setSt(fromInput(inp))
  const sh = solved ? solved.ships : []

  return (
    <>
      <Samples list={SAMPLES.assign} onPick={apply} />
      <div className="main">
        <div className="col">
          <section className="card">
            <div className="card-h"><h2>Danh sách tàu</h2><span>{st.ships.length} tàu</span></div>
            <div className="card-b"><Editor max={60} rows={st.ships} setRows={(ships) => setSt({ ...st, ships })}
              cols={[{ key: 'name', label: 'Tàu', w: '0.8fr' }, { key: 's', label: 'Đến', type: 'number', step: 0.5, w: '0.6fr' }, { key: 'e', label: 'Rời', type: 'number', step: 0.5, w: '0.6fr' }, { key: 'need', label: 'Kỹ năng cần (cách nhau phẩy)', list: true, w: '1.4fr' }]}
              newRow={(rows) => ({ name: `S${rows.length + 1}`, s: 0, e: 4, need: [] })} /></div>
          </section>
          <section className="card">
            <div className="card-h"><h2>Đội phục vụ</h2><span>{st.teams.length} đội</span></div>
            <div className="card-b"><Editor max={12} rows={st.teams} setRows={(teams) => setSt({ ...st, teams })}
              cols={[{ key: 'name', label: 'Đội', w: '0.8fr' }, { key: 'skills', label: 'Kỹ năng (cách nhau phẩy)', list: true, w: '1.6fr' }, { key: 'rate', label: 'Giá/giờ', type: 'number', w: '0.6fr' }]}
              newRow={(rows) => ({ name: `Đội ${rows.length + 1}`, skills: [], rate: 10 })} /></div>
          </section>
          <section className="card">
            <div className="card-h"><h2>Ràng buộc phụ</h2></div>
            <div className="card-b">
              <label className="lbl">Cặp tàu không được chung đội (dạng A-B, cách nhau dấu phẩy)
                <textarea className="in" value={st.pairsText} onChange={(e) => setSt({ ...st, pairsText: e.target.value })} placeholder="Ví dụ: S1-S3" /></label>
              <p className="hint">Hai tàu trùng giờ luôn không chung đội. Chi phí = Σ giá/giờ của đội × thời gian cập.</p>
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
              {res.hall && <div className="alert warn" role="status"><b>Kiểm tra điều kiện cần:</b> {res.hall.msg}</div>}
              <AlgoPicker algos={res.algos} value={algo} onChange={setAlgo} />
              <Player p={p} step={step} />
              <Pseudo mod="assign" algo={algo} kind={step.kind} />
              <Kpis items={[['Chi phí tạm thời', step.cost != null ? num(step.cost) : '—'], ['Phương án tốt nhất hiện có', step.best != null ? num(step.best) : '—'],
                ['Đã giao', `${step.col.filter((c) => c >= 0).length}/${sh.length}`], ['Kết quả cuối', a.status === 'ok' ? num(a.cost) : 'Không có']]} />
              <Cands cands={step.cands} picked={step.to} nameOf={(k) => solved.teams[k].name} unit="đội nào nhận được tàu đang xét" />
              <section className="card">
                <div className="card-h"><h2>Lịch phân công</h2></div>
                <div className="card-b">
                  <Gantt rows={solved.teams.map((t) => t.name)} hlRow={step.to}
                    tmin={Math.floor(Math.min(...sh.map((x) => x.s)))} tmax={Math.ceil(Math.max(...sh.map((x) => x.e)))}
                    band={step.cur >= 0 ? { s: sh[step.cur].s, e: sh[step.cur].e } : null}
                    bars={step.col.map((k, i) => (k >= 0 ? { row: k, s: sh[i].s, e: sh[i].e, label: sh[i].name, cls: i === step.cur ? 'cur' : '' } : null)).filter(Boolean)} />
                  <p className="legend">Hàng là đội, thanh là tàu được giao. Khung nét đứt xanh là giờ của tàu đang xét.</p>
                </div>
              </section>
              <CompareTable selected={algo} head={['Thuật toán', 'Kết quả', 'Chi phí', 'Số bước', 'Nút', 'ms', 'Độ phức tạp', 'Đánh giá']}
                foot="Tham lam có thể kẹt dù bài có nghiệm. Quay lui kết luận vô nghiệm chỉ khi đã duyệt hết hoặc kiểm tra điều kiện cần (Hall) thất bại."
                rows={res.algos.map((x) => ({ key: x.key, cells: [x.name, STATUS[x.status], x.cost != null ? num(x.cost) : '—', x.steps.length - 1, x.nodes || '—', x.ms.toFixed(2), CX.assign[x.key],
                  <Verdict key="v" ok={x.optimal === true ? true : x.optimal === false ? false : null} text={x.optimal === true ? (x.status === 'ok' ? 'Tối ưu' : 'Đã chứng minh') : x.optimal === false ? 'Chưa chứng minh tối ưu' : '—'} />] }))} />
              <Glossary />
            </>
          )}
        </div>
      </div>
    </>
  )
}
