<template>
  <div class="HomePage">
    <common-header activeIndex="/"></common-header>
  </div>
</template>
<script>
import commonHeader from './common/Header.vue';
  export default {
     components: {
       commonHeader
     },
    name: 'HomePage',
    data() {
      return {
        activeIndex: '/'
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>