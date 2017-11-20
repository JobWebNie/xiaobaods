const express = require('express')
const router = express.Router()
const tools = require('./tools')
router.get("/prod/search", (Request, Response) => {
  tools.sentparams('get','_ps', Response)
})
router.post("/prod/search", (Request, Response) => {
  tools.sentparams('_ps',Request, Response)
})
router.get("/prod/hot", (Request, Response) => {
  tools.sentparams('get','_ph', Response)
})
router.post("/prod/hot", (Request, Response) => {
  tools.sentparams('_ph',Request, Response)  
})
router.get("/prod/hotid", (Request, Response) => {
  const spawnSync = require('child_process').spawnSync
  const spawnSync1 = spawnSync('python', ['xiaobaods.py',"{'fun':'al','table':'bc_attribute_granularity_sales'}"],{cwd:'./python'})
  var data = JSON.parse(spawnSync1.stdout)
  console.log(data)
})
module.exports = router
