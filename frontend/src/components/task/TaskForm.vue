<template>
  <div class="space-y-4">
    <h3 class="text-accent font-bold text-lg">{{ isEdit ? '编辑任务' : '新建任务' }}</h3>

    <div>
      <label class="block text-gray-400 text-sm mb-1">任务标题 <span class="text-red-400">*</span></label>
      <input
        v-model="form.title"
        type="text"
        placeholder="输入任务标题..."
        class="game-input"
        :class="{ 'border-red-500': errors.title }"
        @keydown.enter="handleSubmit"
      />
      <p v-if="errors.title" class="text-red-400 text-xs mt-1">{{ errors.title }}</p>
    </div>

    <div>
      <label class="block text-gray-400 text-sm mb-1">任务描述</label>
      <textarea
        v-model="form.description"
        placeholder="任务详情（可选）..."
        rows="2"
        class="game-input resize-none"
      ></textarea>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <div>
        <label class="block text-gray-400 text-sm mb-1">分类</label>
        <select v-model="form.category" class="game-input">
          <option value="daily">日常</option>
          <option value="main">主线</option>
          <option value="challenge">挑战</option>
          <option value="side">支线</option>
        </select>
      </div>
      <div>
        <label class="block text-gray-400 text-sm mb-1">难度</label>
        <div class="flex items-center gap-1 mt-2">
          <button
            v-for="i in 5"
            :key="i"
            type="button"
            @click="form.difficulty = i"
            class="text-xl transition-colors"
            :class="i <= form.difficulty ? 'text-accent' : 'text-gray-700 hover:text-gray-500'"
          >★</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="bg-red-900/30 border border-red-500/50 rounded px-3 py-2">
      <p class="text-red-400 text-sm">{{ error }}</p>
    </div>

    <div class="flex gap-3 pt-2">
      <button
        @click="handleSubmit"
        :disabled="loading"
        class="game-btn-primary flex-1 flex items-center justify-center gap-2"
      >
        <span v-if="loading" class="w-4 h-4 border-2 border-space-900 border-t-transparent rounded-full animate-spin"></span>
        <span>{{ isEdit ? '保存修改' : '创建任务' }}</span>
      </button>
      <button @click="$emit('cancel')" class="game-btn px-6">取消</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const isEdit = computed(() => !!props.task)

import { computed } from 'vue'

const form = reactive({
  title: '',
  description: '',
  category: 'daily',
  difficulty: 1,
})

const errors = reactive({ title: '' })

watch(() => props.task, (task) => {
  if (task) {
    Object.assign(form, {
      title: task.title || '',
      description: task.description || '',
      category: task.category || 'daily',
      difficulty: task.difficulty || 1,
    })
  } else {
    Object.assign(form, {
      title: '', description: '', category: 'daily', difficulty: 1,
    })
  }
}, { immediate: true })

function validate() {
  errors.title = ''
  if (!form.title.trim()) {
    errors.title = '请输入任务标题'
    return false
  }
  return true
}

function handleSubmit() {
  if (!validate()) return
  emit('submit', { ...form })
}
</script>
