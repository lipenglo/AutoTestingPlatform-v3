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
                      prop="elementTotal"
                      align= "center"
                      label="元素数量">
                    </el-table-column>
                    <el-table-column
                      width="150px"
                      prop="caseTotal"
                      align= "center"
                      label="测试用例">
                    </el-table-column>
                    <el-table-column
                      width="150px"
                      prop="taskTotal"
                      align= "center"
                      label="定时任务">
                    </el-table-column>
                    <el-table-column
                      width="150px"
                      prop="batchTotal"
                      align= "center"
                      label="批量任务">
                    </el-table-column>
                  </el-table>
                </div>
                <div>
                  <el-table
                    :data="RomeData.proTableData">
                    <el-table-column
                      prop="weekTotal"
                      align= "center"
                      label="本周新增">
                    </el-table-column>
                    <el-table-column
                      prop="performWeekTotal"
                      align= "center"
                      label="本周执行">
                    </el-table-column>
                    <el-table-column
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
                      height="389px"
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
                      height="389px"
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
    
   
  },
  beforeDestroy(){//生命周期-离开时

  },
  methods: {
    
  }
};
</script>

<style>
.MainCard{
  /* height: 759px; */
  height: 775px;
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
