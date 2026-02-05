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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>
          <router-link to="/square" class="text-sm text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">返回广场</router-link>
        </div>
      </div>
    </nav>

    <!-- 页面标题 -->
    <div class="pt-20 pb-6 bg-light-lighter dark:bg-cyber-darker/50 border-b border-light-border dark:border-dark-border">
      <div class="max-w-4xl mx-auto px-4">
        <h1 class="text-2xl font-bold text-cyber-dark dark:text-white">我的队伍</h1>
      </div>
    </div>

    <!-- 队伍列表 -->
    <div class="max-w-4xl mx-auto px-4 py-6">
      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-10 h-10 border-3 border-cyber-primary/30 border-t-cyber-primary animate-spin"></div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="teams.length === 0" class="sharp-card p-12 text-center">
        <svg class="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
        </svg>
        <p class="text-gray-500 dark:text-gray-400 mb-4">还没有加入任何队伍</p>
        <router-link to="/square" class="btn-primary inline-block">去广场看看</router-link>
      </div>

      <!-- 队伍卡片列表 -->
      <div v-else class="space-y-4">
        <div
          v-for="team in teams"
          :key="team.id"
          @click="goToRecruitment(team.recruitment_id)"
          class="sharp-card p-5 cursor-pointer hover:border-cyber-primary/50 transition-all group"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="text-lg font-semibold text-cyber-dark dark:text-white group-hover:text-cyber-primary transition-colors">
                {{ team.name }}
              </h3>
              <p class="text-sm text-cyber-accent mt-1">{{ team.competition_name }}</p>
            </div>
            <span :class="['px-2 py-0.5 text-xs font-medium border', team.is_active ? 'bg-green-50 dark:bg-green-900/20 text-green-500 border-green-200 dark:border-green-800' : 'bg-gray-100 dark:bg-cyber-darkGray text-gray-500 border-gray-200 dark:border-gray-700']">
              {{ team.is_active ? '活跃中' : '已解散' }}
            </span>
          </div>

          <!-- 成员预览 -->
          <div class="flex items-center gap-2 mt-4">
            <div class="flex -space-x-2">
              <div
                v-for="(member, index) in team.members.slice(0, 4)"
                :key="member.user_id"
                class="w-8 h-8 bg-cyber-primary/10 border border-cyber-primary/30 flex items-center justify-center overflow-hidden rounded-full"
              >
                <span class="text-cyber-primary text-xs font-bold">{{ (member.username || 'U')?.charAt(0) }}</span>
              </div>
              <div
                v-if="team.members.length > 4"
                class="w-8 h-8 bg-gray-100 dark:bg-cyber-darkGray border border-gray-200 dark:border-gray-700 flex items-center justify-center overflow-hidden rounded-full"
              >
                <span class="text-gray-500 dark:text-gray-400 text-xs">+{{ team.members.length - 4 }}</span>
              </div>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">
              {{ team.members.length }} 名成员
            </span>
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
