<template>
  <div class="login-root min-h-screen bg-space-900 overflow-hidden lg:grid lg:grid-cols-2">

    <!-- ══════════════════════════════════════
         左侧：深空传送门（lg 以上显示）
    ═══════════════════════════════════════ -->
    <div class="left-panel hidden lg:flex items-center justify-center relative overflow-hidden">
      <!-- 深空星域背景 -->
      <div class="starfield starfield-far"></div>
      <div class="starfield starfield-mid"></div>
      <div class="starfield starfield-near"></div>

      <!-- 大型能量环/传送门 -->
      <div class="portal-wrap relative flex items-center justify-center">
        <!-- 同心旋转圆环 -->
        <div class="ring ring-1"></div>
        <div class="ring ring-2"></div>
        <div class="ring ring-3"></div>
        <div class="ring ring-4"></div>
        <!-- 中心光晕 -->
        <div class="portal-core"></div>

        <!-- 文字 -->
        <div class="portal-text absolute flex flex-col items-center z-10">
          <span class="game-title">GAME SEER</span>
          <span class="game-subtitle">星际指挥官系统</span>
          <div class="title-line"></div>
          <span class="game-version">v2.0.0 · COMMANDER ACCESS</span>
        </div>
      </div>

      <!-- 浮动精灵光点 -->
      <div class="float-orb orb-1"></div>
      <div class="float-orb orb-2"></div>
      <div class="float-orb orb-3"></div>
      <div class="float-orb orb-4"></div>
      <div class="float-orb orb-5"></div>
    </div>

    <!-- ══════════════════════════════════════
         右侧：登录表单
    ═══════════════════════════════════════ -->
    <div class="right-panel flex flex-col items-center justify-center min-h-screen bg-space-800 px-8 relative overflow-hidden">
      <!-- 右侧背景纹理扫描线 -->
      <div class="scan-lines-bg"></div>

      <!-- 表单容器 -->
      <div
        class="form-container relative w-full max-w-md z-10"
        :class="{ 'form-enter': formVisible }"
      >
        <!-- 标题 -->
        <div class="form-item mb-8" :class="{ 'item-visible': formVisible }" style="--delay:0ms">
          <p class="hud-label mb-1">SYSTEM ACCESS PORTAL</p>
          <h1 class="commander-title">COMMANDER<br>LOGIN</h1>
          <div class="title-underline mt-3"></div>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6" autocomplete="off">

          <!-- 邮箱 -->
          <div class="form-item" :class="{ 'item-visible': formVisible }" style="--delay:80ms">
            <div class="field-wrap" :class="{ 'field-error': errors.email, 'field-focused': focused.email }">
              <label class="float-label" :class="{ 'label-up': focused.email || form.email }">
                指挥官邮箱
              </label>
              <input
                v-model="form.email"
                type="email"
                class="hud-input"
                autocomplete="email"
                @focus="focused.email = true"
                @blur="focused.email = false"
              />
              <div class="field-border-glow"></div>
            </div>
            <div v-if="errors.email" class="sys-alert mt-1">
              <span class="alert-prefix">[ ERROR ]</span> {{ errors.email }}
            </div>
          </div>

          <!-- 密码 -->
          <div class="form-item" :class="{ 'item-visible': formVisible }" style="--delay:160ms">
            <div class="field-wrap" :class="{ 'field-error': errors.password, 'field-focused': focused.password }">
              <label class="float-label" :class="{ 'label-up': focused.password || form.password }">
                作战密码
              </label>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="hud-input pr-10"
                autocomplete="current-password"
                @focus="focused.password = true"
                @blur="focused.password = false"
              />
              <button
                type="button"
                class="pwd-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
              >
                <svg v-if="showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21"/>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </button>
              <div class="field-border-glow"></div>
            </div>
            <div v-if="errors.password" class="sys-alert mt-1">
              <span class="alert-prefix">[ ERROR ]</span> {{ errors.password }}
            </div>
          </div>

          <!-- 系统错误警报 -->
          <div
            v-if="loginError"
            class="form-item sys-alert-block"
            :class="{ 'item-visible': formVisible }"
            style="--delay:200ms"
          >
            <span class="alert-prefix alert-blink">[ SYSTEM ALERT ]</span>
            <span class="ml-2">{{ loginError }}</span>
          </div>

          <!-- 登录按钮 -->
          <div class="form-item" :class="{ 'item-visible': formVisible }" style="--delay:240ms">
            <button
              type="submit"
              :disabled="loading"
              class="hud-btn w-full relative overflow-hidden"
            >
              <span class="btn-scan-line"></span>
              <span class="relative z-10 flex items-center justify-center gap-2 font-black tracking-widest">
                <span v-if="loading" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                {{ loading ? 'AUTHENTICATING...' : 'ENTER COMMAND CENTER' }}
              </span>
            </button>
          </div>
        </form>

        <!-- 分隔线 -->
        <div class="form-item flex items-center gap-3 my-6" :class="{ 'item-visible': formVisible }" style="--delay:300ms">
          <div class="flex-1 h-px bg-space-500"></div>
          <span class="text-space-500 text-xs font-mono tracking-widest">OR</span>
          <div class="flex-1 h-px bg-space-500"></div>
        </div>

        <!-- 注册链接 -->
        <div class="form-item text-center" :class="{ 'item-visible': formVisible }" style="--delay:360ms">
          <p class="text-gray-600 text-sm font-mono">
            NO CREDENTIALS?
            <router-link
              to="/register"
              class="register-link ml-2"
            >
              REGISTER COMMANDER
            </router-link>
          </p>
        </div>

        <!-- 版本信息 -->
        <div class="form-item mt-8 text-center" :class="{ 'item-visible': formVisible }" style="--delay:420ms">
          <p class="text-space-600 text-xs font-mono tracking-widest">
            GAME SEER © 2024 &nbsp;·&nbsp; BUILD 2.0.0 &nbsp;·&nbsp; 游戏化任务系统
          </p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const loginError = ref('')
