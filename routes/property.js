const express = require('express')
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync

//市场详情
var storegroup = ['左街系', '欧选系', '淑美林', '自然相伴', '你牛我裤', '禾彩系', '小窝系', '线下品牌'];
router.get("/market/prop", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_c.py'])
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    data: data
  })
})
router.post("/market/prop", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = ''
  var time_length = query.data_time_length ? query.data_time_length : ''
  var category = query.data_items[0] ? query.data_items[0] : ''
  var classfication = query.data_items[1] ? query.data_items[1] : ''
  var attributes = query.data_items[2] ? query.data_items[2] : ''
  var variable = query.data_reorder ? query.data_reorder : ''
  var titlechoice = query.titlechoice ? query.titlechoice : ''
  var choice = query.choice ? query.choice : ''

  if (storegroup.indexOf(query.choice) > -1) {
    choice = "','storegroupchoice':'" + query.choice
  } else {
    choice = "','storechoice':'" + query.choice
  }
  console.log(choice)
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + choice + "','titlechoice':'" + titlechoice + "','length':" + time_length + ",'classfication':'" + classfication + "','attributes':'" + attributes + "','variable':'" + variable + "'}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_c.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    message: '查询成功',
    data: data
  })
})

//home数据页
router.get("/component", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_m.py'])
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
  const spawnSync1 = spawnSync('python', ['xiaobaods_m.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    data: data
  })
})
router.get('/pete/shop', (request, response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_e.py', "{'attribute':'list'}"])
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
  const spawnSync1 = spawnSync('python', ['xiaobaods_e.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  response.send({
    message: 'ok',
    data: data
  })
})
router.post('/proper/trend', (request, response) => {
var query = request.body.data
  if (query.feature == '' || query.feature == 'list') {
    var string = JSON.stringify(query).replace(/\"/g, "'")
    const spawnSync1 = spawnSync('python', ['xiaobaods_et.py', string])
    var data = JSON.parse(spawnSync1.stdout)
   response.send({data:data})
  }else{
     var string0="{'category':'" + query.category + "','attribute':'" + query.attribute +"','variable':'" + query.variable + "','feature':'all'}"
     var string1 = "{'category':'" + query.category + "','attribute':'" + query.attribute +"','variable':'" + query.variable + "','feature':'"+query.feature+"','stats':0}"
     var string2="{'category':'" + query.category + "','attribute':'" + query.attribute +"','variable':'" + query.variable + "','feature':'"+query.feature+"','stats':1}"
     const spawnSync0 = spawnSync('python', ['xiaobaods_et.py', string0])
     const spawnSync1 = spawnSync('python', ['xiaobaods_et.py', string1])
     const spawnSync2 = spawnSync('python', ['xiaobaods_et.py', string2])
     var data0 = JSON.parse(spawnSync0.stdout)
     var data1 = JSON.parse(spawnSync1.stdout)
     var data2 = JSON.parse(spawnSync2.stdout)
     response.send({data0:data0,data1:data1,data2:data2})
  }
})
module.exports = router
