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

    <!-- 加载状态 -->
    <div v-if="loading" class="pt-20 flex items-center justify-center min-h-screen">
      <div class="w-10 h-10 border-3 border-cyber-primary/30 border-t-cyber-primary animate-spin"></div>
    </div>

    <!-- 招募详情 -->
    <div v-else-if="recruitment" class="pt-20 pb-12">
      <div class="max-w-3xl mx-auto px-4">
        <!-- 面包屑 -->
        <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-4">
          <router-link to="/square" class="hover:text-cyber-primary transition-colors">广场</router-link>
          <span>/</span>
          <span class="text-gray-400">招募详情</span>
        </div>

        <!-- 标题区域 -->
        <div class="sharp-card p-6 mb-4">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div>
              <h1 class="text-2xl font-bold text-cyber-dark dark:text-white">{{ recruitment.title }}</h1>
              <p class="text-cyber-accent mt-1">{{ recruitment.competition_name }}</p>
            </div>
            <span :class="['px-3 py-1 text-sm font-medium border', statusClass(recruitment.status)]">
              {{ statusText(recruitment.status) }}
            </span>
          </div>

          <!-- 发布者信息 -->
          <div class="flex items-center gap-3 py-4 border-t border-light-border dark:border-dark-border">
            <router-link :to="`/profile/${recruitment.creator_id}`" class="flex items-center gap-3 group">
              <div class="w-10 h-10 bg-cyber-primary/10 border border-cyber-primary/30 flex items-center justify-center overflow-hidden">
                <span class="text-cyber-primary font-bold">{{ recruitment.creator_name?.charAt(0) }}</span>
              </div>
              <div>
                <p class="text-cyber-dark dark:text-white group-hover:text-cyber-primary transition-colors">{{ recruitment.creator_name }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">发布者</p>
              </div>
            </router-link>
          </div>

          <!-- 操作按钮 -->
          <div v-if="isOwner" class="flex gap-3 pt-4 border-t border-light-border dark:border-dark-border">
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
              发布
            </button>
            <button v-if="recruitment.status === 'open'" @click="closeRecruitment" class="btn-secondary flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              关闭
            </button>
            <button v-if="recruitment.status === 'draft'" @click="deleteRecruitment" class="text-red-500 dark:text-red-400 hover:text-red-400 dark:hover:text-red-300 flex items-center gap-2 px-4 py-2 border border-red-200 dark:border-red-800 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              删除
            </button>
          </div>

          <!-- 非发布者显示申请按钮 -->
          <div v-else-if="recruitment.status === 'open'" class="flex gap-3 pt-4 border-t border-light-border dark:border-dark-border">
            <button @click="applyRecruitment" class="btn-primary flex-1 flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
              申请加入
            </button>
          </div>
        </div>

        <!-- 详细信息 -->
        <div class="sharp-card p-6 mb-4">
          <h2 class="text-lg font-semibold text-cyber-dark dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 bg-cyber-primary"></span>
            招募详情
          </h2>

          <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="p-4 border border-light-border dark:border-dark-border">
              <p class="text-gray-500 dark:text-gray-400 text-sm">招募人数</p>
              <p class="text-xl font-bold text-cyber-dark dark:text-white">{{ recruitment.required_number }} 人</p>
            </div>
            <div class="p-4 border border-light-border dark:border-dark-border">
              <p class="text-gray-500 dark:text-gray-400 text-sm">当前人数</p>
              <p class="text-xl font-bold text-cyber-dark dark:text-white">{{ recruitment.current_number }} 人</p>
            </div>
          </div>

          <div class="prose max-w-none">
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{{ recruitment.description }}</p>
          </div>

          <div v-if="recruitment.competition_url" class="mt-4">
            <a :href="recruitment.competition_url" target="_blank" class="text-cyber-primary hover:text-cyber-secondary flex items-center gap-1 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
              竞赛官网链接
            </a>
          </div>
        </div>

        <!-- 技能要求 -->
        <div v-if="recruitment.required_skills?.length" class="sharp-card p-6 mb-4">
          <h2 class="text-lg font-semibold text-cyber-dark dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 bg-cyber-secondary"></span>
            技能要求
          </h2>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="skill in recruitment.required_skills"
              :key="skill.id"
              class="px-3 py-1.5 bg-cyber-primary/10 text-cyber-primary border border-cyber-primary/30 text-sm"
            >
              {{ skill.name }}
            </span>
          </div>
        </div>

        <!-- 时间安排 -->
        <div class="sharp-card p-6">
          <h2 class="text-lg font-semibold text-cyber-dark dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 bg-cyber-accent"></span>
            时间安排
          </h2>
          <div class="space-y-3">
            <div class="flex items-center justify-between py-2 border-b border-light-border dark:border-dark-border">
              <span class="text-gray-500 dark:text-gray-400">招募截止</span>
              <span class="text-cyber-dark dark:text-white">{{ formatDateTime(recruitment.deadline) }}</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b border-light-border dark:border-dark-border">
              <span class="text-gray-500 dark:text-gray-400">预计开始</span>
              <span class="text-cyber-dark dark:text-white">{{ formatDateTime(recruitment.expected_start) }}</span>
            </div>
            <div class="flex items-center justify-between py-2">
              <span class="text-gray-500 dark:text-gray-400">预计结束</span>
              <span class="text-cyber-dark dark:text-white">{{ formatDateTime(recruitment.expected_end) }}</span>
            </div>
          </div>
        </div>

        <!-- 队伍成员 -->
        <div v-if="recruitment.team && recruitment.team.members?.length" class="sharp-card p-6">
          <h2 class="text-lg font-semibold text-cyber-dark dark:text-white mb-4 flex items-center gap-2">
            <span class="w-1 h-5 bg-green-500"></span>
            队伍成员 ({{ recruitment.team.members.length }}/{{ recruitment.required_number }})
          </h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            <router-link
              v-for="member in recruitment.team.members"
              :key="member.user_id"
              :to="`/profile/${member.user_id}`"
              class="flex flex-col items-center p-4 border border-light-border dark:border-dark-border hover:border-cyber-primary/50 transition-all"
            >
              <div class="w-14 h-14 bg-cyber-primary/10 border border-cyber-primary/30 flex items-center justify-center overflow-hidden rounded-full">
                <span class="text-cyber-primary font-bold text-lg">{{ (member.username || '用户')?.charAt(0) }}</span>
              </div>
              <span class="mt-2 text-sm text-gray-700 dark:text-gray-300 truncate max-w-full">{{ member.username || '用户' + member.user_id }}</span>
              <span :class="['text-xs px-2 py-0.5 mt-1 border', member.role === 'leader' ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-500 border-yellow-200 dark:border-yellow-800' : 'bg-gray-100 dark:bg-cyber-darkGray text-gray-500 border-gray-200 dark:border-gray-700']">
                {{ member.role === 'leader' ? '队长' : '成员' }}
              </span>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 不存在 -->
    <div v-else class="pt-20 flex items-center justify-center min-h-screen">
      <div class="text-center">
        <p class="text-gray-500 dark:text-gray-400 mb-4">招募不存在</p>
        <router-link to="/square" class="btn-primary">返回广场</router-link>
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
