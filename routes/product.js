const express = require('express')
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process').spawnSync

//店铺搜索功能
var storegroup = ['左街系', '欧选系', '淑美林', '自然相伴', '你牛我裤', '禾彩系', '小窝系', '线下品牌'];
router.get('/shop/search', (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_storegroup.py'])
  var data = storegroup = JSON.parse(spawnSync1.stdout)
  Response.send({
    data: data
  })
})
router.get("/prod/search", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', "{'table':'bc_attribute_granularity_visitor'}"])
  var timTep = new Date() - 24 * 60 * 60 * 1000
  var dateArgv = moment(timTep).format('YYYY-MM-DD')
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'ps-' + dateArgv + '牛仔裤热销排名7'
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
router.post("/prod/search", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = ''
  var time_length = query.data_time_length ? query.data_time_length : ''
  var table = 'bc_attribute_granularity_visitor'
  var category = query.data_items ? query.data_items : ''
  var variable = query.data_reorder ? query.data_reorder : ''
  var titlechoice = query.titlechoice ? query.titlechoice : ''
  var choice = query.choice ? query.choice : ''
  if (storegroup.indexOf(query.choice) > -1) {
    choice = "','storegroupchoice':'" + query.choice
  } else {
    choice = "','storechoice':'" + query.choice
  }
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','table':'" + table + choice + "','titlechoice':'" + titlechoice + "','length':" + time_length + ",'variable':'" + variable + "'}"

  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'ps-' + dateArgv + category + variable + time_length
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
    fs.writeFile('./static/public/' + filename + '.csv', strgbk, function (err) {
      if (err) throw err;
    });
  }

})
router.get("/prod/hot", (Request, Response) => {
  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', "{'table':'bc_attribute_granularity_sales'}"])
  var timTep = new Date() - 24 * 60 * 60 * 1000
  var dateArgv = moment(timTep).format('YYYY-MM-DD')
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'ph-' + dateArgv + '牛仔裤热销排名7'
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

        for (let i in data) {
          var myDataItem = {}
          for (let j in data[i]) {

            if (j == '宝贝链接' || j == '店铺链接' || j == '查看详情' || j == '同款货源' || j == '主图缩略图') {
              continue
            } else {
              myDataItem[j] = data[i][j]
            }
          }
          myData.push(myDataItem)
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
router.post("/prod/hot", (Request, Response) => {
  var query = JSON.parse(Request.body.data)
  var dateArgv = ''
  var time_length = query.data_time_length ? query.data_time_length : ''
  var table = 'bc_attribute_granularity_sales'
  var category = query.data_items ? query.data_items : ''
  var variable = query.data_reorder ? query.data_reorder : ''
  var choice = query.choice ? query.choice : ''
  var titlechoice = query.titlechoice ? query.titlechoice : ''
  if (storegroup.indexOf(query.choice) > -1) {
    choice = "','storegroupchoice':'" + query.choice
  } else {
    choice = "','storechoice':'" + query.choice
  }
  if (query.data_time !== null && query.data_time !== undefined && query.data_time !== '') {
    dateArgv = moment(query.data_time).format('YYYY-MM-DD')
  }
  var string = "{'date':'" + dateArgv + "','category':'" + category + "','table':'" + table + choice + "','titlechoice':'" + titlechoice + "','length':" + time_length + ",'variable':'" + variable + "'}"

  const spawnSync1 = spawnSync('python', ['xiaobaods_a.py', string])
  var data = JSON.parse(spawnSync1.stdout)
  var filename = 'ph-' + dateArgv + category + choice + variable + time_length
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
    fs.writeFile('./static/public/' + filename + '.csv', strgbk, function (err) {
      if (err) throw err;
    });
  }
})

module.exports = router
