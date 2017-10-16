var express = require('express');
var fs = require('fs');
var db = require('../db');
var router = express.Router();

router.post('/conversion/parms', (Request, Response) => {
  var name = Request.body.name
  db.pool.query('SELECT * FROM `Tools_conversion` WHERE `category` = ?', [name], function (err, results, fields) {
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
router.get('/weekreport', (Request, Response) => {

  if (!Request.query.listIndex) {
    db.pool.query('SELECT * FROM weekly_publication ORDER BY id DESC LIMIT 0,1;', function (err, result) {
      if (err) throw (err);
      fs.readFile('./markdown/' + result[0].name, 'utf8', function (err, data) {
        if (err) throw (err);
        Response.send({
          code: 200,
          msg: result[0].title,
          data: data,
          count: result[0].id
        })
      })
    })
  } else {
      db.pool.query('select * from weekly_publication where `id`=?', [+Request.query.listIndex], function (err, result) {
        if (err) console.log(err);
        fs.readFile('./markdown/' + result[0].name, 'utf8', function (err, data) {
          if (err) console.log(err);
          if (data) {
            Response.send({
              code: 200,
              msg: result[0].title,
              data: data
            })
          } else {
            Response.send({
              code: 400,
              msg: '已经是最后一篇了'
            })
          }

        })
      })
  }

})
module.exports = router;
