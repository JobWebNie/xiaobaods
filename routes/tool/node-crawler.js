var http = require('http')
var fs = require('fs')
var path = require('path')
var archiver = require('archiver')

//得到标准的imgUrl地址数组connCutImg

exports.downLoad = function (databse,username) {

    var pictures = []
    var filesname = [];
    for(var i in databse){
        var imgArr = []
        for (let j in databse[i]) {

            if (j == '主图缩略图') {

                var imgpath = 'http:' + databse[i][j]

                imgArr.push(imgpath)
            }
            else {

                continue;
            }
        }
        imgArr.map(function (item) {
            pictures.push(asyncDown(item))
        })
    }
    function asyncDown(url) {
        return new Promise(function (resolve, reject) {
            // console.log('正在下载..' + url)
            http.get(url, function (res) {
                res.setEncoding('binary')//转换为二进制
                var content = ''
                var picturename = path.join(__dirname + '/images/' + path.basename(url))
              
                res.on('data', function (data) {
                    content += data
                }).on('end', function () {
                    fs.writeFile(picturename, content, 'binary', function (err) {
                        if (err) reject(err);
                        resolve(picturename)
                    })
                })
            })
        })
    }
    //收到下载文件请求开始打包文件
    http.get('/download/picture',function(Request, Response){
    // 打包文件
    Promise.all(pictures)
        .then(function (items) {
            var archive = archiver('zip', { store: true });
            archive.on('error', function (err) {
                throw err;
            });
            archive.pipe(fs.createWriteStream(__dirname + '/static/public/'+username+'.zip'));
            items.map(function (val) {
                archive.append(fs.createReadStream(val), { name: path.basename(val) })
            })

            archive.finalize();
            console.log("打包完成")
            return items
        }).then(function(items){
             console.log('开始删除文件夹')
             items.map(function(item){
              var itemPath = 'images/'+  path.basename(item)
               fs.unlink(itemPath)
             })
             console.log('删除完成')
        })
        Response.send({message:'获取信息'})
    })
}
