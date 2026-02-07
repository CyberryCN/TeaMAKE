<template>
  <div class="min-h-screen zen-bg" :class="{ 'dark': isDark }">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 nav-glass">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
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
          <router-link v-if="currentUser" :to="`/profile/${currentUser.id}`" class="flex items-center gap-2 px-3 py-1.5 rounded-zen-full bg-tea-50 dark:bg-cyber-darkGray hover:bg-tea-100 dark:hover:bg-cyber-darkBorder transition-all">
            <div class="w-7 h-7 rounded-full bg-gradient-to-br from-tea-400 to-tea-500 flex items-center justify-center">
              <span class="text-white text-xs font-bold">{{ currentUser.username?.charAt(0) }}</span>
            </div>
            <span class="text-sm text-gray-700 dark:text-gray-300">{{ currentUser.username }}</span>
          </router-link>
          <button @click="logout" class="text-sm text-gray-500 dark:text-gray-400 hover:text-tea-500 dark:hover:text-tea-light transition-colors px-3 py-2">退出</button>
        </div>
      </div>
    </nav>

    <!-- Banner区域 -->
    <div class="h-48 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-tea-500/10 via-transparent to-cyber-blue/10"></div>
      <div class="absolute top-0 right-1/4 w-96 h-96 bg-tea-500/10 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-0 left-1/4 w-64 h-64 bg-cyber-blue/10 rounded-full blur-[100px]"></div>
    </div>

    <div class="max-w-6xl mx-auto px-4">
      <!-- 用户信息卡片 -->
      <div class="relative -mt-16 mb-6 animate-scale-in">
        <div class="zen-card p-6">
          <div class="flex flex-col md:flex-row gap-6">
            <!-- 头像 -->
            <div class="relative flex-shrink-0 self-center md:self-start">
              <div class="w-28 h-28 rounded-zen-xl bg-gradient-to-br from-tea-400 to-tea-500 shadow-tea-glow flex items-center justify-center overflow-hidden">
                <img v-if="user?.avatar_url" :src="user.avatar_url" class="w-full h-full object-cover" />
                <span v-else class="text-3xl font-bold text-white">{{ user?.username?.charAt(0)?.toUpperCase() }}</span>
              </div>
              <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-gradient-to-br from-cyber-blue to-tea-light rounded-full border-2 border-white dark:border-cyber-dark"></div>
            </div>

            <!-- 用户信息 -->
            <div class="flex-1 pt-2">
              <div class="flex items-start justify-between mb-3">
                <div>
                  <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                    {{ user?.username }}
                    <span v-if="user?.authenticated" class="px-2.5 py-1 bg-gradient-to-r from-tea-500/20 to-cyber-blue/20 text-tea-600 dark:text-tea-light text-xs font-medium rounded-full border border-tea-500/30 dark:border-tea-500/50">
                      已认证
                    </span>
                  </h1>
                  <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">{{ user?.college }}</p>
                </div>
                <!-- 操作按钮 -->
                <div v-if="isOwnProfile" class="flex gap-2">
                  <button @click="showEditProfile = true" class="btn-secondary px-4 py-2 text-sm flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                    编辑资料
                  </button>
                  <router-link to="/create" class="btn-primary px-4 py-2 text-sm flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    发布招募
                  </router-link>
                </div>
              </div>

              <!-- 简介 -->
              <p v-if="user?.bio" class="text-gray-600 dark:text-gray-300 text-sm mb-4">{{ user.bio }}</p>

              <!-- 统计信息 -->
              <div class="flex flex-wrap items-center gap-4 text-sm">
                <div class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  {{ user?.email }}
                </div>
                <div v-if="user?.phone" class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                  {{ user.phone }}
                </div>
                <div class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                  </svg>
                  QQ: {{ user?.QQ_num }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 标签页导航 -->
      <div class="tabs-nav mb-6">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="['tab-item', { 'active': activeTab === tab.key }]"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="relative">
          <div class="w-16 h-16 rounded-full border-4 border-tea-200 dark:border-cyber-darkGray border-t-tea-500 animate-spin"></div>
        </div>
      </div>

      <!-- 用户不存在 -->
      <div v-else-if="!user" class="zen-card p-12 text-center">
        <div class="empty-state-icon mx-auto">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <h3 class="empty-state-title">用户不存在</h3>
        <router-link to="/login" class="btn-primary inline-flex items-center gap-2 mt-6">
          返回登录
        </router-link>
      </div>

      <!-- 标签页内容 -->
      <template v-else>
        <!-- 主页/技能标签页 -->
        <div v-show="activeTab === 'skills'" class="space-y-6">
          <div class="zen-card p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white">技能标签</h2>
              <button v-if="isOwnProfile" @click="showEditSkills = true" class="tag-category text-sm">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                </svg>
                编辑技能
              </button>
            </div>
            <div v-if="user.skills?.length" class="flex flex-wrap gap-2">
              <span
                v-for="skill in user.skills"
                :key="skill.id"
                class="tag-skill"
              >
                {{ skill.name }}
              </span>
            </div>
            <p v-else class="text-gray-500 dark:text-gray-400 text-sm">暂无技能标签</p>
          </div>
        </div>

        <!-- 动态/竞赛经历页 -->
        <div v-show="activeTab === 'experiences'" class="zen-card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">竞赛经历</h2>
          <div class="text-center py-12">
            <div class="empty-state-icon mx-auto">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
              </svg>
            </div>
            <p class="empty-state-desc mx-auto">暂无竞赛经历</p>
          </div>
        </div>

        <!-- 参与标签页 -->
        <div v-show="activeTab === 'tags'" class="zen-card p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">参与的标签</h2>
          <div class="text-center py-12">
            <div class="empty-state-icon mx-auto">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
              </svg>
            </div>
            <p class="empty-state-desc mx-auto">暂无参与的标签</p>
          </div>
        </div>

        <!-- 我的招募页 -->
        <div v-show="activeTab === 'recruitments'" class="space-y-4">
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white">我的招募</h2>
            <div class="flex gap-2">
              <button
                v-for="status in statusFilters"
                :key="status.value"
                @click="activeStatus = status.value"
                :class="['tag-category text-xs', { 'active': activeStatus === status.value }]"
              >
                {{ status.label }}
              </button>
            </div>
          </div>

          <!-- 加载招募中 -->
          <div v-if="recruitmentLoading" class="flex justify-center py-12">
            <div class="w-10 h-10 rounded-full border-3 border-tea-200 dark:border-cyber-darkGray border-t-tea-500 animate-spin"></div>
          </div>

          <!-- 无招募 -->
          <div v-else-if="!recruitments.length" class="zen-card p-12 text-center">
            <div class="empty-state-icon mx-auto">
              <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <h3 class="empty-state-title">暂无招募信息</h3>
            <p class="empty-state-desc">还没有发布过招募，快去发布一个吧</p>
            <router-link v-if="isOwnProfile" to="/create" class="btn-primary inline-flex items-center gap-2 mt-6">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              发布招募
            </router-link>
          </div>

          <!-- 招募列表 -->
          <div v-else class="space-y-3 stagger-animation">
            <div
              v-for="item in recruitments"
              :key="item.id"
              @click="goToRecruitment(item.id)"
              class="zen-card p-4 cursor-pointer hover:shadow-tea-md transition-all group"
            >
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <h3 class="text-base font-semibold text-gray-900 dark:text-white group-hover:text-tea-500 dark:group-hover:text-tea-light transition-colors truncate">
                      {{ item.title }}
                    </h3>
                    <span :class="['tag-status', statusClass(item.status)]">
                      {{ statusText(item.status) }}
                    </span>
                  </div>
                  <p class="text-sm text-gradient-cyber">{{ item.competition_name }}</p>
                  <p class="text-gray-500 dark:text-gray-400 text-sm mt-1 line-clamp-2">{{ item.description }}</p>
                </div>
                <div class="text-right text-xs text-gray-500 dark:text-gray-400 flex-shrink-0">
                  <p>{{ formatDate(item.created_at) }}</p>
                  <p class="mt-1 flex items-center justify-end gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                    </svg>
                    招募 {{ item.current_number || 0 }}/{{ item.required_number }} 人
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- 编辑资料弹窗 -->
    <div v-if="showEditProfile" class="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="zen-card w-full max-w-md p-6 animate-scale-in">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6">编辑资料</h3>
        <form @submit.prevent="saveProfile" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-700 dark:text-gray-300 mb-2">个人简介</label>
            <textarea
              v-model="editForm.bio"
              rows="3"
              class="zen-input resize-none"
              placeholder="介绍一下自己"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm text-gray-700 dark:text-gray-300 mb-2">头像URL</label>
            <input v-model="editForm.avatar_url" type="url" class="zen-input" placeholder="头像图片链接" />
          </div>
          <div>
            <label class="block text-sm text-gray-700 dark:text-gray-300 mb-2">手机号</label>
            <input v-model="editForm.phone" type="tel" class="zen-input" placeholder="手机号" />
          </div>
          <div v-if="profileError" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm rounded-zen">
            {{ profileError }}
          </div>
          <div class="flex gap-3 pt-2">
            <button type="button" @click="showEditProfile = false" class="btn-secondary flex-1">取消</button>
            <button type="submit" :disabled="profileLoading" class="btn-primary flex-1">
              {{ profileLoading ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑技能弹窗 -->
    <div v-if="showEditSkills" class="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="zen-card w-full max-w-2xl max-h-[70vh] p-6 overflow-hidden flex flex-col animate-scale-in">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">编辑技能标签</h3>
        <div class="flex gap-2 mb-4 flex-wrap">
          <button
            @click="selectedCategory = ''"
            :class="['tag-category', { 'active': !selectedCategory }]"
          >
            全部
          </button>
          <button
            v-for="cat in categories"
            :key="cat.name"
            @click="selectedCategory = cat.name"
            :class="['tag-category', { 'active': selectedCategory === cat.name }]"
          >
            {{ cat.name }}
          </button>
        </div>
        <div class="flex-1 overflow-y-auto space-y-3 max-h-80 pr-2">
          <div v-for="cat in filteredCategories" :key="cat.name">
            <h4 class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">{{ cat.name }}</h4>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="skill in cat.skills"
                :key="skill.id"
                @click="toggleSkill(skill.id)"
                :class="[
                  'tag-category text-xs',
                  { 'active': selectedSkillIds.includes(skill.id) }
                ]"
              >
                {{ skill.name }}
              </button>
            </div>
          </div>
        </div>
        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">已选择 {{ selectedSkillIds.length }} 个技能</p>
          <div class="flex gap-3">
            <button @click="showEditSkills = false" class="btn-secondary flex-1">取消</button>
            <button @click="saveSkills" :disabled="skillLoading" class="btn-primary flex-1">
              {{ skillLoading ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userAPI, skillAPI, recruitmentAPI, tokenManager } from '../api'

const route = useRoute()
const router = useRouter()

const isDark = ref(false)
const tabs = [
  { key: 'skills', name: '技能标签' },
  { key: 'experiences', name: '竞赛经历' },
  { key: 'tags', name: '参与标签' },
  { key: 'recruitments', name: '我的招募' }
]

const statusFilters = [
  { value: '', label: '全部' },
  { value: 'open', label: '招募中' },
  { value: 'draft', label: '草稿' },
  { value: 'closed', label: '已关闭' },
  { value: 'completed', label: '已完成' }
]

const activeTab = ref('skills')
const activeStatus = ref('')
const loading = ref(true)
const recruitmentLoading = ref(false)
const user = ref(null)
const skills = ref([])
const categories = ref([])
const recruitments = ref([])
const currentUser = ref(null)
const showEditProfile = ref(false)
const showEditSkills = ref(false)
const editForm = reactive({ bio: '', avatar_url: '', phone: '', college: '' })
const profileLoading = ref(false)
const profileError = ref('')
const skillLoading = ref(false)
const selectedCategory = ref('')
const selectedSkillIds = ref([])

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

const isOwnProfile = computed(() => {
  return currentUser.value && user.value && currentUser.value.id === user.value.id
})

const filteredCategories = computed(() => {
  if (!selectedCategory.value) return categories.value
  return categories.value.filter(c => c.name === selectedCategory.value)
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

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}-${date.getDate()}`
}

function goToRecruitment(id) {
  router.push(`/recruitment/${id}`)
}

function getCurrentUser() {
  currentUser.value = tokenManager.getUser()
}

async function loadUser() {
  loading.value = true
  try {
    user.value = await userAPI.getDetail(route.params.id)
    editForm.bio = user.value.bio || ''
    editForm.avatar_url = user.value.avatar_url || ''
    editForm.phone = user.value.phone || ''
    editForm.college = user.value.college || ''
    selectedSkillIds.value = (user.value.skills || []).map(s => s.id)
  } catch (err) {
    console.error('加载用户失败:', err)
    user.value = null
  } finally {
    loading.value = false
  }
}

async function loadSkills() {
  try {
    const [skillsData, catsData] = await Promise.all([
      skillAPI.getAll(),
      skillAPI.getCategories()
    ])
    const categoryMap = {}
    for (const cat of catsData) categoryMap[cat] = []
    for (const skill of skillsData) {
      const catName = skill.category_name || '未分类'
      if (!categoryMap[catName]) categoryMap[catName] = []
      categoryMap[catName].push(skill)
    }
    categories.value = Object.entries(categoryMap).map(([name, skills]) => ({ name, skills }))
  } catch (err) {
    console.error('加载技能失败:', err)
  }
}

async function loadRecruitments() {
  if (!isOwnProfile.value) return

  recruitmentLoading.value = true
  try {
    const status = activeStatus.value || undefined
    const list = await recruitmentAPI.getMyList(status)
    recruitments.value = list || []
  } catch (err) {
    console.error('加载招募列表失败:', err)
    recruitments.value = []
  } finally {
    recruitmentLoading.value = false
  }
}

function toggleSkill(skillId) {
  const index = selectedSkillIds.value.indexOf(skillId)
  if (index > -1) selectedSkillIds.value.splice(index, 1)
  else selectedSkillIds.value.push(skillId)
}

async function saveProfile() {
  profileError.value = ''
  profileLoading.value = true
  try {
    await userAPI.updateProfile(user.value.id, {
      bio: editForm.bio || null,
      avatar_url: editForm.avatar_url || null,
      phone: editForm.phone || null,
      college: editForm.college || null
    })
    showEditProfile.value = false
    await loadUser()
  } catch (err) {
    profileError.value = err.message || '保存失败'
  } finally {
    profileLoading.value = false
  }
}

async function saveSkills() {
  skillLoading.value = true
  try {
    await userAPI.updateSkills(user.value.id, selectedSkillIds.value)
    showEditSkills.value = false
    await loadUser()
  } catch (err) {
    console.error('保存技能失败:', err)
  } finally {
    skillLoading.value = false
  }
}

function logout() {
  tokenManager.removeToken()
  currentUser.value = null
  router.push('/login')
}

watch(activeTab, (newTab) => {
  if (newTab === 'recruitments') {
    loadRecruitments()
  }
})

watch(activeStatus, () => {
  loadRecruitments()
})

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  getCurrentUser()
  loadUser()
  loadSkills()
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
