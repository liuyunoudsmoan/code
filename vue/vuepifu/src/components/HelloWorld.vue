<template>
  <div class="greetings" id="element">
      <button @click="onclick">点我啊</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name:'greetings',
    methods:{
        onclick:function (){
            axios.post('http://127.0.0.1:8000/pifuvueweb/demo/').then(response =>{
                console.log('123');
            }).catch(error =>{
                console.log(error);
            })
        }
    }
}

</script>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
