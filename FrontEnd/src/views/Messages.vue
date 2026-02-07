<template>
  <div class="min-h-screen zen-bg" :class="{ 'dark': isDark }">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 nav-glass">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/square" class="flex items-center gap-2 group">
          <div class="relative">
            <div class="absolute inset-0 bg-tea-500/30 rounded-zen-lg blur-md animate-pulse-soft"></div>
            <div class="relative w-9 h-9 rounded-zen-lg bg-gradient-to-br from-tea-500 to-tea-600 flex items-center justify-center shadow-tea-md group-hover:shadow-tea-glow transition-all">
              <span class="text-white font-bold">茶</span>
            </div>
          </div>
          <span class="text-lg font-bold text-gradient-tea">TeaMAKE</span>
        </router-link>
        <div class="flex items-center gap-3">
          <button @click="toggleTheme" class="p-2 rounded-zen-full bg-tea-50 dark:bg-cyber-darkGray hover:bg-tea-100 dark:hover:bg-cyber-darkBorder transition-all">
            <svg v-if="isDark" class="w-5 h-5 text-cyber-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5 text-tea-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 0 008.354-5.646z"/>
            </svg>
          </button>
          <router-link to="/square" class="px-4 py-2 rounded-zen-full text-sm text-gray-500 dark:text-gray-400 hover:text-tea-500 dark:hover:text-tea-light transition-colors">
            返回广场
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 页面标题 -->
    <div class="pt-24 pb-4 px-4 bg-white/50 dark:bg-cyber-dark/50 backdrop-blur-sm border-b border-tea-200/30 dark:border-cyber-darkBorder/30">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">消息中心</h1>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="bg-white/30 dark:bg-cyber-dark/30 backdrop-blur-sm border-b border-tea-200/30 dark:border-cyber-darkBorder/30">
      <div class="max-w-4xl mx-auto px-4">
        <div class="tabs-nav">
          <button
            @click="activeTab = 'received'"
            :class="['tab-item', { 'active': activeTab === 'received' }]"
          >
            收到的申请
            <span v-if="unreadCount > 0" class="ml-2 badge">{{ unreadCount }}</span>
          </button>
          <button
            @click="activeTab = 'sent'"
            :class="['tab-item', { 'active': activeTab === 'sent' }]"
          >
            发出的申请
          </button>
        </div>
      </div>
    </div>

    <!-- 申请列表 -->
    <div class="max-w-4xl mx-auto px-4 py-6">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="relative">
          <div class="w-16 h-16 rounded-full border-4 border-tea-200 dark:border-cyber-darkGray border-t-tea-500 animate-spin"></div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="applications.length === 0" class="zen-card p-12 text-center">
        <div class="empty-state-icon mx-auto">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
          </svg>
        </div>
        <h3 class="empty-state-title">{{ activeTab === 'received' ? '暂无收到的申请' : '暂无发出的申请' }}</h3>
        <p class="empty-state-desc">{{ activeTab === 'received' ? '等待其他用户向你提交申请' : '去广场看看感兴趣的招募吧' }}</p>
        <router-link v-if="activeTab === 'sent'" to="/square" class="btn-primary inline-flex items-center gap-2 mt-6">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          浏览招募
        </router-link>
      </div>

      <!-- 申请卡片列表 -->
      <div v-else class="space-y-4 stagger-animation">
        <div
          v-for="app in applications"
          :key="app.id"
          class="zen-card p-5 hover:shadow-tea-md transition-all"
        >
          <div class="flex gap-4">
            <!-- 左侧用户信息 -->
            <router-link :to="`/profile/${activeTab === 'received' ? app.applicant_id : app.receiver_id}`" class="flex-shrink-0 flex flex-col items-center group">
              <div class="w-14 h-14 rounded-zen-xl bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center shadow-tea-md group-hover:shadow-tea-glow transition-all">
                <span class="text-white font-bold text-lg">{{ (activeTab === 'received' ? app.applicant_name : app.receiver_name)?.charAt(0) }}</span>
              </div>
            </router-link>

            <!-- 右侧内容 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ activeTab === 'received' ? `${app.applicant_name} 申请加入` : `申请 ${app.receiver_name}` }}
                  </h3>
                  <p class="text-sm text-gradient-cyber mt-1 font-medium">{{ app.recruitment_title }}</p>
                </div>
                <span :class="['tag-status', statusClass(app.status)]">
                  {{ statusText(app.status) }}
                </span>
              </div>

              <!-- 时间 -->
              <p class="text-xs text-gray-400 dark:text-gray-500 mt-3">
                {{ formatDateTime(app.created_at) }}
              </p>

              <!-- 操作按钮（收到的申请 且 状态为等待中） -->
              <div v-if="activeTab === 'received' && app.status === 'waiting'" class="flex gap-3 mt-4">
                <button
                  @click="respondApplication(app.id, true)"
                  class="btn-primary flex-1 flex items-center justify-center gap-2 py-2.5"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  接受
                </button>
                <button
                  @click="respondApplication(app.id, false)"
                  class="btn-secondary flex-1 flex items-center justify-center gap-2 py-2.5"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                  拒绝
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { applicationAPI } from '../api'

const router = useRouter()

const isDark = ref(false)
const loading = ref(true)
const activeTab = ref('received')
const applications = ref([])
const unreadCount = ref(0)

function toggleTheme() {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  updateTheme()
}

function updateTheme() {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

function statusClass(status) {
  const classes = {
    'waiting': 'waiting',
    'accept': 'accept',
    'reject': 'reject'
  }
  return classes[status] || 'draft'
}

function statusText(status) {
  const texts = {
    'waiting': '待响应',
    'accept': '已接受',
    'reject': '已拒绝'
  }
  return texts[status] || status
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

async function loadUnreadCount() {
  try {
    const result = await applicationAPI.getUnreadCount()
    unreadCount.value = result.unread_count || 0
  } catch (err) {
    console.error('获取未读数量失败:', err)
  }
}

async function loadApplications() {
  loading.value = true
  try {
    if (activeTab.value === 'received') {
      const result = await applicationAPI.getReceived()
      applications.value = result.applications || []
    } else {
      const result = await applicationAPI.getSent()
      applications.value = result.applications || []
    }
  } catch (err) {
    console.error('获取申请列表失败:', err)
  } finally {
    loading.value = false
  }
}

async function respondApplication(applicationId, accept) {
  if (!confirm(accept ? '确定要接受这个申请吗？对方将成为队伍成员。' : '确定要拒绝这个申请吗？')) return

  try {
    await applicationAPI.respond(applicationId, accept)

    if (accept) {
      alert('已接受申请！对方已加入队伍。')
      const app = applications.value.find(a => a.id === applicationId)
      if (app) {
        router.push(`/recruitment/${app.recruitment_id}`)
        return
      }
    } else {
      alert('已拒绝申请')
    }

    await loadApplications()
    await loadUnreadCount()
  } catch (err) {
    alert(err.message || '操作失败')
  }
}

watch(activeTab, () => {
  loadApplications()
})

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  loadApplications()
  loadUnreadCount()
})
</script>
