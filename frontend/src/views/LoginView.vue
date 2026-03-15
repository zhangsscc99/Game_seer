<template>
  <div class="min-h-screen bg-space-900 flex items-center justify-center px-4">
    <!-- 星空背景装饰 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-rare/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-ur/5 rounded-full blur-3xl"></div>
    </div>

    <div class="relative w-full max-w-md">
      <!-- 标题区 -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto rounded-full bg-accent/20 border-2 border-accent/50 flex items-center justify-center mb-4 glow-pulse">
          <span class="text-4xl">🌟</span>
        </div>
        <h1 class="text-3xl font-bold text-accent mb-2">Game Seer</h1>
        <p class="text-gray-400 text-lg">指挥官登录</p>
      </div>

      <!-- 登录卡片 -->
      <div class="bg-space-800 border border-space-500 rounded-xl p-8 shadow-2xl">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- 邮箱 -->
          <div>
            <label class="block text-gray-400 text-sm mb-2">指挥官邮箱</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">📧</span>
              <input
                v-model="form.email"
                type="email"
                placeholder="your@email.com"
                class="game-input pl-9"
                :class="{ 'border-red-500': errors.email }"
                autocomplete="email"
              />
            </div>
            <p v-if="errors.email" class="text-red-400 text-xs mt-1">{{ errors.email }}</p>
          </div>

          <!-- 密码 -->
          <div>
            <label class="block text-gray-400 text-sm mb-2">作战密码</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">🔐</span>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="输入密码..."
                class="game-input pl-9 pr-10"
                :class="{ 'border-red-500': errors.password }"
                autocomplete="current-password"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
              >
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
            <p v-if="errors.password" class="text-red-400 text-xs mt-1">{{ errors.password }}</p>
          </div>

          <!-- 错误提示 -->
          <div v-if="loginError" class="bg-red-900/30 border border-red-500/50 rounded-lg px-4 py-3">
            <p class="text-red-400 text-sm flex items-center gap-2">
              <span>⚠️</span>
              {{ loginError }}
            </p>
          </div>

          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full game-btn-primary py-3 text-base font-bold flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="w-5 h-5 border-2 border-space-900 border-t-transparent rounded-full animate-spin"></span>
            <span v-else>⚡</span>
            {{ loading ? '登录中...' : '进入战场' }}
          </button>
        </form>

        <!-- 分隔线 -->
        <div class="my-6 flex items-center gap-3">
          <div class="flex-1 h-px bg-space-500"></div>
          <span class="text-gray-600 text-xs">OR</span>
          <div class="flex-1 h-px bg-space-500"></div>
        </div>

        <!-- 注册链接 -->
        <p class="text-center text-gray-500 text-sm">
          还没有账号？
          <router-link to="/register" class="text-accent hover:text-accent-light hover:underline transition-colors font-medium ml-1">
            注册成为指挥官
          </router-link>
        </p>
      </div>

      <!-- 版权信息 -->
      <p class="text-center text-gray-700 text-xs mt-6">Game Seer © 2024 · 游戏化任务系统</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const loginError = ref('')
const showPassword = ref(false)

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

function validate() {
  errors.email = ''
  errors.password = ''
  let valid = true
  if (!form.email) {
    errors.email = '请输入邮箱'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = '邮箱格式不正确'
    valid = false
  }
  if (!form.password) {
    errors.password = '请输入密码'
    valid = false
  }
  return valid
}

async function handleLogin() {
  if (!validate()) return
  loading.value = true
  loginError.value = ''
  try {
    await userStore.login(form.email, form.password)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    loginError.value = err.response?.data?.detail || '登录失败，请检查邮箱和密码'
  } finally {
    loading.value = false
  }
}
</script>
