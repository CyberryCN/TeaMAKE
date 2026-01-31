const API_BASE = 'http://localhost:8000/api/v1'

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
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

export default {
  auth: authAPI,
  user: userAPI,
  skill: skillAPI
}
