import { useState, useEffect, useCallback } from 'react'
import { 
  MoreVertical, 
  ShieldCheck, 
  ShieldAlert,
  BellRing, 
  X, 
  CheckCircle2, 
  ChevronRight, 
  Clock3, 
  Sliders, 
  Settings2, 
  Lock, 
  Unlock, 
  Camera, 
  Lightbulb, 
  Wifi, 
  Users, 
  Sparkles,
  Zap,
  Play,
  RotateCcw,
  Check,
  Server
} from 'lucide-react'

import Header from './components/Header.jsx'
import DeviceSummary from './components/DeviceSummary.jsx'
import CameraCard from './components/CameraCard.jsx'
import CameraModal from './components/CameraModal.jsx'
import DeviceDetailModal from './components/DeviceDetailModal.jsx'
import { 
  ThermostatCard, 
  DoorLockCard, 
  LightControlCard, 
  BlindsCard, 
  VacuumCard, 
  MovieModeCard,
  SecuritySummaryCard 
} from './components/SmartControls.jsx'

import { api } from './api/client.js'

// Primary camera feeds matching the reference image layout
const defaultCameras = [
  { 
    id: 'cam-pet-01', 
    name: 'Pet cam', 
    location: 'Dining Room CCTV', 
    className: 'camera-pet', 
    image: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=85' 
  },
  { 
    id: 'cam-doorbell-02', 
    name: 'Smart Doorbell', 
    location: 'Living Room CCTV', 
    className: 'camera-doorbell', 
    image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85' 
  },
  { 
    id: 'cam-yard-03', 
    name: 'Yard cam', 
    location: 'Living Room CCTV', 
    className: 'camera-yard', 
    image: 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85' 
  },
]

