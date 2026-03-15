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
      <p class="text-red-400 text-lg mb-4">⚠️ {{ error }}</p>
      <button @click="loadElf" class="game-btn">重新加载</button>
    </div>

    <!-- 精灵详情 -->
    <div v-else-if="elf" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 左侧：精灵立绘 -->
      <div class="flex flex-col items-center">
        <div
          class="relative w-64 h-64 rounded-2xl overflow-hidden border-4 mb-6 animate-float"
          :class="rarityBorderClass"
        >
          <img
            :src="`http://localhost:8000/static/elves/${elf.id}.png`"
            :alt="elf.name"
            class="w-full h-full object-cover"
            @error="handleImgError"
          />
          <div class="absolute inset-0" :class="rarityGlowOverlay"></div>
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
            {{ userElf.is_active ? '✓ 当前主战' : '⚔️ 设为主战' }}
          </button>
        </div>
      </div>

      <!-- 右侧：精灵信息 -->
      <div class="space-y-5">
        <!-- 精灵描述 -->
        <div class="game-card">
          <h3 class="section-title">📖 精灵介绍</h3>
          <p class="text-gray-300 leading-relaxed">{{ elf.description || '这只精灵还没有详细介绍。' }}</p>
        </div>

        <!-- 基础属性 -->
        <div class="game-card">
          <h3 class="section-title">⚔️ 基础属性</h3>
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
        <div v-else-if="elf.unlock_condition" class="game-card border-dashed border-gray-600">
          <h3 class="text-gray-500 font-bold mb-2">🔒 解锁条件</h3>
          <p class="text-gray-400 text-sm">{{ elf.unlock_condition }}</p>
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
import { useElfStore } from '@/stores/elf'
import RarityBadge from '@/components/common/RarityBadge.vue'
import ExpBar from '@/components/common/ExpBar.vue'

const route = useRoute()
const router = useRouter()
const elfStore = useElfStore()

const elf = ref(null)
const loading = ref(false)
const error = ref(null)
const settingActive = ref(false)

const userElf = computed(() =>
  elfStore.myElves.find(e => (e.elf_id || e.id) === Number(route.params.id))
)

const rarityBorderClass = computed(() => {
  if (!elf.value) return 'border-gray-600'
  const map = {
    N: 'border-gray-600', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr shadow-glow-ssr', UR: 'border-ur shadow-glow-ur'
  }
  return map[elf.value.rarity?.toUpperCase()] || 'border-gray-600'
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
