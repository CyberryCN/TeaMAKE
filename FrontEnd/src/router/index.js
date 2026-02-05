import { createRouter, createWebHistory } from 'vue-router'
import Welcome from '../views/Welcome.vue'
import Square from '../views/Square.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import CreateRecruitment from '../views/CreateRecruitment.vue'
import RecruitmentDetail from '../views/RecruitmentDetail.vue'
import Messages from '../views/Messages.vue'
import Teams from '../views/Teams.vue'
import { tokenManager } from '../api'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome,
    meta: { title: 'TeaMAKE - 大学生竞赛组队平台' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录 - TeaMAKE', guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册 - TeaMAKE', guest: true }
  },
  {
    path: '/square',
    name: 'Square',
    component: Square,
    meta: { title: '广场 - TeaMAKE', requiresAuth: true }
  },
  {
    path: '/profile/:id',
    name: 'Profile',
    component: Profile,
    meta: { title: '个人主页 - TeaMAKE', requiresAuth: true }
  },
  {
    path: '/create',
    name: 'CreateRecruitment',
    component: CreateRecruitment,
    meta: { title: '发布招募 - TeaMAKE', requiresAuth: true }
  },
  {
    path: '/recruitment/:id',
    name: 'RecruitmentDetail',
    component: RecruitmentDetail,
    meta: { title: '招募详情 - TeaMAKE', requiresAuth: true }
  },
  {
    path: '/recruitment/:id/edit',
    name: 'EditRecruitment',
    component: CreateRecruitment,
    meta: { title: '编辑招募 - TeaMAKE', requiresAuth: true }
  },
  {
    path: '/messages',
    name: 'Messages',
    component: Messages,
    meta: { title: '消息中心 - TeaMAKE', requiresAuth: true }
  },
  {
    path: '/teams',
    name: 'Teams',
    component: Teams,
    meta: { title: '我的队伍 - TeaMAKE', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'TeaMAKE'

  const isLoggedIn = tokenManager.isLoggedIn()

  // 需要登录才能访问
  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // 游客才能访问（如登录页、注册页）
  if (to.meta.guest && isLoggedIn) {
    next({ name: 'Square' })
    return
  }

  next()
})

export default router
