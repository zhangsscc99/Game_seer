<template>
  <div class="hud-root min-h-screen bg-space-900 overflow-x-hidden" :class="{ 'hud-visible': animate }">

    <!-- ═══════════════════════════════════════════════════════════
         SECTION 1 · 顶部横幅：指挥官信息 + 战况数字仪表盘
    ════════════════════════════════════════════════════════════════ -->
    <div
      class="hud-banner relative w-full px-8 py-8 mb-0 overflow-hidden border-b border-space-500"
      :style="{ transitionDelay: '0ms' }"
    >
      <!-- 扫描线背景层 -->
      <div class="scanlines-overlay"></div>
      <!-- 左侧边装饰线 -->
      <div class="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-transparent via-accent to-transparent opacity-60"></div>

      <div class="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">

        <!-- 指挥官信息 -->
        <div class="flex-1 min-w-0">
          <p class="commander-tag text-xs tracking-[0.4em] text-space-400 mb-1 uppercase font-orbitron">
            Commander · Active
          </p>
          <h1 class="font-orbitron text-2xl sm:text-3xl font-bold text-accent leading-none mb-2 truncate"
              style="text-shadow: 0 0 30px rgba(240,192,64,0.5);">
            {{ displayName }}
          </h1>
          <div class="flex items-center gap-3 mt-2">
            <span class="inline-block w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <p class="text-gray-500 text-sm font-mono">{{ todayDateStr }}</p>
          </div>
          <div class="mt-4 flex items-center gap-3">
            <span class="px-3 py-1 border border-rare/40 text-rare text-xs font-orbitron tracking-widest uppercase">
              LV.{{ userStore.level }}
            </span>
            <div class="flex-1 max-w-xs">
              <div class="h-1 bg-space-700 rounded-full overflow-hidden">
                <div
                  class="h-full bg-rare rounded-full transition-all duration-1000"
                  :style="{ width: levelExpPercent + '%', boxShadow: '0 0 8px #4080ff' }"
                ></div>
              </div>
              <p class="text-gray-600 text-xs mt-1 font-mono">
                {{ userStore.currentExp }} / {{ userStore.nextLevelExp }} EXP
              </p>
            </div>
          </div>
        </div>

        <!-- 右侧数字仪表盘 -->
        <div class="flex gap-6 sm:gap-10 flex-shrink-0">
          <div class="stat-digit-block text-center" :style="{ transitionDelay: '150ms' }">
            <p class="stat-number font-orbitron tabular-nums text-accent" style="font-size: clamp(2.5rem, 6vw, 4.5rem); line-height:1; text-shadow: 0 0 20px rgba(240,192,64,0.6);">
              {{ pendingCount }}
            </p>
            <p class="text-gray-500 text-xs tracking-[0.2em] uppercase font-mono mt-1">Missions</p>
            <p class="text-gray-600 text-xs font-mono">待完成</p>
          </div>
          <div class="w-px bg-gradient-to-b from-transparent via-space-400 to-transparent self-stretch"></div>
          <div class="stat-digit-block text-center" :style="{ transitionDelay: '250ms' }">
            <p class="stat-number font-orbitron tabular-nums text-green-400" style="font-size: clamp(2.5rem, 6vw, 4.5rem); line-height:1; text-shadow: 0 0 20px rgba(74,222,128,0.6);">
              {{ profile?.streak_days || 0 }}
            </p>
            <p class="text-gray-500 text-xs tracking-[0.2em] uppercase font-mono mt-1">Streak</p>
            <p class="text-gray-600 text-xs font-mono">连续天数</p>
          </div>
          <div class="w-px bg-gradient-to-b from-transparent via-space-400 to-transparent self-stretch"></div>
          <div class="stat-digit-block text-center" :style="{ transitionDelay: '350ms' }">
            <p class="stat-number font-orbitron tabular-nums text-rare" style="font-size: clamp(2.5rem, 6vw, 4.5rem); line-height:1; text-shadow: 0 0 20px rgba(64,128,255,0.6);">
              {{ totalExp }}
            </p>
            <p class="text-gray-500 text-xs tracking-[0.2em] uppercase font-mono mt-1">EXP</p>
            <p class="text-gray-600 text-xs font-mono">今日获得</p>
          </div>
        </div>

      </div>

      <!-- 底部进度指示条 -->
      <div class="relative z-10 mt-6">
        <div class="flex justify-between text-xs text-gray-600 font-mono mb-1">
          <span>TODAY PROGRESS</span>
          <span>{{ completedCount }} / {{ totalCount }} &nbsp;·&nbsp; {{ completionRate }}%</span>
        </div>
        <div class="w-full h-px bg-space-600 overflow-hidden">
          <div
            class="h-full transition-all duration-1000"
            :style="{
              width: completionRate + '%',
              background: 'linear-gradient(90deg, #4080ff, #f0c040)',
              boxShadow: '0 0 6px #f0c040'
            }"
          ></div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════
         SECTION 2 · 精灵展示区（非对称）+ 任务终端
    ════════════════════════════════════════════════════════════════ -->
    <div
      class="hud-section flex flex-col lg:flex-row gap-0 border-b border-space-500"
      :style="{ transitionDelay: '100ms' }"
    >

      <!-- 左侧：精灵展示 -->
      <div class="relative lg:w-2/5 px-8 py-10 bg-space-800 flex flex-col items-center justify-center border-r border-space-500 min-h-[360px]">
        <!-- 背景放射渐变 -->
        <div
          class="absolute inset-0 pointer-events-none"
          :style="elfGlowStyle"
        ></div>

        <div v-if="elfStore.activeElf" class="relative z-10 flex flex-col items-center w-full">
          <!-- 能量环容器 -->
          <div class="elf-ring-container relative flex items-center justify-center mb-6"
               style="width: 220px; height: 220px;">
            <!-- 外旋转环 -->
            <div class="energy-ring ring-outer absolute inset-0 rounded-full"></div>
            <!-- 内旋转环 -->
            <div class="energy-ring ring-inner absolute rounded-full" style="inset: 18px;"></div>

            <!-- 八边形图片容器 -->
            <div
              class="elf-octagon relative overflow-hidden z-10 flex items-center justify-center"
              :class="rarityBorderOcta"
              style="width: 160px; height: 160px;"
            >
              <img
                :src="elfStore.activeElf.image_path || `http://localhost:8000/static/elves/${elfStore.activeElf.elf_id || elfStore.activeElf.id}.png`"
                :alt="elfStore.activeElf.name"
                class="w-full h-full object-cover"
                @error="handleElfImgError"
              />
            </div>
          </div>

          <!-- 精灵名字 & 稀有度 -->
          <h2 class="font-orbitron text-white text-xl font-bold tracking-wider mb-1"
              style="text-shadow: 0 0 15px rgba(255,255,255,0.3);">
            {{ elfStore.activeElf.name }}
          </h2>
          <div class="flex items-center gap-3 mb-5">
            <span class="text-xs font-orbitron tracking-widest px-2 py-0.5 border"
                  :class="rarityTagClass">
              {{ elfStore.activeElf.rarity?.toUpperCase() || 'N' }}
            </span>
            <span class="text-gray-400 text-sm font-mono">Lv.{{ elfStore.activeElf.level }}</span>
          </div>

          <!-- 属性三栏 -->
          <div class="w-full grid grid-cols-3 gap-2 max-w-xs">
            <div class="bg-space-700/60 border border-space-500 p-2 text-center">
              <p class="text-white font-bold font-mono text-sm">{{ elfStore.activeElf.attack || '--' }}</p>
              <p class="text-gray-600 text-xs font-mono uppercase tracking-wider mt-0.5">ATK</p>
            </div>
            <div class="bg-space-700/60 border border-space-500 p-2 text-center">
              <p class="text-white font-bold font-mono text-sm">{{ elfStore.activeElf.defense || '--' }}</p>
              <p class="text-gray-600 text-xs font-mono uppercase tracking-wider mt-0.5">DEF</p>
            </div>
            <div class="bg-space-700/60 border border-space-500 p-2 text-center">
              <p class="text-white font-bold font-mono text-sm">{{ elfStore.activeElf.speed || '--' }}</p>
              <p class="text-gray-600 text-xs font-mono uppercase tracking-wider mt-0.5">SPD</p>
            </div>
          </div>

          <!-- EXP 条 -->
          <div class="w-full max-w-xs mt-4">
            <ExpBar
              :current="elfStore.activeElf.current_exp || 0"
              :max="elfStore.activeElf.next_level_exp || 100"
              :level="elfStore.activeElf.level"
              size="md"
              :show-label="true"
            />
          </div>
        </div>

        <!-- 无精灵状态 -->
        <div v-else class="relative z-10 flex flex-col items-center text-center py-8">
          <div class="elf-octagon-empty mb-4 flex items-center justify-center"
               style="width: 140px; height: 140px;">
            <SparklesIcon class="w-12 h-12 text-space-500" />
          </div>
          <p class="text-gray-400 text-sm mb-1">还没有设置主战精灵</p>
          <p class="text-gray-600 text-xs mb-4">去「我的精灵」选一只陪你完成任务</p>
          <router-link to="/my-elves" class="px-4 py-2 border border-accent/50 text-accent text-xs font-orbitron tracking-widest hover:bg-accent/10 transition-colors">
            前往设置
          </router-link>
        </div>

        <!-- 左下角装饰 -->
        <div class="absolute bottom-4 left-4 text-space-500 text-xs font-mono">精灵位</div>
        <div class="absolute top-4 right-4 text-space-500 text-xs font-mono">[ 主战 ]</div>
      </div>

      <!-- 右侧：任务终端 -->
      <div class="flex-1 px-8 py-10 bg-space-900 flex flex-col min-h-[360px]">
        <!-- 终端标题栏 -->
        <div class="flex items-center gap-3 mb-6 pb-3 border-b border-space-600">
          <div class="flex gap-1.5">
            <span class="w-3 h-3 rounded-full bg-red-500/70"></span>
            <span class="w-3 h-3 rounded-full bg-yellow-500/70"></span>
            <span class="w-3 h-3 rounded-full bg-green-500/70"></span>
          </div>
          <p class="text-gray-500 text-xs font-mono tracking-widest flex-1">
            任务终端 · 待完成队列
          </p>
          <router-link to="/tasks" class="text-rare text-xs font-mono hover:text-accent transition-colors">
            查看全部 →
          </router-link>
        </div>

        <!-- 加载中 -->
        <div v-if="taskStore.loading" class="flex-1 flex items-center justify-center">
          <div class="flex flex-col items-center gap-3">
            <div class="w-6 h-6 border border-accent border-t-transparent rounded-full animate-spin"></div>
            <p class="text-gray-600 text-xs font-mono">加载中...</p>
          </div>
        </div>

        <!-- 无任务 -->
        <div v-else-if="recentPendingTasks.length === 0" class="flex-1 flex items-center justify-center">
          <div class="text-center">
            <p class="text-green-400 font-mono text-sm mb-2">[ 今日任务全部完成 ]</p>
            <p class="text-gray-600 text-xs font-mono">继续保持，明天再接再厉</p>
          </div>
        </div>

        <!-- 终端任务列表 -->
        <div v-else class="terminal-list flex-1 overflow-y-auto space-y-0">
          <div
            v-for="(task, idx) in recentPendingTasks"
            :key="task.id"
            class="terminal-row flex items-baseline gap-2 py-2.5 px-2 border-b border-space-700/50 hover:bg-space-800/50 transition-colors cursor-default group"
            :style="{ animationDelay: (idx * 80) + 'ms' }"
          >
            <span class="terminal-cursor text-green-400 font-mono text-sm flex-shrink-0 group-hover:animate-blink">▶</span>
            <span class="text-gray-500 font-mono text-xs flex-shrink-0">
              [任务-{{ String(idx + 1).padStart(3, '0') }}]
            </span>
            <span class="text-gray-300 font-mono text-sm flex-1 truncate">{{ task.title }}</span>
            <span class="terminal-dots flex-shrink-0 text-space-500 font-mono text-xs hidden sm:inline">
              ···············
            </span>
            <span class="text-accent font-mono text-xs flex-shrink-0 whitespace-nowrap">
              +{{ task.exp_reward || 10 }} EXP
            </span>
          </div>
        </div>

        <!-- 终端输入提示行 -->
        <div class="mt-4 pt-3 border-t border-space-700">
          <p class="text-green-400/50 font-mono text-xs">
            <span class="text-green-400">›</span> 系统就绪 ·
            今日已完成 <span class="text-accent">{{ completedCount }}</span> 个任务
            <span class="terminal-blink-cursor">_</span>
          </p>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════
         SECTION 3 · 快捷入口（已移除）
    ════════════════════════════════════════════════════════════════ -->

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useTaskStore } from '@/stores/task'
import { useElfStore } from '@/stores/elf'
import ExpBar from '@/components/common/ExpBar.vue'
import { SparklesIcon } from '@heroicons/vue/24/outline'

