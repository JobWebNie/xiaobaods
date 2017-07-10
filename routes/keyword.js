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
  const spawnSync1 = spawnSync('python', ['xiaobaods_w.py'])
  var timTep = new Date() - 24 * 60 * 60 * 1000
  var dateArgv = moment(timTep).format('YYYY-MM-DD')
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'hw-' + dateArgv + '牛仔裤热搜核心词排名7'
  var fullpath = './static/public/' + filename + '.csv'
  fs.exists(fullpath, function (exists) {
    if (exists) {
      Response.send({
        data: data,
        filename: filename
      })
    } else {
      if (JSON.stringify(data) == "{}") {
        Response.send({
          message: '类目无店铺'
        })
      } else {
        Response.send({
          message: '查询成功',
          filename: filename,
          data: data
        })
        var myData = []
        for (var i in data) {
          myData.push(data[i])
        }
        var csv = json2csv({
          data: myData,
          quotes: ""
        });
        var strgbk = iconv.encode(csv, 'gbk')
        fs.writeFile(fullpath, strgbk, function (err) {
          if (err) throw err;
        });
      }
    }
  })
})
router.post("/keyWord/hot", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = ''
  var time_length = query.data_time_length ? query.data_time_length : ''
  var category = query.data_items ? query.data_items : ''
  var choice = query.data_reorder[0] ? query.data_reorder[0] : ''
  var variable = query.data_reorder[1] ? query.data_reorder[1] : ''
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','length':" + time_length + ",'choice':'" + choice + "','variable':'" + variable + "'}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_w.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'hw-' + dateArgv + category + choice + variable + time_length
  var fullpath = './static/public/' + filename + '.csv'
  fs.exists(fullpath, function (exists) {
    if (exists) {
      Response.send({
        data: data,
        filename: filename
      })
    } else {
      if (JSON.stringify(data) == "{}") {
        Response.send({
          message: '类目无店铺'
        })
      } else {
        Response.send({
          message: '查询成功',
          filename: filename,
          data: data
        })
        var myData = []
        for (var i in data) {
          myData.push(data[i])
        }
        var csv = json2csv({
          data: myData,
          quotes: ""
        });
        var strgbk = iconv.encode(csv, 'gbk')
        fs.writeFile(fullpath, strgbk, function (err) {
          if (err) throw err;
        });
      }
    }
  })
})
// 关键词处理
router.get('/keyWord/up', (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_w.py', "{'choice':'飙升核心词'}"]) //由于参数不同默认选中飙升
  var timTep = new Date() - 24 * 60 * 60 * 1000
  var dateArgv = moment(timTep).format('YYYY-MM-DD')
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'uw-' + dateArgv + '牛仔裤飙升核心词排名7'
  var fullpath = './static/public/' + filename + '.csv'
  fs.exists(fullpath, function (exists) {
    if (exists) {
      Response.send({
        data: data,
        filename: filename
      })
    } else {
      if (JSON.stringify(data) == "{}") {
        Response.send({
          message: '类目无店铺'
        })
      } else {
        Response.send({
          message: '查询成功',
          filename: filename,
          data: data
        })
        var myData = []
        for (var i in data) {
          myData.push(data[i])
        }
        var csv = json2csv({
          data: myData,
          quotes: ""
        });
        var strgbk = iconv.encode(csv, 'gbk')
        fs.writeFile(fullpath, strgbk, function (err) {
          if (err) throw err;
        });
      }
    }
  })
})
router.post("/keyWord/up", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = ''
  var time_length = query.data_time_length ? query.data_time_length : ''
  var category = query.data_items ? query.data_items : ''
  var choice = query.data_reorder[0] ? query.data_reorder[0] : ''
  var variable = query.data_reorder[1] ? query.data_reorder[1] : ''
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','length':" + time_length + ",'choice':'" + choice + "','variable':'" + variable + "'}"

  const spawnSync1 = spawnSync('python', ['xiaobaods_w.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'uw-' + dateArgv + category + choice + variable + time_length
  var fullpath = './static/public/' + filename + '.csv'
  fs.exists(fullpath, function (exists) {
    if (exists) {
      Response.send({
        data: data,
        filename: filename
      })
    } else {
      if (JSON.stringify(data) == "{}") {
        Response.send({
          message: '类目无店铺'
        })
      } else {
        Response.send({
          message: '查询成功',
          filename: filename,
          data: data
        })
        var myData = []
        for (var i in data) {
          myData.push(data[i])
        }
        var csv = json2csv({
          data: myData,
          quotes: ""
        });
        var strgbk = iconv.encode(csv, 'gbk')
        fs.writeFile(fullpath, strgbk, function (err) {
          if (err) throw err;
        });
      }
    }
  })
})
// 高级词汇处理
router.get('/keyWord/entry', (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_ws.py'])
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
  const spawnSync1 = spawnSync('python', ['xiaobaods_ws.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  Response.send({
    message: '查询成功',
    data: data
  })
})
module.exports = router
