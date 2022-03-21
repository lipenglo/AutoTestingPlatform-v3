<template>
  <div ref="tab-main">
    <template>
      <el-container>
        <el-header class="top-header">
          <el-row>
            <el-col :span="19">
              <el-menu
                mode="horizontal"
                @select="handleSelect"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b">
                <el-menu-item index="0" >
                  <template slot="title" >
                    <i class="el-icon-star-off"></i>
                    <a>Home</a>
                  </template>
                </el-menu-item>
                <el-submenu 
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
                      :index="item.index" :key="item.menuName"
                      >{{item.menuName}}
                    </el-menu-item>
                </el-submenu>
                <!-- <el-menu-item
                  v-for="itemLevel1 in RomeData.menuTable"
                  :index="itemLevel1.index"
                  :key="itemLevel1.menuName">
                  {{itemLevel1.menuName}}
                </el-menu-item> -->
                <!-- <el-menu-item index="0" >
                  <template slot="title" >
                    <i class="el-icon-star-off"></i>
                    <a>Home</a>
                  </template>
                </el-menu-item>
                <el-submenu index="2" :disabled="MenuDisPlay.Setting">
                  <template slot="title">
                    <i class="el-icon-setting"></i>
                    <a>Setting</a>
                  </template>
                    <el-menu-item
                      class="title"
                      v-for="item in MenuTable.Setting"
                      :index="item.index" :key="item.menuName"
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
          <div>
            <!-- 留坑，非常重要 -->
            <router-view></router-view>
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
import store from '../../../store/index'
import {PrintConsole} from "../../js/Logger.js";
import DialogUserInfo from "./UserInfo.vue";
import DialogRemindInfo from "../Home/RemindInfo.vue";

export default {
  components: {
    DialogUserInfo,DialogRemindInfo
  },
  data() {
    return {
      RomeData:{
        socket:'',
        nickName:'',
        userImage:'',
        menuTable:[],
        remindNum:0
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
    this.LoadUserInfo();
    this.GetHomePermissions();
    this.getUserStatisticsInfo();
    this.SelectRemindInfoData();

    // //定时执行
    // this.RemindInfoData = setInterval(() => {
    //   setTimeout(, 0)}, 1000*3
    // );
  },
  beforeDestroy(){//生命周期-离开时
    // clearInterval(this.RemindInfoData);
  },
  watch:{

  },
  methods: {
    handleSelect(key, keyPath) {//点击菜单跳转页面
      PrintConsole(key);
      let self = this;
      if(key=='0'){
        self.$router.push('/Choose');
      }else{
        self.GetRouterPath(key).then(d => {//这种方法用来遵守执行顺序
          switch(key){
            case key:
              this.$router.push(d);
              break;
          }
        });
      }
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
      self.$axios.get('/api/home/LoadUserInfo', {
        params:{}
      }).then(res => {
        if(res.data.statusCode==2000){
          this.$cookies.set('nickName',res.data.baseInfo.nickName,"0") 
          self.RomeData.nickName = this.$cookies.get('nickName');
          if(res.data.baseInfo.userImg){
            self.$store.commit("userImage",res.data.baseInfo.userImg);
            self.RomeData.userImage = 'data:image/png;base64,'+store.state.userImage ;
          }
          self.$router.push('/Choose');
        }else{
          self.$message.error('用户数据获取失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
        console.log(error);
      })
    },
    GetHomePermissions(){//加载用户菜单和权限信息
      let self = this;
      self.$axios.get('/api/home/GetHomePermissions', {
        params:{}
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.menuTable = res.data.menuTable;
          // res.data.menuTable.forEach(d => {
          //   if(d.menuName=='Setting'){
          //     self.MenuDisPlay.Setting = d.disPlay;
          //     self.MenuTable.Setting = d.children;
          //   }
          // });
        }else{
          self.$message.error(':'+res.data.errorMsg);
        }
      }).catch(function (error) {
        console.log(error);
      })
    },
    GetRouterPath(key){//获取二级菜单页面地址
        let self = this;
        return self.$axios.get('/api/home/GetRouterPath',{
            params:{
              'sysType':'Home',
              'index':key,
            }
          }).then(res => {
            if(res.data.statusCode==2000){
              return res.data.routerPath;
            }else{
              self.$message.error(res.data.errorMsg);
            }
          }).catch(function (error) {
            console.log(error);
          })
    },
    getUserStatisticsInfo(){
      let self = this;
      self.$axios.get('/api/home/GetUserStatisticsInfo', {
        params:{}
      }).then(res => {
        if(res.data.statusCode==2000){
          self.$notify({
            title: '欢迎 '+self.$cookies.get('userName')+' 登录',
            dangerouslyUseHTMLString: true,
            message: res.data.message,
            position: 'bottom-right'
          });
        }else{
          self.$message.error('用户统计数据获取失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
        console.log(error);
      })
       
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
    SelectRemindInfoData(){//刷新列表数据
      let self = this;
      self.$axios.get('/api/info/UserOperationalInfo',{
          params:{
            'current':1,
            'pageSize':9999
          }
      }).then(res => {
        if(res.data.statusCode==2000){
            self.RomeData.remindNum = res.data.Total;
        }else{
            // self.$message.error('操作信息获取失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
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
  /* height: 8px; */
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
.fun-top-msg{
  margin-top: -50px;
  font-size: 12px;
  height: 60px;
  display: flex; 
  justify-content: flex-end; 
  background-color:#545c64;
}
</style>