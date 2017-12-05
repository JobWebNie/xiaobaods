<style scoped>
  .comment-Chin {
    padding: 0 20px 0 30px;
  }
  .comment-Chin .el-main span{
    display:inline-block;
    width:100px;
  }
</style>
<template>
  <div class="comment-Chin">
    <el-container>
      <el-aside width="200px">
        <h3>{{chinTitle}}</h3>
      </el-aside>
      <el-main>
        <span v-for="option in options">
          <el-select v-model="value">
            <el-option v-for="item in option" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </span>
      </el-main>
    </el-container>
  </div>
</template>
<script>
  export default {
    props: {
      chinTitle: {
        type: String
      }
    },
    data(){
      return {
        options:[[{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }],
        [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }],
        [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }]],
        value: ''
      }
    }
  }

</script>
