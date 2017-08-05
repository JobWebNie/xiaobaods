const express = require('express')
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync

//店铺搜索功能
var storegroup;

router.get('/shop/search', (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_storegroup.py'])
  var data = storegroup = JSON.parse(spawnSync1.stdout)
  Response.send(data)
})
router.get("/prod/search/:name?", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', "{'table':'bc_attribute_granularity_visitor'}"])
  var data = JSON.parse(spawnSync1.stdout)
  if (Request.params.name == "download") { // 添加下载拦截器
    var fullpath = './static/public/ps-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤热销排名7.csv'
    try {
      fs.exists(fullpath, function (exists) {
        if (!exists) {
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
        }
        Response.send({
          data: data,
          fullpath: fullpath
        })
      })
    } catch (e) {
      console.log('文件写入错误' + e)
    }
  } else {
    Response.send({
      data: data
    })
  }
})
router.post("/prod/search", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = query.data_time ? moment(query.data_time).format('YYYY-MM-DD'):''
  var time_length = query.data_time_length ? query.data_time_length : ''
  var table = 'bc_attribute_granularity_visitor'
  var category = query.data_items ? query.data_items : ''
  var variable = query.data_reorder ? query.data_reorder : ''
  var titlechoice = query.titlechoice ? query.titlechoice : ''
  var choice;
  if (storegroup.indexOf(query.choice) > -1) {
    choice = "','storegroupchoice':'" + query.choice
  } else {
    choice = "','storechoice':'" + query.choice
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','table':'" + table + choice + "','titlechoice':'" + titlechoice + "','length':" + time_length + ",'variable':'" + variable + "'}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './static/public/ps-' + dateArgv + category + choice + variable + time_length + '.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (var i in data) {
      myData.push(data[i])
    }
    var csv = json2csv({
      data: myData,
      quotes: ""
    });
    var strgbk = iconv.encode(csv, 'gbk')
    fs.writeFile(fullpath, strgbk)
    Response.send({
      fullpath: fullpath,
      data: data
    })
  }
})

router.get("/prod/hot/:name?", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', "{'table':'bc_attribute_granularity_sales'}"])
  var data = JSON.parse(spawnSync1.stdout)
  if (Request.params.name == "download") { // 添加下载拦截器
    var fullpath = './static/public/ph-' + moment(new Date() - 8.64e7).format('YYYY-MM-DD') + '牛仔裤热销排名7.csv'
    try {
      fs.exists(fullpath, function (exists) {
        if (!exists) {
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
        }
        Response.send({
          fullpath: fullpath
        })
      })
    } catch (e) {
      console.log('文件写入错误' + e)
    }
  } else {
    Response.send({
      data: data
    })
  }
})
router.post("/prod/hot", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = query.data_time ? moment(query.data_time).format('YYYY-MM-DD'):''
  var time_length =  query.data_time_length ? query.data_time_length : ''
  var table = 'bc_attribute_granularity_sales'
  var category = query.data_items ? query.data_items : ''
  var variable = query.data_reorder ? query.data_reorder : ''
  var titlechoice = query.titlechoice ? query.titlechoice : ''
  var choice;

  if (storegroup.indexOf(query.choice) > -1) {
    choice = "','storegroupchoice':'" + query.choice
  } else {
    choice = "','storechoice':'" + query.choice
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','table':'" + table + choice + "','titlechoice':'" + titlechoice + "','length':" + time_length + ",'variable':'" + variable + "'}"
  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  var fullpath = './static/public/ph-' + dateArgv + category + choice + variable + time_length + '.csv'
  if (JSON.stringify(data) !== "{}") {
    var myData = []
    for (var i in data) {
      myData.push(data[i])
    }
    var csv = json2csv({
      data: myData,
      quotes: ""
    });
    var strgbk = iconv.encode(csv, 'gbk')
    fs.writeFile(fullpath, strgbk)
    Response.send({
      fullpath: fullpath,
      data: data
    })
  }
})

module.exports = router
