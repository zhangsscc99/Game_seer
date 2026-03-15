<template>
  <div
    class="relative group rounded-xl overflow-hidden border-2 transition-all duration-300 cursor-pointer"
    :class="boss.defeated
      ? 'border-green-500/40 opacity-70'
      : 'border-ssr/60 hover:border-ssr hover:shadow-glow-ssr hover:-translate-y-1 hover:scale-[1.02]'"
    @click="!boss.defeated ? $emit('challenge', boss) : null"
  >
    <!-- Boss图片 -->
    <div class="relative bg-space-800 aspect-video overflow-hidden">
      <img
        v-if="boss.image_path"
        :src="boss.image_path"
        :alt="boss.name"
        class="w-full h-full object-contain p-2 transition-transform duration-300 group-hover:scale-110"
        @error="handleImgError"
      />
      <div v-else class="w-full h-full flex items-center justify-center">
        <span class="text-6xl">👾</span>
      </div>

      <!-- 已击败遮罩 -->
      <div v-if="boss.defeated" class="absolute inset-0 bg-black/40 flex items-center justify-center">
        <div class="bg-green-500/80 text-white font-bold px-4 py-2 rounded-full text-sm transform -rotate-12">
          已击败
        </div>
      </div>

      <!-- 难度标识 -->
      <div class="absolute top-2 right-2 bg-black/60 rounded px-2 py-1">
        <div class="flex items-center gap-0.5">
          <span v-for="i in (boss.difficulty || 3)" :key="i" class="text-ssr text-xs">★</span>
        </div>
      </div>

      <!-- Boss类型标签 -->
      <div class="absolute top-2 left-2">
        <span class="bg-ssr/80 text-white text-xs px-2 py-0.5 rounded font-bold">
          {{ boss.boss_type || 'BOSS' }}
        </span>
      </div>
    </div>

    <!-- Boss信息 -->
    <div class="p-4 bg-space-800">
      <h3 class="text-white font-bold text-base mb-1">{{ boss.name }}</h3>
      <p class="text-gray-400 text-xs mb-3 line-clamp-2">{{ boss.description || '传说中的强大Boss，等待着勇敢的指挥官前来挑战。' }}</p>

      <!-- 奖励预览 -->
      <div v-if="!boss.defeated" class="flex items-center gap-3 mt-3">
        <div class="flex items-center gap-1 text-xs">
          <span class="text-accent">+{{ boss.reward_exp }}</span>
          <span class="text-gray-500">EXP</span>
        </div>
        <div class="flex items-center gap-1 text-xs">
          <span class="text-yellow-400">+{{ boss.reward_coins }}</span>
          <span class="text-gray-500">金币</span>
        </div>
        <div v-if="boss.reward_elf" class="flex items-center gap-1 text-xs">
          <span class="text-ur">解锁精灵</span>
        </div>
      </div>

      <!-- 挑战按钮 -->
      <button
        v-if="!boss.defeated"
        class="mt-3 w-full game-btn-primary text-sm py-2"
      >
        发起挑战
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  boss: {
    type: Object,
    required: true
  }
})

defineEmits(['challenge'])

const requirementPercent = computed(() => {
  if (!props.boss.required_tasks) return 0
  return Math.min(100, Math.round((props.boss.user_tasks_completed / props.boss.required_tasks) * 100))
})

function handleImgError(e) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  const div = document.createElement('div')
  div.className = 'w-full h-full flex items-center justify-center text-6xl bg-space-800'
  div.textContent = '👾'
  parent.appendChild(div)
}
</script>
