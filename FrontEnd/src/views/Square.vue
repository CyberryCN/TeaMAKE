<template>
  <div class="min-h-screen zen-bg" :class="{ 'dark': isDark }">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 nav-glass">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <!-- Logo -->
        <router-link to="/square" class="flex items-center gap-2 group">
          <div class="relative">
            <div class="absolute inset-0 bg-tea-500/30 rounded-zen-lg blur-md animate-pulse-soft"></div>
            <div class="relative w-10 h-10 rounded-zen-lg bg-gradient-to-br from-tea-500 to-tea-600 flex items-center justify-center shadow-tea-md group-hover:shadow-tea-glow transition-all">
              <span class="text-white font-bold text-lg">茶</span>
            </div>
          </div>
          <span class="text-xl font-bold text-gradient-tea">TeaMAKE</span>
        </router-link>

        <!-- 右侧操作区 -->
        <div class="flex items-center gap-3">
          <!-- 主题切换 -->
          <button @click="toggleTheme" class="p-2.5 rounded-zen-full bg-tea-50 dark:bg-cyber-darkGray hover:bg-tea-100 dark:hover:bg-cyber-darkBorder transition-all group">
            <svg v-if="isDark" class="w-5 h-5 text-cyber-blue group-hover:text-cyber-blueGlow transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5 text-tea-500 group-hover:text-tea-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 0 008.354-5.646z"/>
            </svg>
          </button>

          <!-- 消息入口 -->
          <router-link to="/messages" class="relative p-2.5 rounded-zen-full bg-tea-50 dark:bg-cyber-darkGray hover:bg-tea-100 dark:hover:bg-cyber-darkBorder transition-all group">
            <svg class="w-5 h-5 text-tea-500 dark:text-cyber-blue group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
            </svg>
            <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 w-5 h-5 rounded-zen-full bg-gradient-to-r from-red-400 to-red-500 text-white text-xs font-bold flex items-center justify-center shadow-lg animate-pulse">
              {{ unreadCount > 9 ? '9+' : unreadCount }}
            </span>
          </router-link>

          <!-- 队伍入口 -->
          <router-link to="/teams" class="p-2.5 rounded-zen-full bg-tea-50 dark:bg-cyber-darkGray hover:bg-tea-100 dark:hover:bg-cyber-darkBorder transition-all group">
            <svg class="w-5 h-5 text-tea-500 dark:text-cyber-blue group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </router-link>

          <!-- 发布招募按钮 -->
          <router-link to="/create" class="btn-primary flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="text-sm">发布招募</span>
          </router-link>

          <!-- 用户菜单 -->
          <template v-if="currentUser">
            <router-link :to="`/profile/${currentUser.id}`" class="flex items-center gap-2 px-3 py-1.5 rounded-zen-full bg-tea-50 dark:bg-cyber-darkGray hover:bg-tea-100 dark:hover:bg-cyber-darkBorder transition-all">
              <div class="w-8 h-8 rounded-zen-full bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center">
                <span class="text-white text-sm font-medium">{{ currentUser.username?.charAt(0) }}</span>
              </div>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ currentUser.username }}</span>
            </router-link>
            <button @click="logout" class="px-3 py-1.5 rounded-zen-full text-sm text-gray-500 dark:text-gray-400 hover:text-tea-500 dark:hover:text-tea-light transition-colors">
              退出
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="px-4 py-2 rounded-zen-full text-sm font-medium text-tea-500 dark:text-cyber-blue hover:bg-tea-50 dark:hover:bg-cyber-darkGray transition-all">
              登录
            </router-link>
          </template>
        </div>
      </div>
    </nav>

    <!-- 搜索区域 -->
    <div class="pt-24 pb-6 px-4">
      <div class="max-w-4xl mx-auto">
        <div class="relative group">
          <div class="absolute -inset-1 bg-gradient-to-r from-tea-500 to-cyber-blue opacity-0 group-hover:opacity-20 rounded-zen-xl transition-opacity duration-300"></div>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索竞赛名称或技能..."
            class="zen-input pl-12 pr-20 text-lg relative"
            @keyup.enter="handleSearch"
          />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-tea-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <button @click="handleSearch" class="absolute right-2 top-1/2 -translate-y-1/2 btn-primary px-4 py-2 text-sm">
            搜索
          </button>
        </div>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="px-4 pb-4">
      <div class="max-w-4xl mx-auto">
        <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
          <button
            @click="activeCategory = ''"
            class="tag-category"
            :class="{ 'active': !activeCategory }"
          >
            全部
          </button>
          <button
            v-for="cat in categories"
            :key="cat"
            @click="activeCategory = cat"
            class="tag-category"
            :class="{ 'active': activeCategory === cat }"
          >
            {{ cat }}
          </button>
        </div>
      </div>
    </div>

    <!-- 招募列表 -->
    <div class="max-w-4xl mx-auto px-4 pb-12">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="relative">
          <div class="w-16 h-16 rounded-full border-4 border-tea-200 dark:border-cyber-darkGray border-t-tea-500 animate-spin"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-tea-500 text-xs font-medium">加载中...</span>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="recruitments.length === 0" class="zen-card p-12 text-center">
        <div class="empty-state-icon mx-auto">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="empty-state-title">暂无招募信息</h3>
        <p class="empty-state-desc">成为第一个发起招募的人吧！</p>
        <router-link to="/create" class="btn-primary inline-flex items-center gap-2 mt-6">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          发布招募
        </router-link>
      </div>

      <!-- 招募卡片列表 -->
      <div v-else class="space-y-4 stagger-animation">
        <div
          v-for="item in recruitments"
          :key="item.id"
          @click="goToDetail(item.id)"
          class="zen-card p-5 cursor-pointer group"
        >
          <div class="flex gap-4">
            <!-- 左侧用户信息 -->
            <div class="flex-shrink-0 flex flex-col items-center">
              <div class="w-14 h-14 rounded-zen-xl bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center shadow-tea-md group-hover:shadow-tea-glow transition-all">
                <span class="text-white font-bold text-lg">{{ item.creator_name?.charAt(0) }}</span>
              </div>
              <span class="text-xs text-gray-500 dark:text-gray-400 mt-2 truncate max-w-[70px]">{{ item.creator_name }}</span>
            </div>

            <!-- 右侧内容 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-tea-500 dark:group-hover:text-tea-light transition-colors truncate">
                    {{ item.title }}
                  </h3>
                  <p class="text-sm text-gradient-cyber mt-1 font-medium">{{ item.competition_name }}</p>
                </div>
                <span :class="['tag-status', statusClass(item.status)]">
                  {{ statusText(item.status) }}
                </span>
              </div>

              <p class="text-gray-500 dark:text-gray-400 text-sm mt-3 line-clamp-2">{{ item.description }}</p>

              <!-- 技能标签 -->
              <div v-if="item.required_skills?.length" class="flex flex-wrap gap-2 mt-4">
                <span
                  v-for="skill in item.required_skills.slice(0, 5)"
                  :key="skill.id"
                  class="tag-skill"
                >
                  {{ skill.name }}
                </span>
                <span v-if="item.required_skills.length > 5" class="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-cyber-darkGray text-gray-500 dark:text-gray-400">
                  +{{ item.required_skills.length - 5 }}
                </span>
              </div>

              <!-- 底部信息 -->
              <div class="flex items-center gap-4 mt-4 pt-4 border-t border-gray-100 dark:border-cyber-darkBorder/50">
                <span class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  <span class="font-medium">{{ item.current_number || 1 }}/{{ item.required_number }} 人</span>
                </span>
                <span v-if="item.deadline" class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  截止 {{ formatDate(item.deadline) }}
                </span>
                <span class="flex items-center gap-1.5 text-sm text-gray-400 dark:text-gray-500 ml-auto">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
          class="px-5 py-2 rounded-zen-full border border-gray-200 dark:border-cyber-darkBorder bg-white dark:bg-cyber-darkGray text-gray-700 dark:text-gray-300 hover:border-tea-400 dark:hover:border-tea-light disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          上一页
        </button>
        <span class="px-4 py-2 text-gray-500 dark:text-gray-400">
          {{ page }} / {{ totalPages }}
        </span>
        <button
          @click="changePage(page + 1)"
          :disabled="page >= totalPages"
          class="px-5 py-2 rounded-zen-full border border-gray-200 dark:border-cyber-darkBorder bg-white dark:bg-cyber-darkGray text-gray-700 dark:text-gray-300 hover:border-tea-400 dark:hover:border-tea-light disabled:opacity-40 disabled:cursor-not-allowed transition-all"
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

const categories = ref(['数学建模', '程序设计', '机械设计', '商业方案', '创新创业'])
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

function statusClass(status) {
  const classes = {
    'open': 'open',
    'draft': 'draft',
    'closed': 'closed',
    'completed': 'completed'
  }
  return classes[status] || 'draft'
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

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
