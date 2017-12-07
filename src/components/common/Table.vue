<template>
  <el-table :data="tableData">
    <el-table-column label="排名" width="50" header-align="center" align="center">
      <template slot-scope="scope">
        <el-tooltip placement="left" effect="light">
          <div slot="content">点击显示商品
            <br>发展周期</div>
          <span style="cursor:pointer;">{{scope.row.热销排名}}</span>
        </el-tooltip>
      </template>
    </el-table-column>
    <el-table-column :label="tableTitle[0]" header-align="center" align="center" width="80">
      <template slot-scope="scope">
        <a target="_blank" alt="">
          <img style="height:44px;" :src="scope.row.主图缩略图" alt="店铺图片">
        </a>
      </template>
    </el-table-column>
    <el-table-column show-overflow-tooltip :label="tableTitle[2]" header-align="center" align="center">
      <template slot-scope="scope" width="420">
        <a target="_blank" :href="scope.row.宝贝链接" alt="">{{scope.row.商品信息}}</a>
      </template>
    </el-table-column>
    <el-table-column show-overflow-tooltip prop="所属店铺" :label="tableTitle[3]" header-align="center" align="center" width="150">
      <template slot-scope="scope">
        <a target="_blank" :href="scope.row.店铺链接">{{scope.row.所属店铺}}</a>
      </template>
    </el-table-column>
    <el-table-column :prop="tableTitle[4]" :label="tableTitle[4]" :formatter="contentFormatter" header-align="right" align="right"
      width="120"></el-table-column>
    <el-table-column :prop="tableTitle[5]" :label="tableTitle[5]" :formatter="contentFormatter" header-align="right" align="right"
      width="120"></el-table-column>
    <el-table-column :prop="tableTitle[6]" :label="tableTitle[6]" :formatter="contentFormatter" header-align="right" align="right"
      width="120"></el-table-column>
    <el-table-column v-for="(title,id) in tableTitle" :key="id" v-if="title.slice(0,2)=='日期'" :prop="title" :render-header="renderHeader"
      :formatter="contentFormatter" align="right" header-align="right" width="60"></el-table-column>
    <el-table-column header-align="center" align="center" label="操作" width="120">
      <template slot-scope="scope">
        <a target="_blank" :href="scope.row.查看详情" value='' alt=""> 查看详情</a>
        <br>
        <a target="_blank" :href="scope.row.同款货源" alt="">同款货源</a>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
  export default {
    components: {

    },
    props: {
      tableData: {
        type: Array,
        required: true
      },
      tableTitle: {
        type: Array,
        required: true
      },
      tableExpend:{
        type: String,
        required: true
      }
    },
    data() {
      return {}
    },
    methods: {
      renderHeader(h, {
        column,
        $index
      }) { //格式化显示表头
        var th = column.property.slice(-4, -2) + '-' + column.property.slice(-2)
        return column.label = th;
      },
      contentFormatter(row, column, cellValue) {
        let reg = String(cellValue).replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
        let percent = Math.round(cellValue * 100) + '%'
        if (column.property.slice(0, 2) == "日期") {
          if (cellValue == null) {
            return ''
          } else {
            const fm = this.tableExpend
            switch (fm) {
              case '支付子订单数':
                return cellValue = reg;
                break;
              case '交易增长幅度':
                return cellValue = percent;
                break;
              case '支付转化率指数':
                return cellValue = reg;
                break;
              default:
                return cellValue = cellValue;
                break;
            }
          }

        } else {
          switch (column.property) {
            case '支付子订单数':
              return cellValue = reg;
              break;
            case '交易增长幅度':
              return cellValue = percent;
              break;
            case '支付转化率指数':
              return cellValue = reg;
              break;
            default:
              return cellValue = cellValue;
              break;
          }
        }
      },
    }
  }

</script>
