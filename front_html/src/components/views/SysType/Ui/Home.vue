<template>
  <div ref="tab-main">
    <template>
      <el-container>
        <el-header class="top-header">
          <el-row>
            <el-col :span="19">
              <el-menu
                router
                mode="horizontal"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b">
                <el-menu-item index='/SysType/Api/ProjectManagement/Main' >
                  <template slot="title" >
                    <i class="el-icon-s-home"></i>
                    <a>项目维护</a>
                  </template>
                </el-menu-item>
                <!-- <el-submenu 
                  v-for="itemLevel1 in RomeData.menuTable"
                  :index="itemLevel1.index"
                  :key="itemLevel1.menuName"
                  :disabled="itemLevel1.disPlay">
                    <template slot="title">
                      <i :class="itemLevel1.icon"></i>
                      <a>{{itemLevel1.menuName}}</a>
                    </template>
                    <el-menu-item
                      class="title"
                      v-for="item in itemLevel1.children"
                      :index="item.path" :key="item.menuName"
                      >{{item.menuName}}
                    </el-menu-item>
                </el-submenu> -->
              </el-menu>
            </el-col>
            <el-col :span="5">
                <el-row>
                  <el-col>
                    <div class="remindInfo">
                      <el-badge :value="RomeData.remindNum" :max="99">
                        <el-button size="small" type="warning" icon="el-icon-message" circle @click="OpenRemindInfo()"></el-button>
                      </el-badge>
                    </div>
                  </el-col>
                  <el-col>
                    <div class="fun-top-msg">
                      <div style="margin-top: 5px;">
                        <el-avatar :size="50" fit="fill" :src="RomeData.userImage"></el-avatar>
                      </div>
                      <div class="top-userName">
                        <el-dropdown trigger="click" @command="handleCommand">
                          <span style="color:white">{{RomeData.nickName}}
                            <i class="el-icon-caret-bottom el-icon--right"></i>
                          </span>
                          <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item command="userinfo">个人信息</el-dropdown-item>
                            <el-dropdown-item command="close">退出登录</el-dropdown-item>
                          </el-dropdown-menu>
                        </el-dropdown>
                      </div>
                    </div>
                  </el-col>
               </el-row>
            </el-col>
          </el-row>
        </el-header>
        <el-main class="down-main">
          <el-card class="Router-Card">
            <el-row :gutter="500">
              <el-col :span="12">
                <div class="Router-Text">
                  <template>
                    <el-breadcrumb class="app-breadcrumb" separator-class="el-icon-arrow-right">
                      <el-breadcrumb-item v-for="(item)  in levelList" :key="item.path" :v-if="item.meta.title">
                          <router-link :to="item.redirect||item.path">{{item.meta.title}}</router-link>
                      </el-breadcrumb-item>
                    </el-breadcrumb>
                  </template>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="Listens-Text">
                  <el-row :gutter="20">
                    <el-col :span="6">
                      <el-row :gutter="20">
                        <el-col :span="6">
                          <label>CPU:</label>
                        </el-col>
                        <el-col :span="18">
                          <div>
                            <el-progress :text-inside="true" :stroke-width="17" :percentage="ServerPerformance.cpu" :status="ServerPerformance.cpuStatus"></el-progress>
                          </div>
                        </el-col>
                      </el-row>
                    </el-col>
                    <el-col :span="6">
                      <el-row :gutter="20">
                        <el-col :span="6">
                          <label>Mem:</label>
                        </el-col>
                        <el-col :span="18">
                          <div>
                            <el-progress :text-inside="true" :stroke-width="17" :percentage="ServerPerformance.mem" :status="ServerPerformance.memStatus"></el-progress>
                          </div>
                        </el-col>
                      </el-row>
                    </el-col>
                    <el-col :span="6">
                      <el-row :gutter="20">
                        <el-col :span="6">
                          <label>Celery:</label>
                        </el-col>
                        <el-col :span="18">
                          <div>
                            <el-progress :stroke-width="17" :percentage="100" :status="ServerPerformance.celery"></el-progress>
                          </div>
                        </el-col>
                      </el-row>
                    </el-col>
                    <el-col :span="6">
                      <el-row :gutter="20">
                        <el-col :span="4">
                          <label>Beat:</label>
                        </el-col>
                        <el-col :span="18">
                          <div>
                            <el-progress :stroke-width="17" :percentage="100" :status="ServerPerformance.celeryBeat"></el-progress>
                          </div>
                        </el-col>
                      </el-row>
                    </el-col>
                  </el-row>
                </div>
              </el-col>
            </el-row>
          </el-card>
          <div style="margin-top:5px;">
            <el-tabs v-model="activeTab" type="card" @tab-remove="removeTab" @tab-click="tabClick">
              <el-tab-pane v-for="item in tabsItem"
                            :key="item.name"
                            :label="item.title"
                            :name="item.name"
                            :closable="item.closable"
                            :ref="item.ref">
                <component :is="item.content"></component>
              </el-tab-pane>
            </el-tabs>
            <!-- <router-view></router-view> -->
          </div>
        </el-main>
      </el-container>
    </template>
    <template>
      <dialog-user-info
          @closeDialog="closeDialog_UserInfo" 
          :isVisible="dialog.userinfo.dialogVisible" 
          :dialogPara="dialog.userinfo.dialogPara">
      </dialog-user-info>
    </template>
    <template>
      <dialog-remind-info
          @closeDialog="closeRemindInfoDialog" 
          :isVisible="dialog.remindInfo.dialogVisible" 
          :dialogPara="dialog.remindInfo.dialogPara"
          @getData="updateRemindNum($event)">
      </dialog-remind-info>
    </template>
  </div>
