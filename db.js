var mysql = require('mysql2');

var user = {
    host: '47.94.172.95',
    port: 3306,
    user: 'program_w',
    password:'KQPp5wrZJG33fwFs',
    database: 'xiaobaods',
    charset:'UTF8_GENERAL_CI'
}

//创建连接

module.exports.pool=mysql.createPool(user)