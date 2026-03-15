<template>
  <div class="space-y-6">
    <!-- 返回按钮 -->
    <div class="flex items-center gap-3">
      <button @click="router.back()" class="game-btn flex items-center gap-2">
        ← 返回
      </button>
      <h1 class="text-xl font-bold text-white">精灵详情</h1>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="py-24 text-center">
      <div class="w-12 h-12 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
      <p class="text-gray-400">加载精灵数据...</p>
    </div>

    <!-- 错误 -->
    <div v-else-if="error" class="game-card border-red-500/30 text-center py-12">
      <p class="text-red-400 text-lg mb-4 flex items-center justify-center gap-2"><ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" /> {{ error }}</p>
      <button @click="loadElf" class="game-btn">重新加载</button>
    </div>

    <!-- 精灵详情 -->
    <div v-else-if="elf" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 左侧：精灵立绘 -->
      <div class="flex flex-col items-center">
        <div
          class="relative w-full max-w-xs aspect-square rounded-2xl overflow-hidden border-4 mb-6 animate-float flex items-center justify-center"
          :class="[rarityBorderClass, rarityBgClass]"
        >
          <img
            :src="elf.image_path || `http://localhost:8000/static/elves/${elf.id}.png`"
            :alt="elf.name"
            class="w-full h-full object-contain p-3"
            @error="handleImgError"
          />
          <div class="absolute inset-0 pointer-events-none" :class="rarityGlowOverlay"></div>
        </div>

        <!-- 稀有度标签 -->
        <RarityBadge :rarity="elf.rarity" />

        <h2 class="text-white text-2xl font-bold mt-3">{{ elf.name }}</h2>
        <p class="text-gray-400 mt-1">{{ elf.element }} 系 · {{ elf.category || '精灵' }}</p>

        <!-- 操作按钮 -->
        <div class="flex gap-3 mt-6" v-if="userElf">
          <button
            @click="handleSetActive"
            :disabled="userElf.is_active || settingActive"
            class="game-btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="settingActive" class="inline-block w-4 h-4 border-2 border-space-900 border-t-transparent rounded-full animate-spin mr-2"></span>
            {{ userElf.is_active ? '✓ 当前主战' : '' }}<template v-if="!userElf.is_active"><ShieldCheckIcon class="w-4 h-4 mr-1 inline-block" />设为主战</template>
          </button>
        </div>
      </div>

      <!-- 右侧：精灵信息 -->
      <div class="space-y-5">
        <!-- 精灵描述 -->
        <div class="game-card">
          <h3 class="section-title flex items-center gap-2"><BookOpenIcon class="w-5 h-5" /> 精灵介绍</h3>
          <p class="text-gray-300 leading-relaxed">{{ elf.description || '这只精灵还没有详细介绍。' }}</p>
        </div>

        <!-- 基础属性 -->
        <div class="game-card">
          <h3 class="section-title flex items-center gap-2"><ChartBarIcon class="w-5 h-5" /> 基础属性</h3>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="stat in baseStats" :key="stat.key" class="bg-space-700 rounded-lg p-3">
              <div class="flex justify-between items-center mb-2">
                <span class="text-gray-400 text-sm">{{ stat.label }}</span>
                <span class="text-white font-bold">{{ elf[stat.key] || '-' }}</span>
              </div>
              <div class="w-full h-1.5 bg-space-600 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-700"
                  :class="stat.color"
                  :style="{ width: Math.min(100, ((elf[stat.key] || 0) / 150) * 100) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 我拥有的这只精灵的等级/经验 -->
        <div v-if="userElf" class="game-card">
          <h3 class="section-title">🌟 我的 {{ elf.name }}</h3>
          <div class="flex items-center gap-4 mb-3">
            <div class="text-center">
              <p class="text-accent text-2xl font-bold">{{ userElf.level }}</p>
              <p class="text-gray-400 text-xs">等级</p>
            </div>
            <div class="flex-1">
              <ExpBar
                :current="userElf.current_exp || 0"
                :max="userElf.next_level_exp || 100"
                :level="userElf.level"
                size="md"
                :show-label="true"
              />
            </div>
          </div>
        </div>
        <!-- 解锁 / 已拥有 -->
        <div v-if="userElf" class="game-card border-green-500/30">
          <h3 class="text-green-400 font-bold mb-1 flex items-center gap-2">
            <CheckCircleIcon class="w-4 h-4" /> 已收集
          </h3>
          <p class="text-gray-400 text-sm">Lv.{{ userElf.level }} · 好感度 {{ userElf.bond }}</p>
        </div>
        <div v-else class="game-card border-accent/30">
          <h3 class="text-gray-400 font-bold mb-3 flex items-center gap-2">
            <LockClosedIcon class="w-4 h-4" /> 解锁精灵
          </h3>
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="text-white text-sm">解锁费用：<span class="text-accent font-bold text-lg">{{ elf.unlock_cost }} 额度</span></p>
              <p class="text-gray-500 text-xs mt-0.5">当前剩余：{{ userStore.profile?.unlock_credits ?? 0 }} 额度</p>
            </div>
            <div class="text-right text-xs text-gray-600">
              <p>完成1个任务</p>
              <p>= +1 额度</p>
            </div>
          </div>
          <button
            @click="handleUnlock"
            :disabled="unlocking || (userStore.profile?.unlock_credits ?? 0) < elf.unlock_cost"
            class="w-full game-btn-primary py-2 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span v-if="unlocking" class="w-4 h-4 border-2 border-space-900 border-t-transparent rounded-full animate-spin"></span>
            <span v-else><SparklesIcon class="w-4 h-4 inline-block" /></span>
            {{ unlocking ? '解锁中...' : `花费 ${elf.unlock_cost} 额度解锁` }}
          </button>
          <p v-if="unlockError" class="text-red-400 text-xs mt-2 text-center">{{ unlockError }}</p>
        </div>

        <!-- 技能列表 -->
        <div v-if="elf.skills && elf.skills.length > 0" class="game-card">
          <h3 class="section-title">✨ 技能</h3>
          <div class="space-y-3">
            <div
              v-for="skill in elf.skills"
              :key="skill.id"
              class="bg-space-700 rounded-lg p-3 border border-space-400"
            >
              <div class="flex justify-between items-start">
                <p class="text-white font-medium">{{ skill.name }}</p>
                <span class="text-gray-500 text-xs">Lv.{{ skill.learn_level || 1 }} 学习</span>
              </div>
              <p class="text-gray-400 text-xs mt-1">{{ skill.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getElf } from '@/api/elves'
import api from '@/api'
import { useElfStore } from '@/stores/elf'
import { useUserStore } from '@/stores/user'
import RarityBadge from '@/components/common/RarityBadge.vue'
import ExpBar from '@/components/common/ExpBar.vue'
import { ChartBarIcon, ShieldCheckIcon, ExclamationTriangleIcon, LockClosedIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
import { BookOpenIcon, SparklesIcon } from '@heroicons/vue/24/solid'

const route = useRoute()
const router = useRouter()
const elfStore = useElfStore()
const userStore = useUserStore()

const elf = ref(null)
const loading = ref(false)
const error = ref(null)
const settingActive = ref(false)
const unlocking = ref(false)
const unlockError = ref('')

const userElf = computed(() =>
  elfStore.myElves.find(e => e.template_id === Number(route.params.id))
)

const rarityBorderClass = computed(() => {
  if (!elf.value) return 'border-gray-600'
  const map = {
    N: 'border-gray-600', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr shadow-glow-ssr', UR: 'border-ur shadow-glow-ur'
  }
  return map[elf.value.rarity?.toUpperCase()] || 'border-gray-600'
})

const rarityBgClass = computed(() => {
  if (!elf.value) return 'bg-space-700'
  const map = {
    N: 'bg-space-700', R: 'bg-[#0d1f3a]', SR: 'bg-[#1a1200]',
    SSR: 'bg-[#1a0800]', UR: 'bg-[#0f0020]'
  }
  return map[elf.value.rarity?.toUpperCase()] || 'bg-space-700'
})

const rarityGlowOverlay = computed(() => {
  if (!elf.value) return ''
  const map = {
    N: '', R: 'bg-rare/5', SR: 'bg-sr/5', SSR: 'bg-ssr/10', UR: 'bg-ur/10'
  }
  return map[elf.value.rarity?.toUpperCase()] || ''
})

const baseStats = [
  { key: 'hp', label: '生命值', color: 'bg-green-500' },
  { key: 'attack', label: '攻击力', color: 'bg-red-500' },
  { key: 'defense', label: '防御力', color: 'bg-blue-500' },
  { key: 'speed', label: '速度', color: 'bg-yellow-400' },
  { key: 'sp_attack', label: '特攻', color: 'bg-purple-500' },
  { key: 'sp_defense', label: '特防', color: 'bg-cyan-500' }
]

async function loadElf() {
  loading.value = true
  error.value = null
  try {
    const response = await getElf(route.params.id)
    elf.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || '加载精灵数据失败'
  } finally {
    loading.value = false
  }
}

async function handleSetActive() {
  if (!userElf.value) return
  settingActive.value = true
  try {
    await elfStore.setActive(userElf.value.id)
  } catch {
    // Error handled in store
  } finally {
    settingActive.value = false
  }
}

async function handleUnlock() {
  if (!elf.value) return
  unlocking.value = true
  unlockError.value = ''
  try {
    await api.post(`/elves/${elf.value.id}/unlock`)
    // 刷新我的精灵列表 + 用户资料（更新额度）
    await Promise.all([elfStore.fetchMyElves(), userStore.fetchProfile()])
  } catch (err) {
    unlockError.value = err.response?.data?.detail || '解锁失败，请稍后重试'
  } finally {
    unlocking.value = false
  }
}
}

function handleImgError(e) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-7xl bg-space-800">🐾</div>'
}

onMounted(() => {
  loadElf()
  if (elfStore.myElves.length === 0) {
    elfStore.fetchMyElves()
  }
})
</script>
