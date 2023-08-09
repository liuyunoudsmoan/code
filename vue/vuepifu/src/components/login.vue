<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'

const username = ref('');
const password = ref('');

const login = async (username,password) => {
    // 发送登录请求到后端

        const response = await axios.post('http://127.0.0.1:8000/pifuvueweb/login',{
            username: username,
            password: password
        });

    // 使用 axios 或其他 HTTP 库发送请求
    // 处理登录成功或失败的逻辑
};
</script>
