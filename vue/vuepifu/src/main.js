import './assets/main.css'
import router from './router'
import { createApp } from 'vue'
import Elementplus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import { createRouter,createWebHistory,RouterView } from 'vue-router'
import Scene from './assets/Scene.js'


// const canvasEl = document.getElementById('sceneCanvas')
// new Scene(canvasEl)


import axios from "axios";
// Vue.use(axios);


createApp(App).use(Elementplus).use(router).component('router-view', RouterView).mount('#app')
// menu.use(changeSidebar).mount('#menu')