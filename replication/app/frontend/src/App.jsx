import { useState } from 'react'
import Berth from './Berth.jsx'
import Assign from './Assign.jsx'
import Knap from './Knap.jsx'
import Bins from './Bins.jsx'

const TABS = [
  { id: 'berth', name: '1 · Thuê bến', desc: 'Tô màu đồ thị khoảng: ký ít tiền thuê nhất', C: Berth },
  { id: 'assign', name: '2 · Phân công đội', desc: 'Gán đội đủ kỹ năng cho từng lượt tàu', C: Assign },
  { id: 'knap', name: '3 · Quỹ giờ công', desc: 'Cái túi 0/1: chọn việc tăng ca giá trị nhất', C: Knap },
  { id: 'bins', name: '4 · Xếp container', desc: 'Đóng thùng: dùng ít tàu nhất', C: Bins },
]

export default function App() {
  const [tab, setTab] = useState('berth')
  const cur = TABS.find((t) => t.id === tab)
  return (
    <>
      <header className="topbar">
        <div className="topbar-in">
          <b>Điều phối cảng cho hãng tàu</b>
          <span>CS112 · bản dựng lại theo Spec Kit</span>
        </div>
      </header>
      <nav className="tabs" role="tablist">
        {TABS.map((t) => (
          <button key={t.id} role="tab" aria-selected={t.id === tab} onClick={() => setTab(t.id)}>
            {t.name}
          </button>
        ))}
      </nav>
      <main className="page">
        <h1>{cur.name}</h1>
        <p className="lead">{cur.desc}</p>
        <cur.C key={cur.id} />
      </main>
    </>
  )
}
