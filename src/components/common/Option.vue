<style scoped>
.comment-select{
    position: absolute;
    top: 30px;
    left: 0;
    margin-top: -1px;
    padding-top: 14px;
    padding-bottom: 5px;
    overflow: hidden;
    background-color: rgba(0,0,0,.8);
    border: 1px solid #dbdbdb;
    border-radius: 3px;

}
.comment-select ul {
    float: left;
    border-left: 1px dashed #d5d5d5;
    margin-left: -1px;
    margin-bottom: 15px;
    height: 132px;
}
ol, ul {
    list-style: none;
    padding:0px;
}
li{
    padding:0px 20px 0px 16px;
    color:#fff;
    font-size: 12px;
}
.comment-select a{
    display: block;
    text-decoration:none;
    color: #fff;
    height: 22px;
    line-height: 22px;
    text-indent: 5px;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 102px;
}
</style>
<template>
    <div class="comment-select">
      <ul v-for="productList in productLists">
        <li v-for="product in productList" @click.prevent="selctTitleClick(product)"><a href="">{{product}}</a></li>
      </ul>
    </div>
</template>
<script>
export default {
    props: {
        productLists:{
            type:Array,
            required: true
        }
    },
    data() {
        return {
            
        }
    },
    methods:{
        selctTitleClick(v) {
            this.$emit('selectOption',v)
        }
    }
}
</script>