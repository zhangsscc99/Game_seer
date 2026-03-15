<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-white">👤 个人资料</h1>

    <!-- 加载中 -->
    <div v-if="loading" class="py-16 text-center">
      <div class="w-10 h-10 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-400">加载资料...</p>
    </div>

    <template v-else>
      <!-- 指挥官卡片 -->
      <div class="game-card">
        <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6">
          <!-- 头像 -->
          <div class="relative flex-shrink-0">
            <div class="w-24 h-24 rounded-full bg-accent/20 border-4 border-accent/50 flex items-center justify-center text-4xl font-bold text-accent glow-pulse">
              {{ displayName.charAt(0).toUpperCase() }}
            </div>
          </div>

          <!-- 基本信息 -->
          <div class="flex-1 text-center sm:text-left">
            <h2 class="text-white text-2xl font-bold">{{ userStore.user?.username || displayName }}</h2>
            <p class="text-gray-400 mt-0.5">{{ userStore.user?.email }}</p>
            <p class="text-accent text-sm mt-1">指挥官</p>
          </div>

          <!-- 连续天数 -->
          <div class="text-center bg-space-700 rounded-xl p-4 border border-space-400">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-2xl">🔥</span>
              <p class="text-accent text-3xl font-bold">{{ stats?.streak_days || 0 }}</p>
            </div>
            <p class="text-gray-400 text-xs">连续打卡天数</p>
          </div>
        </div>
      </div>

      <!-- 解锁额度 -->
      <div class="game-card flex items-center justify-between">
        <div class="flex items-center gap-3">
          <SparklesIcon class="w-8 h-8 text-accent" />
          <div>
            <p class="text-white font-bold text-2xl">{{ userStore.profile?.unlock_credits ?? 0 }}</p>
            <p class="text-gray-400 text-sm">可用解锁额度</p>
          </div>
        </div>
        <p class="text-gray-500 text-xs text-right">完成任务 +1 额度<br>用于图鉴解锁精灵</p>
      </div>

      <!-- 统计数据 -->
      <div class="game-card">
        <h2 class="section-title">📊 统计数据</h2>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div
            v-for="stat in statCards"
            :key="stat.key"
            class="bg-space-700 rounded-xl p-4 text-center border border-space-400 hover:border-accent/30 transition-colors"
          >
            <component :is="stat.icon" class="w-8 h-8 mx-auto mb-2 text-accent" />
            <p class="text-white font-bold text-xl">{{ stats?.[stat.key] ?? '-' }}</p>
            <p class="text-gray-400 text-xs mt-1">{{ stat.label }}</p>
          </div>
        </div>
      </div>

      <!-- 最近获得的成就 -->
      <div class="game-card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="section-title mb-0">🏆 最近成就</h2>
          <router-link to="/achievements" class="text-accent text-sm hover:underline">查看全部</router-link>
        </div>
        <div v-if="recentAchievements.length === 0" class="py-8 text-center text-gray-500">
          还没有解锁任何成就，快去完成任务吧！
        </div>
        <div v-else class="flex flex-wrap gap-3">
          <div
            v-for="ach in recentAchievements"
            :key="ach.id"
            class="flex items-center gap-2 bg-space-700 rounded-lg p-3 border border-space-400 hover:border-accent/30 transition-colors"
            :title="ach.description"
          >
            <span class="text-2xl">{{ ach.icon || '🏅' }}</span>
            <div>
              <p class="text-white text-sm font-medium">{{ ach.name }}</p>
              <p class="text-gray-500 text-xs">{{ formatDate(ach.unlocked_at) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 主战精灵 -->
      <div v-if="elfStore.activeElf" class="game-card">
        <h2 class="section-title flex items-center gap-2"><StarIcon class="w-5 h-5 text-accent" /> 主战精灵</h2>
        <div class="flex items-center gap-4">
          <div
            class="w-20 h-20 rounded-xl overflow-hidden border-2 flex-shrink-0"
            :class="activeBorderClass"
          >
            <img
              :src="`http://localhost:8000/static/elves/${elfStore.activeElf.elf_id || elfStore.activeElf.id}.png`"
              :alt="elfStore.activeElf.name"
              class="w-full h-full object-cover"
              @error="handleImgError"
            />
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-1">
              <h3 class="text-white font-bold text-lg">{{ elfStore.activeElf.name }}</h3>
              <RarityBadge :rarity="elfStore.activeElf.rarity || 'N'" />
            </div>
            <p class="text-accent text-sm mb-2">Lv.{{ elfStore.activeElf.level }}</p>
            <ExpBar
              :current="elfStore.activeElf.current_exp || 0"
              :max="elfStore.activeElf.next_level_exp || 100"
              :level="elfStore.activeElf.level"
              size="md"
              :show-label="true"
            />
          </div>
          <router-link to="/my-elves" class="game-btn text-sm">更换</router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useElfStore } from '@/stores/elf'
import { getStats } from '@/api/profile'
import api from '@/api'
import ExpBar from '@/components/common/ExpBar.vue'
import RarityBadge from '@/components/common/RarityBadge.vue'
import { StarIcon, CheckCircleIcon, ClockIcon, BoltIcon, SparklesIcon } from '@heroicons/vue/24/solid'

const userStore = useUserStore()
const elfStore = useElfStore()

const loading = ref(false)
const stats = ref(null)
const recentAchievements = ref([])

const displayName = computed(() => userStore.displayName)

const activeBorderClass = computed(() => {
  const elf = elfStore.activeElf
  if (!elf) return 'border-gray-600'
  const map = {
    N: 'border-gray-500', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr', UR: 'border-ur'
  }
  return map[elf.rarity?.toUpperCase()] || 'border-gray-600'
})

const statCards = [
  { key: 'total_tasks_completed', icon: CheckCircleIcon, label: '总完成任务' },
  { key: 'streak_days', icon: BoltIcon, label: '连续打卡' },
  { key: 'focus_hours', icon: ClockIcon, label: '专注时长(h)' },
  { key: 'elves_collected', icon: SparklesIcon, label: '精灵收集数' }
]

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function handleImgError(e) {
  e.target.parentElement.innerHTML = '<div class="w-full h-full flex items-center justify-center text-3xl bg-space-700">🐾</div>'
}

async function loadData() {
  loading.value = true
  try {
    const [statsRes, achRes] = await Promise.allSettled([
      getStats(),
      api.get('/achievements/?limit=6&unlocked=true')
    ])
    if (statsRes.status === 'fulfilled') {
      stats.value = statsRes.value.data
    }
    if (achRes.status === 'fulfilled') {
      recentAchievements.value = (achRes.value.data || []).filter(a => a.unlocked).slice(0, 6)
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
  if (elfStore.myElves.length === 0) {
    elfStore.fetchMyElves()
  }
})
</script>
