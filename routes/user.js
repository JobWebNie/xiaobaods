const db = require('../db')
const express = require('express')
const app = express()
const router = express.Router()
// 用户登录
router.post("/base/login", (Request, Response) => {
  var data = JSON.parse(Request.body.data)
  db.pool.query('SELECT * FROM `xiaobaods_users_tables` WHERE `name` = ?', [data.name], function (err, results, fields) {
    if (err) throw err
    else if (results.length > 0) {
      if (results[0].password == data.password) {
        Response.send({
          message: "success",
          data: results[0]
        })
      } else {
        Response.send({
          message: 'pasErr'
        })
      }

    } else {
      Response.send({
        message: "acountErr"
      })
    }

  })
})
// 用户注册

router.post("/user/register", (Request, Response, next) => {
  var data = JSON.parse(Request.body.data)
  // console.log(data)
  db.pool.query("SELECT * FROM `xiaobaods_users_tables` WHERE `id` = ?", [data.id], function (err, results, fields) {
    if (err) throw err
    else if (results.length <= 0) {
      Response.send({
        message: "idErr"
      })
    } else {
      db.pool.query("UPDATE xiaobaods_users_tables SET `name`=?,`password`=? where `id`=?;", [data.name, data.password, data.id], function (err, results, fields) {
        if (err) {
          Response.send({
            message: "false"
          })
        } else {
          Response.send({
            message: "success"
          })
        }
      })
    }
  })
})
// 找回密码
router.put("/modify/seekPassw", (Request, Response) => {
  var data = Request.body.data
  db.pool.query('SELECT * FROM `xiaobaods_users_tables` WHERE `name` = ? and `id`=?', [data.name, data.id], function (err, results, fields) {
    if (err) throw err
    else if (results.length > 0) {
      Response.send({
        message: "success",
        data: results[0].password
      })
    } else {
      Response.send({
        message: "acountErr"
      })
    }
  })
})

router.post('/conversion/parms',(Request, Response)=>{
     var name = Request.body.name
  db.pool.query('SELECT * FROM `Tools_conversion` WHERE `category` = ?', [name],function(err,results,fields){
    if (err) throw err
    else if (results.length > 0) {
      Response.send(results[0])
    } else {
      Response.send({
        message: "acountErr"
      })
    }
  })
})
module.exports = router
