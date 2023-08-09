import { createRouter, createWebHashHistory } from 'vue-router'
import Generate from '@/components/Generate.vue'
import Home from '@/components/Home.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/generate',
        name: 'generate',
        component: Generate
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
