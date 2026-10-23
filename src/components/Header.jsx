import { useState, useEffect } from 'react'
import { 
  Home, 
  LayoutDashboard, 
  Workflow, 
  Cpu, 
  Activity, 
  Settings, 
  Moon, 
  Sun, 
  Bell, 
  Menu, 
  X, 
  Maximize, 
  Minimize 
} from 'lucide-react'

const navItems = [
  { id: 'Dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'Automation', label: 'Automation', icon: Workflow },
  { id: 'Device', label: 'Device', icon: Cpu },
  { id: 'Activity', label: 'Activity', icon: Activity },
  { id: 'Settings', label: 'Settings', icon: Settings },
]

export default function Header({ 
  activePage, 
  setActivePage, 
  lightTheme, 
  setLightTheme, 
  unreadCount = 1,
  onOpenNotifications 
}) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)

  // Listen for fullscreen state changes (including Esc key exit)
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(Boolean(document.fullscreenElement))
    }
    document.addEventListener('fullscreenchange', handleFullscreenChange)
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange)
  }, [])

  const toggleFullscreen = async () => {
    try {
      if (!document.fullscreenElement) {
        if (document.documentElement.requestFullscreen) {
          await document.documentElement.requestFullscreen()
        } else if (document.documentElement.webkitRequestFullscreen) {
          await document.documentElement.webkitRequestFullscreen()
        }
      } else {
        if (document.exitFullscreen) {
          await document.exitFullscreen()
        } else if (document.webkitExitFullscreen) {
          await document.webkitExitFullscreen()
        }
      }
    } catch (err) {
      console.warn('Fullscreen request could not be completed:', err)
    }
  }

  return (
    <header className="topbar">
      <div className="topbar-left">
        {/* House Logo Squircle matching reference */}
        <button 
          className="brand-squircle" 
          aria-label="SafeHome AI Dashboard" 
          onClick={() => setActivePage('Dashboard')}
          title="SafeHome AI"
        >
          <Home size={17} strokeWidth={2.4} fill="currentColor" />
        </button>

        {/* Navigation Items */}
        <nav className={`nav-links ${mobileOpen ? 'nav-open' : ''}`} aria-label="Main navigation">
          {navItems.map(({ id, label, icon: Icon }) => {
            const isActive = activePage === id
            return (
              <button
                key={id}
                className={`nav-pill-item ${isActive ? 'active-pill' : ''}`}
                onClick={() => {
                  setActivePage(id)
                  setMobileOpen(false)
                }}
              >
                <Icon className="nav-mobile-icon" size={15} />
                <span>{label}</span>
              </button>
            )
          })}
        </nav>
      </div>

      <div className="topbar-actions">
        {/* Mobile menu trigger */}
        <button 
          className="mobile-menu-button" 
          aria-label="Toggle navigation menu" 
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X size={18} /> : <Menu size={18} />}
        </button>

        {/* Dual Theme Pill (Moon & Sun) */}
        <button 
          className="theme-capsule-toggle" 
          aria-label={`Switch to ${lightTheme ? 'dark' : 'light'} mode`}
          onClick={() => setLightTheme(!lightTheme)}
          title={`Switch to ${lightTheme ? 'dark' : 'light'} mode`}
        >
          <span className={`theme-icon moon-icon ${!lightTheme ? 'inactive' : 'active'}`}>
            <Moon size={14} strokeWidth={2} />
          </span>
          <span className={`theme-icon sun-icon ${!lightTheme ? 'active' : 'inactive'}`}>
            <Sun size={14} strokeWidth={2.2} />
          </span>
        </button>

        {/* Fullscreen Toggle Button */}
        <button 
          className={`icon-button fullscreen-button ${isFullscreen ? 'active-fullscreen' : ''}`}
          aria-label={isFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'}
          onClick={toggleFullscreen}
          title={isFullscreen ? 'Exit Fullscreen (Esc)' : 'Enter Fullscreen (Kiosk Display)'}
        >
          {isFullscreen ? (
            <Minimize size={16} strokeWidth={2.2} />
          ) : (
            <Maximize size={16} strokeWidth={2.2} />
          )}
        </button>

        {/* Notifications Button */}
        <button 
          className="icon-button notification-button" 
          aria-label="Open notifications" 
          onClick={onOpenNotifications}
          title="Notifications"
        >
          <Bell size={16} strokeWidth={2} />
          {unreadCount > 0 && <span className="notification-dot" />}
        </button>

        {/* User Profile Avatar */}
        <div className="profile-wrap">
          <button 
            className="avatar-button" 
            aria-label="Open profile menu" 
            onClick={() => setProfileOpen(!profileOpen)}
            title="User Profile"
          >
            <img 
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80" 
              alt="Alex Morgan" 
            />
          </button>

          {profileOpen && (
            <div className="profile-menu">
              <div className="profile-menu-head">
                <div className="profile-avatar-mini">
                  <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=80&q=80" alt="" />
                </div>
                <div>
                  <strong>Alex Morgan</strong>
                  <span>alex@safehome.ai</span>
                </div>
              </div>
              <div className="menu-divider" />
              <button onClick={() => { setActivePage('Device'); setProfileOpen(false) }}>
                Connected Devices (19)
              </button>
              <button onClick={() => { setActivePage('Activity'); setProfileOpen(false) }}>
                Security Event Log
              </button>
              <button onClick={() => { setActivePage('Settings'); setProfileOpen(false) }}>
                Home Settings
              </button>
              <div className="menu-divider" />
              <button onClick={() => { toggleFullscreen(); setProfileOpen(false) }}>
                {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen Display'}
              </button>
              <div className="menu-divider" />
              <button className="menu-close-btn" onClick={() => setProfileOpen(false)}>
                Close
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}