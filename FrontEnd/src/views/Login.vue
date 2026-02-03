<template>
  <div class="min-h-screen cyber-bg flex items-center justify-center p-4">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-cyber-primary/10 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-cyber-accent/10 rounded-full blur-[100px]"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="sharp-card w-full max-w-md p-8 relative animate-slide-up">
      <!-- Logo区域 -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 mb-4">
          <svg class="w-10 h-10 text-cyber-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gradient">TeaMAKE</h1>
        <p class="text-cyber-textSecondary mt-2">大学生竞赛组队平台</p>
      </div>

      <!-- 表单 -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <!-- 用户名 -->
        <div>
          <label class="block text-sm font-medium text-cyber-text mb-2">用户名</label>
          <input
            v-model="form.username"
            type="text"
            class="cyber-input"
            placeholder="请输入用户名"
            required
          />
        </div>

        <!-- 密码 -->
        <div>
          <label class="block text-sm font-medium text-cyber-text mb-2">密码</label>
          <input
            v-model="form.password"
            type="password"
            class="cyber-input"
            placeholder="请输入密码"
            required
          />
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-600 text-sm">
          {{ error }}
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          :disabled="loading"
          class="btn-primary w-full flex items-center justify-center gap-2"
        >
          <svg v-if="loading" class="animate-spin w-5 h-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          <span>{{ loading ? '登录中...' : '登录' }}</span>
        </button>
      </form>

      <!-- 底部链接 -->
      <div class="mt-6 text-center">
        <p class="text-cyber-textSecondary">
          还没有账号？
          <router-link to="/register" class="text-cyber-primary hover:underline">
            立即注册
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI, tokenManager } from '../api'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: ''
})

async function handleLogin() {
  error.value = ''
  loading.value = true

  try {
    const response = await authAPI.login(form)

    tokenManager.setToken(response.token, response.expires_in)
    tokenManager.setUser({
      id: response.id,
      username: response.username,
      email: response.email,
      college: response.college
    })

    router.push('/square')
  } catch (err) {
    error.value = err.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>
