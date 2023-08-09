<template>
    <!--    <div><p @click="uploadimg">上传啊</p></div>-->
    <div class="generatebox">
        <div class="showimgbox">
            <div class="uploadbox">
                <el-button type="primary" @click="executeScript">生成</el-button>
                <div v-if="isLoading">加载中...</div>
            </div>
        </div>
    </div>
    <div ref="sceneCanvas" class="sceneCanvas">
        <p>展示3D模型</p>
    </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import {ref, reactive} from 'vue';
import {OBJLoader} from "@/assets/three/loaders/OBJLoader.mjs";
import {OrbitControls} from "@/assets/three/controls/OrbitControls.mjs";


const isLoading = ref(false);
const result = ref('');
const data = reactive({});
const executeScript = async () => {
    isLoading.value = true;
    try {
        const response = await axios.post('http://127.0.0.1:8000/pifuvueweb/generate');
        result.value = response.data.result;
    } catch (error) {
        // 处理错误
    } finally {
        isLoading.value = false;
        console.log('123')
    }
    addmodel();
};
const file = ref(null);
// 加载3D模型
const sceneCanvas = ref(null);
const addmodel=() => {
    const canvasWidth = sceneCanvas.value.clientWidth*1.2;
    const canvasHeight = sceneCanvas.value.clientHeight;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvasWidth / canvasHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(canvasWidth, canvasHeight);
    sceneCanvas.value.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement)
    const objloader = new OBJLoader()
    objloader.load('http://127.0.0.1:8000/img/results/results/result_0_0_00.obj', (obj) => {
        const scale = 20
        obj.scale.set(scale, scale, scale)
        obj.position.set(0,-15,-10)
        scene.add(obj);
    });
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1);
    scene.add(ambientLight);
    scene.add(directionalLight);
    const bgloader = new THREE.TextureLoader();
    const texture = bgloader.load('http://127.0.0.1:8000/img/background/park.webp',() =>{
        const rt = new THREE.WebGLCubeRenderTarget(texture.image.height)
        // texture.repeat.set(100,100);
        rt.fromEquirectangularTexture(renderer, texture)
        scene.background = rt.texture
    })
    camera.position.z = 50;
    camera.aspect = canvasWidth / canvasHeight;
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.rotateSpeed = 0.5
    const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene,camera);
    }
    animate();
}

</script>

<style scoped>

</style>