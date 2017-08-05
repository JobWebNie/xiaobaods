import Vue from 'vue'
export const PICTURE_INSERT = 'PICTURE_INSERT' //插入图片
export const PICTURE_PUT = 'PICTURE_PUT' //修改数据
export const PICTURE_DELETE = 'PICTURE_DELETE' //删除数据

export default {
  state: JSON.parse(sessionStorage.getItem('pictures')) || [],
  getters:{
    getPictureArray:(state,picture)=>{
      return state.picture
    }
  },
  mutations: {
    PICTURE_INSERT(state, picture) {
        var data= picture.map(function (item) {
              var name = item['所属店铺']
             var url =  item['主图缩略图'].slice(0, -10)
             var detail = item['宝贝链接']
             var count = item['支付子订单数']
          return {
            name:name,
            url:url,
            detail:detail,
            count:count
          }
        })
      sessionStorage.setItem('pictures', JSON.stringify(data))
     Object.assign(state, data)//触发视图更新返回data数据对象
    },
    PICTURE_PUT(state, key) {
      Vue.delete(state, key)
    },
    PICTURE_DELETE(state, picture) {
      sessionStorage.removeItem(picture)
      Object.keys(state).forEach(k => Vue.delete(state, k))
      Object.assign(state,[])
    }
  },
  actions: {
    PICTURE_INSERT({
      commit
    }, picture) {
      commit(PICTURE_INSERT, picture)
    },
    PICTURE_PUT({
      commit
    }, key) {
      commit(PICTURE_PUT, key)
    },
    PICTURE_DELETE({
      commit
    }) {
      commit(PICTURE_DELETE)
    }
  }
}
