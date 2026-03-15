<template>
  <div class="space-y-6">
    <!-- 页面标题 + 收集进度 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white">📖 精灵图鉴</h1>
        <p class="text-gray-400 text-sm mt-1">收集并培育你的精灵伙伴</p>
      </div>
      <div class="game-card !p-3 flex items-center gap-3 min-w-48">
        <span class="text-2xl">🏆</span>
        <div>
          <p class="text-white font-bold text-lg">{{ elfStore.unlockedCount }}<span class="text-gray-500 font-normal text-base">/{{ elfStore.total }}</span></p>
          <p class="text-gray-400 text-xs">已收集</p>
        </div>
        <div class="flex-1">
          <div class="w-full h-1.5 bg-space-700 rounded-full overflow-hidden">
            <div
              class="h-full bg-accent rounded-full transition-all duration-700"
              :style="{ width: collectProgress + '%' }"
            ></div>
          </div>
          <p class="text-gray-500 text-xs mt-0.5 text-right">{{ collectProgress }}%</p>
        </div>
      </div>
    </div>

    <!-- 搜索框 -->
    <div class="relative">
      <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索精灵名称..."
        class="game-input pl-9 pr-8 w-full sm:w-72"
        @input="onSearchInput"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
      >
        <XMarkIcon class="w-4 h-4" />
      </button>
    </div>

    <!-- 筛选栏 -->
    <div class="flex flex-wrap gap-3">
      <!-- 稀有度筛选 -->
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-gray-500 text-sm">稀有度:</span>
        <button
          v-for="r in rarities"
          :key="r.value"
          @click="toggleFilter('rarity', r.value)"
          class="px-3 py-1 rounded-full text-xs font-bold border transition-all duration-200"
          :class="filters.rarity === r.value
            ? r.activeClass
            : 'border-space-400 text-gray-500 hover:border-gray-400'"
        >{{ r.label }}</button>
      </div>

      <!-- 属性筛选 -->
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-gray-500 text-sm">属性:</span>
        <button
          v-for="el in elements"
          :key="el.value"
          @click="toggleFilter('element', el.value)"
          class="px-3 py-1 rounded-full text-xs border transition-all duration-200"
          :class="filters.element === el.value
            ? 'border-accent bg-accent/20 text-accent'
            : 'border-space-400 text-gray-500 hover:border-gray-400'"
        >{{ el.icon }} {{ el.label }}</button>
      </div>

      <!-- 显示状态 -->
      <button
        @click="filters.unlocked_only = !filters.unlocked_only"
        class="px-3 py-1 rounded-full text-xs border transition-all duration-200 ml-auto"
        :class="filters.unlocked_only
          ? 'border-green-500 bg-green-500/20 text-green-400'
          : 'border-space-400 text-gray-500 hover:border-gray-400'"
      >
        {{ filters.unlocked_only ? '✓ 仅已解锁' : '全部精灵' }}
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="elfStore.loading" class="py-16 text-center">
      <div class="w-10 h-10 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-400">加载精灵图鉴...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="elfStore.error" class="game-card border-red-500/30 text-center py-8">
      <p class="text-red-400 mb-3 flex items-center justify-center gap-2"><ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" /> {{ elfStore.error }}</p>
      <button @click="loadElves" class="game-btn">重新加载</button>
    </div>

    <!-- 精灵网格 -->
    <div v-else>
      <div v-if="displayElves.length === 0" class="py-16 text-center">
        <MagnifyingGlassIcon class="w-16 h-16 mx-auto mb-3 text-gray-600" />
        <p class="text-gray-400">没有符合条件的精灵</p>
      </div>
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <ElfCard
          v-for="elf in displayElves"
          :key="elf.id"
          :elf="elf"
          @click="handleElfClick"
        />
      </div>

      <!-- 分页 -->
      <div v-if="elfStore.total > pageSize" class="flex items-center justify-center gap-3 mt-8">
        <button
          @click="changePage(elfStore.page - 1)"
          :disabled="elfStore.page <= 1"
          class="game-btn px-4 py-2 disabled:opacity-30 disabled:cursor-not-allowed"
        >← 上一页</button>
        <span class="text-gray-400 text-sm">{{ elfStore.page }} / {{ totalPages }}</span>
        <button
          @click="changePage(elfStore.page + 1)"
          :disabled="elfStore.page >= totalPages"
          class="game-btn px-4 py-2 disabled:opacity-30 disabled:cursor-not-allowed"
        >下一页 →</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useElfStore } from '@/stores/elf'
import ElfCard from '@/components/elf/ElfCard.vue'
import { MagnifyingGlassIcon, XMarkIcon, ExclamationTriangleIcon, FunnelIcon } from '@heroicons/vue/24/solid'

const router = useRouter()
const elfStore = useElfStore()

const pageSize = 25
const searchQuery = ref('')
let searchTimer = null

const filters = reactive({
  rarity: null,
  element: null,
  unlocked_only: false
})

const rarities = [
  { value: null, label: '全部', activeClass: 'border-gray-400 bg-gray-800 text-gray-300' },
  { value: 'N', label: 'N', activeClass: 'border-gray-500 bg-gray-700 text-gray-300' },
  { value: 'R', label: 'R', activeClass: 'border-rare bg-rare/20 text-rare' },
  { value: 'SR', label: 'SR', activeClass: 'border-sr bg-sr/20 text-sr' },
  { value: 'SSR', label: 'SSR', activeClass: 'border-ssr bg-ssr/20 text-ssr' },
  { value: 'UR', label: 'UR', activeClass: 'border-ur bg-ur/20 text-ur' }
]

const elements = [
  { value: 'fire', icon: '🔥', label: '火' },
  { value: 'water', icon: '💧', label: '水' },
  { value: 'grass', icon: '🌿', label: '草' },
  { value: 'electric', icon: '⚡', label: '电' },
  { value: 'ice', icon: '❄️', label: '冰' },
  { value: 'dark', icon: '🌑', label: '暗' },
  { value: 'light', icon: '✨', label: '光' }
]

const collectProgress = computed(() => {
  if (!elfStore.total) return 0
  return Math.round((elfStore.unlockedCount / elfStore.total) * 100)
})

const totalPages = computed(() => Math.ceil(elfStore.total / pageSize))

const displayElves = computed(() => {
  let list = elfStore.elves
  if (filters.unlocked_only) {
    list = list.filter(e => e.unlocked)
  }
  return list
})

function toggleFilter(type, value) {
  if (filters[type] === value) {
    filters[type] = null
  } else {
    filters[type] = value
  }
  loadElves(1)
}

async function loadElves(page = 1) {
  const params = { page, page_size: pageSize }
  if (filters.rarity) params.rarity = filters.rarity
  if (filters.element) params.element = filters.element
  if (searchQuery.value.trim()) params.name = searchQuery.value.trim()
  await elfStore.fetchElves(params)
}

function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => loadElves(1), 400)
}

function clearSearch() {
  searchQuery.value = ''
  loadElves(1)
}

async function changePage(newPage) {
  if (newPage < 1 || newPage > totalPages.value) return
  await loadElves(newPage)
}

function handleElfClick(elf) {
  router.push(`/elves/${elf.id}`)
}

onMounted(() => {
  loadElves(1)
})
</script>
