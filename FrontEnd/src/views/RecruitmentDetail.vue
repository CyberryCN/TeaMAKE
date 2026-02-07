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

    <!-- 加载状态 -->
    <div v-if="loading" class="pt-24 flex items-center justify-center min-h-screen">
      <div class="relative">
        <div class="w-16 h-16 rounded-full border-4 border-tea-200 dark:border-cyber-darkGray border-t-tea-500 animate-spin"></div>
      </div>
    </div>

    <!-- 招募详情 -->
    <div v-else-if="recruitment" class="pt-24 pb-12">
      <div class="max-w-3xl mx-auto px-4">
        <!-- 面包屑 -->
        <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-6">
          <router-link to="/square" class="hover:text-tea-500 transition-colors">广场</router-link>
          <span>/</span>
          <span class="text-gray-400">招募详情</span>
        </div>

        <!-- 标题卡片 -->
        <div class="zen-card p-6 mb-4 animate-scale-in">
          <div class="flex items-start justify-between gap-4 mb-6">
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ recruitment.title }}</h1>
              <p class="text-gradient-cyber font-medium">{{ recruitment.competition_name }}</p>
            </div>
            <span :class="['tag-status', statusClass(recruitment.status)]">
              {{ statusText(recruitment.status) }}
            </span>
          </div>

          <!-- 发布者信息 -->
          <router-link :to="`/profile/${recruitment.creator_id}`" class="flex items-center gap-3 py-4 border-t border-gray-100 dark:border-cyber-darkBorder/50 group">
            <div class="w-12 h-12 rounded-zen-xl bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center shadow-tea-md group-hover:shadow-tea-glow transition-all">
              <span class="text-white font-bold">{{ recruitment.creator_name?.charAt(0) }}</span>
            </div>
            <div>
              <p class="font-medium text-gray-800 dark:text-gray-200 group-hover:text-tea-500 transition-colors">{{ recruitment.creator_name }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">发起者</p>
            </div>
          </router-link>

          <!-- 操作按钮 -->
          <div v-if="isOwner" class="flex flex-wrap gap-3 pt-4 border-t border-gray-100 dark:border-cyber-darkBorder/50">
            <router-link :to="`/recruitment/${recruitment.id}/edit`" class="btn-secondary flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              编辑
            </router-link>
            <button v-if="recruitment.status === 'draft'" @click="publishDraft" class="btn-primary flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
              发布招募
            </button>
            <button v-if="recruitment.status === 'open'" @click="closeRecruitment" class="btn-secondary flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              关闭招募
            </button>
            <button v-if="recruitment.status === 'draft'" @click="deleteRecruitment" class="px-4 py-2 rounded-zen-lg text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              删除
            </button>
          </div>

          <!-- 非发布者申请按钮 -->
          <div v-else-if="recruitment.status === 'open'" class="flex gap-3 pt-4 border-t border-gray-100 dark:border-cyber-darkBorder/50">
            <button @click="applyRecruitment" class="btn-primary flex-1 flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
              申请加入
            </button>
          </div>
        </div>

        <!-- 招募信息 -->
        <div class="zen-card p-6 mb-4 animate-slide-up animate-delay-100">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 rounded-full bg-gradient-to-b from-tea-500 to-tea-400"></span>
            招募详情
          </h2>

          <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="p-4 rounded-zen-lg bg-tea-50 dark:bg-tea-900/20 border border-tea-200 dark:border-tea-800/30">
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">招募人数</p>
              <p class="text-2xl font-bold text-gradient-tea">{{ recruitment.required_number }}</p>
            </div>
            <div class="p-4 rounded-zen-lg bg-gradient-to-br from-tea-500/10 to-cyber-blue/10 dark:bg-tea-900/30 border border-tea-200 dark:border-tea-800/30">
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">当前成员</p>
              <p class="text-2xl font-bold text-gradient-cyber">{{ recruitment.current_number || 1 }}</p>
            </div>
          </div>

          <div class="prose max-w-none">
            <p class="text-gray-600 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">{{ recruitment.description }}</p>
          </div>

          <div v-if="recruitment.competition_url" class="mt-6 pt-4 border-t border-gray-100 dark:border-cyber-darkBorder/50">
            <a :href="recruitment.competition_url" target="_blank" class="inline-flex items-center gap-2 text-tea-500 hover:text-tea-600 dark:text-cyber-blue dark:hover:text-cyber-blueGlow transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
              访问竞赛官网
            </a>
          </div>
        </div>

        <!-- 技能要求 -->
        <div v-if="recruitment.required_skills?.length" class="zen-card p-6 mb-4 animate-slide-up animate-delay-200">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 rounded-full bg-gradient-to-b from-cyber-blue to-tea-400"></span>
            技能要求
          </h2>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="skill in recruitment.required_skills"
              :key="skill.id"
              class="tag-skill"
            >
              {{ skill.name }}
            </span>
          </div>
        </div>

        <!-- 时间安排 -->
        <div class="zen-card p-6 mb-4 animate-slide-up animate-delay-300">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 rounded-full bg-gradient-to-b from-cyber-accent to-tea-500"></span>
            时间安排
          </h2>
          <div class="space-y-4">
            <div class="flex items-center justify-between py-3 border-b border-gray-100 dark:border-cyber-darkBorder/50">
              <span class="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                <svg class="w-5 h-5 text-tea-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                招募截止
              </span>
              <span class="font-medium text-gray-800 dark:text-gray-200">{{ formatDateTime(recruitment.deadline) }}</span>
            </div>
            <div class="flex items-center justify-between py-3 border-b border-gray-100 dark:border-cyber-darkBorder/50">
              <span class="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                <svg class="w-5 h-5 text-cyber-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                预计开始
              </span>
              <span class="font-medium text-gray-800 dark:text-gray-200">{{ formatDateTime(recruitment.expected_start) }}</span>
            </div>
            <div class="flex items-center justify-between py-3">
              <span class="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                <svg class="w-5 h-5 text-cyber-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                预计结束
              </span>
              <span class="font-medium text-gray-800 dark:text-gray-200">{{ formatDateTime(recruitment.expected_end) }}</span>
            </div>
          </div>
        </div>

        <!-- 队伍成员 -->
        <div v-if="recruitment.team && recruitment.team.members?.length" class="zen-card p-6 animate-slide-up animate-delay-400">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 rounded-full bg-gradient-to-b from-cyber-green to-tea-500"></span>
            队伍成员 ({{ recruitment.team.members.length }}/{{ recruitment.required_number }})
          </h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            <router-link
              v-for="member in recruitment.team.members"
              :key="member.user_id"
              :to="`/profile/${member.user_id}`"
              class="flex flex-col items-center p-4 rounded-zen-lg border border-gray-100 dark:border-cyber-darkBorder/50 hover:border-tea-400 dark:hover:border-tea-light hover:bg-tea-50 dark:hover:bg-tea-900/20 transition-all group"
            >
              <div class="w-14 h-14 rounded-zen-xl bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center shadow-tea-md group-hover:shadow-tea-glow transition-all">
                <span class="text-white font-bold text-lg">{{ (member.username || 'U')?.charAt(0) }}</span>
              </div>
              <span class="mt-2 text-sm font-medium text-gray-700 dark:text-gray-300 truncate max-w-full">{{ member.username || '用户' }}</span>
              <span :class="['text-xs px-3 py-0.5 rounded-full mt-2 border', member.role === 'leader' ? 'bg-yellow-50 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800/50' : 'bg-tea-50 dark:bg-tea-900/30 text-tea-600 dark:text-tea-light border-tea-200 dark:border-tea-700/50']">
                {{ member.role === 'leader' ? '队长' : '成员' }}
              </span>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 不存在 -->
    <div v-else class="pt-24 flex items-center justify-center min-h-screen">
      <div class="zen-card p-12 text-center">
        <div class="empty-state-icon mx-auto">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="empty-state-title">招募不存在</h3>
        <router-link to="/square" class="btn-primary inline-flex items-center gap-2 mt-6">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          返回广场
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { recruitmentAPI, applicationAPI, tokenManager } from '../api'

const route = useRoute()
const router = useRouter()

const isDark = ref(false)
const loading = ref(true)
const recruitment = ref(null)
const currentUser = ref(null)

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

const isOwner = computed(() => {
  return currentUser.value && recruitment.value && currentUser.value.id === recruitment.value.creator_id
})

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

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

async function loadRecruitment() {
  loading.value = true
  try {
    recruitment.value = await recruitmentAPI.getDetail(route.params.id)
  } catch (err) {
    console.error('加载招募详情失败:', err)
    recruitment.value = null
  } finally {
    loading.value = false
  }
}

async function publishDraft() {
  try {
    await recruitmentAPI.publishDraft(recruitment.value.id)
    await loadRecruitment()
  } catch (err) {
    alert(err.message || '发布失败')
  }
}

async function closeRecruitment() {
  if (!confirm('确定要关闭这个招募吗？')) return
  try {
    await recruitmentAPI.close(recruitment.value.id)
    await loadRecruitment()
  } catch (err) {
    alert(err.message || '关闭失败')
  }
}

async function deleteRecruitment() {
  if (!confirm('确定要删除这个草稿吗？')) return
  try {
    await recruitmentAPI.delete(recruitment.value.id)
    router.push(`/profile/${currentUser.value.id}`)
  } catch (err) {
    alert(err.message || '删除失败')
  }
}

async function applyRecruitment() {
  if (!confirm('确定要申请加入这个团队吗？')) return
  try {
    await applicationAPI.send({ recruitment_id: recruitment.value.id })
    alert('申请已发送！等待对方响应')
  } catch (err) {
    alert(err.message || '申请失败')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  currentUser.value = tokenManager.getUser()
  loadRecruitment()
})
</script>
