<template>
  <div
    class="w-full h-full rounded-full overflow-hidden flex items-center justify-center"
    :class="[bgClass, borderClass]"
    :style="sizeStyle"
  >
    <img
      v-if="elf"
      :src="`http://localhost:8000/static/elves/${elf.elf_id || elf.id}.png`"
      :alt="elf.name"
      class="w-full h-full object-cover"
      @error="handleError"
    />
    <span v-else class="text-2xl">🐾</span>
    <span v-if="showFallback" class="text-2xl">🐾</span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  elf: {
    type: Object,
    default: null
  },
  size: {
    type: Number,
    default: 40
  },
  bordered: {
    type: Boolean,
    default: false
  }
})

const showFallback = ref(false)

const sizeStyle = computed(() => ({
  width: props.size + 'px',
  height: props.size + 'px'
}))

const bgClass = computed(() => 'bg-space-700')

const borderClass = computed(() => {
  if (!props.bordered || !props.elf) return ''
  const rarity = props.elf.rarity?.toUpperCase()
  const map = {
    N: 'border-2 border-gray-500',
    R: 'border-2 border-rare',
    SR: 'border-2 border-sr',
    SSR: 'border-2 border-ssr',
    UR: 'border-2 border-ur'
  }
  return map[rarity] || ''
})

function handleError(e) {
  e.target.style.display = 'none'
  showFallback.value = true
}
</script>
