import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CustomerList from '../views/CustomerList.vue'
import CustomerForm from '../views/CustomerForm.vue'
import ContractList from '../views/ContractList.vue'
import ContractForm from '../views/ContractForm.vue'
import QuoteForm from '../views/QuoteForm.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import AIAnalyticsView from '../views/AIAnalyticsView.vue'
import CalendarView from '../views/CalendarView.vue'
import PaymentView from '../views/PaymentView.vue'
import FeedbackView from '../views/FeedbackView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { public: true }
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/customers',
      name: 'customers',
      component: CustomerList
    },
    {
      path: '/customers/new',
      name: 'new-customer',
      component: CustomerForm
    },
    {
      path: '/customers/:id/edit',
      name: 'edit-customer',
      component: CustomerForm
    },
    {
      path: '/contracts',
      name: 'contracts',
      component: ContractList
    },
    {
      path: '/quotes/new',
      name: 'new-quote',
      component: QuoteForm
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView
    },
    {
      path: '/ai-analytics',
      name: 'ai-analytics',
      component: AIAnalyticsView
    },
    {
      path: '/contracts/new',
      name: 'new-contract',
      component: ContractForm
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: CalendarView
    },
    {
      path: '/payments',
      name: 'payments',
      component: PaymentView
    },
    {
      path: '/feedbacks',
      name: 'feedbacks',
      component: FeedbackView
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isPublicRoute = to.meta.public
  const hasToken = localStorage.getItem('token') || sessionStorage.getItem('token')

  // If route requires auth and no token is present
  if (!isPublicRoute && !hasToken) {
    ElMessage.warning('Please sign in to continue')
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  next()
})

export default router
