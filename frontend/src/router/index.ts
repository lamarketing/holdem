import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import Menu from "@/views/Menu.vue";
import Home from "@/views/Home.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/holdem/home'
  },
  {
    path: '/holdem',
    component: Menu,
    children: [
      {
        path: 'home',
        name: 'home',
        component: Home
      },
      {
        path: 'tournament',
        name: 'tournament',
        component: () => import('@/views/Tournament.vue')
      },
      {
        path: 'tournament/play',
        name: 'play',
        component: () => import('@/views/Play.vue')
      },
      {
        path: 'watch',
        component: () => import('@/views/Watch.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
