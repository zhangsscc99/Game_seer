<template>
  <div class="space-y-6">
    <!-- 欢迎语 -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white">
          🌟 指挥官，今日任务已就绪
        </h1>
        <p class="text-gray-400 mt-1">{{ todayDateStr }}</p>
      </div>
      <div class="text-right">
        <div class="flex items-center gap-2 text-accent">
          <span class="text-2xl">🔥</span>
          <div>
            <p class="text-2xl font-bold">{{ profile?.streak_days || 0 }}</p>
            <p class="text-gray-400 text-xs">连续天数</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 主战精灵大卡片 + 今日概览 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 主战精灵 -->
      <div class="lg:col-span-1">
        <div class="game-card h-full">
          <h2 class="section-title">⭐ 主战精灵</h2>
          <div v-if="elfStore.activeElf" class="flex flex-col items-center">
            <!-- 精灵大图 -->
            <div
              class="w-32 h-32 rounded-xl overflow-hidden border-2 mb-4 animate-float"
              :class="rarityBorderClass"
            >
              <img
                :src="`http://localhost:8000/static/elves/${elfStore.activeElf.elf_id || elfStore.activeElf.id}.png`"
                :alt="elfStore.activeElf.name"
                class="w-full h-full object-cover"
                @error="handleElfImgError"
              />
            </div>
            <h3 class="text-white font-bold text-lg">{{ elfStore.activeElf.name }}</h3>
            <p class="text-accent text-sm mb-3">Lv.{{ elfStore.activeElf.level }}</p>
            <!-- 经验条 -->
            <div class="w-full">
              <ExpBar
                :current="elfStore.activeElf.current_exp || 0"
                :max="elfStore.activeElf.next_level_exp || 100"
                :level="elfStore.activeElf.level"
                size="md"
                :show-label="true"
              />
            </div>
            <!-- 属性 -->
            <div class="flex gap-3 mt-3">
              <div class="text-center">
                <p class="text-white font-bold">{{ elfStore.activeElf.attack || '--' }}</p>
                <p class="text-gray-500 text-xs">攻击</p>
              </div>
              <div class="w-px bg-space-500"></div>
              <div class="text-center">
                <p class="text-white font-bold">{{ elfStore.activeElf.defense || '--' }}</p>
                <p class="text-gray-500 text-xs">防御</p>
              </div>
              <div class="w-px bg-space-500"></div>
              <div class="text-center">
                <p class="text-white font-bold">{{ elfStore.activeElf.speed || '--' }}</p>
                <p class="text-gray-500 text-xs">速度</p>
              </div>
            </div>
          </div>
          <div v-else class="flex flex-col items-center py-8 text-center">
            <span class="text-5xl mb-3">🐾</span>
            <p class="text-gray-400 text-sm mb-3">还没有主战精灵</p>
            <router-link to="/my-elves" class="game-btn text-sm">前往设置</router-link>
          </div>
        </div>
      </div>

      <!-- 今日概览 -->
      <div class="lg:col-span-2 space-y-4">
        <!-- 任务摘要 -->
        <div class="game-card">
          <h2 class="section-title">📋 今日任务</h2>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="bg-space-700 rounded-lg p-4 text-center border border-space-400">
              <p class="text-3xl font-bold text-accent">{{ pendingCount }}</p>
              <p class="text-gray-400 text-xs mt-1">待完成</p>
            </div>
            <div class="bg-space-700 rounded-lg p-4 text-center border border-space-400">
              <p class="text-3xl font-bold text-green-400">{{ completedCount }}</p>
              <p class="text-gray-400 text-xs mt-1">已完成</p>
            </div>
            <div class="bg-space-700 rounded-lg p-4 text-center border border-space-400">
              <p class="text-3xl font-bold text-blue-400">{{ totalExp }}</p>
              <p class="text-gray-400 text-xs mt-1">今日EXP</p>
            </div>
            <div class="bg-space-700 rounded-lg p-4 text-center border border-space-400">
              <p class="text-3xl font-bold text-yellow-400">{{ completionRate }}%</p>
              <p class="text-gray-400 text-xs mt-1">完成率</p>
            </div>
          </div>
          <!-- 进度条 -->
          <div class="mt-4">
            <div class="flex justify-between text-xs text-gray-400 mb-1">
              <span>今日进度</span>
              <span>{{ completedCount }}/{{ totalCount }}</span>
            </div>
            <div class="w-full h-2 bg-space-700 rounded-full overflow-hidden">
              <div
                class="h-full bg-green-500 rounded-full transition-all duration-700"
                :style="{ width: completionRate + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <!-- 指挥官状态 -->
        <div class="game-card">
          <h2 class="section-title">👤 指挥官状态</h2>
          <div class="flex items-center gap-4 mb-3">
            <div class="w-14 h-14 rounded-full bg-accent/20 border-2 border-accent/50 flex items-center justify-center flex-shrink-0">
              <span class="text-accent font-bold text-xl">{{ displayName.charAt(0).toUpperCase() }}</span>
            </div>
            <div class="flex-1">
              <p class="text-white font-bold text-lg">{{ displayName }}</p>
              <p class="text-accent text-sm">Lv.{{ userStore.level }} 指挥官</p>
            </div>
          </div>
          <ExpBar
            :current="userStore.currentExp"
            :max="userStore.nextLevelExp"
            :level="userStore.level"
            size="lg"
            :show-label="true"
            :show-level="true"
          />
        </div>
      </div>
    </div>

    <!-- 快捷入口 -->
    <div class="game-card">
      <h2 class="section-title">⚡ 快捷入口</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <router-link
          v-for="item in quickLinks"
          :key="item.path"
          :to="item.path"
          class="flex flex-col items-center gap-2 p-4 bg-space-700 rounded-lg border border-space-400 hover:border-accent/50 hover:bg-space-600 transition-all duration-200 group"
        >
          <span class="text-3xl group-hover:scale-110 transition-transform">{{ item.icon }}</span>
          <span class="text-gray-300 text-sm font-medium group-hover:text-white">{{ item.label }}</span>
          <span v-if="item.desc" class="text-gray-600 text-xs text-center">{{ item.desc }}</span>
        </router-link>
      </div>
    </div>

    <!-- 最近任务 -->
    <div class="game-card">
      <div class="flex items-center justify-between mb-4">
        <h2 class="section-title mb-0">📌 待完成任务</h2>
        <router-link to="/tasks" class="text-accent text-sm hover:underline">查看全部 →</router-link>
      </div>
      <div v-if="taskStore.loading" class="py-8 text-center text-gray-500">
        <div class="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        加载中...
      </div>
      <div v-else-if="recentPendingTasks.length === 0" class="py-8 text-center">
        <span class="text-4xl block mb-2">✅</span>
        <p class="text-gray-400">今日任务已全部完成！</p>
      </div>
      <div v-else class="space-y-2">
        <div
          v-for="task in recentPendingTasks"
          :key="task.id"
          class="flex items-center gap-3 p-3 bg-space-700 rounded-lg"
        >
          <div class="w-2 h-2 rounded-full bg-accent flex-shrink-0"></div>
          <span class="text-white text-sm flex-1 truncate">{{ task.title }}</span>
          <span class="text-accent text-xs">+{{ task.exp_reward || 10 }} EXP</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useTaskStore } from '@/stores/task'
