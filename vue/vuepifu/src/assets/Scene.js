import {OBJLoader} from "@/assets/three/loaders/OBJLoader.mjs";
import {OrbitControls} from "@/assets/three/controls/OrbitControls.mjs";
import * as Three from './three/three.js'
export default class Scene{
    canvas
    scene
    camera
    renderer
    constructor(el){
        this.canvas = el
        this.init()
    }
    init(){
        this.setScene()
        this.setCamera()
        this.setRenderer()
        const controls = new OrbitControls(this.camera,this.renderer.domElement)
        controls.addEventListener("change", this.renderer)
        this.animate()
        this.setModel()
        this.setLight()
        // this.setcontrol()
    }
    setScene(){
        this.scene = new THREE.Scene()
        this.scene.background = new THREE.Color(0x00121)
    }
    setCamera(){
        this.camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 5000)
        this.camera.position.z = 5
        this.scene.add(this.camera)
    }
    setRenderer(){
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas
        })
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight)
    }
    animate = () => {
        this.renderer.render(this.scene, this.camera)
        window.requestAnimationFrame(this.animate)
    }
    setModel(){
        const objloader = new OBJLoader()
        objloader.load('../static/results/result_0_0_00.obj', (obj) =>{
            const scale = .01
            obj.scale.set(scale, scale, scale)
            this.scene.add(obj)
        })
    }
    setLight(){
        const spotLight = new THREE.SpotLight()
        spotLight.position.set(-10, 10, 10)
        this.scene.add(spotLight)
    }
}