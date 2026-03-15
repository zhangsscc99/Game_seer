import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/TasksView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'elves',
        name: 'Elves',
        component: () => import('@/views/ElvesView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'elves/:id',
        name: 'ElfDetail',
        component: () => import('@/views/ElfDetailView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'my-elves',
        name: 'MyElves',
        component: () => import('@/views/MyElvesView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'boss',
        name: 'Boss',
        component: () => import('@/views/BossView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'achievements',
        name: 'Achievements',
        component: () => import('@/views/AchievementsView.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/ProfileView.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if ((to.name === 'Login' || to.name === 'Register') && token) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
