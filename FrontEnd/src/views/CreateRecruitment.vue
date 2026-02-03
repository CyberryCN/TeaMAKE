<template>
  <div class="min-h-screen" :class="{ 'dark': isDark }">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-cyber-dark border-b border-light-border dark:border-dark-border">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/square" class="text-lg font-bold text-cyber-primary">TeaMAKE</router-link>
        <router-link to="/square" class="text-sm text-gray-500 dark:text-gray-400 hover:text-cyber-primary transition-colors">返回广场</router-link>
      </div>
    </nav>

    <div class="pt-20 pb-12">
      <div class="max-w-2xl mx-auto px-4">
        <!-- 标题 -->
        <div class="mb-8">
          <h1 class="text-2xl font-bold text-cyber-dark dark:text-white">发布招募</h1>
          <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">填写招募信息，找到合适的队友</p>
        </div>

        <!-- 表单 -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 基本信息 -->
          <div class="sharp-card p-6 space-y-4">
            <h2 class="text-lg font-semibold text-cyber-dark dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 bg-cyber-primary"></span>
              基本信息
            </h2>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                招募标题 <span class="text-cyber-primary">*</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                placeholder="例如：招募数学建模队友"
                required
                maxlength="200"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                目标竞赛 <span class="text-cyber-primary">*</span>
              </label>
              <input
                v-model="form.competition_name"
                type="text"
                class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                placeholder="例如：全国大学生数学建模竞赛"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">竞赛链接</label>
              <input
                v-model="form.competition_url"
                type="url"
                class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                placeholder="竞赛官网链接（可选）"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                招募人数 <span class="text-cyber-primary">*</span>
              </label>
              <input
                v-model.number="form.required_number"
                type="number"
                min="1"
                max="20"
                class="w-32 px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                required
              />
            </div>
          </div>

          <!-- 详细内容 -->
          <div class="sharp-card p-6 space-y-4">
            <h2 class="text-lg font-semibold text-cyber-dark dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 bg-cyber-secondary"></span>
              详细内容
            </h2>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                详细描述 <span class="text-cyber-primary">*</span>
              </label>
              <textarea
                v-model="form.description"
                rows="5"
                class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors resize-none"
                placeholder="详细介绍你的招募需求，包括：&#10;- 项目背景&#10;- 需要的技能&#10;- 时间安排&#10;- 期望的目标"
                required
              ></textarea>
            </div>
          </div>

          <!-- 时间安排 -->
          <div class="sharp-card p-6 space-y-4">
            <h2 class="text-lg font-semibold text-cyber-dark dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 bg-cyber-accent"></span>
              时间安排
            </h2>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  招募截止 <span class="text-cyber-primary">*</span>
                </label>
                <input
                  v-model="form.deadline"
                  type="datetime-local"
                  class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  预计开始 <span class="text-cyber-primary">*</span>
                </label>
                <input
                  v-model="form.expected_start"
                  type="datetime-local"
                  class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                  required
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                预计结束 <span class="text-cyber-primary">*</span>
              </label>
              <input
                v-model="form.expected_end"
                type="datetime-local"
                class="w-full px-4 py-2.5 bg-white dark:bg-cyber-darkGray border border-light-border dark:border-dark-border text-gray-900 dark:text-white focus:outline-none focus:border-cyber-primary/50 transition-colors"
                required
              />
            </div>
          </div>

          <!-- 技能要求 -->
          <div class="sharp-card p-6 space-y-4">
            <h2 class="text-lg font-semibold text-cyber-dark dark:text-white flex items-center gap-2">
              <span class="w-1 h-5 bg-gradient-to-b from-cyber-primary to-cyber-secondary"></span>
              技能要求
            </h2>

            <div class="flex gap-2 mb-4 flex-wrap">
              <button
                type="button"
                @click="selectedCategory = ''"
                :class="['px-3 py-1.5 text-sm transition-all border', !selectedCategory ? 'bg-cyber-primary text-white border-cyber-primary' : 'bg-white dark:bg-cyber-dark border-light-border dark:border-dark-border text-gray-600 dark:text-gray-400']"
              >
                全部
              </button>
              <button
                type="button"
                v-for="cat in categories"
                :key="cat.name"
                @click="selectedCategory = cat.name"
                :class="['px-3 py-1.5 text-sm transition-all border', selectedCategory === cat.name ? 'bg-cyber-primary text-white border-cyber-primary' : 'bg-white dark:bg-cyber-dark border-light-border dark:border-dark-border text-gray-600 dark:text-gray-400']"
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
                  'px-3 py-1.5 text-sm transition-all border',
                  selectedSkillIds.includes(skill.id)
                    ? 'bg-cyber-primary text-white border-cyber-primary'
                    : 'bg-white dark:bg-cyber-dark border-light-border dark:border-dark-border text-gray-700 dark:text-gray-300 hover:border-cyber-primary/50'
                ]"
              >
                {{ skill.name }}
              </button>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">已选择 {{ selectedSkillIds.length }} 个技能</p>
          </div>

          <!-- 错误提示 -->
          <div v-if="error" class="p-4 border bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-500 dark:text-red-400 text-sm">
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
import { useRouter } from 'vue-router'
import { recruitmentAPI, skillAPI } from '../api'

const router = useRouter()

const isDark = ref(false)
const loading = ref(false)
const error = ref('')
const categories = ref([])
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

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    const data = {
      ...form,
      deadline: new Date(form.deadline).toISOString(),
      expected_start: new Date(form.expected_start).toISOString(),
      expected_end: new Date(form.expected_end).toISOString(),
      required_skills: selectedSkillIds.value
    }

    const result = await recruitmentAPI.publish(data)
    router.push(`/recruitment/${result.id}`)
  } catch (err) {
    error.value = err.message || '发布失败，请检查必填项'
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

    const result = await recruitmentAPI.createDraft(data)
    router.push(`/recruitment/${result.id}`)
  } catch (err) {
    error.value = err.message || '保存失败'
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

  loadSkills()
})
</script>
