<template>
  <div
    class="relative group cursor-pointer rounded-xl overflow-hidden border-2 transition-all duration-300"
    :class="[rarityBorderClass, elf.unlocked ? 'hover:scale-105 hover:-translate-y-1' : 'opacity-70']"
    @click="$emit('click', elf)"
  >
    <!-- 精灵图片区域 -->
    <div class="relative bg-space-700 aspect-square overflow-hidden">
      <img
        v-if="elf.unlocked"
        :src="`http://localhost:8000/static/elves/${elf.id}.png`"
        :alt="elf.name"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
        @error="handleImgError"
      />
      <!-- 未解锁黑色剪影遮罩 -->
      <div v-else class="w-full h-full flex items-center justify-center bg-space-800">
        <img
          :src="`http://localhost:8000/static/elves/${elf.id}.png`"
          :alt="'???'"
          class="w-full h-full object-cover filter brightness-0 opacity-40"
          @error="handleImgError"
        />
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-3xl">🔒</span>
          <p class="text-gray-500 text-xs mt-1">未解锁</p>
        </div>
      </div>

      <!-- 稀有度发光遮罩 -->
      <div
        v-if="elf.unlocked"
        class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        :class="rarityGlowOverlay"
      ></div>

      <!-- 稀有度标签 -->
      <div class="absolute top-2 left-2">
        <RarityBadge :rarity="elf.rarity" />
      </div>

      <!-- 属性图标 -->
      <div class="absolute top-2 right-2">
        <span
          class="w-6 h-6 rounded-full flex items-center justify-center text-sm"
          :class="elementBgClass"
          :title="elf.element"
        >{{ elementIcon }}</span>
      </div>
    </div>

    <!-- 精灵信息 -->
    <div class="p-3 bg-space-800">
      <p
        class="font-medium text-sm truncate"
        :class="elf.unlocked ? 'text-white' : 'text-gray-500'"
      >{{ elf.unlocked ? elf.name : '???' }}</p>
      <div v-if="elf.unlocked" class="flex items-center justify-between mt-1">
        <span class="text-gray-400 text-xs">{{ elf.element || '未知' }}</span>
        <span v-if="elf.level" class="text-accent text-xs font-bold">Lv.{{ elf.level }}</span>
      </div>
      <p v-else class="text-gray-600 text-xs mt-1">完成任务解锁</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import RarityBadge from '@/components/common/RarityBadge.vue'

const props = defineProps({
  elf: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const rarityBorderClass = computed(() => {
  const map = {
    N:   'border-gray-600',
    R:   'border-rare/60 shadow-glow-rare',
    SR:  'border-sr/60 shadow-glow-sr',
    SSR: 'border-ssr/60 shadow-glow-ssr',
    UR:  'border-ur/60 shadow-glow-ur'
  }
  return map[props.elf.rarity?.toUpperCase()] || map['N']
})

const rarityGlowOverlay = computed(() => {
  const map = {
    N:   'bg-transparent',
    R:   'bg-rare/10',
    SR:  'bg-sr/10',
    SSR: 'bg-ssr/10',
    UR:  'bg-ur/10'
  }
  return map[props.elf.rarity?.toUpperCase()] || 'bg-transparent'
})

const elementIcon = computed(() => {
  const map = {
    fire: '🔥', water: '💧', grass: '🌿', electric: '⚡',
    ice: '❄️', dark: '🌑', light: '✨', earth: '🌏',
    wind: '🌪️', poison: '☠️'
  }
  return map[props.elf.element?.toLowerCase()] || '✦'
})

const elementBgClass = computed(() => {
  const map = {
    fire: 'bg-red-900/60',
    water: 'bg-blue-900/60',
    grass: 'bg-green-900/60',
    electric: 'bg-yellow-900/60',
    ice: 'bg-cyan-900/60',
    dark: 'bg-gray-900/60',
    light: 'bg-yellow-600/30'
  }
  return map[props.elf.element?.toLowerCase()] || 'bg-space-600'
})

function handleImgError(e) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  if (!parent.querySelector('.fallback-icon')) {
    const div = document.createElement('div')
    div.className = 'fallback-icon w-full h-full flex items-center justify-center text-4xl'
    div.textContent = '🐾'
    parent.appendChild(div)
  }
}
</script>
