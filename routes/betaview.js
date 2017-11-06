const express = require("express")
const app = express()
const json2csv = require('json2csv')
const fs = require('fs')
const moment = require('moment')
const iconv = require('iconv-lite')
const router = express.Router()
const spawnSync = require('child_process')


function production() {
    console.log(this)
this.items = []
this.fullpath=''
}

production.prototype.sentparams=function(spawnSync){
    const spawnSync1 = spawnSync('python', ['xiaobaods.py', "{'fun':'a','table':'bc_attribute_granularity_visitor'}"], {
        cwd: './python'
      })
    var data = JSON.parse(spawnSync1.stdout)
    if(JSON.stringify(data) !== "{}"){
        this.getfullpath('/prod/search')
        this.itemsFilter(data)
        this.writeFile()
    }
}
production.prototype.getfullpath=function(_key){
    var filetime = moment(new Date() - 8.64e7).format('YYYY-MM-DD')
    var pathnames={
        "/prod/search":['./dist/static/public/ps-','牛仔裤热销排名7.csv']
    }
    this.fullpath = pathnames[_key].join(filetime)
}
production.prototype.itemsFilter=function(dumpdata){
    for(let outerkey in dumpdata){
        var singledata = {}
        for(let innerkey in dumpdata[outerkey]){
            switch(innerkey){
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
}
production.prototype.writeFile = function () {
  var hashjson = json2csv({
    data: this.items,
    quotes: ""
  })
  var codejson = iconv.encode(hashjson, 'gbk')
  fs.writeFile(this.fullpath, codejson, function (err) {
    if (err) throw err;
  })

}
var bar = new production()
bar.sentparams()