export default function App() {
  // Navigation & Theme
  const [activePage, setActivePage] = useState('Dashboard')
  const [lightTheme, setLightTheme] = useState(false)

  // Backend Sync Status
  const [backendConnected, setBackendConnected] = useState(false)
  const [dashboardSummary, setDashboardSummary] = useState(null)

  // Device States (initialized from defaults, then synced with backend)
  const [temperature, setTemperature] = useState(70)
  const [locked, setLocked] = useState(true)
  const [brightness, setBrightness] = useState(84)
  const [lightEnabled, setLightEnabled] = useState(true)
  const [blindsOpen, setBlindsOpen] = useState(true)
  const [vacuumRunning, setVacuumRunning] = useState(true)
  const [movieModeActive, setMovieModeActive] = useState(true)

  // Security & Alert States
  const [acknowledged, setAcknowledged] = useState(false)
  const [noticeOpen, setNoticeOpen] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [notificationsList, setNotificationsList] = useState([])
  const [unreadCount, setUnreadCount] = useState(1)

  // Modal Dialogs
  const [activeCameraModal, setActiveCameraModal] = useState(null)
  const [detailModalType, setDetailModalType] = useState(null)

  // 1. Initial Data Fetch from FastAPI Backend
  const refreshBackendData = useCallback(async () => {
    try {
      const [summary, devices, notifs, events] = await Promise.all([
        api.dashboard.getSummary().catch(() => null),
        api.devices.getDevices().catch(() => null),
        api.notifications.getNotifications().catch(() => null),
        api.security.getEvents().catch(() => null),
      ])

      if (summary) {
        setBackendConnected(true)
        setDashboardSummary(summary)
      }

      if (devices && Array.isArray(devices)) {
        // Find individual device states
        const pantry = devices.find(d => d.id === 'light-pantry-01' || d.name.toLowerCase().includes('pantry'))
        if (pantry) {
          setLightEnabled(pantry.is_enabled)
          setBrightness(pantry.configuration?.brightness ?? 84)
        }

        const lockDev = devices.find(d => d.id === 'lock-front-01' || d.device_type === 'door_lock')
        if (lockDev) {
          setLocked(lockDev.status === 'locked' || lockDev.configuration?.is_locked === true)
        }

        const therm = devices.find(d => d.id === 'thermostat-hallway-01' || d.device_type === 'thermostat')
        if (therm) {
          setTemperature(therm.configuration?.target_temperature ?? 70)
        }

        const blindsDev = devices.find(d => d.id === 'blinds-lr-01' || d.device_type === 'smart_blinds')
        if (blindsDev) {
          setBlindsOpen((blindsDev.configuration?.opening_percentage ?? 100) > 0)
        }

        const vacDev = devices.find(d => d.id === 'vacuum-01' || d.device_type === 'smart_vacuum')
        if (vacDev) {
          setVacuumRunning(vacDev.status === 'running')
        }
      }

      if (notifs && Array.isArray(notifs)) {
        setNotificationsList(notifs)
        const unread = notifs.filter(n => !n.is_read).length
        setUnreadCount(unread)
      }

      if (events && Array.isArray(events)) {
        const unackedAlerts = events.filter(e => !e.is_acknowledged && e.severity !== 'informational')
        setAcknowledged(unackedAlerts.length === 0)
      }
    } catch (err) {
      console.warn('Backend unavailable, running in local fallback mode:', err)
      setBackendConnected(false)
    }
  }, [])

  useEffect(() => {
    refreshBackendData()
  }, [refreshBackendData])

  // Handlers with Backend Sync
  const handleToggleLock = async () => {
    const nextLocked = !locked
    setLocked(nextLocked)
    try {
      await api.devices.setPower('lock-front-01', nextLocked)
      await api.devices.updateDevice('lock-front-01', { 
        status: nextLocked ? 'locked' : 'unlocked',
        configuration: { is_locked: nextLocked }
      })
    } catch {
      // Optimistic update retained
    }
  }

  const handleUpdateBrightness = async (newVal) => {
    setBrightness(newVal)
    try {
      await api.devices.setBrightness('light-pantry-01', newVal)
    } catch {
      // Optimistic update retained
    }
  }

  const handleToggleLight = async (enabled) => {
    setLightEnabled(enabled)
    try {
      await api.devices.setPower('light-pantry-01', enabled)
    } catch {
      // Optimistic update retained
    }
  }

  const handleUpdateTemperature = async (newTemp) => {
    setTemperature(newTemp)
    try {
      await api.devices.setTemperature('thermostat-hallway-01', newTemp)
    } catch {
      // Optimistic update retained
    }
  }

  const handleToggleBlinds = async () => {
    const nextOpen = !blindsOpen
    setBlindsOpen(nextOpen)
    try {
      await api.devices.setBlinds('blinds-lr-01', nextOpen ? 100 : 0)
    } catch {
      // Optimistic update retained
    }
  }

  const handleToggleVacuum = async (running) => {
    setVacuumRunning(running)
    try {
      await api.devices.setVacuum('vacuum-01', running)
    } catch {
      // Optimistic update retained
    }
  }

  const handleAcknowledgeAlerts = async () => {
    setAcknowledged(true)
    try {
      await api.security.acknowledgeAll()
      await api.notifications.markAllRead()
      setUnreadCount(0)
      refreshBackendData()
    } catch {
      // Optimistic update retained
    }
  }

  const handleTriggerDemoAlert = async () => {
    try {
      await api.security.triggerDemoEvent({
        event_type: 'motion_detection',
        location: 'Front Porch'
      })
      setAcknowledged(false)
      setUnreadCount(prev => prev + 1)
      refreshBackendData()
    } catch {
      setAcknowledged(false)
    }
  }

  return (
    <div className={`app-shell ${lightTheme ? 'light-theme' : ''}`}>
      <div className="dashboard-frame">
        {/* Top Navigation Bar */}
        <Header 
          activePage={activePage} 
          setActivePage={setActivePage} 
          lightTheme={lightTheme} 
          setLightTheme={setLightTheme} 
          unreadCount={unreadCount}
          onOpenNotifications={() => setNoticeOpen(!noticeOpen)}
        />

        {/* Notifications Popover */}
        {noticeOpen && (
          <aside className="notification-popover" role="dialog" aria-label="Notifications panel">
            <div className="popover-head">
              <div className="popover-title">
                <BellRing size={15} />
                <strong>Notifications ({unreadCount})</strong>
              </div>
              <button 
                onClick={() => setNoticeOpen(false)} 
                aria-label="Close notifications"
                className="popover-close-btn"
              >
                <X size={14} />
              </button>
            </div>

            <div className="popover-body">
              {notificationsList.length > 0 ? (
                notificationsList.slice(0, 4).map((n) => (
                  <div className={`alert-item ${!n.is_read ? 'unread' : ''}`} key={n.id}>
                    <span className={!n.is_read ? 'alert-ping-dot' : 'info-dot'} />
                    <div className="alert-info">
                      <strong>{n.title}</strong>
                      <span>{n.message}</span>
                    </div>
                    {!n.is_read && (
                      <button 
                        className="quick-ack-btn"
                        onClick={async () => {
                          await api.notifications.markRead(n.id).catch(() => null)
                          setNotificationsList(prev => prev.map(item => item.id === n.id ? { ...item, is_read: true } : item))
                          setUnreadCount(prev => Math.max(0, prev - 1))
                        }}
                      >
                        Read
                      </button>
                    )}
                  </div>
                ))
              ) : (
                <div className="alert-item resolved">
                  <CheckCircle2 size={15} />
                  <div className="alert-info">
                    <strong>All alerts resolved</strong>
                    <span>SafeHome AI active & monitoring</span>
                  </div>
                </div>
              )}
            </div>

            <div className="popover-footer">
              <button 
                className="text-action-link"
                onClick={() => { setActivePage('Activity'); setNoticeOpen(false) }}
              >
                <span>View Full Activity Log</span>
                <ChevronRight size={13} />
              </button>
            </div>
          </aside>
        )}

        {/* Five Summary Device Cards */}
        <DeviceSummary onSelectCategory={() => setActivePage('Device')} />

        {/* Thin divider matching reference */}
        <div className="section-divider" />

        {/* MAIN CONTENT AREA */}
        {activePage === 'Dashboard' ? (
          <section className="favorites-container" aria-label="Favorites panel">
            {/* Header: "Favorites" + three dots menu */}
            <div className="favorites-header">
              <div className="favorites-title-wrap">
                <h1 className="favorites-title">Favorites</h1>
                <span className={`sync-pill ${backendConnected ? 'connected' : 'offline'}`} title="FastAPI Backend Status">
                  <span className="sync-dot" />
                  {backendConnected ? 'FastAPI Connected' : 'Local Demo'}
                </span>
              </div>
              
              <div className="favorites-tools">
                <button 
                  className="dots-menu-button" 
                  aria-label="Dashboard options"
                  onClick={() => setMenuOpen(!menuOpen)}
                >
                  <MoreVertical size={18} />
                </button>

                {menuOpen && (
                  <div className="favorites-dropdown-menu">
                    <button onClick={() => { handleAcknowledgeAlerts(); setMenuOpen(false) }}>
                      <Check size={14} /> Acknowledge all alerts
                    </button>
                    <button onClick={() => { handleTriggerDemoAlert(); setMenuOpen(false) }}>
                      <Zap size={14} /> Trigger Demo Alert
                    </button>
                    <button onClick={() => {
                      setTemperature(70)
                      setLocked(true)
                      setBrightness(84)
                      setLightEnabled(true)
                      setBlindsOpen(true)
                      setVacuumRunning(true)
                      setMovieModeActive(true)
                      setAcknowledged(false)
                      setMenuOpen(false)
                    }}>
                      <RotateCcw size={14} /> Reset Demo States
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* THREE COLUMN GRID: Left Controls | Center Cameras | Right Controls */}
            <div className="favorites-grid">
              {/* LEFT COLUMN: 4 Colored/Dark Smart Device Cards */}
              <div className="left-controls-column">
                <ThermostatCard 
                  temperature={temperature} 
                  setTemperature={handleUpdateTemperature}
                  onOpenDetails={() => setDetailModalType('thermostat')}
                />
                
                <DoorLockCard 
                  locked={locked} 
                  setLocked={handleToggleLock}
                  onOpenDetails={() => setDetailModalType('lock')}
                />

                <LightControlCard 
                  brightness={brightness} 
                  setBrightness={handleUpdateBrightness}
                  enabled={lightEnabled}
                  setEnabled={handleToggleLight}
                />

                <BlindsCard 
                  blindsOpen={blindsOpen}
                  setBlindsOpen={handleToggleBlinds}
                  onOpenDetails={() => setDetailModalType('blinds')}
                />
              </div>

              {/* CENTER COLUMN: 3 Photographic Camera Preview Tiles */}
              <div className="center-cameras-column">
                <div className="camera-grid-layout">
                  {defaultCameras.map((camera) => (
                    <CameraCard 
                      key={camera.id}
                      camera={camera}
                      onOpen={setActiveCameraModal}
                    />
                  ))}
                </div>
              </div>

              {/* RIGHT COLUMN: Smart Vacuum, Security Status, Movie Mode */}
              <div className="right-controls-column">
                <VacuumCard 
                  running={vacuumRunning} 
                  setRunning={handleToggleVacuum}
                  progress={46}
                />

                <SecuritySummaryCard 
                  acknowledged={acknowledged}
                  onAcknowledge={handleAcknowledgeAlerts}
                  onOpenVisitor={() => setActivePage('Device')}
                />

                <MovieModeCard 
                  active={movieModeActive}
                  setActive={setMovieModeActive}
                  onOpenDetails={() => setDetailModalType('movie')}
                />
              </div>
            </div>

            {/* Subtle disclaimer badge */}
            <div className="dashboard-demo-notice">
              <ShieldCheck size={13} />
              <span>SafeHome AI · Full-Stack Smart Home Security · FastAPI backend live at http://localhost:8000</span>
            </div>
          </section>
        ) : activePage === 'Automation' ? (
          <AutomationView />
        ) : activePage === 'Device' ? (
          <DeviceInventoryView />
        ) : activePage === 'Activity' ? (
          <ActivityTimelineView 
            acknowledged={acknowledged} 
            onAcknowledge={handleAcknowledgeAlerts} 
          />
        ) : (
          <SettingsView />
        )}

        {/* Subtle Footer */}
        <footer className="dashboard-footer">
          <div className="footer-left">
            <span className="footer-status-dot" />
            <span>SafeHome AI · Smart Home Security System (FastAPI + React)</span>
          </div>
          <div className="footer-right">
            <span>Encrypted end-to-end · Privacy first</span>
          </div>
        </footer>
      </div>

      {/* Camera Live Preview Modal */}
      {activeCameraModal && (
        <CameraModal 
          camera={activeCameraModal} 
          onClose={() => setActiveCameraModal(null)} 
        />
      )}

      {/* Interactive Detail Modal for Thermostat, Lock, Blinds, and Movie mode */}
      {detailModalType && (
        <DeviceDetailModal 
          type={detailModalType}
          onClose={() => setDetailModalType(null)}
          data={{
            temperature,
            locked,
            blindsOpen,
            movieModeActive
          }}
          onUpdate={(updates) => {
            if (updates.temperature !== undefined) handleUpdateTemperature(updates.temperature)
            if (updates.locked !== undefined) handleToggleLock()
            if (updates.blindsOpen !== undefined) handleToggleBlinds()
            if (updates.movieModeActive !== undefined) setMovieModeActive(updates.movieModeActive)
          }}
        />
      )}
    </div>
  )
}

// ---------------- Secondary Navigation Views ----------------

function AutomationView() {
  const [routines, setRoutines] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.automations.getAutomations()
      .then(res => setRoutines(res || []))
      .catch(() => {
        setRoutines([
          { id: '1', name: 'Movie Night Scene', description: 'Dims pantry lighting to 15%, shuts blinds, sets Dolby Atmos.', is_enabled: true, trigger_type: 'scene' },
          { id: '2', name: 'Away Security Shield', description: 'Arms all perimeter CCTV cameras and locks exterior doors.', is_enabled: false, trigger_type: 'geofence' },
          { id: '3', name: 'Night Owl Guard', description: 'Activates yard motion tripwires and turns porch downlights to amber.', is_enabled: true, trigger_type: 'schedule' },
        ])
      })
      .finally(() => setLoading(false))
  }, [])

  const toggleRoutine = async (id) => {
    try {
      const updated = await api.automations.toggleAutomation(id)
      setRoutines(prev => prev.map(r => r.id === id ? { ...r, is_enabled: updated.is_enabled } : r))
    } catch {
      setRoutines(prev => prev.map(r => r.id === id ? { ...r, is_enabled: !r.is_enabled } : r))
    }
  }

  const testRoutine = async (id) => {
    try {
      const res = await api.automations.testAutomation(id)
      alert(`[Automation Executed]: ${res.simulated_actions.join(', ')}`)
    } catch {
      alert('Automation routine executed in local simulation mode.')
    }
  }

  return (
    <section className="page-view-panel">
      <div className="page-view-header">
        <div>
          <h2>Automation & Routines</h2>
          <p>Create automated workflows for security, convenience, and energy savings.</p>
        </div>
        <button className="primary-pill-btn">+ New Routine</button>
      </div>

      <div className="secondary-cards-grid">
        {routines.map((r) => (
          <article className="routine-card" key={r.id}>
            <div className="routine-head">
              <span className="routine-tag">{r.trigger_type || 'Routine'}</span>
              <div style={{ display: 'flex', gap: '6px' }}>
                <button 
                  className="routine-toggle-pill"
                  onClick={() => testRoutine(r.id)}
                  title="Test trigger this routine"
                >
                  Test
                </button>
                <button 
                  className={`routine-toggle-pill ${r.is_enabled ? 'active' : ''}`}
                  onClick={() => toggleRoutine(r.id)}
                >
                  {r.is_enabled ? 'Active' : 'Disabled'}
                </button>
              </div>
            </div>
            <strong>{r.name}</strong>
            <p>{r.description}</p>
          </article>
        ))}
      </div>
    </section>
  )
}

