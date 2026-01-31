import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录 - TeaMAKE' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册 - TeaMAKE' }
  },
  {
    path: '/profile/:id',
    name: 'Profile',
    component: Profile,
    meta: { title: '个人主页 - TeaMAKE' }
  },
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 更新页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'TeaMAKE'
  next()
})

export default router
