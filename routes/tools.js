const express = require("express")
const app = express()
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync

module.exports = {
  fullpath: '',
  parms:{
    "_ps": [
      ['./dist/static/public/ps-', '牛仔裤热销排名7.csv'], "{'fun':'a','table':'bc_attribute_granularity_visitor'}"
    ],
    "_ph": [
      ['./dist/static/public/ph-', '牛仔裤热销排名7.csv'], "{'fun':'a','table':'bc_attribute_granularity_sales'}"
    ],
    "_hw": [
      ['./dist/static/public/hw-', '牛仔裤热搜核心词排名7.csv'], "{'fun':'w'}"
    ]
  },
  items: [],
  isEmpty: function (obj) {
    for (var key in obj) {
      return false;
    }
    return true;
  },
  getStringOut(method,req,res){
    if (method == 'get') {
      var filetime = moment(new Date() - 8.64e7).format('YYYY-MM-DD')
      this.fullpath = this.parms[req][0].join(filetime)
      return spawnSync('python', ['xiaobaods.py', this.parms[req][1]], {
        cwd: './python'
      })
    } else{
      var query = JSON.parse(req.body.data)
      query.date = moment(query.date).format('YYYY-MM-DD')
      var string = JSON.stringify(query).replace(/"/g, "'")
      this.fullpath = this.parms[method][0][0] + query.date.slice(0, 10) + query.category + query.variable + query.length + '.csv'
      return spawnSync('python', ['xiaobaods.py', string], {
        cwd: './python'
      })
    }
  },
  sentparams: function (method,req, res) {
    var spawnSync1 = this.getStringOut(method,req,res)
    var data = JSON.parse(spawnSync1.stdout)
    if (!this.isEmpty(data)) {
      this.itemsFilter(data)
      this.writeFile()
      res.send({
        code: 200,
        fullpath: this.fullpath,
        data: data
      })
    } else {
      res.send({
        code: 302,
        msg: '没有返回内容'
      })
    }
  },
  itemsFilter: function (dumpdata) {
    this.items=[]
    for (let outerkey in dumpdata) {
      var singledata = {}
      for (let innerkey in dumpdata[outerkey]) {
        switch (innerkey) {
          case '宝贝链接':
            continue;
          case '查看详情':
            continue;
          case '同款货源':
            continue;
          case '主图缩略图':
            continue;
          case 'total':
            continue;
          default:
            singledata[innerkey] = dumpdata[outerkey][innerkey]
        }
      }
      this.items.push(singledata)
    }
  },
  writeFile: function () {
    var hashjson = json2csv({
      data: this.items,
      quotes: ""
    })
    var codejson = iconv.encode(hashjson, 'gbk')
    fs.writeFile(this.fullpath, codejson, function (err) {
      if (err) throw err;
    })

  }
}
