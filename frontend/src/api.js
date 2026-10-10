export async function solve(payload) {
  let res
  try {
    res = await fetch('/api/solve', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
  } catch {
    throw new Error('Không kết nối được backend (cổng 8000). Hãy chạy: uvicorn server:app --port 8000')
  }
  if (!res.ok) {
    let d = ''
    try { d = (await res.json()).detail } catch { /* ignore */ }
    throw new Error(typeof d === 'string' && d ? d : `Lỗi backend (${res.status})`)
  }
  return res.json()
}
