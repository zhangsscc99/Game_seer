import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as tasksApi from '@/api/tasks'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)

  const pendingTasks = computed(() => tasks.value.filter(t => !t.completed))
  const completedTasks = computed(() => tasks.value.filter(t => t.completed))
  const dailyTasks = computed(() => tasks.value.filter(t => t.category === 'daily'))
  const mainTasks = computed(() => tasks.value.filter(t => t.category === 'main'))
  const challengeTasks = computed(() => tasks.value.filter(t => t.category === 'challenge'))

  async function fetchTasks(params = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await tasksApi.getTasks(params)
      tasks.value = response.data.items || response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '获取任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addTask(data) {
    loading.value = true
    error.value = null
    try {
      const response = await tasksApi.createTask(data)
      tasks.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '创建任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function completeTask(id) {
    error.value = null
    try {
      const response = await tasksApi.completeTask(id)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = { ...tasks.value[index], completed: true }
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '完成任务失败'
      throw err
    }
  }

  async function deleteTask(id) {
    error.value = null
    try {
      await tasksApi.deleteTask(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
    } catch (err) {
      error.value = err.response?.data?.detail || '删除任务失败'
      throw err
    }
  }

  async function updateTask(id, data) {
    error.value = null
    try {
      const response = await tasksApi.updateTask(id, data)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '更新任务失败'
      throw err
    }
  }

  return {
    tasks,
    loading,
    error,
    pendingTasks,
    completedTasks,
    dailyTasks,
    mainTasks,
    challengeTasks,
    fetchTasks,
    addTask,
    completeTask,
    deleteTask,
    updateTask
  }
})
