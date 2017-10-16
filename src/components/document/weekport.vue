<template>
  <div>
    <el-row style="text-align:center;background:#34c0e3;color:#fff;">
      <h1>{{title}}</h1>
    </el-row>
    <el-row style="background:#F9FAFC;">
      <div style="margin:0px auto;width:66.667%;background:#fff;box-shadow: 0px 0px 10px 5px #D3DCE6;" v-html="ht"></div>
    </el-row>
    <el-row style="text-align:center">
      <el-col :span="12">
        <h2><a v-on:click="prev">上一篇</a></h2>
      </el-col>
      <el-col :span="12">
        <h2>
          <a v-on:click="next">下一篇</a></h2>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import marked from 'marked'
  export default {
    data() {
      return {
        ht: '',
        title: null,
        weekId: null,
        maxcount: null
      }
    },
    mounted() {
      this.$http.get('weekreport').then((response) => {
        this.ht = marked(response.body.data, {
          gfm: true,
          tables: true,
          breaks: false,
          pedantic: false,
          sanitize: false,
          smartLists: true,
          smartypants: false
        })
        this.title = response.body.msg
        this.maxcount = response.body.count
        this.weekId = response.body.count
      })
    },
    methods: {
      next() {
        if (this.weekId==this.maxcount) {
          this.$message({
            showClose: true,
            message: '已经是最近一篇了',
            type: 'warning'
          })

        } else {
          ++this.weekId 
          this.wanttosee()
        }

      },
      prev() {
        if (this.weekId == 1) {
          this.$message({
            showClose: true,
            message: '已经是最后一篇了',
            type: 'warning'
          })
        } else{
          --this.weekId
          this.wanttosee()
        }
      },
      wanttosee() {
        this.$http.get('/weekreport', {
          params: {
            listIndex: this.weekId
          }
        }).then((response) => {
          if (response.body.code == 200) {
            this.ht = marked(response.body.data, {
              sanitize: true
            })
            this.title = response.body.msg
            window.scroll(0, 0)

          } else if (response.body.code == 401) {
            this.weekId = this.weekId + 1
            this.$message({
              showClose: true,
              message: response.body.msg,
              type: 'warning'
            });
          } else if (response.body.code == 402) {
            this.weekId = this.weekId - 1
            this.$message({
              showClose: true,
              message: response.body.msg,
              type: 'warning'
            });
          } else {
            this.$message({
              showClose: true,
              message: response.body.msg,
              type: 'error'
            });
          }

        })
      }
    }
  }

</script>
