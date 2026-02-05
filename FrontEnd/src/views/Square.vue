<template>
  <div class="min-h-screen" :class="{ 'dark': isDark }">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-cyber-dark border-b border-light-border dark:border-dark-border">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/square" class="text-lg font-bold text-cyber-primary">TeaMAKE</router-link>
        <div class="flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>
          <!-- 消息入口 -->
          <router-link to="/messages" class="relative p-2 text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
            </svg>
            <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
              {{ unreadCount > 9 ? '9+' : unreadCount }}
            </span>
          </router-link>
          <!-- 队伍入口 -->
          <router-link to="/teams" class="p-2 text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </router-link>
          <router-link to="/create" class="btn-primary text-sm px-4 py-2 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            发布招募
          </router-link>
          <template v-if="currentUser">
            <router-link :to="`/profile/${currentUser.id}`" class="flex items-center gap-2">
              <div class="w-8 h-8 bg-cyber-primary/10 border border-cyber-primary/30 flex items-center justify-center overflow-hidden">
                <span class="text-sm text-cyber-primary font-medium">{{ currentUser.username?.charAt(0) }}</span>
              </div>
              <span class="text-sm text-gray-600 dark:text-gray-300">{{ currentUser.username }}</span>
            </router-link>
            <button @click="logout" class="text-sm text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="text-sm text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">登录</router-link>
          </template>
        </div>
      </div>
    </nav>

    <!-- 搜索区域 -->
    <div class="pt-20 pb-6 border-b border-light-border dark:border-dark-border bg-light-lighter dark:bg-cyber-darker/50">
      <div class="max-w-4xl mx-auto px-4">
        <div class="flex gap-4">
          <div class="flex-1 relative">
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索竞赛名称..."
              class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border rounded text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:border-cyber-primary/50 transition-colors"
              @keyup.enter="handleSearch"
            />
            <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <button @click="handleSearch" class="btn-primary px-6">搜索</button>
        </div>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="bg-light-lighter dark:bg-cyber-darker/30 border-b border-light-border dark:border-dark-border">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <div class="flex gap-2 overflow-x-auto pb-2">
          <button
            @click="activeCategory = ''"
            :class="['px-4 py-1.5 text-sm whitespace-nowrap transition-all border', !activeCategory ? 'bg-cyber-primary text-white border-cyber-primary' : 'bg-white dark:bg-cyber-dark border-light-border dark:border-dark-border text-gray-600 dark:text-gray-400 hover:border-cyber-primary/50']"
          >
            全部
          </button>
          <button
            v-for="cat in categories"
            :key="cat"
            @click="activeCategory = cat"
            :class="['px-4 py-1.5 text-sm whitespace-nowrap transition-all border', activeCategory === cat ? 'bg-cyber-primary text-white border-cyber-primary' : 'bg-white dark:bg-cyber-dark border-light-border dark:border-dark-border text-gray-600 dark:text-gray-400 hover:border-cyber-primary/50']"
          >
            {{ cat }}
          </button>
        </div>
      </div>
    </div>

    <!-- 招募列表 -->
    <div class="max-w-4xl mx-auto px-4 py-4">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-3 border-cyber-primary/30 border-t-cyber-primary animate-spin"></div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="recruitments.length === 0" class="sharp-card p-12 text-center">
        <svg class="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-gray-500 dark:text-gray-400 mb-4">暂无招募信息</p>
        <router-link to="/create" class="btn-primary inline-block">发布招募</router-link>
      </div>

      <!-- 招募卡片列表 -->
      <div v-else class="space-y-4">
        <div
          v-for="item in recruitments"
          :key="item.id"
          @click="goToDetail(item.id)"
          class="sharp-card p-5 cursor-pointer hover:border-cyber-primary/50 transition-all group"
        >
          <div class="flex gap-4">
            <!-- 左侧用户信息 -->
            <div class="flex-shrink-0 flex flex-col items-center">
              <div class="w-12 h-12 bg-cyber-primary/10 border border-cyber-primary/30 flex items-center justify-center overflow-hidden">
                <span class="text-cyber-primary font-bold">{{ item.creator_name?.charAt(0) }}</span>
              </div>
              <span class="text-xs text-gray-500 dark:text-gray-400 mt-1 truncate max-w-[60px]">{{ item.creator_name }}</span>
            </div>

            <!-- 右侧内容 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-cyber-primary transition-colors truncate">
                    {{ item.title }}
                  </h3>
                  <p class="text-sm text-cyber-accent mt-1">{{ item.competition_name }}</p>
                </div>
                <span :class="['px-2 py-0.5 text-xs font-medium border', statusClass(item.status)]">
                  {{ statusText(item.status) }}
                </span>
              </div>

              <p class="text-gray-500 dark:text-gray-400 text-sm mt-2 line-clamp-2">{{ item.description }}</p>

              <!-- 技能标签 -->
              <div v-if="item.required_skills?.length" class="flex flex-wrap gap-1.5 mt-3">
                <span
                  v-for="skill in item.required_skills.slice(0, 4)"
                  :key="skill.id"
                  class="px-2 py-0.5 bg-cyber-primary/10 text-cyber-primary text-xs border border-cyber-primary/20"
                >
                  {{ skill.name }}
                </span>
                <span v-if="item.required_skills.length > 4" class="px-2 py-0.5 bg-gray-100 dark:bg-cyber-darkGray text-gray-500 dark:text-gray-400 text-xs">
                  +{{ item.required_skills.length - 4 }}
                </span>
              </div>

              <!-- 底部信息 -->
              <div class="flex items-center gap-4 mt-3 text-xs text-gray-500 dark:text-gray-400">
                <span class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  招募 {{ item.required_number }} 人
                </span>
                <span v-if="item.deadline" class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  截止 {{ formatDate(item.deadline) }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  {{ formatDate(item.created_at) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-8">
        <button
          @click="changePage(page - 1)"
          :disabled="page <= 1"
          class="px-4 py-2 border border-light-border dark:border-dark-border bg-white dark:bg-cyber-dark text-gray-700 dark:text-gray-300 hover:border-cyber-primary/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-sm"
        >
          上一页
        </button>
        <span class="px-4 py-2 text-gray-500 dark:text-gray-400 text-sm">
          {{ page }} / {{ totalPages }}
        </span>
        <button
          @click="changePage(page + 1)"
          :disabled="page >= totalPages"
          class="px-4 py-2 border border-light-border dark:border-dark-border bg-white dark:bg-cyber-dark text-gray-700 dark:text-gray-300 hover:border-cyber-primary/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-sm"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { recruitmentAPI, applicationAPI, tokenManager } from '../api'

const router = useRouter()

const isDark = ref(false)
const loading = ref(true)
const recruitments = ref([])
const currentUser = ref(null)
const searchKeyword = ref('')
const activeCategory = ref('')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const unreadCount = ref(0)

async function loadUnreadCount() {
  try {
    const result = await applicationAPI.getUnreadCount()
    unreadCount.value = result.unread_count || 0
  } catch (err) {
    console.error('获取未读数量失败:', err)
  }
}

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

// 模拟分类数据
const categories = ref(['数学建模', '程序设计', '机械设计', '商业方案', '创新创业'])

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

function statusClass(status) {
  const classes = {
    'open': 'bg-cyber-primary/10 text-cyber-primary border-cyber-primary/20',
    'draft': 'bg-gray-100 dark:bg-cyber-darkGray text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700',
    'closed': 'bg-red-50 dark:bg-red-900/20 text-red-500 dark:text-red-400 border-red-200 dark:border-red-800',
    'completed': 'bg-cyber-secondary/10 text-cyber-secondary border-cyber-secondary/20'
  }
  return classes[status] || 'bg-gray-100 dark:bg-cyber-darkGray text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700'
}

function statusText(status) {
  const texts = {
    'open': '招募中',
    'draft': '草稿',
    'closed': '已关闭',
    'completed': '已完成'
  }
  return texts[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}-${date.getDate()}`
}

function goToDetail(id) {
  router.push(`/recruitment/${id}`)
}

function handleSearch() {
  page.value = 1
  loadRecruitments()
}

function changePage(newPage) {
  page.value = newPage
  loadRecruitments()
}

async function loadRecruitments() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      pageSize: pageSize.value,
      status: 'open'
    }
    if (searchKeyword.value) {
      params.competition_name = searchKeyword.value
    }
    const result = await recruitmentAPI.getList(params)
    recruitments.value = result.recruitments || []
    total.value = result.total || 0
  } catch (err) {
    console.error('加载招募列表失败:', err)
  } finally {
    loading.value = false
  }
}

function logout() {
  tokenManager.removeToken()
  currentUser.value = null
  router.push('/login')
}

onMounted(() => {
  // 初始化主题
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  currentUser.value = tokenManager.getUser()
  loadRecruitments()
  loadUnreadCount()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
