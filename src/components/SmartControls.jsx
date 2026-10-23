import { useState } from 'react'
import { 
  Thermometer, 
  Lock, 
  Unlock, 
  Lightbulb, 
  Blinds, 
  Sparkles, 
  ChevronDown, 
  Fan, 
  ShieldCheck, 
  BellRing, 
  CheckCircle2, 
  ArrowUpRight,
  SlidersHorizontal
} from 'lucide-react'

// Sleek Pill Toggle matching reference
function ToggleSwitch({ checked, onChange, label }) {
  return (
    <button 
      role="switch" 
      aria-checked={checked} 
      aria-label={label} 
      className={`pill-toggle-switch ${checked ? 'is-active' : ''}`}
      onClick={(e) => {
        e.stopPropagation()
        onChange(!checked)
      }}
    >
      <span className="toggle-thumb" />
    </button>
  )
}

// 1. Hallway Thermostat (Blue Card)
export function ThermostatCard({ temperature, setTemperature, onOpenDetails }) {
  return (
    <article 
      className="smart-card thermostat-card"
      onClick={() => onOpenDetails && onOpenDetails('thermostat')}
      role="button"
      tabIndex={0}
    >
      <div className="card-icon-badge">
        <Thermometer size={17} strokeWidth={2.2} />
      </div>

      <div className="card-info-col">
        <strong className="card-main-title">Hallway thermostat</strong>
        <span className="card-sub-value">Indoor {temperature}°</span>
      </div>

      <button 
        className="card-chevron-circle"
        onClick={(e) => {
          e.stopPropagation()
          onOpenDetails && onOpenDetails('thermostat')
        }}
        aria-label="Thermostat settings"
      >
        <ChevronDown size={15} strokeWidth={2.4} />
      </button>
    </article>
  )
}

// 2. Front Door Lock (Magenta Card)
export function DoorLockCard({ locked, setLocked, onOpenDetails }) {
  return (
    <article 
      className="smart-card door-lock-card"
      onClick={() => setLocked(!locked)}
      role="button"
      tabIndex={0}
      title="Click to toggle lock state"
    >
      <div className="card-icon-badge">
        {locked ? <Lock size={17} strokeWidth={2.2} /> : <Unlock size={17} strokeWidth={2.2} />}
      </div>

      <div className="card-info-col">
        <strong className="card-main-title">Front door lock</strong>
        <span className="card-sub-value">{locked ? 'Locked' : 'Unlocked'}</span>
      </div>

      <button 
        className="card-chevron-circle"
        onClick={(e) => {
          e.stopPropagation()
          onOpenDetails && onOpenDetails('lock')
        }}
        aria-label="Door lock controls"
      >
        <ChevronDown size={15} strokeWidth={2.4} />
      </button>
    </article>
  )
}

// 3. Pantry Light (Dark Card with Interactive Brightness Slider)
export function LightControlCard({ brightness, setBrightness, enabled, setEnabled }) {
  return (
    <article className="smart-card dark-control-card light-control-card">
      <div className="card-head-row">
        <span className="dark-icon-badge">
          <Lightbulb size={15} strokeWidth={2.2} />
        </span>
        <ToggleSwitch 
          checked={enabled} 
          onChange={setEnabled} 
          label="Toggle pantry light" 
        />
      </div>

      <div className="card-body-text">
        <strong className="card-main-title">Pantry light</strong>
        <span className="card-room-label">Living Room</span>
      </div>

      {/* Glow Slider with Pill Badge matching reference */}
      <div className="slider-track-container">
        <div 
          className="slider-filled-bar" 
          style={{ width: `${enabled ? brightness : 0}%` }}
        />
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={enabled ? brightness : 0} 
          onChange={(e) => {
            if (!enabled) setEnabled(true)
            setBrightness(Number(e.target.value))
          }}
          className="slider-range-input"
          aria-label="Pantry light brightness"
        />
        <span 
          className="slider-percent-badge" 
          style={{ left: `calc(${enabled ? brightness : 0}% - 14px)` }}
        >
          {enabled ? `${brightness}%` : '0%'}
        </span>
      </div>
    </article>
  )
}