const userStore = useUserStore()
const taskStore = useTaskStore()
const elfStore = useElfStore()

// ── 入场动画控制 ──────────────────────────────
const animate = ref(false)

// ── 基础数据 ──────────────────────────────────
const displayName = computed(() => userStore.displayName)
const profile = computed(() => userStore.profile)

const todayDateStr = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')} // ${['SUN','MON','TUE','WED','THU','FRI','SAT'][d.getDay()]}`
})

// ── 任务统计 ──────────────────────────────────
const totalCount = computed(() => taskStore.tasks.length)
const pendingCount = computed(() => taskStore.pendingTasks.length)
const completedCount = computed(() => taskStore.completedTasks.length)
const completionRate = computed(() => {
  if (!totalCount.value) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})
const totalExp = computed(() =>
  taskStore.completedTasks.reduce((sum, t) => sum + (t.exp_reward || 10), 0)
)
const recentPendingTasks = computed(() => taskStore.pendingTasks.slice(0, 6))

// ── 等级经验百分比 ─────────────────────────────
const levelExpPercent = computed(() => {
  const cur = userStore.currentExp || 0
  const max = userStore.nextLevelExp || 100
  return Math.min(100, Math.round((cur / max) * 100))
})

// ── 精灵相关 ──────────────────────────────────
const rarityColorMap = {
  N:   { border: '#555', glow: 'rgba(120,120,120,0.15)', ring: '#666', tag: 'border-gray-600 text-gray-400' },
  R:   { border: '#4080ff', glow: 'rgba(64,128,255,0.12)', ring: '#4080ff', tag: 'border-rare text-rare' },
  SR:  { border: '#ffa500', glow: 'rgba(255,165,0,0.14)', ring: '#ffa500', tag: 'border-sr text-sr' },
  SSR: { border: '#ff4500', glow: 'rgba(255,69,0,0.16)', ring: '#ff4500', tag: 'border-ssr text-orange-400' },
  UR:  { border: '#9b30ff', glow: 'rgba(155,48,255,0.18)', ring: '#9b30ff', tag: 'border-ur text-purple-400' },
}

