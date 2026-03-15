<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-white">🏆 成就系统</h1>
      <p class="text-gray-400 text-sm mt-1">记录你的成长与荣耀</p>
    </div>

    <!-- 成就统计 -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="game-card text-center">
        <p class="text-3xl font-bold text-accent">{{ unlockedCount }}</p>
        <p class="text-gray-400 text-xs mt-1">已解锁</p>
      </div>
      <div class="game-card text-center">
        <p class="text-3xl font-bold text-gray-500">{{ totalCount }}</p>
        <p class="text-gray-400 text-xs mt-1">全部成就</p>
      </div>
      <div class="game-card text-center">
        <p class="text-3xl font-bold text-yellow-400">{{ totalPoints }}</p>
        <p class="text-gray-400 text-xs mt-1">成就点数</p>
      </div>
      <div class="game-card text-center">
        <p class="text-3xl font-bold text-green-400">{{ completionRate }}%</p>
        <p class="text-gray-400 text-xs mt-1">完成度</p>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="py-16 text-center">
      <div class="w-10 h-10 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-400">加载成就...</p>
    </div>

    <div v-else-if="error" class="game-card border-red-500/30 text-center py-8">
      <p class="text-red-400 mb-3">⚠️ {{ error }}</p>
      <button @click="loadAchievements" class="game-btn">重试</button>
    </div>

    <div v-else>
      <!-- 分类 Tab -->
      <div class="flex gap-1 bg-space-800 p-1 rounded-lg border border-space-500">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          class="flex-1 py-2 px-3 rounded text-sm font-medium transition-all duration-200"
          :class="activeTab === tab.key
            ? 'bg-accent text-space-900 font-bold'
            : 'text-gray-400 hover:text-white hover:bg-space-600'"
        >{{ tab.label }}</button>
      </div>

      <!-- 成就列表 -->
      <div v-if="filteredAchievements.length === 0" class="py-12 text-center">
        <span class="text-5xl block mb-3">🔍</span>
        <p class="text-gray-400">暂无成就</p>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="achievement in filteredAchievements"
          :key="achievement.id"
          class="game-card transition-all duration-300"
          :class="achievement.unlocked
            ? 'border-accent/30 hover:border-accent/60'
            : 'opacity-60'"
        >
          <div class="flex items-start gap-4">
            <div
              class="w-14 h-14 rounded-xl flex items-center justify-center text-3xl flex-shrink-0 border-2"
              :class="achievement.unlocked ? 'border-accent/50 bg-accent/10' : 'border-gray-700 bg-space-700'"
            >
              {{ achievement.icon || '🏅' }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <h3
                  class="font-bold text-sm"
                  :class="achievement.unlocked ? 'text-white' : 'text-gray-500'"
                >{{ achievement.name }}</h3>
                <span
                  v-if="achievement.unlocked"
                  class="text-xs bg-accent/20 text-accent px-1.5 py-0.5 rounded font-bold"
                >+{{ achievement.points }}pt</span>
              </div>
              <p class="text-gray-400 text-xs mt-1 line-clamp-2">{{ achievement.description }}</p>
              <!-- 进度条（未解锁） -->
              <div v-if="!achievement.unlocked && achievement.progress !== undefined" class="mt-2">
                <div class="flex justify-between text-xs text-gray-600 mb-0.5">
                  <span>进度</span>
                  <span>{{ achievement.progress }}/{{ achievement.max_progress }}</span>
                </div>
                <div class="w-full h-1 bg-space-700 rounded-full overflow-hidden">
                  <div
                    class="h-full bg-gray-500 rounded-full transition-all duration-500"
                    :style="{ width: Math.min(100, (achievement.progress / achievement.max_progress) * 100) + '%' }"
                  ></div>
                </div>
              </div>
              <!-- 解锁时间 -->
              <p v-if="achievement.unlocked && achievement.unlocked_at" class="text-gray-600 text-xs mt-1">
                {{ formatDate(achievement.unlocked_at) }} 解锁
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'

const achievements = ref([])
const loading = ref(false)
const error = ref(null)
const activeTab = ref('all')

const tabs = [
  { key: 'all', label: '全部' },
  { key: 'unlocked', label: '已解锁' },
  { key: 'locked', label: '未解锁' }
]

const unlockedCount = computed(() => achievements.value.filter(a => a.unlocked).length)
const totalCount = computed(() => achievements.value.length)
const totalPoints = computed(() => achievements.value.filter(a => a.unlocked).reduce((sum, a) => sum + (a.points || 0), 0))
const completionRate = computed(() => {
  if (!totalCount.value) return 0
  return Math.round((unlockedCount.value / totalCount.value) * 100)
})

const filteredAchievements = computed(() => {
  if (activeTab.value === 'unlocked') return achievements.value.filter(a => a.unlocked)
  if (activeTab.value === 'locked') return achievements.value.filter(a => !a.unlocked)
  return achievements.value
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

async function loadAchievements() {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/achievements')
    achievements.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || '加载成就失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAchievements()
})
</script>
