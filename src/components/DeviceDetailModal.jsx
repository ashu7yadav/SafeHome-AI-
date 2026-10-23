import { useState } from 'react'
import { 
  X, 
  Thermometer, 
  Lock, 
  Unlock, 
  Blinds, 
  Sparkles, 
  Flame, 
  Snowflake, 
  Leaf, 
  KeyRound, 
  Clock, 
  Check, 
  ShieldCheck, 
  SunMedium, 
  Volume2
} from 'lucide-react'

export default function DeviceDetailModal({ type, onClose, data = {}, onUpdate = () => {} }) {
  if (!type) return null

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="device-detail-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="detail-modal-header">
          <div className="detail-header-info">
            <span className={`detail-category-chip ${type}`}>
              {type === 'thermostat' && 'Climate Control'}
              {type === 'lock' && 'Access Security'}
              {type === 'blinds' && 'Window Covering'}
              {type === 'movie' && 'Scene Preset'}
            </span>
            <h3>
              {type === 'thermostat' && 'Hallway Thermostat'}
              {type === 'lock' && 'Front Door Smart Lock'}
              {type === 'blinds' && 'Living Room Blinds'}
              {type === 'movie' && 'Movie Mode Scene'}
            </h3>
          </div>
          <button className="detail-close-btn" onClick={onClose} aria-label="Close dialog">
            <X size={17} />
          </button>
        </div>

        <div className="detail-modal-body">
          {type === 'thermostat' && (
            <ThermostatDetailContent 
              temperature={data.temperature ?? 70} 
              onUpdateTemp={(val) => onUpdate({ temperature: val })} 
            />
          )}

          {type === 'lock' && (
            <LockDetailContent 
              locked={data.locked ?? true} 
              onToggleLock={() => onUpdate({ locked: !data.locked })} 
            />
          )}

          {type === 'blinds' && (
            <BlindsDetailContent 
              blindsOpen={data.blindsOpen ?? true}
              onToggleBlinds={(val) => onUpdate({ blindsOpen: val })}
            />
          )}

          {type === 'movie' && (
            <MovieDetailContent 
              active={data.movieModeActive ?? true}
              onToggleActive={(val) => onUpdate({ movieModeActive: val })}
            />
          )}
        </div>
      </div>
    </div>
  )
}

function ThermostatDetailContent({ temperature, onUpdateTemp }) {
  const [mode, setMode] = useState('heat')

  return (
    <div className="detail-content-wrap">
      <div className="temp-dial-display">
        <button 
          className="dial-btn minus" 
          onClick={() => onUpdateTemp(Math.max(60, temperature - 1))}
          aria-label="Decrease temperature"
        >
          -
        </button>
        <div className="temp-big-value">
          <span className="big-num">{temperature}</span>
          <span className="unit">°F</span>
          <span className="dial-sub">Target Setpoint</span>
        </div>
        <button 
          className="dial-btn plus" 
          onClick={() => onUpdateTemp(Math.min(85, temperature + 1))}
          aria-label="Increase temperature"
        >
          +
        </button>
      </div>

      <div className="mode-selector-row">
        {[
          { id: 'heat', label: 'Heating', icon: Flame },
          { id: 'cool', label: 'Cooling', icon: Snowflake },
          { id: 'eco', label: 'Eco Guard', icon: Leaf },
        ].map(({ id, label, icon: Icon }) => (
          <button 
            key={id}
            className={`mode-btn ${mode === id ? 'active' : ''}`}
            onClick={() => setMode(id)}
          >
            <Icon size={14} />
            <span>{label}</span>
          </button>
        ))}
      </div>

      <div className="detail-meta-box">
        <div className="meta-line">
          <span>Current Indoor Ambient</span>
          <strong>70.4°F (21.3°C)</strong>
        </div>
        <div className="meta-line">
          <span>Relative Humidity</span>
          <strong>44% Optimal</strong>
        </div>
      </div>
    </div>
  )
}

