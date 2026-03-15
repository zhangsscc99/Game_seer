<template>
  <div class="min-h-screen bg-space-900 flex items-center justify-center px-4">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/3 right-1/4 w-80 h-80 bg-ur/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/3 left-1/4 w-64 h-64 bg-rare/5 rounded-full blur-3xl"></div>
    </div>

    <div class="relative w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto rounded-full bg-ur/20 border-2 border-ur/50 flex items-center justify-center mb-4">
          <span class="text-4xl">🚀</span>
        </div>
        <h1 class="text-3xl font-bold text-accent mb-2">Game Seer</h1>
        <p class="text-gray-400 text-lg">注册指挥官账号</p>
      </div>

      <div class="bg-space-800 border border-space-500 rounded-xl p-8 shadow-2xl">
        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- 用户名 -->
          <div>
            <label class="block text-gray-400 text-sm mb-2">指挥官代号</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">👤</span>
              <input
                v-model="form.username"
                type="text"
                placeholder="输入你的代号..."
                class="game-input pl-9"
                :class="{ 'border-red-500': errors.username }"
                autocomplete="username"
              />
            </div>
            <p v-if="errors.username" class="text-red-400 text-xs mt-1">{{ errors.username }}</p>
          </div>

          <!-- 邮箱 -->
          <div>
            <label class="block text-gray-400 text-sm mb-2">联系邮箱</label>
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
            <label class="block text-gray-400 text-sm mb-2">设置密码</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">🔐</span>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="至少6位字符..."
                class="game-input pl-9 pr-10"
                :class="{ 'border-red-500': errors.password }"
                autocomplete="new-password"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
              >
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
            <p v-if="errors.password" class="text-red-400 text-xs mt-1">{{ errors.password }}</p>
          </div>

          <!-- 确认密码 -->
          <div>
            <label class="block text-gray-400 text-sm mb-2">确认密码</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">🔑</span>
              <input
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                placeholder="再次输入密码..."
                class="game-input pl-9"
                :class="{ 'border-red-500': errors.confirmPassword }"
                autocomplete="new-password"
              />
            </div>
            <p v-if="errors.confirmPassword" class="text-red-400 text-xs mt-1">{{ errors.confirmPassword }}</p>
          </div>

          <!-- 错误提示 -->
          <div v-if="registerError" class="bg-red-900/30 border border-red-500/50 rounded-lg px-4 py-3">
            <p class="text-red-400 text-sm flex items-center gap-2">
              <span>⚠️</span>
              {{ registerError }}
            </p>
          </div>

          <!-- 注册按钮 -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full game-btn-primary py-3 text-base font-bold flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="w-5 h-5 border-2 border-space-900 border-t-transparent rounded-full animate-spin"></span>
            <span v-else>🚀</span>
            {{ loading ? '注册中...' : '加入战场' }}
          </button>
        </form>

        <div class="my-6 flex items-center gap-3">
          <div class="flex-1 h-px bg-space-500"></div>
          <span class="text-gray-600 text-xs">OR</span>
          <div class="flex-1 h-px bg-space-500"></div>
        </div>

        <p class="text-center text-gray-500 text-sm">
          已有账号？
          <router-link to="/login" class="text-accent hover:text-accent-light hover:underline transition-colors font-medium ml-1">
            立即登录
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const registerError = ref('')
const showPassword = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

function validate() {
  let valid = true
  errors.username = ''
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''

  if (!form.username.trim()) {
    errors.username = '请输入指挥官代号'
    valid = false
  } else if (form.username.length < 2) {
    errors.username = '代号至少2个字符'
    valid = false
  }

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
  } else if (form.password.length < 6) {
    errors.password = '密码至少6位字符'
    valid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = '请确认密码'
    valid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = '两次密码不一致'
    valid = false
  }

  return valid
}

async function handleRegister() {
  if (!validate()) return
  loading.value = true
  registerError.value = ''
  try {
    await userStore.register(form.username, form.email, form.password)
    router.push('/')
  } catch (err) {
    registerError.value = err.response?.data?.detail || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
