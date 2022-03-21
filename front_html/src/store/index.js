import Vue from 'vue'
import Vuex from 'vuex'//引入vuex
import createPersistedState from "vuex-persistedstate" //刷新也不会清除vuex信息

Vue.use(Vuex); //使用 vuex
const store = new Vuex.Store({
  // 如果此刻想配置多个选项，将plugins写成一个一维数组，不然会报错,刷新也不会清除vuex信息
  plugins:[createPersistedState()],
  state: {
    isDebug:true,
    userImage:'',
    version:'220209',//首页显示的版本号
    
    // // 部署
    // userName:'',
    // passWord:'',

    // // 部署配置
    // BackService:'http://192.168.2.38:9090',
    // nginxUrl:'http://192.168.2.38:9092/',// 注意这里的端口不是网页的端口，是网络目录的地址
    // WebSock:'ws://192.168.2.38:9090',

    // 调试配置
    userName:'admin',
    passWord:'hbwj@123',
    
    //调试配置
    BackService:'http://192.168.2.12:9090',
    nginxUrl:'http://192.168.2.12:9092/',// 注意这里的端口不是网页的端口，是网络目录的地址
    WebSock:'ws://192.168.2.12:9090',


  },
  mutations: {
    //vueX 不能直接赋值，必须在这里声明
    userImage(state,payload){
      state.userImage = payload;
    },
  }
})

export default store