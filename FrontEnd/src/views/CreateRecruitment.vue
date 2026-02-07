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
        <router-link to="/square" class="px-4 py-2 rounded-zen-full text-sm text-gray-500 dark:text-gray-400 hover:text-tea-500 dark:hover:text-tea-light transition-colors">
          返回广场
        </router-link>
      </div>
    </nav>

    <div class="pt-20 pb-12">
      <div class="max-w-2xl mx-auto px-4">
        <!-- 标题 -->
        <div class="mb-8 animate-fade-in">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ isEditing ? '编辑招募' : '发布招募' }}</h1>
          <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">{{ isEditing ? '修改招募信息' : '填写招募信息，找到合适的队友' }}</p>
        </div>

        <!-- 表单 -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 基本信息 -->
          <div class="zen-card p-6 space-y-4 animate-slide-up">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 rounded-full bg-gradient-to-b from-tea-500 to-tea-400"></span>
              基本信息
            </h2>

            <div class="group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                招募标题 <span class="text-tea-500">*</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                class="zen-input"
                placeholder="例如：招募数学建模队友"
                required
                maxlength="200"
              />
            </div>

            <div class="group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                目标竞赛 <span class="text-tea-500">*</span>
              </label>
              <input
                v-model="form.competition_name"
                type="text"
                class="zen-input"
                placeholder="例如：全国大学生数学建模竞赛"
                required
              />
            </div>

            <div class="group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                竞赛链接
              </label>
              <input
                v-model="form.competition_url"
                type="url"
                class="zen-input"
                placeholder="竞赛官网链接（可选）"
              />
            </div>

            <div class="group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                招募人数 <span class="text-tea-500">*</span>
              </label>
              <input
                v-model.number="form.required_number"
                type="number"
                min="1"
                max="20"
                class="zen-input w-32"
                required
              />
            </div>
          </div>

          <!-- 详细内容 -->
          <div class="zen-card p-6 space-y-4 animate-slide-up animate-delay-100">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 rounded-full bg-gradient-to-b from-cyber-blue to-tea-400"></span>
              详细内容
            </h2>

            <div class="group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                详细描述 <span class="text-tea-500">*</span>
              </label>
              <textarea
                v-model="form.description"
                rows="5"
                class="zen-input resize-none"
                placeholder="详细介绍你的招募需求，包括：&#10;- 项目背景&#10;- 需要的技能&#10;- 时间安排&#10;- 期望的目标"
                required
              ></textarea>
            </div>
          </div>

          <!-- 时间安排 -->
          <div class="zen-card p-6 space-y-4 animate-slide-up animate-delay-200">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 rounded-full bg-gradient-to-b from-cyber-green to-tea-500"></span>
              时间安排
            </h2>

            <div class="grid grid-cols-2 gap-4">
              <div class="group">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                  招募截止 <span class="text-tea-500">*</span>
                </label>
                <input
                  v-model="form.deadline"
                  type="datetime-local"
                  class="zen-input"
                  required
                />
              </div>
              <div class="group">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                  预计开始 <span class="text-tea-500">*</span>
                </label>
                <input
                  v-model="form.expected_start"
                  type="datetime-local"
                  class="zen-input"
                  required
                />
              </div>
            </div>

            <div class="group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 transition-colors group-focus-within:text-tea-500">
                预计结束 <span class="text-tea-500">*</span>
              </label>
              <input
                v-model="form.expected_end"
                type="datetime-local"
                class="zen-input"
                required
              />
            </div>
          </div>

          <!-- 技能要求 -->
          <div class="zen-card p-6 space-y-4 animate-slide-up animate-delay-300">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 rounded-full bg-gradient-to-b from-cyber-accent to-tea-500"></span>
              技能要求
            </h2>

            <div class="flex gap-2 mb-4 flex-wrap">
              <button
                type="button"
                @click="selectedCategory = ''"
                :class="['tag-category', { 'active': !selectedCategory }]"
              >
                全部
              </button>
              <button
                type="button"
                v-for="cat in categories"
                :key="cat.name"
                @click="selectedCategory = cat.name"
                :class="['tag-category', { 'active': selectedCategory === cat.name }]"
              >
                {{ cat.name }}
              </button>
            </div>

            <div class="flex flex-wrap gap-2">
              <button
                type="button"
                v-for="skill in filteredSkills"
                :key="skill.id"
                @click="toggleSkill(skill.id)"
                :class="[
                  'tag-category',
                  { 'active': selectedSkillIds.includes(skill.id) }
                ]"
              >
                {{ skill.name }}
              </button>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">已选择 {{ selectedSkillIds.length }} 个技能</p>
          </div>

          <!-- 错误提示 -->
          <div v-if="error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm rounded-zen animate-fade-in">
            {{ error }}
          </div>

          <!-- 提交按钮 -->
          <div class="flex gap-4">
            <button
              type="button"
              @click="saveDraft"
              :disabled="loading"
              class="btn-secondary flex-1 flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
              </svg>
              保存草稿
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="btn-primary flex-1 flex items-center justify-center gap-2"
            >
              <svg v-if="loading" class="animate-spin w-5 h-5" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
              {{ loading ? '发布中...' : '直接发布' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { recruitmentAPI, skillAPI } from '../api'

const router = useRouter()
const route = useRoute()

const isDark = ref(false)
const loading = ref(false)
const error = ref('')
const categories = ref([])
const selectedCategory = ref('')
const selectedSkillIds = ref([])

// 判断是否为编辑模式
const isEditing = computed(() => !!route.params.id)
const recruitmentId = computed(() => route.params.id ? parseInt(route.params.id) : null)

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

const form = reactive({
  title: '',
  description: '',
  competition_name: '',
  competition_url: '',
  required_number: 1,
  deadline: '',
  expected_start: '',
  expected_end: '',
  required_skills: []
})

const filteredSkills = computed(() => {
  if (!selectedCategory.value) {
    return categories.value.flatMap(c => c.skills || [])
  }
  const cat = categories.value.find(c => c.name === selectedCategory.value)
  return cat?.skills || []
})

function toggleSkill(skillId) {
  const index = selectedSkillIds.value.indexOf(skillId)
  if (index > -1) {
    selectedSkillIds.value.splice(index, 1)
  } else {
    selectedSkillIds.value.push(skillId)
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

async function loadRecruitment() {
  if (!isEditing.value) return

  loading.value = true
  try {
    const data = await recruitmentAPI.getDetail(recruitmentId.value)
    form.title = data.title || ''
    form.description = data.description || ''
    form.competition_name = data.competition_name || ''
    form.competition_url = data.competition_url || ''
    form.required_number = data.required_number || 1
    form.required_skills = data.required_skills?.map(s => s.id) || []

    // 转换日期格式
    if (data.deadline) {
      form.deadline = new Date(data.deadline).toISOString().slice(0, 16)
    }
    if (data.expected_start) {
      form.expected_start = new Date(data.expected_start).toISOString().slice(0, 16)
    }
    if (data.expected_end) {
      form.expected_end = new Date(data.expected_end).toISOString().slice(0, 16)
    }

    selectedSkillIds.value = data.required_skills?.map(s => s.id) || []
  } catch (err) {
    console.error('加载招募信息失败:', err)
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    const data = {
      title: form.title,
      description: form.description,
      competition_name: form.competition_name,
      competition_url: form.competition_url || null,
      required_number: form.required_number,
      deadline: new Date(form.deadline).toISOString(),
      expected_start: new Date(form.expected_start).toISOString(),
      expected_end: new Date(form.expected_end).toISOString(),
      required_skills: selectedSkillIds.value
    }

    if (isEditing.value) {
      await recruitmentAPI.update(recruitmentId.value, data)
      router.push(`/recruitment/${recruitmentId.value}`)
    } else {
      const result = await recruitmentAPI.publish(data)
      router.push(`/recruitment/${result.id}`)
    }
  } catch (err) {
    error.value = err.message || (isEditing.value ? '更新失败' : '发布失败')
  } finally {
    loading.value = false
  }
}

async function saveDraft() {
  error.value = ''
  loading.value = true

  try {
    const data = {
      title: form.title || null,
      description: form.description || null,
      competition_name: form.competition_name || null,
      competition_url: form.competition_url || null,
      required_number: form.required_number,
      deadline: form.deadline ? new Date(form.deadline).toISOString() : null,
      expected_start: form.expected_start ? new Date(form.expected_start).toISOString() : null,
      expected_end: form.expected_end ? new Date(form.expected_end).toISOString() : null,
      required_skills: selectedSkillIds.value
    }

    if (isEditing.value) {
      await recruitmentAPI.update(recruitmentId.value, data)
      router.push(`/recruitment/${recruitmentId.value}`)
    } else {
      const result = await recruitmentAPI.createDraft(data)
      router.push(`/recruitment/${result.id}`)
    }
  } catch (err) {
    error.value = err.message || (isEditing.value ? '更新失败' : '保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  updateTheme()

  await loadSkills()
  await loadRecruitment()
})
</script>
