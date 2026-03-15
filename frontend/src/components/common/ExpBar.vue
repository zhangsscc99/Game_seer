<template>
  <div class="w-full">
    <div v-if="showLabel" class="flex justify-between items-center mb-1">
      <span class="text-xs text-gray-400">经验值</span>
      <span class="text-xs text-accent">{{ current }} / {{ max }}</span>
    </div>
    <div
      class="overflow-hidden rounded-full bg-space-700"
      :class="heightClass"
    >
      <div
        class="exp-bar-fill h-full rounded-full transition-all duration-700 ease-out"
        :style="{ width: percent + '%' }"
      ></div>
    </div>
    <div v-if="showLevel" class="flex justify-between items-center mt-1">
      <span class="text-xs text-gray-500">Lv.{{ level }}</span>
      <span class="text-xs text-gray-500">{{ percent }}%</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  current: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 100
  },
  level: {
    type: Number,
    default: 1
  },
  size: {
    type: String,
    default: 'md' // sm | md | lg
  },
  showLabel: {
    type: Boolean,
    default: false
  },
  showLevel: {
    type: Boolean,
    default: false
  }
})

const percent = computed(() => {
  if (!props.max || props.max === 0) return 0
  return Math.min(100, Math.round((props.current / props.max) * 100))
})

const heightClass = computed(() => {
  const map = { sm: 'h-1.5', md: 'h-2.5', lg: 'h-4' }
  return map[props.size] || 'h-2.5'
})
</script>
