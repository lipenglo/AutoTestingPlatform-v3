<template>
  <div ref="tab-main"  id="tab-main">
    <template>
      <div class="MainCard">
          <div>
            <el-row :gutter="10">
              <el-col :span="11">
                <div>
                  <el-card class="TopCard">
                    <div id="topline" style="width:830px;height:300px;margin-left:-20px;"></div>   
                  </el-card>
                </div>
              </el-col>
              <el-col :span="13">
                <el-card class="TopCard">
                  <div>
                    <el-table
                      height="200px"
                      :data="RomeData.pageTableData">
                      <el-table-column
                        prop="pageName"
                        align= "center"
                        label="所属页面">
                      </el-table-column>
                      <el-table-column
                        width="150px"
                        prop="apiTotal"
                        align= "center"
                        label="接口数量">
                      </el-table-column>
                      <el-table-column
                        width="150px"
                        prop="unitTotal"
                        align= "center"
                        label="单元用例">
                      </el-table-column>
                      <el-table-column
                        width="150px"
                        prop="hybridTestTotal"
                        align= "center"
                        label="混合用例">
                      </el-table-column>
                      <el-table-column
                        width="150px"
                        prop="caseTotal"
                        align= "center"
                        label="测试用例">
                      </el-table-column>
                      <!-- <el-table-column
                        width="80px"
                        prop="taskTotal"
                        align= "center"
                        label="定时任务">
                      </el-table-column>
                      <el-table-column
                        width="80px"
                        prop="batchTotal"
                        align= "center"
                        label="批量任务">
                      </el-table-column> -->
                      <!-- <el-table-column
                        width="80px"
                        prop="weekTotal"
                        align= "center"
                        label="本周新增">
                      </el-table-column>
                      <el-table-column
                        width="100px"
                        prop="performWeekTotal"
                        align= "center"
                        label="本周执行">
                      </el-table-column>
                      <el-table-column
                        width="100px"
                        prop="perforHistoryTotal"
                        align= "center"
                        label="历史执行">
                      </el-table-column> -->
                    </el-table>
                  </div>
                  <div>
                    <el-table
                      :data="RomeData.proTableData">
                      <el-table-column
                        width="185px"
                        prop="taskTotal"
                        align= "center"
                        label="定时任务">
                      </el-table-column>
                      <el-table-column
                        width="185px"
                        prop="batchTotal"
                        align= "center"
                        label="批量任务">
                      </el-table-column>
                      <el-table-column
                        width="185px"
                        prop="weekTotal"
                        align= "center"
                        label="本周新增">
                      </el-table-column>
                      <el-table-column
                        width="185px"
                        prop="performWeekTotal"
                        align= "center"
                        label="本周执行">
                      </el-table-column>
                      <el-table-column
                        width="185px"
                        prop="perforHistoryTotal"
                        align= "center"
                        label="历史执行">
                      </el-table-column>
                    </el-table>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <div style="margin-top:10px">
            <el-row :gutter="10">
              <el-col :span="11">
                <div>
                  <el-card class="DownCard">
                    <div style="margin-top:-10px">
                      <el-tag type="info">过去7天内失败TOP 10 </el-tag>
                    </div>
                    <div style="margin-top:10px">
                      <el-table
                        height="379px"
                        :data="RomeData.formerlyTableData">
                        <el-table-column
                          prop="index"
                          width="70px"
                          align= "center"
                          label="排名">
                          <template slot-scope="scope">
                              <el-tag type="danger" v-if="scope.row.index=='1'" >{{scope.row.index}}</el-tag>
                              <el-tag type="warning" v-else-if="scope.row.index=='2'">{{scope.row.index}}</el-tag>
                              <el-tag type="primary" v-else-if="scope.row.index=='3'">{{scope.row.index}}</el-tag>
                              <span v-else>{{scope.row.index}}</span>
                          </template>
                        </el-table-column>
                        <el-table-column
                          prop="taskName"
                          align= "center"
                          label="任务名称">
                        </el-table-column>
                        <el-table-column
                          prop="itsName"
                          align= "center"
                          label="所属页面/功能">
                        </el-table-column>
                        <el-table-column
                          align= "center"
                          width="100px"
                          label="任务类型">
                          <template slot-scope="scope">
                              <el-tag v-if="scope.row.taskType=='API'" > 独立接口</el-tag>
                              <el-tag type="success" v-else-if="scope.row.taskType=='CASE'" >测试用例</el-tag>
                              <el-tag type="warning" v-else-if="scope.row.taskType=='TASK'" >定时任务</el-tag>
                              <el-tag type="danger" v-else-if="scope.row.taskType=='BATCH'" >批量任务</el-tag>
                          </template>
                        </el-table-column>
                        <el-table-column
                          prop="number"
                          align= "center"
                          width="100px"
                          label="失败次数">
                        </el-table-column>
                      </el-table>
                    </div>
                  </el-card>
                </div>
              </el-col>
              <el-col :span="13">
                 <el-card class="DownCard">
                    <div style="margin-top:-10px">
                      <el-tag type="info">我的工单</el-tag>
                    </div>
                    <div style="margin-top:10px">
                    <el-table
                        height="379px"
                        :data="RomeData.myWorkTableData">
                        <el-table-column
                          label="编号"
                          prop="codeId"
                          width="70px"
                          align= "center">
                        </el-table-column>
                        <el-table-column
                          label="工单类型"
                          width="80px"
                          align= "center">
                          <template slot-scope="scope">
                            <el-tag type="success" v-if="scope.row.workType=='Add'">新增</el-tag>
                            <el-tag type="warning"  v-else-if="scope.row.workType=='Edit'">修改</el-tag>
                            <el-tag type="danger"  v-else-if="scope.row.workType=='Delete'">删除</el-tag>
                            <el-tag type="warning"  v-else-if="scope.row.workType=='BUG'">BUG</el-tag>
                            <el-tag type="info" v-else>其他</el-tag>
                          </template>
                        </el-table-column>
                        <!-- <el-table-column
                          label="所属页面/功能"
                          width="250px"
                          align= "center"
                          prop="pageNameAndfunName">
                        </el-table-column> -->
                        <el-table-column
                          label="工单名称"
                          align= "center"
                          prop="workName">
                        </el-table-column>
                        <el-table-column
                          label="工单信息"
                          show-overflow-tooltip
                          align= "center"
                          prop="message">
                        </el-table-column>
                        <el-table-column
                            label="工单状态"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="info" v-if="scope.row.workState==0">待受理</el-tag>
                                <el-tag type="danger" v-else-if="scope.row.workState==1">受理中</el-tag>
                                <el-tag type="warning" v-else-if="scope.row.workState==2">已解决</el-tag>
                                <el-tag type="success" v-else>已关闭</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="更新时间"
                            align= "center"
                            width="160px"
                            prop="updateTime">
                        </el-table-column>   
                        <el-table-column
                            label="创建者"
                            align= "center"
                            width="120px"
                            prop="createUserName">
                        </el-table-column>
                        <el-table-column
                            label="操作"
                            align="center"
                            width="80px">
                        <template slot-scope="scope" style="width:100px">
                          <el-button
                              size="mini"
                              type="warning"
                              @click="handleJump(scope.$index, scope.row)">跳转
                          </el-button>
                        </template>
                        </el-table-column>
                      </el-table>
                    </div>
                 </el-card>
              </el-col>
            </el-row>
          </div>
          <div ref="dragDiv" class="float-drag-button" v-if="dialog.queue.dialogVisible==false && dialog.myWork.dialogVisible==false">
            <span @click="OpenQueueDialog()">队列({{RomeData.queueTableData.length}})</span>
          </div>
      </div>
    </template>
    <template>
      <el-drawer
      :title="dialog.queue.dialogPara.dialogTitle"
      size="1200px"
      :visible.sync="dialog.queue.dialogVisible"
      direction='rtl'
      :before-close="closeQueueDialog">
        <div>
          <el-table
            height="850px"
            :data="RomeData.queueTableData">
            <el-table-column
              prop="taskName"
              align= "center"
              label="任务名称">
            </el-table-column>
            <el-table-column
              prop="itsName"
              align= "center"
              label="所属页面/功能">
            </el-table-column>
            <el-table-column
              width="100px"
              align= "center"
              label="任务类型">
              <template slot-scope="scope">
                  <el-tag v-if="scope.row.taskType=='API'" >接口</el-tag>
                  <el-tag type="success" v-else-if="scope.row.taskType=='CASE'" >测试用例</el-tag>
                  <el-tag type="warning" v-else-if="scope.row.taskType=='TASK'" >定时任务</el-tag>
                  <el-tag type="danger" v-else-if="scope.row.taskType=='BATCH'" >批量任务</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              width="100px"
              align= "center"
              label="任务状态">
              <template slot-scope="scope">
                  <el-tag type="info" v-if="scope.row.taskState=='0'" >未开始</el-tag>
                  <el-tag type="warning" v-else-if="scope.row.taskState=='1'" >执行中</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              prop="performProgress"
              width="100px"
              align= "center"
              label="执行进度">
            </el-table-column>
            <el-table-column
              prop="updateTime"
              width="150px"
              align= "center"
              label="发布时间">
            </el-table-column>
            <el-table-column
              prop="userName"
              width="150px"
              align= "center"
              label="发起者">
            </el-table-column>
            <el-table-column
              label="操作"
              align="center"
              width="80px">
              <template slot-scope="scope" style="width:100px">
                <el-button
                  type="info"
                  size="mini"
                  @click="handleState(scope.$index, scope.row)">取消
                </el-button>
            </template>
          </el-table-column>
          </el-table>
        </div>
      </el-drawer>
    </template>
    <template>
      <dialog-my-work
          @closeDialog="closeMyWorkDialog" 
          :isVisible="dialog.myWork.dialogVisible" 
          :dialogPara="dialog.myWork.dialogPara">
      </dialog-my-work>
    </template>
  </div>
