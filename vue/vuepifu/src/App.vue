<template>
    <div>
    <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
        <el-radio-button :label="false">expand</el-radio-button>
        <el-radio-button :label="true">collapse</el-radio-button>
    </el-radio-group>
    </div>
    <div class="showpage">
    <el-menu
        ref="menu"
        :default-active="activeIndex"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        @open="handleOpen"
        @close="handleClose"
    >
        <el-menu-item index="" @click="changeSidebar('home')">
            <el-icon><location /></el-icon>
            <template #title>Home</template>
        </el-menu-item>
        <el-menu-item index="generate" @click="changeSidebar('generate')">
            <el-icon><icon-menu /></el-icon>
            <template #title>Template</template>
        </el-menu-item>
        <el-menu-item index="3">
            <el-icon><document /></el-icon>
            <template #title>Navigator Three</template>
        </el-menu-item>
        <el-menu-item index="4">
            <el-icon><setting /></el-icon>
            <template #title>Navigator Four</template>
        </el-menu-item>
    </el-menu>

        <div class="navshow"><router-view></router-view></div>
    </div>
</template>



<script lang="ts" setup>
import * as Three from './assets/three/three.js'
import { ref,defineComponent } from 'vue'
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
} from '@element-plus/icons-vue'

const isCollapse = ref(true)
const activeIndex = ref('home')
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}

const menu = ref<HTMLElement | null>(null)
const changeSidebar = (index:string) =>{
    activeIndex.value = index
    console.log(index)
    router.push({ name : index})
}
import  router from './router'
defineComponent({
    name: 'menu',
    data(){
        return {
            activeIndex:'home'
        }
    },
    methods:{

    },
    components:{}
})

</script>



<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}
</style>