const activeRarity = computed(() => {
  const r = elfStore.activeElf?.rarity?.toUpperCase() || 'N'
  return rarityColorMap[r] || rarityColorMap['N']
})

const rarityBorderClass = computed(() => {
  const elf = elfStore.activeElf
  if (!elf) return 'border-gray-600'
  const map = {
    N: 'border-gray-600', R: 'border-rare', SR: 'border-sr',
    SSR: 'border-ssr shadow-glow-ssr', UR: 'border-ur shadow-glow-ur'
  }
  return map[elf.rarity?.toUpperCase()] || 'border-gray-600'
})

const rarityBorderOcta = computed(() => {
  return `rarity-octa-${(elfStore.activeElf?.rarity || 'n').toLowerCase()}`
})

const rarityTagClass = computed(() => activeRarity.value.tag)

const elfGlowStyle = computed(() => {
  const color = activeRarity.value.glow
  return {
    background: `radial-gradient(ellipse at 50% 40%, ${color} 0%, transparent 70%)`
  }
})

// ── 快捷入口 ──────────────────────────────────
const quickLinks = [
  { path: '/tasks',        num: '01', label: '今日任务',  desc: 'DAILY MISSIONS',    glowColor: '#f0c040' },
  { path: '/elves',        num: '02', label: '精灵图鉴',  desc: 'ELF COMPENDIUM',    glowColor: '#4080ff' },
  { path: '/boss',         num: '03', label: 'Boss挑战',  desc: 'BOSS ENCOUNTER',    glowColor: '#ff4500' },
  { path: '/achievements', num: '04', label: '成就系统',  desc: 'ACHIEVEMENTS',      glowColor: '#9b30ff' },
]

