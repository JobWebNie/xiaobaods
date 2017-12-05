<style scoped>
  .comment-select {
    float: left;
    border: 1px dotted #999;
    position: relative;
  }
  .comment-select a{
    display:inline-block;
    margin-bottom:3px;
  }
</style>
<template>
  <div class="comment-select" @mouseenter="interToMakeSelectDown" @mouseleave.self="leaveToMakeSelectUp">
    <a href="">{{label}}</a>
    <i :class="iconName"></i>
    <commonOption v-show="show" :productLists="productLists" v-on:selectOption="selctTitleReceive"></commonOption>
  </div>
</template>
<script>
  import commonOption from './Option.vue';
  export default {
    components: {
      commonOption
    },
    props: {
      splitNumber: {
        type: Number,
        default: 6
      },
      productLists:{
        type: Array,
        required: true
      }
    },
    data() {
      return {
        iconName: 'el-icon-arrow-down',
        show: false,
        label: ''
      }
    },
    mounted() {
      this.selctTitleReceive()
    },
    methods: {
      selctTitleReceive(v) {
        this.label = v ? v : this.productLists[0][0]
      },
      interToMakeSelectDown() {
        this.iconName = "el-icon-arrow-up"
        this.show = true
      },
      leaveToMakeSelectUp() {
        this.iconName = "el-icon-arrow-down"
        this.show = false
      }
    }
  }
</script>