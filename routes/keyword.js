const express = require("express")
const app = express()
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync
// 热词处理
router.get('/keyWord/hot', (Request, Response) => {
  var fullpath = './dist/static/public/hw-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤热搜核心词排名7.csv'
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', "{'fun':'w'}"], {cwd: './python'})
  var data = JSON.parse(spawnSync1.stdout)
  
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      myData.push(data[i])
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
router.post("/keyWord/hot", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  query.date = moment(query.date).format('YYYY-MM-DD')
  var string = JSON.stringify(query).replace(/"/g, "'")
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', string], {
    cwd: './python'
  })
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/hw-' + query.date.slice(0, 10) + query.category + query.variable + query.length + '.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      myData.push(data[i])
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
// 关键词处理
router.get('/keyWord/up', (Request, Response) => {
  var fullpath = './dist/static/public/hw-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤热搜核心词排名7.csv'
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', "{'fun':'w','choice':'飙升核心词'}"], {cwd: './python'})
  var data = JSON.parse(spawnSync1.stdout)
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      myData.push(data[i])
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
router.post("/keyWord/up", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  query.date = moment(query.date).format('YYYY-MM-DD')
  var string = JSON.stringify(query).replace(/"/g, "'")
  const spawnSync1 = spawnSync('python', ['xiaobaods.py', string], {
    cwd: './python'
  })

  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './dist/static/public/uw-' + query.date.slice(0, 10) + query.category + query.variable + query.length + '.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (let i in data) {
      myData.push(data[i])
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
// 高级词汇处理
router.get('/keyWord/entry', (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_ws.py'],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    data: data
  })
})
router.post("/keyWord/entry", (Request, Response) => {
  var query = JSON.parse(Request.body.data)

  var dateArgv = ''
  var category = query.data_items ? query.data_items : ''
  var choice = query.data_choice[0] ? query.data_choice[0] : ''
  var variable = query.data_choice[1] ? query.data_choice[1] : ''
  // var lbd = query.data_lbd ? query.data_lbd : ''
  var head = query.data_head ? query.data_head : ''
  var time_length = query.time_length ? query.time_length : ''
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','choice':'" + choice + "','variable':'" + variable + "','length':" + time_length + ",'head':" + head + "}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_ws.py', string],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    message: '查询成功',
    data: data
  })
})
module.exports = router
