<template>
  <div
    class="elf-card relative cursor-pointer overflow-hidden transition-all duration-300"
    :class="[cardClass, { 'card-unlocked': elf.unlocked, 'card-locked': !elf.unlocked }]"
    :data-rarity="rarity"
    @click="$emit('click', elf)"
    @mousemove="onMouseMove"
    @mouseleave="onMouseLeave"
    :style="cardStyle"
  >
    <!-- UR 彩虹渐变动态边框 -->
    <div v-if="rarity === 'UR'" class="ur-border-ring"></div>

    <!-- SR 顶部三角装饰 -->
    <div v-if="rarity === 'SR'" class="sr-triangle-top"></div>

    <!-- SSR 彩虹薄膜遮罩（screen混合模式） -->
    <div v-if="rarity === 'SSR' && elf.unlocked" class="ssr-rainbow-film"></div>

    <!-- 精灵编号 -->
    <div class="card-number absolute top-2 right-2 z-20 font-mono text-xs opacity-60 tracking-widest">
      #{{ String(elf.id || 0).padStart(3, '0') }}
    </div>

    <!-- 图片区域 -->
    <div class="relative aspect-square overflow-hidden flex items-center justify-center" :class="imgBgClass">
      <!-- 精灵图片（图鉴全部可见） -->
      <img
        :src="elf.image_path || `http://localhost:8000/static/elves/${elf.id}.png`"
        :alt="elf.name"
        class="w-full h-full object-contain p-2 transition-transform duration-500 hover:scale-110 img-main"
        @error="handleImgError"
      />

      <!-- SR 扫描光线（从上到下） -->
      <div v-if="rarity === 'SR'" class="sr-scan-line"></div>

      <!-- 已收集角标 -->
      <div v-if="elf.collected" class="absolute bottom-2 left-2 z-20 bg-green-500/90 rounded-full px-1.5 py-0.5 flex items-center gap-1">
        <span class="text-white text-xs font-bold">✓ 已收集</span>
      </div>

      <!-- 悬停发光遮罩 -->
      <div class="hover-glow-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" :class="glowOverlayClass"></div>
    </div>

    <!-- 信息区域 -->
    <div class="card-info relative z-10 px-3 py-2 bg-space-800">
      <!-- 稀有度标签 + 属性 -->
      <div class="flex items-center justify-between mb-1">
        <span class="rarity-badge" :class="rarityBadgeClass">{{ rarity }}</span>
        <span
          class="element-dot w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold border"
          :class="elementClass"
          :title="elf.element"
        >{{ elementSymbol }}</span>
      </div>

      <!-- 精灵名 -->
      <p class="font-semibold text-sm truncate leading-tight text-white">
        {{ elf.name }}
      </p>

      <!-- 等级（已收集时显示） -->
      <div class="mt-1 flex items-center justify-between">
        <span v-if="elf.collected && elf.level" class="level-text font-black tracking-widest text-xs text-accent">
          LV.{{ String(elf.level).padStart(2, '0') }}
        </span>
        <span v-else class="text-gray-500 text-xs truncate">{{ elf.unlock_condition || '完成任务解锁' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onUnmounted } from 'vue'

const props = defineProps({
  elf: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

// 鼠标 3D 倾斜（UR 专属）
const tiltX = ref(0)
const tiltY = ref(0)

// rarity 必须在所有依赖它的 computed 之前声明
const rarity = computed(() => (props.elf.rarity || 'N').toUpperCase())

const imgBgClass = computed(() => {
  const map = {
    N:   'bg-space-700',
    R:   'bg-[#0d1f3a]',
    SR:  'bg-[#1a1200]',
    SSR: 'bg-[#1a0800]',
    UR:  'bg-[#0f0020]',
  }
  return map[rarity.value] || 'bg-space-700'
})

const cardStyle = computed(() => {
  if (rarity.value === 'UR') {
    return {
      transform: `perspective(600px) rotateX(${tiltX.value}deg) rotateY(${tiltY.value}deg)`,
      transition: tiltX.value === 0 && tiltY.value === 0 ? 'transform 0.5s ease' : 'transform 0.08s linear'
    }
  }
  return {}
})

let _mounted = true
onUnmounted(() => { _mounted = false })

function onMouseMove(e) {
  if (!_mounted || rarity.value !== 'UR') return
  const rect = e.currentTarget?.getBoundingClientRect()
  if (!rect) return
  const cx = rect.left + rect.width / 2
  const cy = rect.top + rect.height / 2
  const dx = (e.clientX - cx) / (rect.width / 2)
  const dy = (e.clientY - cy) / (rect.height / 2)
  tiltX.value = -dy * 12
  tiltY.value = dx * 12
}

function onMouseLeave() {
  if (!_mounted) return
  tiltX.value = 0
  tiltY.value = 0
}

const cardClass = computed(() => {
  const base = 'group'
  const map = {
    N:   'card-n border-2 border-gray-600',
    R:   'card-r border-2',
    SR:  'card-sr border-2',
    SSR: 'card-ssr border-2',
    UR:  'card-ur border-2'
  }
  return `${base} ${map[rarity.value] || map['N']}`
})

const glowOverlayClass = computed(() => {
  const map = {
    N:   'bg-white/5',
    R:   'bg-rare/15',
    SR:  'bg-sr/15',
    SSR: 'bg-ssr/15',
    UR:  'bg-ur/15'
  }
  return map[rarity.value] || 'bg-transparent'
})

const rarityBadgeClass = computed(() => {
  const map = {
    N:   'badge-n',
    R:   'badge-r',
    SR:  'badge-sr',
    SSR: 'badge-ssr',
    UR:  'badge-ur'
  }
  return map[rarity.value] || 'badge-n'
})

const elementSymbol = computed(() => {
  const map = {
    fire:     'F',
    water:    'W',
    grass:    'G',
    electric: 'E',
    ice:      'I',
    dark:     'D',
    light:    'L',
    earth:    'T',
    wind:     'A',
    poison:   'P'
  }
  return map[props.elf.element?.toLowerCase()] || '?'
})

const elementClass = computed(() => {
  const map = {
    fire:     'bg-red-900/60 border-red-600/60 text-red-300',
    water:    'bg-blue-900/60 border-blue-600/60 text-blue-300',
    grass:    'bg-green-900/60 border-green-600/60 text-green-300',
    electric: 'bg-yellow-900/60 border-yellow-500/60 text-yellow-300',
    ice:      'bg-cyan-900/60 border-cyan-600/60 text-cyan-200',
    dark:     'bg-gray-900/80 border-gray-600/60 text-gray-400',
    light:    'bg-yellow-700/30 border-yellow-400/60 text-yellow-200',
    earth:    'bg-orange-900/60 border-orange-600/60 text-orange-300',
    wind:     'bg-teal-900/60 border-teal-600/60 text-teal-300',
    poison:   'bg-purple-900/60 border-purple-600/60 text-purple-300'
  }
  return map[props.elf.element?.toLowerCase()] || 'bg-space-600 border-space-400 text-gray-400'
})

function handleImgError(e) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  if (parent && !parent.querySelector('.fallback-icon')) {
    const div = document.createElement('div')
    div.className = 'fallback-icon w-full h-full flex items-center justify-center text-3xl text-gray-600'
    div.textContent = '◈'
    parent.appendChild(div)
  }
}
</script>

<style scoped>
/* ─────────────────────────────────────────
   基础卡片
───────────────────────────────────────── */
.elf-card {
  border-radius: 4px;
  will-change: transform;
  user-select: none;
}

/* ─────────────────────────────────────────
   N 级 — 暗灰，悬停轻微白光
───────────────────────────────────────── */
.card-n {
  border-color: #4b5563;
  background: #1a1f2e;
}
.card-n:hover {
  box-shadow: 0 0 8px rgba(255,255,255,0.08);
  transform: translateY(-2px);
}

/* ─────────────────────────────────────────
   R 级 — 蓝色流动边框
───────────────────────────────────────── */
.card-r {
  border-color: #4080ff;
  background: #111827;
  animation: border-flow-r 3s linear infinite;
}
@keyframes border-flow-r {
  0%   { border-color: #4080ff; box-shadow: 0 0 6px #4080ff66; }
  25%  { border-color: #60a0ff; box-shadow: 0 0 12px #60a0ff88; }
  50%  { border-color: #80c0ff; box-shadow: 0 0 8px #80c0ff66; }
  75%  { border-color: #60a0ff; box-shadow: 0 0 12px #60a0ff88; }
  100% { border-color: #4080ff; box-shadow: 0 0 6px #4080ff66; }
}
.card-r:hover {
  box-shadow: 0 0 20px #4080ffaa, 0 4px 24px #4080ff44;
  transform: translateY(-3px);
}

/* ─────────────────────────────────────────
   SR 级 — 金橙色，顶部三角，扫描光线
───────────────────────────────────────── */
.card-sr {
  border-color: #ffa500;
  background: #131008;
  box-shadow: 0 0 10px #ffa50044;
}
.card-sr:hover {
  box-shadow: 0 0 22px #ffa500aa, 0 4px 24px #ffa50044;
  transform: translateY(-4px);
}

/* 顶部三角装饰 */
.sr-triangle-top {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 14px solid transparent;
  border-right: 14px solid transparent;
  border-top: 16px solid #ffa500;
  z-index: 30;
  filter: drop-shadow(0 0 4px #ffa500);
}

/* 扫描光线：悬停时从上到下扫过 */
.sr-scan-line {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 15;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(255,255,255,0.0) 30%,
    rgba(255,220,100,0.25) 48%,
    rgba(255,255,255,0.35) 50%,
    rgba(255,220,100,0.25) 52%,
    transparent 70%,
    transparent 100%
  );
  background-size: 100% 200%;
  animation: scan-pass 4s ease-in-out infinite;
  opacity: 0;
  transition: opacity 0.3s;
}
.card-sr:hover .sr-scan-line {
  opacity: 1;
}
@keyframes scan-pass {
  0%   { background-position: 0 -100%; }
  60%  { background-position: 0 200%; }
  100% { background-position: 0 200%; }
}

/* ─────────────────────────────────────────
   SSR 级 — 红橙，呼吸脉冲，彩虹薄膜
───────────────────────────────────────── */
.card-ssr {
  border-color: #ff4500;
  background: #150800;
  animation: pulse-ssr 2.5s ease-in-out infinite;
}
@keyframes pulse-ssr {
  0%, 100% { box-shadow: 0 0 8px #ff450066, 0 0 16px #ff450033; }
  50%      { box-shadow: 0 0 20px #ff4500cc, 0 0 40px #ff450066; }
}
.card-ssr:hover {
  transform: translateY(-4px) scale(1.02);
}

/* 彩虹渐变薄膜 */
.ssr-rainbow-film {
  position: absolute;
  inset: 0;
  z-index: 12;
  pointer-events: none;
  background: linear-gradient(
    135deg,
    rgba(255,0,0,0.18),
    rgba(255,165,0,0.15),
    rgba(255,255,0,0.12),
    rgba(0,255,0,0.1),
    rgba(0,128,255,0.15),
    rgba(128,0,255,0.18)
  );
  mix-blend-mode: screen;
  opacity: 0.3;
  border-radius: 2px;
}

/* ─────────────────────────────────────────
   UR 级 — 紫色全息，粒子扩散，conic渐变边框
───────────────────────────────────────── */
.card-ur {
  border-color: #9b30ff;
  background: #0d0414;
  position: relative;
  animation: hue-shift-ur 4s linear infinite;
}
@keyframes hue-shift-ur {
  0%   { filter: hue-rotate(0deg); }
  100% { filter: hue-rotate(360deg); }
}

/* 动态 conic-gradient 边框环 */
.ur-border-ring {
  position: absolute;
  inset: -2px;
  z-index: 0;
  border-radius: 4px;
  background: conic-gradient(
    from var(--angle, 0deg),
    #9b30ff,
    #ff4500,
    #4080ff,
    #ffa500,
    #9b30ff
  );
  animation: conic-spin 3s linear infinite;
  pointer-events: none;
}
.ur-border-ring::after {
  content: '';
  position: absolute;
  inset: 2px;
  background: #0d0414;
  border-radius: 3px;
}
@property --angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}
@keyframes conic-spin {
  to { --angle: 360deg; }
}

/* 悬停粒子扩散（box-shadow animate） */
.card-ur:hover {
  transform: translateY(-4px);
  animation: hue-shift-ur 4s linear infinite, particle-burst 0.6s ease-out forwards;
}
@keyframes particle-burst {
  0%   { box-shadow: 0 0 0 0 #9b30ff88, 0 0 0 0 #4080ff66; }
  40%  { box-shadow: 0 0 0 8px #9b30ff44, 0 0 0 4px #4080ff33; }
  80%  { box-shadow: 0 0 0 16px #9b30ff22, 0 0 0 10px #4080ff11; }
  100% { box-shadow: 0 0 0 24px transparent, 0 0 0 18px transparent; }
}

/* ─────────────────────────────────────────
   未解锁
───────────────────────────────────────── */
.filter-silhouette {
  filter: brightness(0);
  opacity: 0.35;
  backdrop-filter: blur(1px);
}
.locked-overlay {
  backdrop-filter: blur(1px);
}
.locked-question {
  font-size: 1.4rem;
  color: #4b5563;
  letter-spacing: 0.2em;
  text-shadow: 0 0 8px #4b556388;
}

/* ─────────────────────────────────────────
   稀有度徽章
───────────────────────────────────────── */
.rarity-badge {
  font-family: 'Orbitron', monospace, sans-serif;
  font-size: 0.6rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  padding: 1px 5px;
  border-radius: 2px;
  border: 1px solid currentColor;
}
.badge-n   { color: #9ca3af; border-color: #4b5563; background: #1f2937; }
.badge-r   { color: #4080ff; border-color: #4080ff88; background: #0a1a3a; }
.badge-sr  { color: #ffa500; border-color: #ffa50088; background: #2a1a00; }
.badge-ssr {
  color: #fff;
  border-color: #ff450088;
  background: linear-gradient(90deg, #ff4500cc, #ff8c00cc);
  text-shadow: 0 0 6px #ff4500;
}
.badge-ur  {
  color: #e0aaff;
  border-color: #9b30ff88;
  background: linear-gradient(90deg, #2d0052, #0d0022);
  text-shadow: 0 0 8px #9b30ffaa;
}

/* ─────────────────────────────────────────
   等级 Orbitron
───────────────────────────────────────── */
.level-text {
  font-family: 'Orbitron', monospace, sans-serif;
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  color: #f0c040;
  text-shadow: 0 0 6px #f0c04066;
}

/* 编号字体 */
.card-number {
  font-family: 'Orbitron', monospace, sans-serif;
  font-size: 0.55rem;
  color: #4b5563;
  letter-spacing: 0.1em;
}
</style>
