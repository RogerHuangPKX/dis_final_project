import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/customers',
      name: 'customers',
      component: () => import('../views/CustomerList.vue')
    },
    {
      path: '/quotes',
      name: 'quotes',
      component: () => import('../views/QuoteForm.vue')
    },
    {
      path: '/contracts',
      name: 'contracts',
      component: () => import('../views/ContractList.vue')
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue')
    }
  ]
})

export default router
