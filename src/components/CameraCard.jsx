import { useState } from 'react'
import { Video, Mic, MicOff, ChevronDown, Maximize2 } from 'lucide-react'

export default function CameraCard({ camera, onOpen }) {
  const [micActive, setMicActive] = useState(false)
  const [quality, setQuality] = useState('FHD')

  const handleMicClick = (e) => {
    e.stopPropagation()
    setMicActive(!micActive)
  }

  const handleQualityClick = (e) => {
    e.stopPropagation()
    setQuality(q => q === 'FHD' ? '2K' : q === '2K' ? '720p' : 'FHD')
  }

  return (
    <div 
      className={`camera-tile ${camera.className || ''}`} 
      onClick={() => onOpen(camera)}
      role="button"
      tabIndex={0}
      aria-label={`Open ${camera.name} live view`}
    >
      {/* Photographic background feed */}
      <img 
        src={camera.image} 
        alt={`${camera.name} view`} 
        className="camera-feed-img"
        loading="lazy" 
      />

      {/* Subtle vignette shade for contrast */}
      <div className="camera-feed-vignette" />

      {/* Top Left: Live Status Pill */}
      <div className="camera-top-left">
        <span className="live-badge-pill">
          <span className="live-dot" />
          <span>Live</span>
        </span>
      </div>

      {/* Top Right: Resolution Dropdown Pill */}
      <div className="camera-top-right">
        <button 
          className="quality-badge-pill" 
          onClick={handleQualityClick}
          title="Toggle Stream Resolution"
          aria-label="Stream Resolution"
        >
          <span>{quality}</span>
          <ChevronDown size={11} strokeWidth={2.4} />
        </button>
      </div>

      {/* Bottom Frosted Glass Action Bar matching reference image */}
      <div className="camera-bottom-glass-bar">
        <div className="camera-title-block">
          <strong className="camera-main-name">{camera.name}</strong>
          <span className="camera-sub-location">{camera.location}</span>
        </div>

        <div className="camera-glass-actions">
          <button 
            className="glass-action-btn" 
            onClick={(e) => { e.stopPropagation(); onOpen(camera) }}
            title="Expand Fullscreen"
            aria-label="Expand Fullscreen"
          >
            <Video size={13} strokeWidth={2} />
          </button>
          <button 
            className={`glass-action-btn ${micActive ? 'mic-on' : ''}`}
            onClick={handleMicClick}
            title={micActive ? 'Mute 2-Way Talk' : 'Enable 2-Way Talk'}
            aria-label="Toggle 2-Way Audio"
          >
            {micActive ? <Mic size={13} strokeWidth={2.2} /> : <Mic size={13} strokeWidth={2} />}
          </button>
        </div>
      </div>
    </div>
  )
}