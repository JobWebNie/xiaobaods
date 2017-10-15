'use strict'
const bodyParser = require('body-parser'),
    cookieParser = require('cookie-parser'),
    express = require('express'),
    template = require('art-template'),
    app = express()

template.config('cache', false)
app.engine('.html', template.__express)
app.set('view engine', 'html')
app.use(express.static('dist'))
app.use(cookieParser())
app.use(bodyParser.urlencoded({ extended: true }))


app.use(require('./routes/user'))
app.use(require('./routes/keyword'))
app.use(require('./routes/product'))
app.use(require('./routes/property'))
app.use(require('./routes/weekport'))

app.listen(3000,'127.0.0.1', () => console.log('正在运行'))