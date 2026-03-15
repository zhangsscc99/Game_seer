<template>
  <header class="bg-space-800 border-b border-space-500 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <button @click="$emit('toggle-sidebar')" class="text-gray-400 hover:text-white transition-colors">
        <span class="text-xl">☰</span>
      </button>
      <h1 class="text-accent font-bold text-xl">Game Seer</h1>
    </div>
    <div class="flex items-center gap-4">
      <span class="text-gray-400 text-sm">Lv.{{ userStore.level }}</span>
      <div class="w-8 h-8 rounded-full bg-accent/20 border border-accent/50 flex items-center justify-center">
        <span class="text-accent font-bold text-sm">{{ displayName.charAt(0).toUpperCase() }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

defineEmits(['toggle-sidebar'])

const userStore = useUserStore()
const displayName = computed(() => userStore.displayName)
</script>
