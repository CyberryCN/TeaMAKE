<template>
  <div class="min-h-screen cyber-bg flex items-center justify-center p-4">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-cyber-secondary/20 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-1/4 left-1/4 w-96 h-96 bg-cyber-accent/20 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
    </div>

    <!-- 注册卡片 -->
    <div class="glass-card w-full max-w-lg p-8 relative animate-slide-up">
      <!-- Logo区域 -->
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-xl bg-cyber-primary/10 border border-cyber-primary/30 mb-3">
          <svg class="w-8 h-8 text-cyber-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gradient">加入 TeaMAKE</h1>
        <p class="text-gray-400 text-sm mt-1">创建你的竞赛组队账号</p>
      </div>

      <!-- 步骤指示器 -->
      <div class="flex items-center justify-center gap-2 mb-6">
        <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all', step >= 1 ? 'bg-cyber-primary text-cyber-dark' : 'bg-white/10 text-gray-500']">1</div>
        <div class="w-12 h-0.5 bg-white/10">
          <div :class="['h-full bg-cyber-primary transition-all', step >= 2 ? 'w-full' : 'w-0']"></div>
        </div>
        <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all', step >= 2 ? 'bg-cyber-primary text-cyber-dark' : 'bg-white/10 text-gray-500']">2</div>
      </div>

      <!-- 步骤1：基本信息 -->
      <form v-show="step === 1" @submit.prevent="nextStep" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">用户名</label>
            <input
              v-model="form.username"
              type="text"
              class="cyber-input"
              placeholder="设置用户名"
              required
              minlength="3"
              maxlength="20"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">QQ号</label>
            <input
              v-model="form.QQ_num"
              type="number"
              class="cyber-input"
              placeholder="你的QQ号"
              required
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">邮箱</label>
          <input
            v-model="form.email"
            type="email"
            class="cyber-input"
            placeholder="你的邮箱"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">密码</label>
          <input
            v-model="form.password"
            type="password"
            class="cyber-input"
            placeholder="设置密码"
            required
            minlength="6"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">学校</label>
          <input
            v-model="form.college"
            type="text"
            class="cyber-input"
            placeholder="你的学校"
            required
          />
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary w-full">
          下一步
        </button>
      </form>

      <!-- 步骤2：确认信息 -->
      <form v-show="step === 2" @submit.prevent="handleRegister" class="space-y-4">
        <div class="glass-card p-4 space-y-3">
          <div class="flex justify-between">
            <span class="text-gray-400">用户名</span>
            <span class="text-white font-medium">{{ form.username }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">QQ号</span>
            <span class="text-white font-medium">{{ form.QQ_num }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">邮箱</span>
            <span class="text-white font-medium">{{ form.email }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">学校</span>
            <span class="text-white font-medium">{{ form.college }}</span>
          </div>
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="p-3 rounded-lg bg-cyber-primary/10 border border-cyber-primary/30 text-cyber-primary text-sm">
          {{ success }}
        </div>

        <div class="flex gap-3">
          <button type="button" @click="step = 1" class="btn-secondary flex-1">
            上一步
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="animate-spin w-5 h-5" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <span>{{ loading ? '注册中...' : '确认注册' }}</span>
          </button>
        </div>
      </form>

      <!-- 底部链接 -->
      <div class="mt-6 text-center">
        <p class="text-gray-400">
          已有账号？
          <router-link to="/login" class="text-cyber-primary hover:text-cyber-secondary transition-colors">
            立即登录
          </router-link>
        </p>
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
  // 简单验证
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
