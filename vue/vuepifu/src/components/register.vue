<template>
    <div>
        <h2>Register</h2>
        <form @submit.prevent="register">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" v-model="confirmPassword" required>
            <button type="submit">Register</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const username = ref('');
const password = ref('');
const confirmPassword = ref('');

const register = () => {
    // 发送注册请求到后端
    // 使用 axios 或其他 HTTP 库发送请求
    // 处理注册成功或失败的逻辑
};
</script>
