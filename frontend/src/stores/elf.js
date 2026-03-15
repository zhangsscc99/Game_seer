import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as elvesApi from '@/api/elves'

export const useElfStore = defineStore('elf', () => {
  const elves = ref([])
  const myElves = ref([])
  const activeElf = ref(null)
  const total = ref(0)
  const page = ref(1)
  const loading = ref(false)
  const error = ref(null)

  const unlockedCount = computed(() => myElves.value.length)

  async function fetchElves(params = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await elvesApi.getElves({ page: page.value, ...params })
      const data = response.data
      const rawItems = data.items || data
      // 标记用户已拥有的精灵
      const ownedIds = new Set(myElves.value.map(e => e.template_id))
      elves.value = rawItems.map(e => ({
        ...e,
        unlocked: true,        // 图鉴全部可见
        collected: ownedIds.has(e.id)  // 是否已收集
      }))
      total.value = data.total || elves.value.length
      page.value = params.page || 1
    } catch (err) {
      error.value = err.response?.data?.detail || '获取精灵图鉴失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMyElves() {
    loading.value = true
    error.value = null
    try {
      const response = await elvesApi.getMyElves()
      myElves.value = response.data
      // 找到主战精灵
      const active = myElves.value.find(e => e.is_active)
      if (active) {
        activeElf.value = active
      }
    } catch (err) {
      error.value = err.response?.data?.detail || '获取我的精灵失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function setActive(id) {
    error.value = null
    try {
      const response = await elvesApi.setActiveElf(id)
      // 更新主战精灵
      myElves.value = myElves.value.map(e => ({
        ...e,
        is_active: e.id === id
      }))
      activeElf.value = myElves.value.find(e => e.id === id) || null
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '设置主战精灵失败'
      throw err
    }
  }

  return {
    elves,
    myElves,
    activeElf,
    total,
    page,
    loading,
    error,
    unlockedCount,
    fetchElves,
    fetchMyElves,
    setActive
  }
})
