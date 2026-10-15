import { useEffect, useMemo, useState } from 'react'
import { post } from './api.js'

/** Gọi API khi dữ liệu hợp lệ thay đổi (đợi 350 ms sau lần sửa cuối). */
export function useSolve(path, body) {
  const [res, setRes] = useState(null)
  const [solved, setSolved] = useState(null)  // dữ liệu đã dùng để ra `res`: giao diện vẽ kết quả theo đúng dữ liệu này
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const key = useMemo(() => (body ? JSON.stringify(body) : ''), [body])
  useEffect(() => {
    if (!key) { setRes(null); setSolved(null); setErr(''); return }
    let dead = false
    setBusy(true)
    const t = setTimeout(() => {
      post(path, JSON.parse(key))
        .then((r) => { if (!dead) { setRes(r); setSolved(JSON.parse(key)); setErr('') } })
        .catch((e) => { if (!dead) { setRes(null); setSolved(null); setErr(e.message) } })
        .finally(() => { if (!dead) setBusy(false) })
    }, 350)
    return () => { dead = true; clearTimeout(t) }
  }, [key, path])
  return { res, err, busy, solved }
}

/** "A-B, C-D" theo tên -> cặp chỉ số. Trả cả cảnh báo cho cặp bị bỏ qua. */
export function parsePairs(text, names) {
  const pairs = [], warns = []
  const idx = new Map(names.map((n, i) => [n.trim(), i]))
  text.split(/[,;\n]+/).map((t) => t.trim()).filter(Boolean).forEach((tok) => {
    const p = tok.split('-').map((x) => x.trim())
    if (p.length !== 2) return warns.push(`Bỏ qua "${tok}": cần dạng A-B.`)
    if (!idx.has(p[0]) || !idx.has(p[1])) return warns.push(`Bỏ qua "${tok}": không có tên đó.`)
    if (p[0] === p[1]) return warns.push(`Bỏ qua "${tok}": hai tên trùng nhau.`)
    pairs.push([idx.get(p[0]), idx.get(p[1])])
  })
  return { pairs, warns }
}

export const pairsToText = (pairs, names) => (pairs || []).filter(([a, b]) => a !== b).map(([a, b]) => `${names[a]}-${names[b]}`).join(', ')
