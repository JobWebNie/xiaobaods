const express = require('express')
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync

//市场详情
router.get("/market/prop", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods.py',"{'fun':'c','table':'bc_attribute_granularity_sales'}"],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/pd-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤款式铅笔裤热销排名7.csv'
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
router.post("/market/prop", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  query.date = moment(query.date).format('YYYY-MM-DD')
  var string = JSON.stringify(query).replace(/"/g, "'")
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', string],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/pd-' + query.date.slice(0, 10) + query.category + query.classfication + query.attributes + query.variable + query.length + '.csv'
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
//home数据页
router.get("/component", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_m.py'],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    data: data
  })
})
router.post("/target/compare", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var category = query.category ? query.category : ''
  var display = query.display
  if (display == '一个月') {
    display = 'month'
  } else if (display == '三个月') {
    display = 'quarter'
  } else if (display == '半年') {
    display = 'halfyear'
  } else {
    display = 'year'
  }
  var string = "{'category':'" + category + "','display':'" + display + "'}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_m.py', string],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    data: data
  })
})
router.get('/pete/shop', (request, response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_e.py', "{'attribute':'list'}"],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  response.send({
    message: 'ok',
    data: data
  })
})
router.post('/pete/shop', (request, response) => {
  var query = JSON.parse(request.body.data)
  var dateArgv = ''
  var category = query.category ? query.category : ''
  var attribute = query.attribute ? query.attribute : ''
  var variable = query.variable ? query.variable : ''
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','attribute':'" + attribute + "','variable':'" + variable + "'}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_e.py', string],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  response.send({
    message: 'ok',
    data: data
  })
})
router.post('/proper/trend', (request, response) => {
  var query = request.body.data
  if (query.attribute == 'list' || query.feature == 'list') {
    var string = JSON.stringify(query).replace(/\"/g, "'")
    const spawnSync1 = spawnSync('python', ['xiaobaods_et.py', string],{cwd:'./python'})
    var data = JSON.parse(spawnSync1.stdout)
    response.send({
      data: data
    })
  } else {
    var string0 = "{'category':'" + query.category + "','attribute':'" + query.attribute + "','variable':'" + query.variable + "','feature':'all'}"
    var string1 = "{'category':'" + query.category + "','attribute':'" + query.attribute + "','variable':'" + query.variable + "','feature':'" + query.feature + "','stats':0}"
    var string2 = "{'category':'" + query.category + "','attribute':'" + query.attribute + "','variable':'" + query.variable + "','feature':'" + query.feature + "','stats':1}"
    const spawnSync0 = spawnSync('python', ['xiaobaods_et.py', string0],{cwd:'./python'})
    const spawnSync1 = spawnSync('python', ['xiaobaods_et.py', string1],{cwd:'./python'})
    const spawnSync2 = spawnSync('python', ['xiaobaods_et.py', string2],{cwd:'./python'})

   
    var data0 = JSON.parse(spawnSync0.stdout)
    var data1 = JSON.parse(spawnSync1.stdout)
    var data2 = JSON.parse(spawnSync2.stdout)
 
    response.send({
      data0: data0,
      data1: data1,
      data2: data2
    })
  }
})
module.exports = router