function LockDetailContent({ locked, onToggleLock }) {
  const [passcodeGenerated, setPasscodeGenerated] = useState(false)

  return (
    <div className="detail-content-wrap">
      <div className="lock-state-banner">
        <div className={`lock-status-circle ${locked ? 'locked' : 'unlocked'}`}>
          {locked ? <Lock size={32} /> : <Unlock size={32} />}
        </div>
        <h4>{locked ? 'Front Door is Securely Locked' : 'Front Door is Unlocked'}</h4>
        <p>Auto-relock engages after 45 seconds of closure</p>

        <button 
          className={`lock-action-btn ${locked ? 'unlock-style' : 'lock-style'}`}
          onClick={onToggleLock}
        >
          {locked ? 'Tap to Unlock Door' : 'Tap to Lock Securely'}
        </button>
      </div>

      <div className="guest-passcode-box">
        <div className="passcode-head">
          <KeyRound size={16} />
          <strong>Visitor Temporary PIN</strong>
        </div>
        <p>Generate a 4-digit code for deliveries or trusted guests.</p>
        
        {passcodeGenerated ? (
          <div className="generated-pin-display">
            <span className="pin-code">8 4 1 9</span>
            <span className="pin-expiry">Valid for next 2 hours</span>
          </div>
        ) : (
          <button 
            className="generate-pin-btn"
            onClick={() => setPasscodeGenerated(true)}
          >
            Generate One-Time Passcode
          </button>
        )}
      </div>
    </div>
  )
}

function BlindsDetailContent({ blindsOpen, onToggleBlinds }) {
  const [percentage, setPercentage] = useState(blindsOpen ? 100 : 0)

  const handlePreset = (pct) => {
    setPercentage(pct)
    onToggleBlinds(pct > 0)
  }

  return (
    <div className="detail-content-wrap">
      <div className="blinds-percent-display">
        <span className="blinds-num">{percentage}%</span>
        <span className="blinds-status">{percentage === 0 ? 'Fully Closed' : percentage === 100 ? 'Fully Open' : 'Partially Open'}</span>
      </div>

      <div className="range-control-wrap">
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={percentage} 
          onChange={(e) => {
            const val = Number(e.target.value)
            setPercentage(val)
            onToggleBlinds(val > 0)
          }}
          className="slider-range-input"
        />
      </div>

      <div className="presets-row">
        {[0, 25, 50, 75, 100].map((pct) => (
          <button 
            key={pct}
            className={`preset-btn ${percentage === pct ? 'active' : ''}`}
            onClick={() => handlePreset(pct)}
          >
            {pct === 0 ? 'Close' : pct === 100 ? 'Open' : `${pct}%`}
          </button>
        ))}
      </div>
    </div>
  )
}

function MovieDetailContent({ active, onToggleActive }) {
  return (
    <div className="detail-content-wrap">
      <div className="movie-scene-preview">
        <div className="sparkle-circle-big">
          <Sparkles size={30} />
        </div>
        <h4>Movie Mode Preset</h4>
        <p>Pre-configured cinema ambiance across living room</p>

        <button 
          className={`scene-toggle-action ${active ? 'active-scene' : ''}`}
          onClick={() => onToggleActive(!active)}
        >
          {active ? 'Movie Scene Active (Locked)' : 'Activate Movie Scene'}
        </button>
      </div>

      <div className="scene-breakdown-list">
        <div className="scene-item">
          <SunMedium size={15} />
          <div>
            <strong>Pantry & Ambient Lighting</strong>
            <span>Dimmed to 15% warm amber</span>
          </div>
          <Check size={14} className="check-ok" />
        </div>
        <div className="scene-item">
          <Blinds size={15} />
          <div>
            <strong>Living Room Blinds</strong>
            <span>Fully drawn down (0% light leakage)</span>
          </div>
          <Check size={14} className="check-ok" />
        </div>
        <div className="scene-item">
          <Volume2 size={15} />
          <div>
            <strong>Dolby Atmos Audio</strong>
            <span>Speakers synced to Smart TV</span>
          </div>
          <Check size={14} className="check-ok" />
        </div>
      </div>
    </div>
  )
}
