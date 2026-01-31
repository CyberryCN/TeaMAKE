<template>
  <div class="min-h-screen cyber-bg">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-cyber-darker/80 backdrop-blur-lg border-b border-white/5">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/login" class="text-lg font-bold text-gradient">TeaMAKE</router-link>
        <div class="flex items-center gap-3">
          <span v-if="currentUser" class="text-sm text-gray-400">{{ currentUser.username }}</span>
          <button @click="logout" class="text-sm text-gray-400 hover:text-white transition-colors">退出</button>
        </div>
      </div>
    </nav>

    <!-- Banner区域 -->
    <div class="h-48 bg-gradient-to-r from-cyber-darker via-cyber-dark to-cyber-darker relative overflow-hidden">
      <!-- 装饰性网格 -->
      <div class="absolute inset-0 cyber-bg opacity-50"></div>
      <!-- 装饰性光斑 -->
      <div class="absolute top-0 right-1/4 w-64 h-64 bg-cyber-primary/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-1/4 w-48 h-48 bg-cyber-secondary/10 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-6xl mx-auto px-4">
      <!-- 用户信息卡片 -->
      <div class="relative -mt-16 mb-6">
        <div class="glass-card p-6">
          <div class="flex flex-col md:flex-row gap-6">
            <!-- 头像 -->
            <div class="relative flex-shrink-0">
              <div class="w-28 h-28 rounded-2xl bg-gradient-to-br from-cyber-primary to-cyber-secondary p-1">
                <div class="w-full h-full rounded-xl bg-cyber-darker flex items-center justify-center overflow-hidden">
                  <img v-if="user?.avatar_url" :src="user.avatar_url" class="w-full h-full object-cover" />
                  <span v-else class="text-2xl font-bold text-cyber-primary">{{ user?.username?.charAt(0)?.toUpperCase() }}</span>
                </div>
              </div>
              <!-- 在线状态指示器 -->
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-cyber-secondary rounded-full border-2 border-cyber-darker"></div>
            </div>

            <!-- 用户信息 -->
            <div class="flex-1 pt-2">
              <div class="flex items-start justify-between mb-3">
                <div>
                  <h1 class="text-2xl font-bold text-white flex items-center gap-2">
                    {{ user?.username }}
                    <span v-if="user?.authenticated" class="px-2 py-0.5 bg-cyber-secondary/20 text-cyber-secondary text-xs rounded-full">已认证</span>
                  </h1>
                  <p class="text-gray-400 text-sm mt-1">{{ user?.college }}</p>
                </div>
                <!-- 操作按钮 -->
                <div v-if="isOwnProfile" class="flex gap-2">
                  <button @click="showEditProfile = true" class="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-sm text-white transition-all">
                    编辑资料
                  </button>
                </div>
              </div>

              <!-- 简介 -->
              <p v-if="user?.bio" class="text-gray-300 text-sm mb-4">{{ user.bio }}</p>

              <!-- 统计信息 -->
              <div class="flex items-center gap-6 text-sm">
                <div class="flex items-center gap-1.5 text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  {{ user?.email }}
                </div>
                <div v-if="user?.phone" class="flex items-center gap-1.5 text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                  {{ user.phone }}
                </div>
                <div class="flex items-center gap-1.5 text-gray-400">
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
      <div class="flex gap-1 border-b border-white/10 mb-6">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="[
            'px-6 py-3 text-sm font-medium transition-all border-b-2 -mb-px',
            activeTab === tab.key
              ? 'text-cyber-primary border-cyber-primary'
              : 'text-gray-400 border-transparent hover:text-white'
          ]"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="w-10 h-10 border-3 border-cyber-primary/30 border-t-cyber-primary rounded-full animate-spin"></div>
      </div>

      <!-- 用户不存在 -->
      <div v-else-if="!user" class="glass-card p-12 text-center">
        <p class="text-gray-400">用户不存在</p>
        <router-link to="/login" class="btn-primary inline-block mt-4">返回登录</router-link>
      </div>

      <!-- 标签页内容 -->
      <template v-else>
        <!-- 主页/技能标签页 -->
        <div v-show="activeTab === 'skills'" class="space-y-6">
          <div class="glass-card p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-white">技能标签</h2>
              <button v-if="isOwnProfile" @click="showEditSkills = true" class="text-sm text-cyber-primary hover:text-cyber-secondary transition-colors">
                编辑技能
              </button>
            </div>
            <div v-if="user.skills?.length" class="flex flex-wrap gap-2">
              <span
                v-for="skill in user.skills"
                :key="skill.id"
                class="px-3 py-1.5 bg-cyber-primary/10 text-cyber-primary border border-cyber-primary/30 rounded-lg text-sm hover:bg-cyber-primary/20 transition-all"
              >
                {{ skill.name }}
              </span>
            </div>
            <p v-else class="text-gray-500 text-sm">暂无技能标签</p>
          </div>
        </div>

        <!-- 动态/竞赛经历页 -->
        <div v-show="activeTab === 'experiences'" class="glass-card p-6">
          <h2 class="text-lg font-semibold text-white mb-4">竞赛经历</h2>
          <p class="text-gray-500 text-sm">暂无竞赛经历</p>
        </div>

        <!-- 标签页 -->
        <div v-show="activeTab === 'tags'" class="glass-card p-6">
          <h2 class="text-lg font-semibold text-white mb-4">参与的标签</h2>
          <p class="text-gray-500 text-sm">暂无参与的标签</p>
        </div>
      </template>
    </div>

    <!-- 编辑资料弹窗 -->
    <div v-if="showEditProfile" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="glass-card w-full max-w-md p-6 animate-slide-up">
        <h3 class="text-xl font-bold text-white mb-6">编辑资料</h3>
        <form @submit.prevent="saveProfile" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-300 mb-2">个人简介</label>
            <textarea v-model="editForm.bio" rows="3" class="cyber-input resize-none" placeholder="介绍一下自己"></textarea>
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-2">头像URL</label>
            <input v-model="editForm.avatar_url" type="url" class="cyber-input" placeholder="头像图片链接" />
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-2">手机号</label>
            <input v-model="editForm.phone" type="tel" class="cyber-input" placeholder="手机号" />
          </div>
          <div v-if="profileError" class="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
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
    <div v-if="showEditSkills" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="glass-card w-full max-w-2xl max-h-[70vh] p-6 animate-slide-up overflow-hidden flex flex-col">
        <h3 class="text-xl font-bold text-white mb-4">编辑技能标签</h3>
        <div class="flex gap-2 mb-4 flex-wrap">
          <button
            @click="selectedCategory = ''"
            :class="['px-3 py-1.5 rounded-lg text-sm transition-all', !selectedCategory ? 'bg-cyber-primary text-cyber-dark' : 'bg-white/5 text-gray-400']"
          >
            全部
          </button>
          <button
            v-for="cat in categories"
            :key="cat.name"
            @click="selectedCategory = cat.name"
            :class="['px-3 py-1.5 rounded-lg text-sm transition-all', selectedCategory === cat.name ? 'bg-cyber-primary text-cyber-dark' : 'bg-white/5 text-gray-400']"
          >
            {{ cat.name }}
          </button>
        </div>
        <div class="flex-1 overflow-y-auto space-y-3 max-h-80">
          <div v-for="cat in filteredCategories" :key="cat.name">
            <h4 class="text-xs text-gray-500 uppercase tracking-wider mb-2">{{ cat.name }}</h4>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="skill in cat.skills"
                :key="skill.id"
                @click="toggleSkill(skill.id)"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm transition-all border',
                  selectedSkillIds.includes(skill.id)
                    ? 'bg-cyber-primary text-cyber-dark border-cyber-primary'
                    : 'bg-white/5 text-gray-300 border-white/10 hover:border-cyber-primary/50'
                ]"
              >
                {{ skill.name }}
              </button>
            </div>
          </div>
        </div>
        <div class="mt-4 pt-4 border-t border-white/10">
          <p class="text-sm text-gray-400 mb-3">已选择 {{ selectedSkillIds.length }} 个技能</p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userAPI, skillAPI } from '../api'

