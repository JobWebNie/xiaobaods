export default {
  // 去除前缀接口 '日期：'
  inptions: function (options) {

    if (options.name == 'rmPrefix') {
      return this.rmPrefix(options)
    }

  },
  rmPrefix: function (options) {
    options.data.map(function (item) {
      for (var i in item) {
        if (i.slice(0, 2) == "日期") {
          let nkey =i.slice(7, 9) + '-' + i.slice(9, 11)
          item[nkey] = item[i]
          delete item[i]
        }
      }
    })
    return options.data
  }
}
