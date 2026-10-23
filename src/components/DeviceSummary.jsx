import { useState } from 'react'
import { Video, Lightbulb, Volume2, Wifi, Mic, Power } from 'lucide-react'

const initialSummaries = [
  { id: 'cctv', title: 'CCTV', value: '3/4 cctv', icon: Video, active: true, isLime: false },
  { id: 'lighting', title: 'Lighting', value: '6 lights', icon: Lightbulb, active: true, isLime: true },
  { id: 'speaker', title: 'Speaker', value: '3 devices', icon: Volume2, active: true, isLime: false },
  { id: 'wifi', title: 'Wi-Fi', value: '2 devices', icon: Wifi, active: true, isLime: false },
  { id: 'assistant', title: 'Assistant', value: '4 devices', icon: Mic, active: true, isLime: false },
]

export default function DeviceSummary({ onSelectCategory }) {
  const [deviceStates, setDeviceStates] = useState(
    initialSummaries.reduce((acc, item) => ({ ...acc, [item.id]: item.active }), {})
  )

  const toggleDevice = (id, e) => {
    e.stopPropagation()
    setDeviceStates(prev => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <section className="summary-grid" aria-label="Connected device summary">
      {initialSummaries.map(({ id, title, value, icon: Icon, isLime }) => {
        const isActive = deviceStates[id]
        const cardClass = isLime 
          ? `summary-card lime-highlight ${!isActive ? 'lime-muted' : ''}`
          : `summary-card ${!isActive ? 'card-inactive' : ''}`

        return (
          <article 
            className={cardClass} 
            key={id}
            onClick={() => onSelectCategory && onSelectCategory(title)}
            role="button"
            tabIndex={0}
            title={`${title} category`}
          >
            <div className="summary-top">
              <span className="summary-icon-circle">
                <Icon size={15} strokeWidth={2.2} />
              </span>

              {/* Vertical Capsule Power Switch matching reference */}
              <button 
                className={`power-capsule ${isActive ? 'active' : 'inactive'}`}
                onClick={(e) => toggleDevice(id, e)}
                aria-label={`Toggle ${title} power`}
                title={isActive ? `Turn off ${title}` : `Turn on ${title}`}
              >
                <Power size={11} strokeWidth={2.4} />
              </button>
            </div>

            <div className="summary-text-block">
              <span className="summary-label">{title}</span>
              <strong className="summary-count">{value}</strong>
            </div>
          </article>
        )
      })}
    </section>
  )
}