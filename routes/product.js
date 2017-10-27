const express = require('express')
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync

//店铺搜索功能

router.get('/shop/search', (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_storegroup.py'], {
    cwd: './python'
  })
  var storegroup = JSON.parse(spawnSync1.stdout)
  Response.send(storegroup)
})
router.get("/prod/search", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', "{'fun':'a','table':'bc_attribute_granularity_visitor'}"], {
    cwd: './python'
  })
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/ps-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤热销排名7.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      var myDataItem = {}
      for (let j in data[i]) {
        switch (j) {
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
            myDataItem[j] = data[i][j];
        }
      }
      myData.push(myDataItem)
    }
    fs.writeFile(fullpath, iconv.encode(json2csv({
      data: myData,
      quotes: ""
    }), 'gbk'), function (err) {
      if (err) throw err;
    })
    Response.send({
      fullpath: fullpath,
      data: data
    })
  }
})
router.post("/prod/search", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  query.date = moment(query.date).format('YYYY-MM-DD')
  var string = JSON.stringify(query).replace(/"/g, "'")
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', string], {
    cwd: './python'
  })
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/ps-' + query.date.slice(0, 10) + query.category + query.variable + query.length + '.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      var myDataItem = {}
      for (let j in data[i]) {
        switch (j) {
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
            myDataItem[j] = data[i][j];
        }
      }
      myData.push(myDataItem)
    }
    fs.writeFile(fullpath, iconv.encode(json2csv({
      data: myData,
      quotes: ""
    }), 'gbk'), function (err) {
      if (err) throw err;
    })
    Response.send({
      code:200,
      fullpath: fullpath,
      data: data
    })
  }else{
    Response.send({
      code:302,
      msg:'没有返回内容'
    })
  }
})

router.get("/prod/hot", (Request, Response) => { 
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', "{'fun':'a',table':'bc_attribute_granularity_sales'}"],{cwd:'./python'})  
  var data = JSON.parse(spawnSync1.stdout)

var fullpath = './dist/static/public/ph-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤热销排名7.csv'
if (JSON.stringify(data) !== "{}") {
   var myData = []
    for (let i in data) {
      var myDataItem = {}
      for (let j in data[i]) {
        switch (j) {
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
            myDataItem[j] = data[i][j];
        }
      }
      myData.push(myDataItem)
    }
    fs.writeFile(fullpath, iconv.encode(json2csv({
      data: myData,
      quotes: ""
    }), 'gbk'), function (err) {
      if (err) throw err;
    })
  Response.send({
    fullpath: fullpath,
    data: data
  })
}
})


router.post("/prod/hot", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  query.date = moment(query.date).format('YYYY-MM-DD')
  var string = JSON.stringify(query).replace(/"/g, "'")
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', string], {
    cwd: './python'
  })
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/ph-' + query.date.slice(0, 10) + query.category + query.variable + query.length + '.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      var myDataItem = {}
      for (let j in data[i]) {
        switch (j) {
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
            myDataItem[j] = data[i][j];
        }
      }
      myData.push(myDataItem)
    }
    fs.writeFile(fullpath, iconv.encode(json2csv({
      data: myData,
      quotes: ""
    }), 'gbk'), function (err) {
      if (err) throw err;
    })
    Response.send({
      code:200,
      fullpath: fullpath,
      data: data
    })
  }else{
    Response.send({
      code:302,
      msg:'没有返回内容'
    })
  }
})

module.exports = router
