<template>
  <div class="min-h-screen" :class="{ 'dark': isDark }">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 bg-light overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-cyber-primary/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyber-secondary/10 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
    </div>

    <!-- 导航栏 -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-cyber-dark border-b border-light-border dark:border-dark-border">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/" class="text-lg font-bold text-cyber-primary">TeaMAKE</router-link>
        <div class="flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>
          <router-link to="/login" class="text-sm text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">登录</router-link>
          <router-link to="/register" class="btn-primary text-sm px-4 py-2">立即注册</router-link>
        </div>
      </div>
    </nav>

    <!-- 主内容 -->
    <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-24 h-24 bg-cyber-primary/10 border border-cyber-primary/30 mb-6 animate-float">
          <svg class="w-14 h-14 text-cyber-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h1 class="text-5xl font-bold text-cyber-dark dark:text-white mb-4">TeaMAKE</h1>
        <p class="text-xl text-gray-500 dark:text-gray-400 mb-2">大学生竞赛组队平台</p>
        <p class="text-gray-400 dark:text-gray-500">找到志同道合的队友，征战各类竞赛</p>
      </div>

      <!-- 功能特性 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mt-12">
        <div class="sharp-card p-6 text-center hover:border-cyber-primary/50 transition-all group">
          <div class="w-14 h-14 mx-auto mb-4 bg-cyber-primary/10 flex items-center justify-center group-hover:bg-cyber-primary/20 transition-all">
            <svg class="w-7 h-7 text-cyber-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-cyber-dark dark:text-white mb-2">组队招募</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm">发布招募信息，快速找到合适的队友</p>
        </div>

        <div class="sharp-card p-6 text-center hover:border-cyber-secondary/50 transition-all group">
          <div class="w-14 h-14 mx-auto mb-4 bg-cyber-secondary/10 flex items-center justify-center group-hover:bg-cyber-secondary/20 transition-all">
            <svg class="w-7 h-7 text-cyber-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-cyber-dark dark:text-white mb-2">技能标签</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm">展示你的技能，快速匹配需求</p>
        </div>

        <div class="sharp-card p-6 text-center hover:border-cyber-accent/50 transition-all group">
          <div class="w-14 h-14 mx-auto mb-4 bg-cyber-accent/10 flex items-center justify-center group-hover:bg-cyber-accent/20 transition-all">
            <svg class="w-7 h-7 text-cyber-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-cyber-dark dark:text-white mb-2">在线交流</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm">私信沟通，实时交流组队意向</p>
        </div>
      </div>

      <!-- 行动按钮 -->
      <div class="flex gap-4 mt-12">
        <router-link to="/register" class="btn-primary px-8 py-3">
          立即开始
        </router-link>
        <router-link to="/square" class="btn-secondary px-8 py-3">
          浏览招募
        </router-link>
      </div>

      <!-- 底部统计 -->
      <div class="mt-16 flex items-center gap-8 text-sm text-gray-500 dark:text-gray-400">
        <span>已有 {{ stats.users }} 位用户</span>
        <span>|</span>
        <span>{{ stats.recruitments }} 个招募信息</span>
        <span>|</span>
        <span>{{ stats.teams }} 支队伍</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { recruitmentAPI } from '../api'

const isDark = ref(false)

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

const stats = ref({
  users: 0,
  recruitments: 0,
  teams: 0
})

onMounted(() => {
  // 读取主题设置
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  // 加载统计数据
  loadStats()
})

async function loadStats() {
  try {
    const result = await recruitmentAPI.getList({ page: 1, pageSize: 1 })
    stats.value.recruitments = result.total || 0
    stats.value.users = 128
    stats.value.teams = 64
  } catch (e) {
    // 忽略错误
  }
}
</script>
