<template>
  <div class="min-h-screen zen-bg flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 动态背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 -right-20 w-80 h-80 bg-tea-500/8 rounded-full blur-[100px] animate-pulse-soft"></div>
      <div class="absolute bottom-1/4 -left-20 w-80 h-80 bg-cyber-blue/8 rounded-full blur-[100px] animate-pulse-soft animate-delay-300"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-tea-500/3 to-cyber-blue/3 rounded-full blur-[120px]"></div>
    </div>

    <!-- 注册卡片 -->
    <div class="zen-card w-full max-w-lg p-8 relative animate-scale-in z-10">
      <!-- 顶部装饰线 -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-transparent via-tea-500 to-transparent opacity-50"></div>

      <!-- Logo区域 -->
      <div class="text-center mb-6 pt-4">
        <div class="inline-flex items-center justify-center w-16 h-16 mb-4 relative">
          <div class="absolute inset-0 bg-tea-500/20 rounded-zen-xl blur-xl animate-pulse-soft"></div>
          <div class="relative w-14 h-14 rounded-zen-xl bg-gradient-to-br from-tea-500 to-tea-600 flex items-center justify-center shadow-tea-glow">
            <span class="text-white font-bold text-xl">茶</span>
          </div>
        </div>
        <h1 class="text-2xl font-bold text-gradient-tea">加入 TeaMAKE</h1>
        <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">创建你的竞赛组队账号</p>
      </div>

      <!-- 步骤指示器 -->
      <div class="flex items-center justify-center gap-3 mb-6">
        <div :class="['w-10 h-10 flex items-center justify-center text-sm font-medium rounded-full transition-all', step >= 1 ? 'bg-gradient-to-br from-tea-500 to-tea-600 text-white shadow-tea-glow' : 'bg-gray-100 dark:bg-cyber-darkGray text-gray-400 dark:text-gray-500']">
          <svg v-if="step >= 2" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <span v-else>1</span>
        </div>
        <div class="w-16 h-1 bg-gray-100 dark:bg-cyber-darkGray rounded-full overflow-hidden">
          <div class="h-full bg-gradient-to-r from-tea-500 to-cyber-blue transition-all duration-500" :style="{ width: step >= 2 ? '100%' : '0%' }"></div>
        </div>
        <div :class="['w-10 h-10 flex items-center justify-center text-sm font-medium rounded-full transition-all', step >= 2 ? 'bg-gradient-to-br from-tea-500 to-tea-600 text-white shadow-tea-glow' : 'bg-gray-100 dark:bg-cyber-darkGray text-gray-400 dark:text-gray-500']">
          2
        </div>
      </div>

      <!-- 步骤1：基本信息 -->
      <form v-show="step === 1" @submit.prevent="nextStep" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div class="group">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
              用户名 <span class="text-tea-500">*</span>
            </label>
            <input
              v-model="form.username"
              type="text"
              class="zen-input"
              placeholder="设置用户名"
              required
              minlength="3"
              maxlength="20"
            />
          </div>
          <div class="group">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
              QQ号 <span class="text-tea-500">*</span>
            </label>
            <input
              v-model="form.QQ_num"
              type="number"
              class="zen-input"
              placeholder="你的QQ号"
              required
            />
          </div>
        </div>

        <div class="group">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
            邮箱 <span class="text-tea-500">*</span>
          </label>
          <input
            v-model="form.email"
            type="email"
            class="zen-input"
            placeholder="你的邮箱"
            required
          />
        </div>

        <div class="group">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
            密码 <span class="text-tea-500">*</span>
          </label>
          <input
            v-model="form.password"
            type="password"
            class="zen-input"
            placeholder="设置密码（至少6位）"
            required
            minlength="6"
          />
        </div>

        <div class="group">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
            学校 <span class="text-tea-500">*</span>
          </label>
          <input
            v-model="form.college"
            type="text"
            class="zen-input"
            placeholder="你的学校"
            required
          />
        </div>

        <div v-if="error" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm rounded-zen animate-fade-in">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary w-full py-3 mt-6 animate-slide-up">
          下一步
        </button>
      </form>

      <!-- 步骤2：确认信息 -->
      <form v-show="step === 2" @submit.prevent="handleRegister" class="space-y-4">
        <div class="zen-card p-4 space-y-3">
          <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-gray-500 dark:text-gray-400">用户名</span>
            <span class="text-gray-900 dark:text-white font-medium">{{ form.username }}</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-gray-500 dark:text-gray-400">QQ号</span>
            <span class="text-gray-900 dark:text-white font-medium">{{ form.QQ_num }}</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-gray-500 dark:text-gray-400">邮箱</span>
            <span class="text-gray-900 dark:text-white font-medium">{{ form.email }}</span>
          </div>
          <div class="flex justify-between items-center py-2">
            <span class="text-gray-500 dark:text-gray-400">学校</span>
            <span class="text-gray-900 dark:text-white font-medium">{{ form.college }}</span>
          </div>
        </div>

        <div v-if="error" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm rounded-zen animate-fade-in">
          {{ error }}
        </div>

        <div v-if="success" class="p-3 bg-tea-50 dark:bg-tea-900/20 border border-tea-200 dark:border-tea-800 text-tea-600 dark:text-tea-light text-sm rounded-zen animate-fade-in">
          {{ success }}
        </div>

        <div class="flex gap-3 mt-6">
          <button type="button" @click="step = 1" class="btn-secondary flex-1 py-3">
            上一步
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="btn-primary flex-1 py-3 flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="animate-spin w-5 h-5" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            <span>{{ loading ? '注册中...' : '确认注册' }}</span>
          </button>
        </div>
      </form>

      <!-- 底部链接 -->
      <div class="mt-6 text-center">
        <p class="text-gray-500 dark:text-gray-400">
          已有账号？
          <router-link to="/login" class="text-tea-500 hover:text-tea-600 dark:hover:text-tea-light font-medium transition-all hover:underline decoration-2 underline-offset-2">
            立即登录
          </router-link>
        </p>
      </div>

      <!-- 装饰角落 -->
      <div class="absolute bottom-0 left-0 w-20 h-20 overflow-hidden pointer-events-none">
        <div class="absolute bottom-0 left-0 w-10 h-10 bg-gradient-to-br from-cyber-blue/10 to-tea-500/10 rounded-tr-zen-xl"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'

const router = useRouter()

const step = ref(1)
const loading = ref(false)
const error = ref('')
const success = ref('')

const form = reactive({
  username: '',
  QQ_num: '',
  email: '',
  password: '',
  college: ''
})

function nextStep() {
  if (!form.username || !form.QQ_num || !form.email || !form.password || !form.college) {
    error.value = '请填写所有必填项'
    return
  }
  if (form.password.length < 6) {
    error.value = '密码至少需要6位'
    return
  }
  error.value = ''
  step.value = 2
}

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    const response = await authAPI.register(form)
    success.value = `注册成功！用户ID: ${response.user_id}`
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    error.value = err.message || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
