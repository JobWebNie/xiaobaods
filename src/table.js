const Table = function (table) {
  this.table = table
  this.formatCash = function (cash) {
    var str_cash = cash + ""; //转换成字符串
    var ret_cash = "";
    var counter = 0;
    for (var i = str_cash.length - 1; i >= 0; i--) {
      ret_cash = str_cash.charAt(i) + ret_cash;
      counter++;
      if (counter == 3) {
        counter = 0;
        if (i != 0) {
          ret_cash = "," + ret_cash;
        }
      }
    }
    return ret_cash;
  }

  this.beautify = function (vule) {
    var tb = [];
    var th = [];
    if (vule) {
      for (let j in vule) {
        for (let k in vule[j]) {
          if (k == 'total') {
            this.Table.total = vule[j][k]
          } else {
            th.push(k)
          }
        }
        break;
      }
      for (let i in vule) {
        tb.push(vule[i])
      }
      this.Table.tableData_title = th
      this.Table.tableData_prepag = tb
    }
  }
  this.valueGroupFliter = function (items, filter) {
    const objectValue = items || {
      "2017-10-11": {
        "排名": 10,
        "支付子订单数": 1954,
        "交易增长幅度": 0.09,
        "支付转化率指数": 157
      },
      "2017-10-12": {
        "排名": 11,
        "支付子订单数": 1954,
        "交易增长幅度": -0.12,
        "支付转化率指数": 157
      },
      "2017-10-13": {
        "排名": 12,
        "支付子订单数": 1954,
        "交易增长幅度": 0.03,
        "支付转化率指数": 157
      }
    }
    console.log(arguments)
    var timeline = [],
      dealwith = [],
      order = [],
      sailBill = [],
      forpay = [];
    for (let item in items) {
      for(filter in items.item){
        timeline.push(items.item)
        order.push(items.item.filter)
        sailBill.push(items.item['支付子订单数'])
        dealwith.push(items.item['交易增长幅度'])
        forpay.push(items.item['支付转化率指数'])
      }
    
    }
    return {
      timeline:timeline,
      order:order,
      sailBill:sailBill,
      dealwith:dealwith,
      forpay:forpay
    }
  }
}