// ── 精灵图片错误处理 ───────────────────────────
function handleElfImgError(e) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-5xl text-gray-600">?</div>'
}

// ── 生命周期 ──────────────────────────────────
onMounted(async () => {
  // 触发入场动画
  requestAnimationFrame(() => {
    setTimeout(() => { animate.value = true }, 50)
  })

  try {
    if (taskStore.tasks.length === 0) {
      await taskStore.fetchTasks()
    }
  } catch {
    // Silent fail
  }
})
</script>

<style scoped>
/* ══════════════════════════════════════════════
   字体
══════════════════════════════════════════════ */
.font-orbitron {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
}

/* ══════════════════════════════════════════════
   入场动画 staggered reveal
══════════════════════════════════════════════ */
.hud-root {
  --anim-dur: 0.6s;
  --anim-ease: cubic-bezier(0.16, 1, 0.3, 1);
}

.hud-banner,
.hud-section {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity var(--anim-dur) var(--anim-ease),
              transform var(--anim-dur) var(--anim-ease);
}

.hud-visible .hud-banner {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0ms;
}

.hud-visible .hud-section:nth-child(2) {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 120ms;
}

.hud-visible .hud-section:nth-child(3) {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 240ms;
}

/* ══════════════════════════════════════════════
   扫描线背景（顶部横幅）
══════════════════════════════════════════════ */
.scanlines-overlay {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 3px,
    rgba(255, 255, 255, 0.018) 3px,
    rgba(255, 255, 255, 0.018) 4px
  );
  pointer-events: none;
  z-index: 1;
}

