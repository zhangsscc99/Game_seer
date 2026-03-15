<template>
  <span
    class="tag font-bold uppercase tracking-wider"
    :class="badgeClass"
  >{{ rarity }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  rarity: {
    type: String,
    default: 'N',
    validator: (v) => ['N', 'R', 'SR', 'SSR', 'UR'].includes(v.toUpperCase())
  }
})

const badgeClass = computed(() => {
  const map = {
    N:   'bg-gray-700 text-gray-300 border border-gray-500',
    R:   'bg-blue-900/50 text-rare border border-rare',
    SR:  'bg-yellow-900/50 text-sr border border-sr',
    SSR: 'bg-orange-900/50 text-ssr border border-ssr',
    UR:  'bg-purple-900/50 text-ur border border-ur'
  }
  return map[props.rarity?.toUpperCase()] || map['N']
})
</script>
