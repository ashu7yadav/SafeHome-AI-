import { useState, useRef, useEffect } from 'react'
import { 
  X, 
  Video, 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  Camera as SnapshotIcon, 
  ShieldAlert, 
  Maximize, 
  Minimize,
  Check
} from 'lucide-react'

export default function CameraModal({ camera, onClose }) {
  if (!camera) return null

  const [muted, setMuted] = useState(false)
  const [micActive, setMicActive] = useState(false)
  const [snapshotTaken, setSnapshotTaken] = useState(false)
  const [sirenActive, setSirenActive] = useState(false)
  const [isVideoFullscreen, setIsVideoFullscreen] = useState(false)
  const videoContainerRef = useRef(null)

  useEffect(() => {
    const handleFsChange = () => {
      setIsVideoFullscreen(Boolean(document.fullscreenElement))
    }
    document.addEventListener('fullscreenchange', handleFsChange)
    return () => document.removeEventListener('fullscreenchange', handleFsChange)
  }, [])

  const handleSnapshot = () => {
    setSnapshotTaken(true)
    setTimeout(() => setSnapshotTaken(false), 2200)
  }

  const handleSiren = () => {
    setSirenActive(!sirenActive)
  }

  const toggleVideoFullscreen = async () => {
    try {
      if (!document.fullscreenElement) {
        if (videoContainerRef.current?.requestFullscreen) {
          await videoContainerRef.current.requestFullscreen()
        }
      } else {
        if (document.exitFullscreen) {
          await document.exitFullscreen()
        }
      }
    } catch (err) {
      console.warn('Video fullscreen request failed:', err)
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="camera-modal" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div className="modal-header">
          <div className="modal-header-meta">
            <div className="modal-title-row">
              <span className="live-dot" />
              <strong>{camera.name}</strong>
              <span className="demo-chip">SIMULATED FEED</span>
            </div>
            <span>{camera.location} · 1080p FHD 30 FPS · H.265</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button 
              className="icon-button modal-fs-btn" 
              onClick={toggleVideoFullscreen}
              title={isVideoFullscreen ? 'Exit Video Fullscreen' : 'Expand Video Fullscreen'}
              aria-label="Toggle Video Fullscreen"
            >
              {isVideoFullscreen ? <Minimize size={16} /> : <Maximize size={16} />}
            </button>

            <button 
              className="icon-button modal-close-btn" 
              onClick={onClose} 
              aria-label="Close camera preview"
              title="Close Preview (Esc)"
            >
              <X size={17} />
            </button>
          </div>
        </div>

        {/* Video Canvas Container with Fullscreen Ref */}
        <div 
          className={`modal-video-container ${isVideoFullscreen ? 'in-fullscreen' : ''}`}
          ref={videoContainerRef}
        >
          <img 
            src={camera.image} 
            alt={camera.name} 
            className="modal-camera-image"
          />

          {snapshotTaken && (
            <div className="snapshot-flash-overlay">
              <div className="snapshot-notice">
                <Check size={16} />
                <span>Snapshot captured & saved to vault</span>
              </div>
            </div>
          )}

          {sirenActive && (
            <div className="siren-warning-banner">
              <ShieldAlert size={16} />
              <span>Deterrence Siren Emitting (Demo)</span>
            </div>
          )}

          <div className="modal-feed-overlay-bar">
            <div className="timestamp-badge">
              LIVE {new Date().toLocaleTimeString()}
            </div>
            <div className="bitrate-badge">
              4.2 Mbps · FHD
            </div>
          </div>
        </div>

        {/* Controls Footer */}
        <div className="modal-footer">
          <div className="footer-control-group">
            <button 
              className={`modal-action-btn ${micActive ? 'active-talk' : ''}`}
              onClick={() => setMicActive(!micActive)}
            >
              {micActive ? <Mic size={15} /> : <MicOff size={15} />}
              <span>{micActive ? 'Talking Live' : 'Push to Talk'}</span>
            </button>

            <button 
              className={`modal-action-btn ${muted ? 'active-muted' : ''}`}
              onClick={() => setMuted(!muted)}
            >
              {muted ? <VolumeX size={15} /> : <Volume2 size={15} />}
              <span>{muted ? 'Muted' : 'Audio On'}</span>
            </button>

            <button 
              className="modal-action-btn"
              onClick={handleSnapshot}
            >
              <SnapshotIcon size={15} />
              <span>Take Snapshot</span>
            </button>

            <button 
              className={`modal-action-btn siren-btn ${sirenActive ? 'siren-flashing' : ''}`}
              onClick={handleSiren}
            >
              <ShieldAlert size={15} />
              <span>{sirenActive ? 'Stop Siren' : 'Sound Siren'}</span>
            </button>

            <button 
              className="modal-action-btn"
              onClick={toggleVideoFullscreen}
              title="Expand to Fullscreen"
            >
              {isVideoFullscreen ? <Minimize size={15} /> : <Maximize size={15} />}
              <span>{isVideoFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}</span>
            </button>
          </div>

          <div className="modal-disclaimer-note">
            <span>Demo camera stream preview. No real hardware connected.</span>
          </div>
        </div>
      </div>
    </div>
  )
}