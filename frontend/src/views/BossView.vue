<template>
  <div class="space-y-6">
    <!-- 标题 -->
    <div>
      <h1 class="text-2xl font-bold text-white">⚔️ Boss 挑战</h1>
      <p class="text-gray-400 mt-1 text-sm">击败强大的 Boss，获取丰厚奖励和稀有精灵</p>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="py-16 text-center">
      <div class="w-10 h-10 border-2 border-ssr border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-gray-400">加载 Boss 数据...</p>
    </div>

    <!-- 错误 -->
    <div v-else-if="error" class="game-card border-red-500/30 text-center py-12">
      <p class="text-red-400 mb-3">⚠️ {{ error }}</p>
      <button @click="loadBosses" class="game-btn">重试</button>
    </div>

    <!-- Boss 网格 -->
    <div v-else>
      <div v-if="bosses.length === 0" class="py-16 text-center">
        <span class="text-5xl block mb-3">👾</span>
        <p class="text-gray-400">暂无可挑战的 Boss</p>
      </div>

      <!-- 分区显示 -->
      <template v-else>
        <!-- 可挑战 -->
        <div v-if="availableBosses.length > 0" class="mb-8">
          <h2 class="section-title text-ssr">
            <span class="w-2 h-5 bg-ssr rounded inline-block"></span>
            可挑战 ({{ availableBosses.length }})
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <BossCard
              v-for="boss in availableBosses"
              :key="boss.id"
              :boss="boss"
              @challenge="handleChallenge"
            />
          </div>
        </div>

        <!-- 已击败 -->
        <div v-if="defeatedBosses.length > 0" class="mb-8">
          <h2 class="section-title text-green-400">
            <span class="w-2 h-5 bg-green-500 rounded inline-block"></span>
            已击败 ({{ defeatedBosses.length }})
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <BossCard
              v-for="boss in defeatedBosses"
              :key="boss.id"
              :boss="boss"
              @challenge="handleChallenge"
            />
          </div>
        </div>

        <!-- 未解锁 -->
        <div v-if="lockedBosses.length > 0">
          <h2 class="section-title text-gray-500">
            <span class="w-2 h-5 bg-gray-600 rounded inline-block"></span>
            未解锁 ({{ lockedBosses.length }})
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <BossCard
              v-for="boss in lockedBosses"
              :key="boss.id"
              :boss="boss"
              @challenge="handleChallenge"
            />
          </div>
        </div>
      </template>
    </div>

    <!-- 挑战结果弹窗 -->
    <Teleport to="body">
      <transition name="fade">
        <div
          v-if="challengeResult"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
          @click.self="challengeResult = null"
        >
          <div class="bg-space-800 border rounded-2xl p-8 w-full max-w-sm text-center shadow-2xl"
            :class="challengeResult.victory ? 'border-accent shadow-glow-accent' : 'border-red-500/50'"
          >
            <div class="text-6xl mb-4">{{ challengeResult.victory ? '🏆' : '💀' }}</div>
            <h3 class="text-2xl font-bold mb-2" :class="challengeResult.victory ? 'text-accent' : 'text-red-400'">
              {{ challengeResult.victory ? '挑战成功！' : '挑战失败' }}
            </h3>
            <p class="text-gray-300 mb-4">{{ challengeResult.message }}</p>
            <div v-if="challengeResult.victory && challengeResult.rewards" class="bg-space-700 rounded-xl p-4 mb-4 space-y-2">
              <p class="text-gray-400 text-sm font-bold mb-2">获得奖励</p>
              <div class="flex justify-center gap-6">
                <div class="text-center">
                  <p class="text-accent font-bold text-lg">+{{ challengeResult.rewards.exp }}</p>
                  <p class="text-gray-500 text-xs">经验值</p>
                </div>
                <div class="text-center">
                  <p class="text-yellow-400 font-bold text-lg">+{{ challengeResult.rewards.coins }}</p>
                  <p class="text-gray-500 text-xs">金币</p>
                </div>
              </div>
              <div v-if="challengeResult.rewards.elf_unlocked" class="mt-2 text-ur font-bold">
                🐾 解锁了新精灵！
              </div>
            </div>
            <button @click="challengeResult = null" class="game-btn-primary px-8">确认</button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getBossList, challengeBoss } from '@/api/boss'
import BossCard from '@/components/boss/BossCard.vue'

const bosses = ref([])
const loading = ref(false)
const error = ref(null)
const challengeResult = ref(null)

const availableBosses = computed(() => bosses.value.filter(b => b.unlocked && !b.defeated))
const defeatedBosses = computed(() => bosses.value.filter(b => b.defeated))
const lockedBosses = computed(() => bosses.value.filter(b => !b.unlocked))

async function loadBosses() {
  loading.value = true
  error.value = null
  try {
    const response = await getBossList()
    bosses.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || '加载 Boss 列表失败'
  } finally {
    loading.value = false
  }
}

async function handleChallenge(boss) {
  try {
    const response = await challengeBoss(boss.id)
    challengeResult.value = response.data
    // 更新Boss状态
    if (response.data.victory) {
      const idx = bosses.value.findIndex(b => b.id === boss.id)
      if (idx !== -1) {
        bosses.value[idx] = { ...bosses.value[idx], defeated: true }
      }
    }
  } catch (err) {
    challengeResult.value = {
      victory: false,
      message: err.response?.data?.detail || '挑战失败，请稍后重试'
    }
  }
}

onMounted(() => {
  loadBosses()
})
</script>