const route = useRoute()
const router = useRouter()

const tabs = [
  { key: 'skills', name: '技能标签' },
  { key: 'experiences', name: '竞赛经历' },
  { key: 'tags', name: '参与标签' }
]

const activeTab = ref('skills')
const loading = ref(true)
const user = ref(null)
const skills = ref([])
const categories = ref([])
const currentUser = ref(null)
const showEditProfile = ref(false)
const showEditSkills = ref(false)
const editForm = reactive({ bio: '', avatar_url: '', phone: '', college: '' })
const profileLoading = ref(false)
const profileError = ref('')
const skillLoading = ref(false)
const selectedCategory = ref('')
const selectedSkillIds = ref([])

const isOwnProfile = computed(() => {
  return currentUser.value && user.value && currentUser.value.id === user.value.id
})

const filteredCategories = computed(() => {
  if (!selectedCategory.value) return categories.value
  return categories.value.filter(c => c.name === selectedCategory.value)
})

function getCurrentUser() {
  const stored = localStorage.getItem('user')
  if (stored) currentUser.value = JSON.parse(stored)
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
  localStorage.removeItem('user')
  currentUser.value = null
  router.push('/login')
}

onMounted(() => {
  getCurrentUser()
  loadUser()
  loadSkills()
})
</script>
