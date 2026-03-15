<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-white flex items-center gap-2">
          <ClipboardDocumentListIcon class="w-7 h-7 text-accent" />
          任务中心
        </h1>
      <button
        @click="showTaskForm = true"
        class="game-btn-primary flex items-center gap-2"
      >
        <span>+</span>
        新建任务
      </button>
    </div>

    <!-- 分类 Tabs -->
    <div class="flex gap-1 bg-space-800 p-1 rounded-lg border border-space-500">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="flex-1 py-2 px-3 rounded text-sm font-medium transition-all duration-200"
        :class="activeTab === tab.key
          ? 'bg-accent text-space-900 font-bold'
          : 'text-gray-400 hover:text-white hover:bg-space-600'"
      >
        {{ tab.label }}
        <span
          v-if="getTabCount(tab.key) > 0"
          class="ml-1 text-xs opacity-70"
        >({{ getTabCount(tab.key) }})</span>
      </button>
    </div>

    <!-- 任务列表 -->
    <div v-if="taskStore.loading" class="py-16 text-center">
      <div class="w-10 h-10 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-400">加载任务中...</p>
    </div>

    <div v-else-if="taskStore.error" class="game-card border-red-500/30">
      <p class="text-red-400 flex items-center gap-2">
        <ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" />{{ taskStore.error }}
      </p>
      <button @click="taskStore.fetchTasks()" class="game-btn mt-3 text-sm">重试</button>
    </div>

    <div v-else>
      <!-- 完成进度条 -->
      <div class="game-card">
        <div class="flex justify-between text-sm text-gray-400 mb-2">
          <span>{{ activeTab === 'all' ? '全部' : tabs.find(t => t.key === activeTab)?.label }}任务进度</span>
          <span class="text-accent font-medium">{{ completedInTab }}/{{ totalInTab }} 已完成</span>
        </div>
        <div class="w-full h-2 bg-space-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-green-500 rounded-full transition-all duration-700"
            :style="{ width: tabCompletionRate + '%' }"
          ></div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredTasks.length === 0" class="py-16 text-center">
        <InboxIcon class="w-16 h-16 mx-auto mb-3 text-gray-600" />
        <p class="text-gray-400 mb-4">暂无{{ activeTab !== 'all' ? tabs.find(t=>t.key===activeTab)?.label : '' }}任务</p>
        <button @click="showTaskForm = true" class="game-btn-primary">+ 创建任务</button>
      </div>

      <!-- 任务列表 -->
      <div v-else class="space-y-2">
        <transition-group name="slide-up">
          <TaskItem
            v-for="task in filteredTasks"
            :key="task.id"
            :task="task"
            @complete="handleComplete"
            @delete="handleDelete"
          />
        </transition-group>
      </div>
    </div>

    <!-- 任务表单弹窗 -->
    <Teleport to="body">
      <transition name="fade">
        <div
          v-if="showTaskForm"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
          @click.self="showTaskForm = false"
        >
          <div class="bg-space-800 border border-space-500 rounded-xl p-6 w-full max-w-md shadow-2xl">
            <TaskForm
              :loading="taskStore.loading"
              :error="taskStore.error"
              @submit="handleCreateTask"
              @cancel="showTaskForm = false"
            />
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- 奖励弹出 -->
    <Teleport to="body">
      <transition name="slide-up">
        <div
          v-if="reward"
          class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50"
        >
          <div class="bg-space-700 border border-accent/50 rounded-xl px-6 py-4 shadow-glow-accent text-center min-w-48">
            <p class="text-accent font-bold text-lg mb-1">✨ 任务完成！</p>
            <div class="flex items-center justify-center gap-4">
              <span class="text-white">+{{ reward.exp }} EXP</span>
              <span class="text-yellow-400">+{{ reward.coin }} 金币</span>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/task'
import TaskItem from '@/components/task/TaskItem.vue'
import TaskForm from '@/components/task/TaskForm.vue'
import { InboxIcon, ExclamationTriangleIcon, ClipboardDocumentListIcon, PlusIcon } from '@heroicons/vue/24/outline'

const taskStore = useTaskStore()

const activeTab = ref('all')
const showTaskForm = ref(false)
const reward = ref(null)

const tabs = [
  { key: 'all',      label: '全部' },
  { key: 'study',    label: '学习' },
  { key: 'work',     label: '工作' },
  { key: 'habit',    label: '习惯' },
  { key: 'health',   label: '健康' },
  { key: 'creative', label: '创作' },
]

const filteredTasks = computed(() => {
  if (activeTab.value === 'all') return taskStore.tasks
  return taskStore.tasks.filter(t => t.category === activeTab.value)
})

const totalInTab = computed(() => filteredTasks.value.length)
const completedInTab = computed(() => filteredTasks.value.filter(t => t.completed).length)
const tabCompletionRate = computed(() => {
  if (!totalInTab.value) return 0
  return Math.round((completedInTab.value / totalInTab.value) * 100)
})

function getTabCount(key) {
  if (key === 'all') return taskStore.pendingTasks.length
  return taskStore.tasks.filter(t => t.category === key && !t.completed).length
}

async function handleComplete(id) {
  try {
    const result = await taskStore.completeTask(id)
    const expGain = result?.exp_gained || 10
    const coinGain = result?.coin_gained || 5
    reward.value = { exp: expGain, coin: coinGain }
    setTimeout(() => { reward.value = null }, 3000)
  } catch {
    // Error handled in store
  }
}

async function handleDelete(id) {
  if (!confirm('确定要删除此任务吗？')) return
  await taskStore.deleteTask(id)
}

async function handleCreateTask(formData) {
  try {
    await taskStore.addTask(formData)
    showTaskForm.value = false
  } catch {
    // Error handled in store
  }
}

onMounted(async () => {
  await taskStore.fetchTasks()
})
</script>