function DeviceInventoryView() {
  const [deviceList, setDeviceList] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.devices.getDevices()
      .then(res => setDeviceList(res || []))
      .catch(() => setDeviceList([]))
      .finally(() => setLoading(false))
  }, [])

  const categories = [
    { title: 'Security Cameras', filter: 'security_camera' },
    { title: 'Smart Lighting', filter: 'smart_light' },
    { title: 'Access & Climate', filter: ['thermostat', 'door_lock', 'smart_blinds'] },
    { title: 'Appliances & Media', filter: ['smart_vacuum', 'speaker', 'wifi_device', 'smart_assistant'] },
  ]

  return (
    <section className="page-view-panel">
      <div className="page-view-header">
        <div>
          <h2>Connected Devices ({deviceList.length || 19})</h2>
          <p>SafeHome AI smart device inventory backed by SQLAlchemy and FastAPI.</p>
        </div>
        <span className="health-badge">
          {deviceList.filter(d => d.is_online).length} / {deviceList.length} Online
        </span>
      </div>

      <div className="devices-category-grid">
        {categories.map((cat) => {
          const matching = deviceList.filter(d => 
            Array.isArray(cat.filter) ? cat.filter.includes(d.device_type) : d.device_type === cat.filter
          )

          return (
            <div className="category-column" key={cat.title}>
              <h3>{cat.title} ({matching.length})</h3>
              <div className="device-list">
                {matching.length > 0 ? matching.map((device) => (
                  <div className="device-item-row" key={device.id}>
                    <div className={`device-dot-online ${!device.is_online ? 'offline' : ''}`} />
                    <span>{device.name}</span>
                    <span className="device-status-chip">
                      {device.room} · {device.is_online ? 'Online' : 'Offline'}
                    </span>
                  </div>
                )) : (
                  <span style={{ fontSize: '11px', color: '#888' }}>Loading devices...</span>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}

function ActivityTimelineView({ acknowledged, onAcknowledge }) {
  const [events, setEvents] = useState([])

  useEffect(() => {
    api.security.getEvents()
      .then(res => setEvents(res || []))
      .catch(() => {
        setEvents([
          { id: '1', title: 'Motion detected at Front Porch', description: 'Smart Doorbell', created_at: new Date().toISOString(), severity: 'warning', is_acknowledged: acknowledged }
        ])
      })
  }, [acknowledged])

  return (
    <section className="page-view-panel">
      <div className="page-view-header">
        <div>
          <h2>Security Event Timeline</h2>
          <p>Real-time audit log of security triggers, visitor rings, and automated actions.</p>
        </div>
        {!acknowledged && (
          <button className="primary-pill-btn" onClick={onAcknowledge}>
            Acknowledge All
          </button>
        )}
      </div>

      <div className="timeline-container">
        {events.map((e) => (
          <div className={`timeline-entry ${!e.is_acknowledged && e.severity === 'warning' ? 'unread-entry' : ''}`} key={e.id}>
            <div className={`timeline-indicator ${e.severity === 'warning' && !e.is_acknowledged ? 'alert-dot' : 'normal-dot'}`} />
            <div className="timeline-details">
              <strong>{e.title}</strong>
              <span>{e.description} · {new Date(e.created_at).toLocaleTimeString()}</span>
            </div>
            {!e.is_acknowledged && e.severity === 'warning' && (
              <button 
                className="timeline-ack-action" 
                onClick={async () => {
                  await api.security.acknowledgeEvent(e.id).catch(() => null)
                  setEvents(prev => prev.map(item => item.id === e.id ? { ...item, is_acknowledged: true } : item))
                }}
              >
                Acknowledge
              </button>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}

function SettingsView() {
  return (
    <section className="page-view-panel">
      <div className="page-view-header">
        <div>
          <h2>SafeHome AI Settings</h2>
          <p>Manage home security policies, Ring/simulator integration, and access pins.</p>
        </div>
      </div>

      <div className="settings-cards-grid">
        <article className="setting-card">
          <strong>Security Mode</strong>
          <p>Configure guard level for automated perimeter defense.</p>
          <div className="segmented-control">
            <button className="active">Home Guard</button>
            <button>Away Mode</button>
            <button>Disarmed</button>
          </div>
        </article>

        <article className="setting-card">
          <strong>FastAPI Backend Status</strong>
          <p>Connected to SQLite SQLAlchemy database with JWT access tokens.</p>
          <span className="demo-chip-large">API LIVE: HTTP://LOCALHOST:8000</span>
        </article>

        <article className="setting-card">
          <strong>Notification Preferences</strong>
          <p>Receive push alerts for human and vehicle detection.</p>
          <div className="setting-toggle-row">
            <span>Doorbell chimes & calls</span>
            <span className="active-text">Enabled</span>
          </div>
        </article>
      </div>
    </section>
  )
}