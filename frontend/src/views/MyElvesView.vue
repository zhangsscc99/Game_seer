<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-white flex items-center gap-2"><StarIcon class="w-7 h-7 text-accent" /> 我的精灵</h1>
      <span class="text-gray-400 text-sm">共 {{ elfStore.myElves.length }} 只</span>
    </div>

    <!-- 当前主战精灵 -->
    <div v-if="elfStore.activeElf" class="game-card border-accent/30">
      <h2 class="section-title flex items-center gap-2"><ShieldCheckIcon class="w-5 h-5" /> 主战精灵</h2>
      <div class="flex items-center gap-6">
        <div
          class="w-24 h-24 rounded-xl overflow-hidden border-2 flex-shrink-0 animate-float"
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
            <h3 class="text-white text-xl font-bold">{{ elfStore.activeElf.name }}</h3>
            <RarityBadge :rarity="elfStore.activeElf.rarity || 'N'" />
          </div>
          <p class="text-accent font-bold mb-2">Lv.{{ elfStore.activeElf.level }}</p>
          <ExpBar
            :current="elfStore.activeElf.current_exp || 0"
            :max="elfStore.activeElf.next_level_exp || 100"
            :level="elfStore.activeElf.level"
            size="md"
            :show-label="true"
          />
        </div>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="elfStore.loading" class="py-16 text-center">
      <div class="w-10 h-10 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-400">加载精灵中...</p>
    </div>

    <!-- 错误 -->
    <div v-else-if="elfStore.error" class="game-card border-red-500/30 text-center py-8">
      <p class="text-red-400 mb-3 flex items-center justify-center gap-2"><ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" /> {{ elfStore.error }}</p>
      <button @click="elfStore.fetchMyElves()" class="game-btn">重试</button>
    </div>

    <!-- 精灵列表 -->
    <div v-else>
      <div v-if="elfStore.myElves.length === 0" class="py-16 text-center">
        <SparklesIcon class="w-16 h-16 mx-auto mb-3 text-gray-600" />
        <p class="text-gray-400 mb-4">还没有精灵，完成任务来解锁精灵吧！</p>
        <router-link to="/tasks" class="game-btn-primary">前往任务</router-link>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="myElf in elfStore.myElves"
          :key="myElf.id"
          class="game-card cursor-pointer transition-all duration-300 hover:-translate-y-1"
          :class="{ 'border-accent/50 shadow-glow-accent': myElf.is_active }"
        >
          <div class="flex items-center gap-4">
            <!-- 精灵图 -->
            <div
              class="w-16 h-16 rounded-xl overflow-hidden border-2 flex-shrink-0"
              :class="getRarityBorder(myElf.rarity)"
            >
              <img
                :src="`http://localhost:8000/static/elves/${myElf.elf_id || myElf.id}.png`"
                :alt="myElf.name"
                class="w-full h-full object-cover"
                @error="handleImgError"
              />
            </div>
            <!-- 精灵信息 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-0.5">
                <p class="text-white font-medium truncate">{{ myElf.name }}</p>
                <span v-if="myElf.is_active" class="text-xs text-accent font-bold">主战</span>
              </div>
              <p class="text-accent text-sm mb-1">Lv.{{ myElf.level }}</p>
              <ExpBar
                :current="myElf.current_exp || 0"
                :max="myElf.next_level_exp || 100"
                :level="myElf.level"
                size="sm"
              />
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex gap-2 mt-3">
            <router-link
              :to="`/elves/${myElf.elf_id || myElf.id}`"
              class="flex-1 text-center py-1.5 rounded border border-space-400 text-gray-400 hover:border-accent/50 hover:text-accent text-xs transition-colors"
            >
              查看详情
            </router-link>
            <button
              @click="handleSetActive(myElf)"
              :disabled="myElf.is_active || settingId === myElf.id"
              class="flex-1 py-1.5 rounded text-xs font-medium transition-all duration-200"
              :class="myElf.is_active
                ? 'bg-accent/20 text-accent cursor-default'
                : 'border border-accent/50 text-accent hover:bg-accent hover:text-space-900'"
            >
              <span v-if="settingId === myElf.id" class="inline-block w-3 h-3 border border-current border-t-transparent rounded-full animate-spin mr-1"></span>
              {{ myElf.is_active ? '✓ 主战中' : '设为主战' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useElfStore } from '@/stores/elf'
import RarityBadge from '@/components/common/RarityBadge.vue'
import ExpBar from '@/components/common/ExpBar.vue'
import { SparklesIcon, ShieldCheckIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import { StarIcon } from '@heroicons/vue/24/solid'

const elfStore = useElfStore()
const settingId = ref(null)

const activeBorderClass = computed(() => {
  const elf = elfStore.activeElf
  if (!elf) return 'border-gray-600'
  const map = {
    N: 'border-gray-500', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr', UR: 'border-ur'
  }
  return map[elf.rarity?.toUpperCase()] || 'border-gray-600'
})

function getRarityBorder(rarity) {
  const map = {
    N: 'border-gray-600', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr', UR: 'border-ur'
  }
  return map[rarity?.toUpperCase()] || 'border-gray-600'
}

async function handleSetActive(myElf) {
  if (myElf.is_active || settingId.value) return
  settingId.value = myElf.id
  try {
    await elfStore.setActive(myElf.id)
  } finally {
    settingId.value = null
  }
}

function handleImgError(e) {
  e.target.parentElement.innerHTML = '<div class="w-full h-full flex items-center justify-center text-3xl bg-space-700">🐾</div>'
}

onMounted(() => {
  elfStore.fetchMyElves()
})
</script>