const showPassword = ref(false)
const formVisible = ref(false)

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const focused = reactive({
  email: false,
  password: false
})

onMounted(() => {
  // 入场动画：延迟触发
  requestAnimationFrame(() => {
    setTimeout(() => { formVisible.value = true }, 60)
  })
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

<style scoped>
/* ─────────────────────────────────────────
   根容器
───────────────────────────────────────── */
.login-root {
  font-family: 'Orbitron', monospace, sans-serif;
}

/* ─────────────────────────────────────────
   左侧：星域
───────────────────────────────────────── */
.left-panel {
  background: radial-gradient(ellipse at 30% 20%, #0a0f2e 0%, #020510 60%, #000 100%);
}

/* 多层星星背景（远/中/近） */
.starfield {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.starfield-far {
  background-image:
    radial-gradient(1px 1px at 10% 12%, #ffffff55 0%, transparent 100%),
    radial-gradient(1px 1px at 20% 45%, #ffffff44 0%, transparent 100%),
    radial-gradient(1px 1px at 35% 80%, #ffffff33 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 18%, #ffffff44 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 60%, #ffffff33 0%, transparent 100%),
    radial-gradient(1px 1px at 82% 30%, #ffffff55 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 75%, #ffffff44 0%, transparent 100%),
    radial-gradient(1px 1px at 15% 65%, #ffffff33 0%, transparent 100%),
    radial-gradient(1px 1px at 45% 40%, #ffffff44 0%, transparent 100%),
    radial-gradient(1px 1px at 62% 88%, #ffffff33 0%, transparent 100%),
    radial-gradient(1px 1px at 78% 5%,  #ffffff44 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 90%, #ffffff33 0%, transparent 100%),
    radial-gradient(1px 1px at 50% 55%, #ffffff22 0%, transparent 100%),
    radial-gradient(1px 1px at 88% 48%, #ffffff33 0%, transparent 100%),
    radial-gradient(1px 1px at 5%  50%, #ffffff44 0%, transparent 100%);
  animation: twinkle-far 8s ease-in-out infinite alternate;
}
.starfield-mid {
  background-image:
    radial-gradient(1.5px 1.5px at 8%  30%, #aaddff66 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 28% 70%, #aaddff44 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 48% 15%, #aaddff55 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 65% 50%, #aaddff44 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 80% 85%, #aaddff55 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 92% 20%, #aaddff44 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 38% 92%, #aaddff33 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 72% 35%, #aaddff55 0%, transparent 100%);
  animation: twinkle-mid 5s ease-in-out infinite alternate;
}
.starfield-near {
  background-image:
    radial-gradient(2px 2px at 18% 22%, #ffffff88 0%, transparent 100%),
    radial-gradient(2px 2px at 42% 60%, #ffffff77 0%, transparent 100%),
    radial-gradient(2px 2px at 68% 10%, #ffffff88 0%, transparent 100%),
    radial-gradient(2px 2px at 85% 70%, #ffffff77 0%, transparent 100%),
    radial-gradient(2px 2px at 3%  85%, #ffffff66 0%, transparent 100%);
  animation: twinkle-near 3s ease-in-out infinite alternate;
}
@keyframes twinkle-far  { from { opacity: 0.6; } to { opacity: 1; } }
@keyframes twinkle-mid  { from { opacity: 0.5; } to { opacity: 0.9; } }
@keyframes twinkle-near { from { opacity: 0.7; } to { opacity: 1; } }

/* ─────────────────────────────────────────
   传送门
───────────────────────────────────────── */
.portal-wrap {
  width: 380px;
  height: 380px;
}

.ring {
  position: absolute;
  border-radius: 50%;
  border-style: solid;
}
.ring-1 {
  width: 340px; height: 340px;
  border-width: 2px;
  border-color: #4080ff44 #4080ffcc #4080ff44 transparent;
  animation: spin-cw 8s linear infinite;
}
.ring-2 {
  width: 280px; height: 280px;
  border-width: 2px;
  border-color: transparent #ffa500cc transparent #ffa50044;
  animation: spin-ccw 6s linear infinite;
}
.ring-3 {
  width: 220px; height: 220px;
  border-width: 1.5px;
  border-color: #9b30ff88 transparent #9b30ff88 transparent;
  animation: spin-cw 10s linear infinite;
}
.ring-4 {
  width: 160px; height: 160px;
  border-width: 1.5px;
  border-color: transparent #ff450088 transparent #ff450066;
  animation: spin-ccw 4s linear infinite;
}
@keyframes spin-cw  { to { transform: rotate(360deg);  } }
@keyframes spin-ccw { to { transform: rotate(-360deg); } }

/* 中心光晕 */
.portal-core {
  width: 80px; height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, #4080ff22 0%, #9b30ff11 50%, transparent 100%);
  box-shadow:
    0 0 20px #4080ff44,
    0 0 60px #9b30ff22,
    inset 0 0 20px #4080ff22;
  animation: core-pulse 2.5s ease-in-out infinite;
  position: absolute;
}
@keyframes core-pulse {
  0%, 100% { box-shadow: 0 0 20px #4080ff44, 0 0 60px #9b30ff22; }
  50%       { box-shadow: 0 0 40px #4080ffaa, 0 0 100px #9b30ff44; }
}

/* 传送门文字 */
.portal-text {
  text-align: center;
}
.game-title {
  font-family: 'Orbitron', monospace;
  font-size: 2.2rem;
  font-weight: 900;
  letter-spacing: 0.25em;
  color: #f0c040;
  text-shadow: 0 0 20px #f0c040aa, 0 0 40px #f0c04055;
  animation: title-glow 3s ease-in-out infinite alternate;
}
@keyframes title-glow {
  from { text-shadow: 0 0 10px #f0c04088, 0 0 30px #f0c04033; }
  to   { text-shadow: 0 0 25px #f0c040cc, 0 0 60px #f0c04066; }
}
.game-subtitle {
  font-family: 'Orbitron', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.3em;
  color: #4080ff;
  opacity: 0.8;
  margin-top: 4px;
}
.title-line {
  width: 120px; height: 1px;
  background: linear-gradient(90deg, transparent, #f0c040, transparent);
  margin: 8px auto;
}
.game-version {
  font-size: 0.55rem;
  letter-spacing: 0.2em;
  color: #4b5563;
}

/* 浮动光点（精灵剪影模拟） */
.float-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(8px);
  animation: orb-float linear infinite;
  pointer-events: none;
}
.orb-1 { width:16px; height:16px; background:#4080ff44; top:15%; left:12%; animation-duration:7s; animation-delay:0s; }
.orb-2 { width:10px; height:10px; background:#9b30ff44; top:65%; left:8%;  animation-duration:9s; animation-delay:2s; }
.orb-3 { width:20px; height:20px; background:#ffa50033; top:30%; right:10%; animation-duration:11s; animation-delay:1s; }
.orb-4 { width:12px; height:12px; background:#4080ff33; top:78%; right:15%; animation-duration:8s; animation-delay:3s; }
.orb-5 { width:8px;  height:8px;  background:#ff450033; top:50%; left:5%;  animation-duration:6s; animation-delay:0.5s; }
@keyframes orb-float {
  0%   { transform: translateY(0px) scale(1);   opacity: 0.4; }
  50%  { transform: translateY(-20px) scale(1.2); opacity: 0.8; }
  100% { transform: translateY(0px) scale(1);   opacity: 0.4; }
}

/* ─────────────────────────────────────────
   右侧：扫描线背景
───────────────────────────────────────── */
.scan-lines-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.015) 2px,
    rgba(255,255,255,0.015) 4px
  );
  z-index: 1;
}

/* ─────────────────────────────────────────
   表单入场动画
───────────────────────────────────────── */
.form-container {
  opacity: 1;
  transform: translateX(0);
}
.form-item {
  opacity: 0;
  transform: translateX(30px);
  transition: opacity 0.5s ease, transform 0.5s ease;
  transition-delay: var(--delay, 0ms);
}
.form-item.item-visible {
  opacity: 1;
  transform: translateX(0);
}

/* ─────────────────────────────────────────
   标题
───────────────────────────────────────── */
.hud-label {
  font-size: 0.6rem;
  letter-spacing: 0.35em;
  color: #4080ff;
  font-weight: 700;
}
.commander-title {
  font-family: 'Orbitron', monospace;
  font-size: 2.4rem;
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: 0.05em;
  color: #f0c040;
  text-shadow: 0 0 20px #f0c04066;
}
.title-underline {
  height: 2px;
  background: linear-gradient(90deg, #f0c040, #4080ff, transparent);
  width: 100%;
}

/* ─────────────────────────────────────────
   输入框（浮动 label）
───────────────────────────────────────── */
.field-wrap {
  position: relative;
  margin-top: 0.5rem;
  border-radius: 2px;
}

.float-label {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-family: 'Orbitron', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  color: #6b7280;
  pointer-events: none;
  transition: all 0.2s ease;
  z-index: 2;
  background: transparent;
}
.float-label.label-up {
  top: -10px;
  transform: translateY(0);
  font-size: 0.6rem;
  color: #4080ff;
  background: #1e2535;
  padding: 0 4px;
  letter-spacing: 0.15em;
}

.hud-input {
  width: 100%;
  padding: 14px 12px 10px;
  background: #0d1117;
  border: 1px solid #2a3040;
  border-radius: 2px;
  color: #e5e7eb;
  font-family: 'Orbitron', monospace;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  caret-color: #f0c040;
}
.hud-input:focus {
  border-color: #f0c04088;
  box-shadow: 0 0 0 2px #f0c04022, 0 0 12px #f0c04033;
}

/* 边框发光层（聚焦时亮起） */
.field-border-glow {
  position: absolute;
  inset: 0;
  border-radius: 2px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
  box-shadow: 0 0 0 1px #f0c04055, 0 0 16px #f0c04033;
}
.field-focused .field-border-glow {
  opacity: 1;
}

/* 错误状态 */
.field-error .hud-input {
  border-color: #ff4444;
  box-shadow: 0 0 8px #ff444433;
  animation: error-blink 0.8s ease-in-out 2;
}
@keyframes error-blink {
  0%, 100% { border-color: #ff4444; }
  50%       { border-color: #ff888888; }
}

/* 密码显示切换 */
.pwd-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #4b5563;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
  z-index: 3;
}
.pwd-toggle:hover { color: #f0c040; }

/* ─────────────────────────────────────────
   系统警报提示
───────────────────────────────────────── */
.sys-alert {
  font-family: 'Orbitron', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.05em;
  color: #ff6666;
}
.sys-alert-block {
  border: 1px solid #ff4444;
  padding: 10px 14px;
  background: #1a0808;
  border-radius: 2px;
  font-family: 'Orbitron', monospace;
  font-size: 0.7rem;
  color: #ff8888;
  animation: alert-border-blink 1.2s ease-in-out infinite;
}
@keyframes alert-border-blink {
  0%, 100% { border-color: #ff4444; box-shadow: 0 0 6px #ff444444; }
  50%       { border-color: #ff0000; box-shadow: 0 0 12px #ff000066; }
}
.alert-prefix {
  color: #ff4444;
  font-weight: 900;
  letter-spacing: 0.08em;
}
.alert-blink {
  animation: prefix-blink 0.8s step-start infinite;
}
@keyframes prefix-blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* ─────────────────────────────────────────
   登录按钮
───────────────────────────────────────── */
.hud-btn {
  padding: 14px 20px;
  background: #0d0d0d;
  border: 2px solid #f0c040;
  border-radius: 2px;
  color: #f0c040;
  font-family: 'Orbitron', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  cursor: pointer;
  transition: background 0.25s, color 0.25s, box-shadow 0.25s;
  overflow: hidden;
}
.hud-btn:hover:not(:disabled) {
  background: #f0c040;
  color: #000;
  box-shadow: 0 0 24px #f0c040aa;
}
.hud-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 扫描线经过按钮动画 */
.btn-scan-line {
  position: absolute;
  inset-x: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f0c040, transparent);
  top: -4px;
  animation: btn-scan 2.5s ease-in-out infinite;
  pointer-events: none;
}
@keyframes btn-scan {
  0%   { top: -4px;   opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 1; }
  100% { top: calc(100% + 4px); opacity: 0; }
}

/* ─────────────────────────────────────────
   注册链接
───────────────────────────────────────── */
.register-link {
  color: #4080ff;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}
.register-link:hover {
  color: #f0c040;
  border-color: #f0c04066;
}
</style>