import { useElfStore } from '@/stores/elf'
import ExpBar from '@/components/common/ExpBar.vue'

const userStore = useUserStore()
const taskStore = useTaskStore()
const elfStore = useElfStore()

const displayName = computed(() => userStore.displayName)
const profile = computed(() => userStore.profile)

const todayDateStr = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 · ${['日','一','二','三','四','五','六'][d.getDay()]}曜日`
})

const totalCount = computed(() => taskStore.tasks.length)
const pendingCount = computed(() => taskStore.pendingTasks.length)
const completedCount = computed(() => taskStore.completedTasks.length)
const completionRate = computed(() => {
  if (!totalCount.value) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})
const totalExp = computed(() =>
  taskStore.completedTasks.reduce((sum, t) => sum + (t.exp_reward || 10), 0)
)

const recentPendingTasks = computed(() => taskStore.pendingTasks.slice(0, 5))

const rarityBorderClass = computed(() => {
  const elf = elfStore.activeElf
  if (!elf) return 'border-gray-600'
  const map = {
    N: 'border-gray-600', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr shadow-glow-ssr', UR: 'border-ur shadow-glow-ur'
  }
  return map[elf.rarity?.toUpperCase()] || 'border-gray-600'
})

const quickLinks = [
  { path: '/tasks', icon: '📋', label: '今日任务', desc: '查看待完成任务' },
  { path: '/elves', icon: '📖', label: '精灵图鉴', desc: '探索全部精灵' },
  { path: '/boss', icon: '⚔️', label: 'Boss挑战', desc: '挑战强大Boss' },
  { path: '/achievements', icon: '🏆', label: '成就系统', desc: '查看获得成就' }
]

function handleElfImgError(e) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-5xl">🐾</div>'
}

onMounted(async () => {
  try {
    if (taskStore.tasks.length === 0) {
      await taskStore.fetchTasks()
    }
  } catch {
    // Silent fail
  }
})
</script>
