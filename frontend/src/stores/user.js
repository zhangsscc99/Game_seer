import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'
import { getProfile } from '@/api/profile'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const profile = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isLoggedIn = computed(() => !!token.value)
  const displayName = computed(() => user.value?.username || '指挥官')
  const level = computed(() => profile.value?.level || 1)
  const currentExp = computed(() => profile.value?.current_exp || 0)
  const nextLevelExp = computed(() => profile.value?.next_level_exp || 100)

  async function login(email, password) {
    const response = await authApi.login(email, password)
    const data = response.data
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    await fetchProfile()
    return data
  }

  async function register(username, email, password) {
    const response = await authApi.register(username, email, password)
    const data = response.data
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    return data
  }

  async function fetchProfile() {
    const response = await authApi.getMe()
    user.value = response.data
    try {
      const profileRes = await getProfile()
      profile.value = profileRes.data
    } catch {
      // profile may not be loaded yet
    }
    return user.value
  }

  function logout() {
    token.value = null
    user.value = null
    profile.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    profile,
    token,
    isLoggedIn,
    displayName,
    level,
    currentExp,
    nextLevelExp,
    login,
    register,
    fetchProfile,
    logout
  }
})
