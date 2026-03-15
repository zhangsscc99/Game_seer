<template>
  <div
    class="group flex items-center gap-3 p-4 rounded-lg border transition-all duration-200"
    :class="[
      task.completed
        ? 'bg-space-800/50 border-space-500 opacity-60'
        : 'bg-space-800 border-space-500 hover:border-accent/40'
    ]"
  >
    <!-- 完成复选框 -->
    <button
      @click.stop="handleComplete"
      :disabled="task.completed || completing"
      class="flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200"
      :class="[
        task.completed
          ? 'border-green-500 bg-green-500/20'
          : 'border-gray-500 hover:border-accent group-hover:border-accent/70'
      ]"
    >
      <span v-if="completing" class="w-3 h-3 border border-accent border-t-transparent rounded-full animate-spin"></span>
      <span v-else-if="task.completed" class="text-green-400 text-xs">✓</span>
    </button>

    <!-- 任务内容 -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2 flex-wrap">
        <p
          class="font-medium text-sm transition-all duration-300"
          :class="task.completed ? 'line-through text-gray-500' : 'text-white'"
        >{{ task.title }}</p>
        <span
          class="tag text-xs"
          :class="categoryClass"
        >{{ categoryLabel }}</span>
      </div>
      <p v-if="task.description" class="text-gray-500 text-xs mt-0.5 truncate">{{ task.description }}</p>

      <!-- 难度星级 -->
      <div class="flex items-center gap-1 mt-1">
        <span
          v-for="i in 5"
          :key="i"
          class="text-xs"
          :class="i <= (task.difficulty || 1) ? 'text-accent' : 'text-gray-700'"
        >★</span>
        <span class="text-gray-500 text-xs ml-1">难度</span>
      </div>
    </div>

    <!-- 奖励预览 -->
    <div class="flex-shrink-0 flex flex-col items-end gap-1">
      <div class="flex items-center gap-1 text-xs">
        <span class="text-accent">+{{ task.exp_reward || 10 }}</span>
        <span class="text-gray-500">EXP</span>
      </div>
      <div class="flex items-center gap-1 text-xs">
        <span class="text-yellow-400">+{{ task.coin_reward || 5 }}</span>
        <span class="text-gray-500">金币</span>
      </div>
    </div>

    <!-- 删除按钮 -->
    <button
      @click.stop="$emit('delete', task.id)"
      class="flex-shrink-0 w-7 h-7 rounded opacity-0 group-hover:opacity-100 flex items-center justify-center text-gray-600 hover:text-red-400 hover:bg-red-900/20 transition-all duration-200"
    >
      <span class="text-sm">✕</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['complete', 'delete'])
const completing = ref(false)

const categoryLabel = computed(() => {
  const map = { daily: '日常', main: '主线', challenge: '挑战', side: '支线' }
  return map[props.task.category] || props.task.category || '日常'
})

const categoryClass = computed(() => {
  const map = {
    daily:     'bg-blue-900/50 text-blue-300',
    main:      'bg-purple-900/50 text-purple-300',
    challenge: 'bg-red-900/50 text-red-300',
    side:      'bg-green-900/50 text-green-300'
  }
  return map[props.task.category] || 'bg-gray-800 text-gray-400'
})

async function handleComplete() {
  if (props.task.completed || completing.value) return
  completing.value = true
  try {
    await new Promise(r => setTimeout(r, 300))
    emit('complete', props.task.id)
  } finally {
    completing.value = false
  }
}
</script>
