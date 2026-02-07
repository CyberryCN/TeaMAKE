<template>
  <div class="min-h-screen zen-bg flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 动态背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 -left-20 w-80 h-80 bg-tea-500/8 rounded-full blur-[100px] animate-pulse-soft"></div>
      <div class="absolute bottom-1/4 -right-20 w-80 h-80 bg-cyber-blue/8 rounded-full blur-[100px] animate-pulse-soft animate-delay-300"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-tea-500/3 to-cyber-blue/3 rounded-full blur-[120px]"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="zen-card w-full max-w-md p-8 relative animate-scale-in z-10">
      <!-- 顶部装饰线 -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-transparent via-tea-500 to-transparent opacity-50"></div>

      <!-- Logo区域 -->
      <div class="text-center mb-8 pt-4">
        <div class="inline-flex items-center justify-center w-16 h-16 mb-4 relative">
          <div class="absolute inset-0 bg-tea-500/20 rounded-zen-xl blur-xl animate-pulse-soft"></div>
          <div class="relative w-14 h-14 rounded-zen-xl bg-gradient-to-br from-tea-500 to-tea-600 flex items-center justify-center shadow-tea-glow">
            <span class="text-white font-bold text-xl">茶</span>
          </div>
        </div>
        <h1 class="text-2xl font-bold text-gradient-tea">TeaMAKE</h1>
        <p class="text-gray-500 dark:text-gray-400 mt-2 text-sm">大学生竞赛组队平台</p>
      </div>

      <!-- 表单 -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        <!-- 用户名 -->
        <div class="group animate-slide-down animate-delay-100">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
            用户名
          </label>
          <div class="relative">
            <input
              v-model="form.username"
              type="text"
              class="zen-input pl-12"
              placeholder="请输入用户名"
              required
            />
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 transition-colors group-focus-within:text-tea-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
        </div>

        <!-- 密码 -->
        <div class="group animate-slide-down animate-delay-200">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
            密码
          </label>
          <div class="relative">
            <input
              v-model="form.password"
              type="password"
              class="zen-input pl-12"
              placeholder="请输入密码"
              required
            />
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 transition-colors group-focus-within:text-tea-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm rounded-zen animate-fade-in">
          {{ error }}
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          :disabled="loading"
          class="btn-primary w-full flex items-center justify-center gap-2 py-3 mt-6 animate-slide-up animate-delay-300"
        >
          <svg v-if="loading" class="animate-spin w-5 h-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          <span>{{ loading ? '登录中...' : '登录' }}</span>
        </button>
      </form>

      <!-- 底部链接 -->
      <div class="mt-8 text-center animate-fade-in animate-delay-400">
        <p class="text-gray-500 dark:text-gray-400">
          还没有账号？
          <router-link to="/register" class="text-tea-500 hover:text-tea-600 dark:hover:text-tea-light font-medium transition-all hover:underline decoration-2 underline-offset-2">
            立即注册
          </router-link>
        </p>
      </div>

      <!-- 装饰角落 -->
      <div class="absolute bottom-0 right-0 w-20 h-20 overflow-hidden pointer-events-none">
        <div class="absolute bottom-0 right-0 w-10 h-10 bg-gradient-to-br from-tea-500/10 to-cyber-blue/10 rounded-tl-zen-xl"></div>
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
