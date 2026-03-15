<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(async () => {
  if (userStore.token) {
    try {
      await userStore.fetchProfile()
    } catch {
      userStore.logout()
    }
  }
})
</script>