</template>

<script>
import Qs from 'qs';
import * as echarts from 'echarts';
import store from '../../../../../store/index';
import {PrintConsole} from "../../../../js/Logger.js";

import DialogMyWork from "../../../WorkorderManagement/WorkorderMaintenance/Editor.vue";

export default {
  components: {
    DialogMyWork
  },
  data() {
    return {
        myChart_line:'',
        RomeData:{
          socket:'',
          topLine:{
            timeData:[],
            passData:[],
            failData:[],
            errorData:[],
          },
          //项目统计
          pageTableData:[
            // {'itsName':'测试页面/测试功能','apiTotal':'1000000','unitTotal':'20','caseTotal':'13','taskTotal':'30','batchTotal':'20','weekTotal':"12",'performWeek':'11','perforHistory':'30'}
          ],
          proTableData:[
          ],
          //过去7天失败错误列表
          formerlyTableData:[
            // {'index':'1','itsName':'测试页面/测试功能','taskType':'API','taskName':'查询项目','number':'999'},
            // {'index':'2','itsName':'测试页面/测试功能','taskType':'CASE','taskName':'验证项目','number':'888'},
            // {'index':'3','itsName':'测试页面/测试功能','taskType':'TASK','taskName':'查询项目','number':'777'},
            // {'index':'4','itsName':'测试页面/测试功能','taskType':'BATCH','taskName':'验证项目','number':'666'},
          ],
          //队列列表
          queueTableData:[
            // {'itsName':'测试页面/测试功能','taskType':'API','taskName':'验证项目','taskState':'0','performProgress':'1/1'},
            // {'itsName':'测试页面/测试功能','taskType':'CASE','taskName':'验证项目','taskState':'1' ,'performProgress':'2/20'},
          ],
          //我的工单
          myWorkTableData:[
            // {'codeId':'A-112','workType':'Add','message':'这你的这是个空的 因该是什么？？？？','workName':'测试上传接口问题','workState':0,'updateTime':'2021-21-12 23:22:22','createUserName':'lipenglo'},
          ],
        },
        dialog:{
          queue:{
            dialogVisible:false,
            dialogPara:{
              dialogTitle:"",//初始化标题
              isAddNew:true,//初始化是否新增\修改
            },
          },
          myWork:{
            dialogVisible:false,
            dialogPara:{
              dialogTitle:"",//初始化标题
              isAddNew:true,//初始化是否新增\修改
            },
          },
        }

    };
  },
  mounted(){
    this.myChart_line = echarts.init(document.getElementById('topline'));//初始化
    // this.topline();
    this.SelectTestResults();//测试结果总览
    this.SelectPageStatistical();//页面下的统计
    this.SelectProStatistical();//项目统计
    this.SelectFormerlyData();//过去7天内Top10
    this.SelectProQueue();//项目队列
    this.SelectMyWorkData();//我的工单

    this.PageMainDataRefresh();//当前页面的4块数据无感刷新
  },
  beforeDestroy(){//生命周期-离开时
    this.RomeData.socket.close(); //关闭TCP连接
  },
  methods: {
    SelectTestResults(){//测试结果总览
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectTestResults',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.topLine.timeData = res.data.timeData;
          self.RomeData.topLine.passData = res.data.passData;
          self.RomeData.topLine.failData = res.data.failData;
          self.RomeData.topLine.errorData = res.data.errorData;
          this.topline();
        }else{
            self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    topline(){
      let self = this;
      var option_line = {
        title: {
          text: '测试结果总览',
          left:'40'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['Pass', 'Fail', 'Error']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        // toolbox: {
        //   feature: {
        //     saveAsImage: {}
        //   }
        // },
        xAxis: {
          type: 'category',
          axisLabel: { interval: 0, rotate: 30 },//底部文字倾斜显示
          data:self.RomeData.topLine.timeData
          // data: ['Mon', 'Tue','123']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            label: {
              show: true,
              position: 'top'
            },
            name: 'Pass',
            type: 'bar',
            // stack: 'Total',
            data:self.RomeData.topLine.passData,
            // data: [
            //       {name:'2016/12/18 6:38:08', value:['2016/12/18 6:38:08', 20]},
            //       {name:'2016/12/18 16:18:18', value:['2016/12/18 16:18:18', 1]},
            //       {name:'2016/12/18 19:18:18', value:['2016/12/18 19:18:18', 1]}
            //   ],
            itemStyle: {normal: {color: '#91cc75'}} 
          },
          {
            label: {
              show: true,
              position: 'top'
            },
            name: 'Fail',
            type: 'bar',
            // stack: 'Total',
            data:self.RomeData.topLine.failData,
            // data: [
            //     {name:'2016/12/17 6:38:08', value:['2016/12/17 6:38:08', 1]},
            //     {name:'2016/12/17 16:18:18', value:['2016/12/17 16:18:18', 22]},
            //     {name:'2016/12/17 19:18:18', value:['2016/12/17 19:18:18', 44]}
            // ],
            itemStyle: {normal: {color: '#fac858'}} 
          },
          {
            label: {
              show: true,
              position: 'top'
            },
            name: 'Error',
            type: 'bar',
            // stack: 'Total',
            data:self.RomeData.topLine.errorData,
            // data: [
            //     {name:'2016/12/16 6:38:08', value:['2016/12/16 6:38:08', 1]},
            //     {name:'2016/12/16 16:18:18', value:['2016/12/16 16:18:18', 22]},
            //     {name:'2016/12/16 19:18:18', value:['2016/12/16 19:18:18', 44]}
            // ],
            itemStyle: {normal: {color: '#ee6666'}} 
          },
        ]
      };
      this.myChart_line.setOption(option_line,true);//加载属性后显示 true自动每次清除数据
    },
    SelectPageStatistical(){//页面下总览
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectPageStatistical',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.pageTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    SelectProStatistical(){//项目总览
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectProStatistical',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.proTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    SelectFormerlyData(){//过去7天内Top10
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectFormerlyData',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.formerlyTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    SelectProQueue(){//项目队列
      let self = this;
      self.$axios.get('/api/home/ApiPageHomeSelectProQueue',{
        params:{
          'proId':self.$cookies.get('proId'),
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          self.RomeData.queueTableData = res.data.dataTable;
        }else{
          self.$message.error('获取数据失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
        console.log(error);
      })
    },
    handleState(index,row){//项目队列取消
      let self = this;
      self.$axios.post('/api/home/ApiPageHomeHandleState',Qs.stringify({
        'queueId':row.id,
      })).then(res => {
        if(res.data.statusCode==2002){
          self.SelectProQueue();
        }
        else{
          self.$message.error('队列状态修改失败:'+res.data.errorMsg);
        }
      }).catch(function (error) {
          console.log(error);
      })
    },
    PageMainDataRefresh(){//当前页面的4块数据无感刷新
      let self = this;
      var socket = new WebSocket(store.state.WebSock+'/api/home/ApiPageMainDataRefresh');
      self.RomeData.socket = socket;
      socket.onopen = function () {
        PrintConsole('WebSocket open');//成功连接上Websocket
        var data ={};
        data.Message = 'Start';
        data.Params = {
          'token':self.$cookies.get('token'),
          'proId':self.$cookies.get('proId'),
        }
        socket.send(JSON.stringify(data));//发送数据到服务端
      };
      socket.onmessage = function (e) {
        // PrintConsole('message: ' + e.data);//打印服务端返回的数据
        let retData = JSON.parse(e.data)
        //测试结果总览
        self.RomeData.topLine.timeData = retData.testResults.timeData;
        self.RomeData.topLine.passData = retData.testResults.passData;
        self.RomeData.topLine.failData = retData.testResults.failData;
        self.RomeData.topLine.errorData = retData.testResults.errorData;
        self.topline();

        //页面下统计数据
        retData.pageStatistical.dataTable.forEach(d=>{
          let tempTable = self.RomeData.pageTableData.find(item=>
            item.id == d.id
          );
          if(tempTable){
            //查看是不是有差异
            if(d.pageName!=tempTable.pageName){
              tempTable.pageName = d.pageName
            }
            if(d.apiTotal!=tempTable.apiTotal){
              tempTable.apiTotal = d.apiTotal
            }
            if(d.unitTotal!=tempTable.unitTotal){
              tempTable.unitTotal = d.unitTotal
            }
            if(d.hybridTestTotal!=tempTable.hybridTestTotal){
              tempTable.hybridTestTotal = d.hybridTestTotal
            }
            if(d.caseTotal!=tempTable.caseTotal){
              tempTable.caseTotal = d.caseTotal
            }
          }else{
            self.RomeData.pageTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.pageTableData.forEach((d,index)=>{
          let tempTable = retData.pageStatistical.dataTable.find(item=>
            item.id == d.id
          );
          if(tempTable){

          }else{
            self.RomeData.pageTableData.splice(index, 1)
          }
        });

        //项目下统计数据
        retData.proStatistical.dataTable.forEach(d=>{
          let tempTable = self.RomeData.proTableData.find(item=>
            item.id == d.id
          );
          if(tempTable){
            //查看是不是有差异
            if(d.taskTotal!=tempTable.taskTotal){
              tempTable.taskTotal = d.taskTotal
            }
            if(d.batchTotal!=tempTable.batchTotal){
              tempTable.batchTotal = d.batchTotal
            }
            if(d.weekTotal!=tempTable.weekTotal){
              tempTable.weekTotal = d.weekTotal
            }
            if(d.performWeekTotal!=tempTable.performWeekTotal){
              tempTable.performWeekTotal = d.performWeekTotal
            }
            if(d.perforHistoryTotal!=tempTable.perforHistoryTotal){
              tempTable.perforHistoryTotal = d.perforHistoryTotal
            }
          }else{
            self.RomeData.pageTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.proTableData.forEach((d,index)=>{
          let tempTable = retData.proStatistical.dataTable.find(item=>
            item.id == d.id
          );
          if(tempTable){

          }else{
            self.RomeData.proTableData.splice(index, 1)
          }
        });

        //过去7天内Top10
        retData.pastSevenDaysTop.dataTable.forEach(d=>{
          let tempTable = self.RomeData.formerlyTableData.find(item=>
            item.taskName == d.taskName
          );
          if(tempTable){
            //查看是不是有差异
            if(d.index!=tempTable.index){
              tempTable.index = d.index
            }
            if(d.taskName!=tempTable.taskName){
              tempTable.taskName = d.taskName
            }
            if(d.itsName!=tempTable.itsName){
              tempTable.itsName = d.itsName
            }
            if(d.taskType!=tempTable.taskType){
              tempTable.taskType = d.taskType
            }
            if(d.number!=tempTable.number){
              tempTable.number = d.number
            }
         

          }else{
            self.RomeData.formerlyTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.formerlyTableData.forEach((d,index)=>{
          let tempTable = retData.pastSevenDaysTop.dataTable.find(item=>
            item.taskName == d.taskName
          );
          if(tempTable){

          }else{
            self.RomeData.formerlyTableData.splice(index, 1)
          }
        });

        //项目队列
        retData.proQueue.dataTable.forEach(d=>{
          let tempTable = self.RomeData.queueTableData.find(item=>
            item.id == d.id
          );
          if(tempTable){
            //查看是不是有差异
            if(d.taskName!=tempTable.taskName){
              tempTable.taskName=d.taskName
            }
            if(d.itsName!=tempTable.itsName){
              tempTable.itsName=d.itsName
            }
            if(d.taskType!=tempTable.taskType){
              tempTable.taskType=d.taskType
            }
            if(d.taskState!=tempTable.taskState){
              tempTable.taskState=d.taskState
            }
            if(d.performProgress!=tempTable.performProgress){
              tempTable.performProgress=d.performProgress
            }
            if(d.updateTime!=tempTable.updateTime){
              tempTable.updateTime=d.updateTime
            }
            if(d.userName!=tempTable.userName){
              tempTable.userName=d.userName
            }

          }else{
            self.RomeData.queueTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.queueTableData.forEach((d,index)=>{
          let tempTable = retData.proQueue.dataTable.find(item=>
            item.id == d.id
          );
          if(tempTable){

          }else{
            self.RomeData.queueTableData.splice(index, 1)
          }
        });

        //我的工单
        retData.myWork.dataTable.forEach(d=>{
          let tempTable = self.RomeData.myWorkTableData.find(item=>
            item.id == d.id
          );
          if(tempTable){
            //查看是不是有差异
            if(d.codeId!=tempTable.codeId){
              tempTable.codeId = d.codeId
            }
            if(d.workType!=tempTable.workType){
              tempTable.workType = d.workType
            }
            if(d.workName!=tempTable.workName){
              tempTable.workName = d.workName
            }
            if(d.message!=tempTable.message){
              tempTable.message = d.message
            }
            if(d.workState!=tempTable.workState){
              tempTable.workState = d.workState
            }
            if(d.updateTime!=tempTable.updateTime){
              tempTable.updateTime = d.updateTime
            }
            if(d.timeStamp!=tempTable.timeStamp){
              tempTable.timeStamp = d.timeStamp
            }
            if(d.createUserName!=tempTable.createUserName){
              tempTable.createUserName = d.createUserName
            }
          }else{
            self.RomeData.myWorkTableData.push(d);//新增数据
          }
        });
        //删除数据
        self.RomeData.myWorkTableData.forEach((d,index)=>{
          let tempTable = retData.myWork.dataTable.find(item=>
            item.id == d.id
          );
          if(tempTable){

          }else{
            self.RomeData.myWorkTableData.splice(index, 1)
          }
        });
        //排序
        self.RomeData.myWorkTableData.sort(function(p1,p2){
          return p2.timeStamp-p1.timeStamp
        });


        var data ={};
        data.Message = 'Heartbeat';
        data.Params = {
          'time':'Date()'
        }
        socket.send(JSON.stringify(data));//发送数据到服务端
          
      };
      socket.onclose=function(e){
        PrintConsole("关闭TCP连接onclose",e);
      };
      if (socket.readyState == WebSocket.OPEN) socket.onopen();       
    },

    //队列
    OpenQueueDialog(){
      let self = this;
      self.dialog.queue.dialogPara={
        dialogTitle:'项目队列',//初始化标题
        isAddNew:true,
      }
      self.dialog.queue.dialogVisible=true;
      self.SelectProQueue();//项目队列
    },
    closeQueueDialog(done){
      done();
      this.dialog.queue.dialogVisible =false;
    },

    //我的工单
    SelectMyWorkData(){
      let self = this;
      self.RomeData.myWorkTableData= [];
      self.$axios.get('/api/WorkorderManagement/SelectData',{
        params:{
            'sysType':'API',
            'myWork':'My',
            'proId':self.$cookies.get('proId'),
            'pageId':'',
            'funId':'',
            'current':1,
            'pageSize':999999999
        }
      }).then(res => {
        if(res.data.statusCode==2000){
          res.data.TableData.forEach(d => {
            let obj = {};
            obj.id = d.id;
            obj.codeId = 'A-'+d.id;
            // obj.workSource=d.workSource;
            obj.workType = d.workType;
            obj.workName = d.workName;
            obj.message=d.message;
            obj.workState=d.workState;
            obj.updateTime = d.updateTime;
            obj.timeStamp = d.timeStamp;
            obj.createUserName = d.createUserName;

            self.RomeData.myWorkTableData.push(obj);
          });
        }else{
          self.$message.error('我的工单获取数据失败:'+res.data.errorMsg);
        }
        // console.log(self.tableData);
      }).catch(function (error) {
        console.log(error);
      })
    },
    handleJump(index,row){
      PrintConsole('handleJump',row);
        let self = this;
        self.dialog.myWork.dialogPara={
          dialogTitle:"编辑工单",//初始化标题
          isAddNew:false,//初始化是否新增\修改
          workId:row.id,
        }
        self.dialog.myWork.dialogVisible=true;
    },
    closeMyWorkDialog(){
      this.dialog.myWork.dialogVisible =false;
    },
  }
};
</script>

<style>
.MainCard{
  /* height: 759px; */
  height: 770px;
}
.TopCard{
  height: 330px;
}
.DownCard{
  height: 430px;
}
.float-drag-button {
  position: absolute;
  right: 0;
  top: 43%;
  z-index: 6666;
  padding: 13px;
  width: 60px;
  opacity: 1;
  background-color: #fff;
  border-radius: 8px 0px 0px 8px;
  box-shadow: 0px 2px 15px 0px rgba(9,41,77,0.15);
  cursor: pointer;
}
</style>
