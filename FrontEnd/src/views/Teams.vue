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
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">我的队伍</h1>
      </div>
    </div>

    <!-- 队伍列表 -->
    <div class="max-w-4xl mx-auto px-4 py-6">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="relative">
          <div class="w-16 h-16 rounded-full border-4 border-tea-200 dark:border-cyber-darkGray border-t-tea-500 animate-spin"></div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="teams.length === 0" class="zen-card p-12 text-center">
        <div class="empty-state-icon mx-auto">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </div>
        <h3 class="empty-state-title">还没有加入任何队伍</h3>
        <p class="empty-state-desc">去广场看看有没有合适的招募吧</p>
        <router-link to="/square" class="btn-primary inline-flex items-center gap-2 mt-6">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          浏览招募
        </router-link>
      </div>

      <!-- 队伍卡片列表 -->
      <div v-else class="space-y-4 stagger-animation">
        <div
          v-for="team in teams"
          :key="team.id"
          @click="goToRecruitment(team.recruitment_id)"
          class="zen-card p-5 cursor-pointer hover:shadow-tea-md transition-all group"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="min-w-0 flex-1">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-tea-500 dark:group-hover:text-tea-light transition-colors">
                {{ team.name }}
              </h3>
              <p class="text-sm text-gradient-cyber mt-1 font-medium">{{ team.competition_name }}</p>
            </div>
            <span :class="['tag-status', team.is_active ? 'open' : 'closed']">
              {{ team.is_active ? '活跃中' : '已结束' }}
            </span>
          </div>

          <!-- 成员预览 -->
          <div class="flex items-center gap-3 mt-4">
            <div class="flex -space-x-2">
              <div
                v-for="(member, index) in (team.members || []).slice(0, 4)"
                :key="member.user_id"
                class="w-9 h-9 rounded-full bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center border-2 border-white dark:border-cyber-dark shadow-tea-sm overflow-hidden"
              >
                <span class="text-white text-xs font-bold">{{ (member.username || 'U')?.charAt(0) }}</span>
              </div>
              <div
                v-if="(team.members || []).length > 4"
                class="w-9 h-9 rounded-full bg-gradient-to-br from-cyber-darkGray to-cyber-dark border-2 border-white dark:border-cyber-dark flex items-center justify-center"
              >
                <span class="text-gray-500 dark:text-gray-400 text-xs font-medium">+{{ (team.members || []).length - 4 }}</span>
              </div>
              <div
                v-if="!(team.members && team.members.length > 0)"
                class="w-9 h-9 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 dark:from-cyber-darkGray dark:to-cyber-dark border-2 border-white dark:border-cyber-dark flex items-center justify-center"
              >
                <span class="text-gray-400 dark:text-gray-500 text-xs">?</span>
              </div>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">
              {{ (team.members || []).length }} 名成员
            </span>
          </div>

          <!-- 进度条（如果有招募信息） -->
          <div v-if="team.recruitment" class="mt-4">
            <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-1">
              <span>招募进度</span>
              <span>{{ team.recruitment.current_number || 0 }} / {{ team.recruitment.required_number || 0 }}</span>
            </div>
            <div class="progress-bar">
              <div
                class="h-full bg-gradient-to-r from-tea-500 to-cyber-blue rounded-full transition-all duration-500"
                :style="{ width: `${Math.min(((team.recruitment.current_number || 0) / (team.recruitment.required_number || 1)) * 100, 100)}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { teamAPI } from '../api'

const router = useRouter()

const isDark = ref(false)
const loading = ref(true)
const teams = ref([])

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

function goToRecruitment(recruitmentId) {
  if (recruitmentId) {
    router.push(`/recruitment/${recruitmentId}`)
  }
}

async function loadTeams() {
  loading.value = true
  try {
    const result = await teamAPI.getMyTeams()
    teams.value = result.teams || []
  } catch (err) {
    console.error('获取队伍列表失败:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  loadTeams()
})
</script>