</template>

<script>
import store from '../../../../store/index';
import {PrintConsole} from "../../../js/Logger.js";
import DialogUserInfo from "../../Home/UserInfo.vue";
import DialogRemindInfo from "../../Home/RemindInfo.vue";

//所有需要在tabs中显示的页面都必须在这里引用一次
import Ui_ProjectManagement from '@/components/views/SysType/Ui/ProjectManagement/Main';

export default {
  components: {
    DialogUserInfo,DialogRemindInfo,
    Ui_ProjectManagement
  },
  data() {
    return {
      activeTab: '1',
      tabIndex: 1,
      tabsItem: [
        {
          title: '项目维护',
          name: '1',
          closable: false,
          ref: 'tabs',
          content: Ui_ProjectManagement
      }],
      tabsPath: [
        {
        name: "1",
        path: '/SysType/Ui/ProjectManagement/Main'
      }
      ],
      levelList: [],//面包屑
      RomeData:{
        nickName:'',
        userImage:'',
        menuTable:[],
        remindNum:0
      },
      ServerPerformance:{
        socket:'',
        cpu:0,
        mem:0,
        cpuStatus:'exception',
        memStatus:'exception',
        
        celery:'exception',//异步服务
        celeryBeat:'exception',//定时任务服务
        },
      dialog:{
        userinfo:{
          dialogVisible:false,
          dialogPara:{
            dialogTitle:"",//初始化标题
          },
        },
        remindInfo:{
          dialogVisible:false,
          dialogPara:{
            dialogTitle:"",//初始化标题
          },
        }
      },
    }
  },
  mounted (){
    this.getBreadcrumb();
    // this.GetApiPermissions();
    this.LoadUserInfo();
    this.CreateSocket();
  },
  beforeDestroy(){//生命周期-离开时
      this.ServerPerformance.socket.close(); //关闭TCP连接
  },
  watch: {
    $route: function (to) {
      //刷新时并不会调用此地方
      this.getBreadcrumb();//面包屑
      //监听路由的变化，动态生成tabs
      // console.log('to',to);
      // console.log('activeTab',this.activeTab)
      let flag = true; //判断是否需要新增页面
      const path = to.path;

      // console.log('to.meta.length',Object.keys(to.meta).length)
      if (Object.keys(to.meta).length != 0) {
        for (let i = 0; i < this.$refs.tabs.length; i++) {
          if (i != 0) {
            //首页不判断 如果页面已存在，则直接定位当页面，否则新增tab页面
            // console.log('label',this.$refs.tabs[i].label)
            if (this.$refs.tabs[i].label == to.meta.name) {
              // console.log('this.$refs.tabs[i].name',this.$refs.tabs[i].name);
              this.activeTab = this.$refs.tabs[i].name; //定位到已打开页面
              flag = false;
              break;
            }
          }
        }
        //新增页面
        if (flag) {
          PrintConsole('开始新增')
          //获得路由元数据的name和组件名
          const thisName = to.meta.name; //在index.js中定义的meta
          const thisComp = to.meta.comp;
          //对tabs的当前激活下标和tabs数量进行自加
          let newActiveIndex = ++this.tabIndex + "";
          //动态双向追加tabs
          this.tabsItem.push({
            title: thisName,
            name: String(newActiveIndex),
            closable: true,
            flag:false,
            ref: "tabs",
            content: thisComp,
          });
          this.activeTab = newActiveIndex;
          /*
          * 当添加tabs的时候，把当前tabs的name作为key，path作为value存入tabsPath数组中
          * ///后面需要得到当前tabs的时候可以通过当前tabs的name获得path
          * */
          if (this.tabsPath.indexOf(path) == -1) {
            this.tabsPath.push({
              name: newActiveIndex,
              path: path,
            });
          }
        }
      }else{
        this.activeTab = '1';//首页
      }
    },
  },
  methods: {
    getBreadcrumb() {//面包屑
      this.levelList = [];
      let matched = this.$route.matched.filter(item => item.name)  // this.$route.matched 可以获取到一个数组，包含当前路由的所有嵌套路径片段的路由记录
      PrintConsole('matched');
      PrintConsole(matched);
      matched.forEach(d=>{
        // console.log('d',d)
        if(d.path=='/SysType/Ui/Home'){
          this.levelList.push({path: '/Choose', meta: { title: '测试系统(功能)'}})
          this.levelList.push({path: '', meta: {title: '项目维护' }})
          // this.levelList.push({path: '/SysType/Api/ProjectManagement/Main', meta: {title: '项目管理' }})
          // this.levelList.push({path: '/TestType_Fun/index', meta: { title: '首页' }})
        }
        else{
          this.levelList.push({path: d.path, meta: { title: d.meta.name }});
        }
      });
    },
    QuitUser(){
      this.$cookies.remove('token');
      this.$router.push({ path:'/'  })
    },
    handleCommand(command){
      let self = this;
      if (command=="close"){
        self.QuitUser();
      }
      else if(command=="userinfo"){
        self.OpenDialog_UserInfo();
      }
    },
    //选项卡
    removeTab(targetName) { //删除Tab
      PrintConsole('targetName',targetName)
      PrintConsole('activeTab',this.activeTab)
      let tabs = this.tabsItem; //当前显示的tab数组
      let activeName = this.activeTab; //点前活跃的tab

      //如果当前tab正活跃 被删除时执行
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
              this.tabClick(nextTab)
            }
          }
        });
      }
      this.activeTab = activeName;
      this.tabsItem = tabs.filter(tab => tab.name !== targetName);
      //在tabsPath中删除当前被删除tab的path
      this.tabsPath = this.tabsPath.filter(item => item.name !== targetName)
    },
    tabClick(thisTab) {//点击tabs
      /*
      * thisTab:当前选中的tabs的实例
      * 通过当前选中tabs的实例获得当前实例的path 重新定位路由
      * */
      let val = this.tabsPath.filter(item => thisTab.name == item.name)
      this.$router.push({ path: val[0].path})
    },
    CreateSocket(){//创建socket连接 获取数据 这里获取2个服务器和1个错误信息的数据
      let self = this;
      var socket = new WebSocket(store.state.WebSock+'/api/home/GetServerIndicators');
      self.ServerPerformance.socket = socket;
      
      socket.onopen = function () {
          PrintConsole('WebSocket open');//成功连接上Websocket
          var data ={};
          data.Message = 'Start';
          data.Params = {
              'token':self.$cookies.get('token')
          }
          socket.send(JSON.stringify(data));//发送数据到服务端
      };
      socket.onmessage = function (e) {
          // PrintConsole('message: ' + e.data);//打印服务端返回的数据
          let retData = JSON.parse(e.data)
          self.RomeData.remindNum=retData.pushCount;
          let cpu = retData.cpu;
          self.ServerPerformance.cpu=cpu;
          if(cpu>=80 && cpu<90){
            self.ServerPerformance.cpuStatus='warning';
          }
          else if(cpu>=90){
            self.ServerPerformance.cpuStatus='exception';
          }
          else{
            self.ServerPerformance.cpuStatus='success';
          }

          let mem = retData.mem;
          self.ServerPerformance.mem=mem;
          if(mem>=80 && mem<90){
            self.ServerPerformance.memStatus='warning';
          }
          else if(mem>=90){
            self.ServerPerformance.memStatus='exception';
          }
          else{
            self.ServerPerformance.memStatus='success';
          }

          //celery服务
          if(retData.celery){
            self.ServerPerformance.celery = 'success';
          }else{
            self.ServerPerformance.celery = 'exception';
          }
          if(retData.celeryBeat){
            self.ServerPerformance.celeryBeat = 'success';
          }else{
            self.ServerPerformance.celeryBeat = 'exception';
          }

          var data ={};
          data.Message = 'Heartbeat';
          data.Params = {
              'time':'Date()'
          }
          socket.send(JSON.stringify(data));//发送数据到服务端
      };
      socket.onclose=function(e){
          PrintConsole("关闭TCP连接onclose",e);
          socket.close(); //关闭TCP连接
          // //10次重连
          // for(let i=1;i<=11;i++){
          //     PrintConsole("正在重连",i);
          //     self.CreateSocket();
          // }
      };
      if (socket.readyState == WebSocket.OPEN) socket.onopen();       
    },

    closeDialog_UserInfo(){
      this.dialog.userinfo.dialogVisible =false;
    },
    OpenDialog_UserInfo(){
      let self = this;
      self.dialog.userinfo.dialogPara={
        dialogTitle:"个人信息",//初始化标题
      }
      self.dialog.userinfo.dialogVisible=true;
    },
    LoadUserInfo(){//基本信息
      let self = this;
      // PrintConsole(store.state)
      self.RomeData.nickName = self.$cookies.get('nickName');
      self.RomeData.userImage = 'data:image/png;base64,'+store.state.userImage;
      self.$router.push('/SysType/Ui/ProjectManagement/Main');
    },
    OpenRemindInfo(){
      let self = this;
      self.dialog.remindInfo.dialogPara={
        dialogTitle:"",//初始化标题
      }
      self.dialog.remindInfo.dialogVisible=true;
    },
    closeRemindInfoDialog(){
      this.dialog.remindInfo.dialogVisible =false;
    },
    updateRemindNum(event){//关闭推送消失时，回调传参数给首页的提醒数量
      PrintConsole(event);
      this.RomeData.remindNum=event;
    },
  }
}

</script>

<style>
.top-header{
  background-color: #545c64
}
.down-main{
  border-radius: 0px;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04); */
  box-shadow: 0 1px 1px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  /* height: 870px; */
  /* background-color: rgb(235, 237, 240); */
}
.top-userName{
  margin-top: 20px;
  margin-left: 10px;
}
.top-msg{
  font-size: 12px;
  height: 60px;
  display: flex; 
  justify-content: flex-end; 
  background-color:#545c64;
}
.remindInfo{
  margin-top: 18px;
  /* float: right; */
}
.Router-Card{
  margin-top: -15px;
  height: 30px;
}
.Router-Text{
  margin-top: -12px;
  text-align: left;
}
.Listens-Text{
  margin-top: -14px;
  /* text-align: right; */
  /* width: 600px; */
}
.fun-top-msg{
  margin-top: -50px;
  font-size: 12px;
  height: 60px;
  display: flex; 
  justify-content: flex-end; 
  background-color:#545c64;
}
</style>