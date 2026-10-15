export async function post(path, body) {
  const r = await fetch('/api/' + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!r.ok) {
    let m = 'Lỗi ' + r.status
    try {
      const j = await r.json()
      m = typeof j.detail === 'string' ? j.detail : JSON.stringify(j.detail)
    } catch { /* giữ thông báo mặc định */ }
    throw new Error(m)
  }
  return r.json()
}
