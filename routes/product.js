const express = require('express')
const router = express.Router()
const tools = require('./tools')
router.get("/prod/search", (Request, Response) => {
  tools.sentparams('get', '_ps', Response)
})
router.post("/prod/search", (Request, Response) => {
  tools.sentparams('_ps', Request, Response)
})
router.get("/prod/hot", (Request, Response) => {
  tools.sentparams('get', '_ph', Response)
})
router.post("/prod/hot", (Request, Response) => {
  tools.sentparams('_ph', Request, Response)
})
router.get("/prod/hotid", (Request, Response) => {
  var prodId = Request.query.id
  if (prodId == undefined) {
    Response.send({
      code: 404,
      message: '需要传入商品编号'
    })
  } else {
    const spawnSync = require('child_process').spawnSync
    const spawnSync1 = spawnSync('python', ['xiaobaods.py', "{'fun':'al','cid':'" + prodId + "'}"], {
      cwd: './python'
    })
    var data = JSON.parse(spawnSync1.stdout)
    Response.send({
      code:200,
      data: data
    })
  }

})
module.exports = router
