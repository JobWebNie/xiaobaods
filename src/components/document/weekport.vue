<template>
  <div>
    <el-row style="text-align:center;background:#34c0e3;color:#fff;">
      <h1>{{title}}</h1>
    </el-row>
    <el-row style="background:#F9FAFC;" class="markdown-body">
      <div style="margin:0px auto;width:66.667%;background:#fff;box-shadow: 0px 0px 10px 5px #D3DCE6;" v-html="ht"></div>
    </el-row>
    <el-row style="text-align:center">
      <el-col :span="12">
        <h2>
          <a v-on:click="prev">上一篇</a>
        </h2>
      </el-col>
      <el-col :span="12">
        <h2>
          <a v-on:click="next">下一篇</a>
        </h2>
      </el-col>
      <div class="page-component-up" v-bind:class="[showbar ? showcompont : hidecompont]" @click="toTop">
        <i class="el-icon-caret-top"></i>
      </div>
    </el-row>
  </div>
</template>
<script>
  import marked from 'marked'
  export default {
    data() {
      return {
        scrollheight: '',
        hidecompont: 'hidecompont',
        showcompont: ' showcompont',
        ht: '',
        showbar: false,
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
    created() {
      window.addEventListener('scroll', this.scrollUp)

    },
    methods: {
      toTop() {
        window.scroll(0, 0)
      },
      scrollUp() {
        this.scrollheight = document.body.scrollTop
        if (this.scrollheight > 2500) {
          this.showbar = true
        } else if (this.scrollheight < 1500) {
          this.showbar = false
        } else {
          this.showbar = this.showbar
        }
      },
      next() {
        if (this.weekId == this.maxcount) {
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
        } else {
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
<style>
  .markdown-body hr {
    height: 0.25em;
    padding: 0;
    margin: 24px 0;
    background-color: #e1e4e8;
    border: 0;
    overflow: hidden;
    box-sizing: content-box;
    display: block;
  }

  .markdown-body tr {
    display: table-row;
    vertical-align: inherit;
    border-color: inherit;
  }

  .markdown-body table tr:nth-child(2n) {
    background-color: #f6f8fa;
  }

  .markdown-body td,
  th {
    display: table-cell;
    vertical-align: inherit;
  }

  .markdown-body table {
    border-color: grey;
    width: auto;
    display: table;
    overflow: auto;
    margin-top: 0;
    margin-bottom: 16px;
    border-spacing: 0;
    border-collapse: collapse;
  }

  .markdown-body table thead,
  tbody {
    display: table-header-group;
    vertical-align: middle;
    border-color: inherit;
  }

  .markdown-body table tr {
    background-color: #fff;
    border-top: 1px solid #c6cbd1;
  }


  .markdown-body table td,
  .markdown-body table th {
    word-break: break-all;
    padding: 6px 13px;
    border: 1px solid #dfe2e5;
  }

  .markdown-body table th {
    font-weight: 600;
  }

  .markdown-body h1 {
    padding-top: 10px;
    border-bottom: 1px solid #eaecef;
  }

  .markdown-body blockquote {
    margin-left: 0px;
    padding-left: 20px;
    border-left: 5px solid #1F343D;
  }

  .markdown-body blockquote p {
    width: 66.7%;
  }

  .page-component-up {
    background-color: #34C0E3;
    position: fixed;
    right: 100px;
    bottom: 150px;
    width: 50px;
    height: 50px;
    border-radius: 25px;
    cursor: pointer;
    opacity: .4;
    transition: .3s;
  }

  .page-component-up:hover {
    opacity: 1;
  }

  .page-component-up i {
    color: #fff;
    display: block;
    line-height: 50px;
    text-align: center;
    font-size: 22px;
  }

  .hidecompont {
    display: none;
  }

  .showcompont {
    display: block;
  }

</style>
