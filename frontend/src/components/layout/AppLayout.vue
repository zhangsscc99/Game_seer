<template>
  <div class="flex h-screen bg-space-900 overflow-hidden">

    <!-- 移动端遮罩层 -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-20 bg-black/60 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- 侧边栏 -->
    <aside
      class="fixed lg:static inset-y-0 left-0 z-30 w-64 flex-shrink-0 bg-space-800 border-r border-space-500 flex flex-col overflow-y-auto transition-transform duration-300 ease-in-out"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
    >
      <!-- Logo区域 -->
      <div class="p-6 border-b border-space-500">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-accent/20 border border-accent/50 flex items-center justify-center">
            <span class="text-accent font-bold text-lg">G</span>
          </div>
          <div>
            <h1 class="text-accent font-bold text-lg leading-none">Game Seer</h1>
            <p class="text-gray-500 text-xs mt-0.5">指挥官系统</p>
          </div>
        </div>
      </div>

      <!-- 用户信息 -->
      <div class="p-4 border-b border-space-500">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-full bg-primary border-2 border-accent/50 flex items-center justify-center overflow-hidden">
            <span class="text-white font-bold">{{ displayName.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-white font-medium truncate">{{ displayName }}</p>
            <p class="text-accent text-xs">Lv.{{ userStore.level }} 指挥官</p>
          </div>
        </div>
        <!-- 经验条 -->
        <ExpBar
          :current="userStore.currentExp"
          :max="userStore.nextLevelExp"
          :level="userStore.level"
          size="sm"
        />
      </div>

      <!-- 主战精灵 -->
      <div v-if="elfStore.activeElf" class="p-4 border-b border-space-500">
        <p class="text-gray-500 text-xs mb-2 uppercase tracking-wider">主战精灵</p>
        <div class="flex items-center gap-3 bg-space-700 rounded-lg p-3 border border-space-400 hover:border-accent/40 transition-colors">
          <div class="w-12 h-12 rounded-lg overflow-hidden bg-space-600 flex-shrink-0">
            <img
              :src="`http://localhost:8000/static/elves/${elfStore.activeElf.elf_id || elfStore.activeElf.id}.png`"
              :alt="elfStore.activeElf.name"
              class="w-full h-full object-cover"
              @error="handleElfImgError"
            />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-white text-sm font-medium truncate">{{ elfStore.activeElf.name }}</p>
            <p class="text-accent text-xs">Lv.{{ elfStore.activeElf.level }}</p>
            <div class="mt-1">
              <div class="w-full h-1 bg-space-600 rounded-full overflow-hidden">
                <div
                  class="h-full bg-accent rounded-full transition-all duration-500"
                  :style="{ width: elfExpPercent + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="p-4 border-b border-space-500">
        <p class="text-gray-500 text-xs mb-2 uppercase tracking-wider">主战精灵</p>
        <div class="bg-space-700 rounded-lg p-3 border border-dashed border-space-400 text-center">
          <p class="text-gray-500 text-sm">尚未设置主战精灵</p>
          <router-link to="/my-elves" class="text-accent text-xs hover:underline mt-1 block">前往设置</router-link>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 p-3 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          custom
          v-slot="{ isActive, navigate }"
        >
          <div
            @click="navigate"
            :class="isActive ? 'nav-item-active' : 'nav-item'"
            class="cursor-pointer"
          >
            <span class="text-xl">{{ item.icon }}</span>
            <span class="text-sm font-medium">{{ item.label }}</span>
            <span
              v-if="item.badge"
              class="ml-auto bg-accent text-space-900 text-xs font-bold px-1.5 py-0.5 rounded-full"
            >{{ item.badge }}</span>
          </div>
        </router-link>
      </nav>

      <!-- 底部登出 -->
      <div class="p-3 border-t border-space-500">
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-900/20 transition-all duration-200"
        >
          <span class="text-xl">🚪</span>
          <span class="text-sm">退出登录</span>
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="flex-1 overflow-y-auto bg-space-900 flex flex-col min-w-0">
      <!-- 顶部栏（移动端） -->
      <div class="sticky top-0 z-10 bg-space-800/80 backdrop-blur-sm border-b border-space-500 px-4 py-3 flex items-center justify-between lg:hidden">
        <button @click="sidebarOpen = !sidebarOpen" class="text-gray-400 hover:text-white p-1">
          <span class="text-2xl">☰</span>
        </button>
        <h1 class="text-accent font-bold">Game Seer</h1>
        <div class="w-8"></div>
      </div>

      <!-- 页面内容 -->
      <div class="flex-1 p-4 md:p-6 pb-24 lg:pb-6">
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </div>
    </main>

    <!-- 移动端底部导航栏 -->
    <nav class="fixed bottom-0 left-0 right-0 z-20 bg-space-800/95 backdrop-blur-sm border-t border-space-500 lg:hidden">
      <div class="flex items-center justify-around px-2 py-2 safe-area-inset-bottom">
        <router-link
          v-for="item in mobileNavItems"
          :key="item.path"
          :to="item.path"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            class="flex flex-col items-center gap-0.5 px-3 py-1 rounded-lg transition-colors"
            :class="isActive ? 'text-accent' : 'text-gray-500'"
          >
            <span class="text-xl leading-none">{{ item.icon }}</span>
            <span class="text-xs leading-none">{{ item.label }}</span>
            <span
              v-if="item.badge"
              class="absolute -top-1 -right-1 bg-accent text-space-900 text-xs font-bold w-4 h-4 rounded-full flex items-center justify-center"
            >{{ item.badge }}</span>
          </button>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useElfStore } from '@/stores/elf'
import { useTaskStore } from '@/stores/task'
import ExpBar from '@/components/common/ExpBar.vue'

const router = useRouter()
const userStore = useUserStore()
const elfStore = useElfStore()
const taskStore = useTaskStore()

const sidebarOpen = ref(false)

// 桌面端默认展开
onMounted(async () => {
  if (window.innerWidth >= 1024) sidebarOpen.value = true
  try {
    await elfStore.fetchMyElves()
    await taskStore.fetchTasks()
  } catch {
    // Silent fail
  }
})

const displayName = computed(() => userStore.displayName)

const elfExpPercent = computed(() => {
  const elf = elfStore.activeElf
  if (!elf || !elf.next_level_exp) return 0
  return Math.min(100, Math.round((elf.current_exp / elf.next_level_exp) * 100))
})

const pendingCount = computed(() => taskStore.pendingTasks.length)

const navItems = computed(() => [
  { path: '/', icon: '🏠', label: '指挥台', badge: null },
  { path: '/tasks', icon: '📋', label: '任务中心', badge: pendingCount.value > 0 ? pendingCount.value : null },
  { path: '/elves', icon: '📖', label: '精灵图鉴', badge: null },
  { path: '/my-elves', icon: '⭐', label: '我的精灵', badge: null },
  { path: '/boss', icon: '⚔️', label: 'Boss挑战', badge: null },
  { path: '/achievements', icon: '🏆', label: '成就', badge: null },
  { path: '/profile', icon: '👤', label: '个人资料', badge: null }
])

// 移动端底部导航只显示5个核心入口
const mobileNavItems = computed(() => [
  { path: '/', icon: '🏠', label: '首页', badge: null },
  { path: '/tasks', icon: '📋', label: '任务', badge: pendingCount.value > 0 ? pendingCount.value : null },
  { path: '/elves', icon: '📖', label: '图鉴', badge: null },
  { path: '/boss', icon: '⚔️', label: 'Boss', badge: null },
  { path: '/profile', icon: '👤', label: '我的', badge: null }
])

function handleElfImgError(e) {
  e.target.src = ''
  e.target.parentElement.innerHTML = '<div class="w-full h-full flex items-center justify-center text-2xl">🐾</div>'
}

function handleLogout() {
  userStore.logout()
  router.push('/login')
}

onMounted(async () => {
  if (window.innerWidth >= 1024) sidebarOpen.value = true
  try {
    await elfStore.fetchMyElves()
    await taskStore.fetchTasks()
  } catch {
    // Silent fail
  }
})
</script>