// 4. Living Room Blinds (Warm Orange Card)
export function BlindsCard({ blindsOpen, setBlindsOpen, onOpenDetails }) {
  return (
    <article 
      className="smart-card blinds-card"
      onClick={() => setBlindsOpen(!blindsOpen)}
      role="button"
      tabIndex={0}
      title="Click to toggle blinds"
    >
      <div className="card-icon-badge">
        <Blinds size={17} strokeWidth={2.2} />
      </div>

      <div className="card-info-col">
        <strong className="card-main-title">Living room blinds</strong>
        <span className="card-sub-value">{blindsOpen ? 'Open' : 'Closed'}</span>
      </div>

      <button 
        className="card-chevron-circle"
        onClick={(e) => {
          e.stopPropagation()
          onOpenDetails && onOpenDetails('blinds')
        }}
        aria-label="Blinds controls"
      >
        <ChevronDown size={15} strokeWidth={2.4} />
      </button>
    </article>
  )
}

// 5. Smart Vacuum (Dark Card with 46% progress bar)
export function VacuumCard({ running, setRunning, progress = 46 }) {
  return (
    <article className="smart-card dark-control-card vacuum-card">
      <div className="card-head-row">
        <span className="dark-icon-badge">
          <Fan size={15} strokeWidth={2.2} />
        </span>
        <ToggleSwitch 
          checked={running} 
          onChange={setRunning} 
          label="Toggle smart vacuum" 
        />
      </div>

      <div className="card-body-text">
        <strong className="card-main-title">Smart Vacuum</strong>
        <span className="card-room-label">{running ? 'Running' : 'Docked'}</span>
      </div>

      {/* Progress Track with Blue Pill Badge matching reference */}
      <div className="progress-track-container">
        <div 
          className="progress-filled-bar" 
          style={{ width: `${running ? progress : 0}%` }}
        />
        <span 
          className="progress-percent-badge"
          style={{ left: `calc(${running ? progress : 0}% - 14px)` }}
        >
          {running ? `${progress}%` : '0%'}
        </span>
      </div>
    </article>
  )
}

// 6. Movie Mode (Purple Card matching reference image bottom right)
export function MovieModeCard({ active, setActive, onOpenDetails }) {
  return (
    <article 
      className="smart-card movie-mode-card"
      onClick={() => setActive(!active)}
      role="button"
      tabIndex={0}
      title="Toggle Movie Mode preset"
    >
      <div className="card-icon-badge">
        <Sparkles size={17} strokeWidth={2.2} />
      </div>

      <div className="card-info-col">
        <strong className="card-main-title">Movie mode</strong>
        <span className="card-sub-value">{active ? 'Locked' : 'Standby'}</span>
      </div>

      <button 
        className="card-chevron-circle"
        onClick={(e) => {
          e.stopPropagation()
          onOpenDetails && onOpenDetails('movie')
        }}
        aria-label="Movie mode scene settings"
      >
        <ChevronDown size={15} strokeWidth={2.4} />
      </button>
    </article>
  )
}

// 7. Security Status & Quick Alert Card (SafeHome AI Integration)
export function SecuritySummaryCard({ acknowledged, onAcknowledge, onOpenVisitor }) {
  return (
    <article className="smart-card dark-control-card security-overview-card">
      <div className="card-head-row">
        <span className="dark-icon-badge security-shield">
          <ShieldCheck size={15} strokeWidth={2.2} />
        </span>
        <span className={`status-pill ${acknowledged ? 'status-all-good' : 'status-alert'}`}>
          <span className="mini-pulse-dot" />
          {acknowledged ? 'Systems Safe' : 'Alert Triggered'}
        </span>
      </div>

      <div className="security-card-content">
        <strong className="card-main-title">
          {acknowledged ? 'All Systems Checked' : 'Front Entrance Motion'}
        </strong>
        <span className="card-room-label">
          {acknowledged ? '19/19 Devices Online' : 'Front Doorbell · 2m ago'}
        </span>
      </div>

      <div className="security-card-actions">
        {!acknowledged ? (
          <button 
            className="security-btn ack-btn"
            onClick={onAcknowledge}
          >
            <CheckCircle2 size={13} />
            <span>Acknowledge Alert</span>
          </button>
        ) : (
          <button 
            className="security-btn visitor-btn"
            onClick={onOpenVisitor}
          >
            <span>Visitor Entry</span>
            <ArrowUpRight size={13} />
          </button>
        )}
      </div>
    </article>
  )
}