/* ══════════════════════════════════════════════
   精灵八边形容器
══════════════════════════════════════════════ */
.elf-octagon,
.elf-octagon-empty {
  clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
  background: #161b35;
}

.elf-octagon-empty {
  border: 2px solid #2e3a6e;
}

/* 各稀有度边框色（通过 box-shadow 模拟，因为 clip-path 裁掉了 border） */
.rarity-octa-n   { box-shadow: 0 0 0 2px #555,    0 0 12px rgba(120,120,120,0.2); }
.rarity-octa-r   { box-shadow: 0 0 0 2px #4080ff, 0 0 16px rgba(64,128,255,0.35); }
.rarity-octa-sr  { box-shadow: 0 0 0 2px #ffa500, 0 0 18px rgba(255,165,0,0.4); }
.rarity-octa-ssr { box-shadow: 0 0 0 2px #ff4500, 0 0 22px rgba(255,69,0,0.5); }
.rarity-octa-ur  { box-shadow: 0 0 0 2px #9b30ff, 0 0 24px rgba(155,48,255,0.55); }

/* ══════════════════════════════════════════════
   能量环动画
══════════════════════════════════════════════ */
.elf-ring-container {
  /* nothing extra */
}

.energy-ring {
  border: 1.5px solid transparent;
  box-sizing: border-box;
  pointer-events: none;
}

.ring-outer {
  border-top-color:    rgba(240, 192, 64, 0.7);
  border-right-color:  rgba(240, 192, 64, 0.15);
  border-bottom-color: rgba(240, 192, 64, 0.0);
  border-left-color:   rgba(240, 192, 64, 0.35);
  animation: spin-cw 4s linear infinite;
}

.ring-inner {
  border-top-color:    rgba(64, 128, 255, 0.0);
  border-right-color:  rgba(64, 128, 255, 0.6);
  border-bottom-color: rgba(64, 128, 255, 0.7);
  border-left-color:   rgba(64, 128, 255, 0.15);
  animation: spin-ccw 3s linear infinite;
}

@keyframes spin-cw {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

@keyframes spin-ccw {
  from { transform: rotate(0deg); }
  to   { transform: rotate(-360deg); }
}

/* ══════════════════════════════════════════════
   终端列表
══════════════════════════════════════════════ */
.terminal-list {
  font-family: 'JetBrains Mono', 'Consolas', 'Fira Mono', monospace;
}

.terminal-row {
  animation: terminal-slide-in 0.4s ease-out both;
}

@keyframes terminal-slide-in {
  from {
    opacity: 0;
    transform: translateX(-12px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 光标闪烁 */
.terminal-blink-cursor {
  animation: blink 1.1s step-end infinite;
  color: #4080ff;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* ══════════════════════════════════════════════
   斜切卡片 clip-path
══════════════════════════════════════════════ */
.clip-card {
  clip-path: polygon(
    0 0,
    calc(100% - 16px) 0,
    100% 16px,
    100% 100%,
    16px 100%,
    0 calc(100% - 16px)
  );
  transition: background-color 0.25s ease, border-color 0.25s ease, transform 0.2s ease;
}

.clip-card:hover {
  transform: translateY(-3px);
}

.clip-card-glow {
  clip-path: inherit;
}

/* ══════════════════════════════════════════════
   稀有度标签颜色（补充 Tailwind 缺失的）
══════════════════════════════════════════════ */
.text-sr   { color: #ffa500; }
.border-sr { border-color: #ffa500; }

/* ══════════════════════════════════════════════
   stat digit 入场
══════════════════════════════════════════════ */
.stat-digit-block {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.hud-visible .stat-digit-block {
  opacity: 1;
  transform: translateY(0);
}
</style>
