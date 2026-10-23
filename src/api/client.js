// SafeHome AI API Client
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

class ApiClient {
  constructor() {
    this.baseUrl = BASE_URL
    this.token = localStorage.getItem('safehome_token') || null
  }

  setToken(token) {
    this.token = token
    if (token) {
      localStorage.setItem('safehome_token', token)
    } else {
      localStorage.removeItem('safehome_token')
    }
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (response.status === 204) {
        return null
      }

      const data = await response.json().catch(() => null)

      if (!response.ok) {
        throw new Error(data?.detail || `API request failed with status ${response.status}`)
      }

      return data
    } catch (error) {
      // Re-throw so caller can handle or fallback gracefully
      throw error
    }
  }

  // Authentication
  auth = {
    login: (credentials) => this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    }).then(res => {
      if (res?.access_token) this.setToken(res.access_token)
      return res
    }),
    register: (userData) => this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    }).then(res => {
      if (res?.access_token) this.setToken(res.access_token)
      return res
    }),
    me: () => this.request('/auth/me'),
    logout: () => {
      this.setToken(null)
      return this.request('/auth/logout', { method: 'POST' }).catch(() => ({}))
    }
  }

  // Dashboard
  dashboard = {
    getSummary: () => this.request('/dashboard/summary')
  }

  // Devices
  devices = {
    getDevices: (deviceType) => {
      const qs = deviceType ? `?device_type=${deviceType}` : ''
      return this.request(`/devices${qs}`)
    },
    getDevice: (id) => this.request(`/devices/${id}`),
    setPower: (id, isEnabled) => this.request(`/devices/${id}/power`, {
      method: 'PATCH',
      body: JSON.stringify({ is_enabled: isEnabled })
    }),
    setBrightness: (id, brightness) => this.request(`/devices/${id}/brightness`, {
      method: 'PATCH',
      body: JSON.stringify({ brightness })
    }),
    setTemperature: (id, temperature, mode = 'heat') => this.request(`/devices/${id}/temperature`, {
      method: 'PATCH',
      body: JSON.stringify({ temperature, mode })
    }),
    setBlinds: (id, openingPercentage) => this.request(`/devices/${id}/blinds`, {
      method: 'PATCH',
      body: JSON.stringify({ opening_percentage: openingPercentage })
    }),
    setVacuum: (id, isRunning, mode = 'auto') => this.request(`/devices/${id}/vacuum`, {
      method: 'PATCH',
      body: JSON.stringify({ is_running: isRunning, mode })
    })
  }

  // Cameras
  cameras = {
    getCameras: () => this.request('/cameras'),
    getCamera: (id) => this.request(`/cameras/${id}`),
    getStatus: (id) => this.request(`/cameras/${id}/status`)
  }

  // Security Events
  security = {
    getEvents: (params = {}) => {
      const search = new URLSearchParams()
      if (params.severity) search.set('severity', params.severity)
      if (params.event_type) search.set('event_type', params.event_type)
      if (params.is_acknowledged !== undefined) search.set('is_acknowledged', params.is_acknowledged)
      const qs = search.toString() ? `?${search.toString()}` : ''
      return this.request(`/security/events${qs}`)
    },
    acknowledgeEvent: (id) => this.request(`/security/events/${id}/acknowledge`, {
      method: 'PATCH'
    }),
    acknowledgeAll: () => this.request('/security/events/acknowledge-all', {
      method: 'POST'
    }),
    triggerDemoEvent: (data = {}) => this.request('/security/events/demo', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
    getStatus: () => this.request('/security/status')
  }

  // Visitors
  visitors = {
    getVisitors: (status) => {
      const qs = status ? `?status=${status}` : ''
      return this.request(`/visitors${qs}`)
    },
    createVisitor: (visitorData) => this.request('/visitors', {
      method: 'POST',
      body: JSON.stringify(visitorData)
    }),
    approveVisitor: (id) => this.request(`/visitors/${id}/approve`, {
      method: 'PATCH'
    }),
    revokeVisitor: (id) => this.request(`/visitors/${id}/revoke`, {
      method: 'PATCH'
    }),
    deleteVisitor: (id) => this.request(`/visitors/${id}`, {
      method: 'DELETE'
    })
  }

  // Automations
  automations = {
    getAutomations: () => this.request('/automations'),
    toggleAutomation: (id) => this.request(`/automations/${id}/toggle`, {
      method: 'PATCH'
    }),
    testAutomation: (id) => this.request(`/automations/${id}/test`, {
      method: 'POST'
    })
  }

  // Notifications
  notifications = {
    getNotifications: (isRead) => {
      const qs = isRead !== undefined ? `?is_read=${isRead}` : ''
      return this.request(`/notifications${qs}`)
    },
    getUnreadCount: () => this.request('/notifications/unread-count'),
    markRead: (id) => this.request(`/notifications/${id}/read`, {
      method: 'PATCH'
    }),
    markAllRead: () => this.request('/notifications/read-all', {
      method: 'PATCH'
    }),
    deleteNotification: (id) => this.request(`/notifications/${id}`, {
      method: 'DELETE'
    })
  }
}

export const api = new ApiClient()
