<template>
  <div class="min-h-screen" :class="{ 'dark': isDark }">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-cyber-dark border-b border-light-border dark:border-dark-border">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/square" class="text-lg font-bold text-cyber-primary">TeaMAKE</router-link>
        <div class="flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 0 008.354-5.646z"/>
            </svg>
          </button>
          <router-link to="/square" class="text-sm text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">返回广场</router-link>
        </div>
      </div>
    </nav>

    <!-- 页面标题 -->
    <div class="pt-20 pb-6 bg-light-lighter dark:bg-cyber-darker/50 border-b border-light-border dark:border-dark-border">
      <div class="max-w-4xl mx-auto px-4">
        <h1 class="text-2xl font-bold text-cyber-dark dark:text-white">消息中心</h1>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="bg-light-lighter dark:bg-cyber-darker/30 border-b border-light-border dark:border-dark-border">
      <div class="max-w-4xl mx-auto px-4">
        <div class="flex gap-2">
          <button
            @click="activeTab = 'received'"
            :class="['px-6 py-3 text-sm font-medium transition-all border-b-2', activeTab === 'received' ? 'border-cyber-primary text-cyber-primary' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300']"
          >
            收到的申请
            <span v-if="unreadCount > 0" class="ml-2 px-2 py-0.5 bg-red-500 text-white text-xs rounded-full">{{ unreadCount }}</span>
          </button>
          <button
            @click="activeTab = 'sent'"
            :class="['px-6 py-3 text-sm font-medium transition-all border-b-2', activeTab === 'sent' ? 'border-cyber-primary text-cyber-primary' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300']"
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
        <div class="w-10 h-10 border-3 border-cyber-primary/30 border-t-cyber-primary animate-spin"></div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="applications.length === 0" class="sharp-card p-12 text-center">
        <svg class="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
        <p class="text-gray-500 dark:text-gray-400 mb-4">{{ activeTab === 'received' ? '暂无收到的申请' : '暂无发出的申请' }}</p>
      </div>

      <!-- 申请卡片列表 -->
      <div v-else class="space-y-4">
        <div
          v-for="app in applications"
          :key="app.id"
          class="sharp-card p-5 hover:border-cyber-primary/50 transition-all"
        >
          <div class="flex gap-4">
            <!-- 左侧用户信息 -->
            <router-link :to="`/profile/${activeTab === 'received' ? app.applicant_id : app.receiver_id}`" class="flex-shrink-0 flex flex-col items-center">
              <div class="w-12 h-12 bg-cyber-primary/10 border border-cyber-primary/30 flex items-center justify-center overflow-hidden">
                <span class="text-cyber-primary font-bold">{{ (activeTab === 'received' ? app.applicant_name : app.receiver_name)?.charAt(0) }}</span>
              </div>
            </router-link>

            <!-- 右侧内容 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <h3 class="text-lg font-semibold text-cyber-dark dark:text-white">
                    {{ activeTab === 'received' ? `${app.applicant_name} 申请加入` : `申请 ${app.receiver_name}` }}
                  </h3>
                  <p class="text-sm text-cyber-accent mt-1">{{ app.recruitment_title }}</p>
                </div>
                <span :class="['px-2 py-0.5 text-xs font-medium border', statusClass(app.status)]">
                  {{ statusText(app.status) }}
                </span>
              </div>

              <!-- 时间 -->
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
                {{ formatDateTime(app.created_at) }}
              </p>

              <!-- 操作按钮（收到的申请 且 状态为等待中） -->
              <div v-if="activeTab === 'received' && app.status === 'waiting'" class="flex gap-3 mt-4">
                <button
                  @click="respondApplication(app.id, true)"
                  class="px-4 py-2 bg-cyber-primary/10 text-cyber-primary border border-cyber-primary/30 hover:bg-cyber-primary/20 transition-colors text-sm"
                >
                  接受
                </button>
                <button
                  @click="respondApplication(app.id, false)"
                  class="px-4 py-2 bg-gray-100 dark:bg-cyber-darkGray text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm"
                >
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
import { ref, computed, onMounted, watch } from 'vue'
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
    'waiting': 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-500 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800',
    'accept': 'bg-green-50 dark:bg-green-900/20 text-green-500 dark:text-green-400 border-green-200 dark:border-green-800',
    'reject': 'bg-red-50 dark:bg-red-900/20 text-red-500 dark:text-red-400 border-red-200 dark:border-red-800'
  }
  return classes[status] || 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700'
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
      // 跳转到招募详情查看队伍
      const app = applications.value.find(a => a.id === applicationId)
      if (app) {
        router.push(`/recruitment/${app.recruitment_id}`)
        return
      }
    } else {
      alert('已拒绝申请')
    }

    // 刷新列表
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
