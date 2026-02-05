const API_BASE = 'http://localhost:8000/api/v1'

// Token 管理
export const tokenManager = {
  getToken() {
    return localStorage.getItem('token')
  },

  setToken(token, expiresIn) {
    localStorage.setItem('token', token)
    localStorage.setItem('token_expires_in', expiresIn)
  },

  removeToken() {
    localStorage.removeItem('token')
    localStorage.removeItem('token_expires_in')
  },

  getUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  setUser(user) {
    localStorage.setItem('user', JSON.stringify(user))
  },

  isLoggedIn() {
    const token = this.getToken()
    return !!token
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`

  // 获取 token 并添加到请求头
  const token = tokenManager.getToken()
  const config = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
      ...options.headers
    },
    ...options
  }

  // 移除空的 Authorization header
  if (!config.headers['Authorization']) {
    delete config.headers['Authorization']
  }

  try {
    const response = await fetch(url, config)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || '请求失败')
    }

    return data
  } catch (error) {
    throw error
  }
}

export const authAPI = {
  // 用户注册
  register(userData) {
    return request('/users/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  },

  // 用户登录
  login(credentials) {
    return request('/users/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
  },

  // 学信网验证
  authenticate(userId, chsiCode) {
    return request('/users/auth', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, chsi_code: chsiCode })
    })
  }
}

export const userAPI = {
  // 获取用户详情
  getDetail(userId) {
    return request(`/users/${userId}/detail`)
  },

  // 更新个人资料
  updateProfile(userId, data) {
    return request(`/users/${userId}/profile`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },

  // 更新技能标签
  updateSkills(userId, skillIds) {
    return request(`/users/${userId}/skills`, {
      method: 'PUT',
      body: JSON.stringify({ skill_ids: skillIds })
    })
  }
}

export const skillAPI = {
  // 获取所有技能
  getAll() {
    return request('/skills')
  },

  // 获取所有分类
  getCategories() {
    return request('/skills/categories')
  },

  // 按分类获取技能
  getByCategory(categoryName) {
    return request(`/skills/categories/${encodeURIComponent(categoryName)}`)
  }
}

export const recruitmentAPI = {
  // 获取招募列表
  getList(params = {}) {
    const queryParams = new URLSearchParams()
    if (params.page) queryParams.set('page', params.page)
    if (params.pageSize) queryParams.set('pageSize', params.pageSize)
    if (params.status) queryParams.set('status', params.status)
    if (params.competition_name) queryParams.set('competition_name', params.competition_name)
    return request(`/recruitments?${queryParams.toString()}`)
  },

  // 获取招募详情
  getDetail(id) {
    return request(`/recruitments/${id}`)
  },

  // 发布招募
  publish(data) {
    return request('/recruitments/publish', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  // 保存草稿
  createDraft(data) {
    return request('/recruitments/draft', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  // 更新招募
  update(id, data) {
    return request(`/recruitments/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },

  // 发布草稿
  publishDraft(id) {
    return request(`/recruitments/${id}/publish`, {
      method: 'POST'
    })
  },

  // 关闭招募
  close(id) {
    return request(`/recruitments/${id}/close`, {
      method: 'POST'
    })
  },

  // 删除招募
  delete(id) {
    return request(`/recruitments/${id}`, {
      method: 'DELETE'
    })
  },

  // 获取我的招募列表
  getMyList(status = null) {
    const url = status ? `/recruitments/my/list?status=${status}` : '/recruitments/my/list'
    return request(url)
  }
}

export const applicationAPI = {
  // 发送申请
  send(data) {
    return request('/applications', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  // 获取未读申请数量（红点）
  getUnreadCount() {
    return request('/applications/unread/count')
  },

  // 获取收到的申请
  getReceived(status = null) {
    const url = status ? `/applications/received?status=${status}` : '/applications/received'
    return request(url)
  },

  // 获取发出的申请
  getSent(status = null) {
    const url = status ? `/applications/sent?status=${status}` : '/applications/sent'
    return request(url)
  },

  // 获取所有相关申请（个人主页用，分页）
  getAll(skip = 0, limit = 50) {
    return request(`/applications/all?skip=${skip}&limit=${limit}`)
  },

  // 响应申请（接受或拒绝）
  respond(applicationId, accept) {
    return request(`/applications/${applicationId}/respond`, {
      method: 'POST',
      body: JSON.stringify({ accept })
    })
  }
}

export const teamAPI = {
  // 获取队伍详情
  getDetail(teamId) {
    return request(`/teams/${teamId}`)
  },

  // 根据招募ID获取队伍
  getByRecruitment(recruitmentId) {
    return request(`/teams/recruitment/${recruitmentId}`)
  },

  // 获取我加入的所有队伍
  getMyTeams() {
    return request('/teams/my/list')
  },

  // 添加队伍成员（队长操作）
  addMember(teamId, userId) {
    return request(`/teams/${teamId}/members/${userId}`, {
      method: 'POST'
    })
  },

  // 移除队伍成员（队长操作）
  removeMember(teamId, userId) {
    return request(`/teams/${teamId}/members/${userId}`, {
      method: 'DELETE'
    })
  }
}

export default {
  auth: authAPI,
  user: userAPI,
  skill: skillAPI,
  recruitment: recruitmentAPI,
  application: applicationAPI,
  team: teamAPI
}
