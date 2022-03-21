<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="11">
                <el-card style="height:850px">
                    <div>
                        <div>
                            <el-card shadow="never" style="height:100px">
                                <el-row>
                                    <el-col :span="6">
                                        <el-row>
                                            <el-col :span="11">
                                                <div>
                                                    <el-image
                                                        style="margin:8px 0px 0px 0px;float:right;width: 60px; height: 60px"
                                                        :src="IconImg.user"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="13">
                                                <div style="float:left">
                                                    <div>用户总数</div>
                                                    <div class="leftTotal">{{RomeData.userTotal}}</div>
                                                </div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="6">
                                        <el-row>
                                            <el-col :span="11">
                                                <div>
                                                    <el-image
                                                        style="margin:8px 5px 0px 0px;float:right;width: 50px; height: 50px"
                                                        :src="IconImg.cases"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="13">
                                                <div style="float:left">
                                                    <div>用例总数</div>
                                                    <div class="leftTotal">{{RomeData.caseTotal}}</div>
                                                </div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="6">
                                       <el-row>
                                            <el-col :span="11">
                                                <div>
                                                    <el-image
                                                        style="margin:8px 5px 0px 0px;float:right;width: 50px; height: 50px"
                                                        :src="IconImg.tasks"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="13">
                                                <div style="float:left">
                                                    <div>任务总数</div>
                                                    <div class="leftTotal">{{RomeData.taskTotal}}</div>
                                                </div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="6">
                                        <el-row>
                                            <el-col :span="11">
                                                <div>
                                                    <el-image
                                                        style="margin:8px 5px 0px 0px;float:right;width: 50px; height: 50px"
                                                        :src="IconImg.total"
                                                        fit="cover">
                                                    </el-image>
                                                </div>
                                            </el-col>
                                            <el-col :span="13">
                                                <div style="float:left">
                                                    <div>执行总数</div>
                                                    <div class="leftTotal">{{RomeData.executeTotal}}</div>
                                                </div>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                </el-row>
                            </el-card>
                        </div>
                        <div style="margin-top:10px">
                            <el-card shadow="never" style="height:364px">
                                <el-table
                                height="345px"
                                :data="RomeData.tableData"
                                style="width: 100%">
                                <el-table-column
                                    label="TOP 5"
                                    align= "center"
                                    width="70">
                                    <template slot-scope="scope">
                                        <div style="margin-top:10px;">
                                            <el-image v-if="scope.row.index==1" style="width: 25px; height: 25px" :src="IconImg.gold" fit="cover"></el-image>
                                            <el-image v-else-if="scope.row.index==2" style="width: 25px; height: 25px" :src="IconImg.silver" fit="cover"></el-image>
                                            <el-image v-else-if="scope.row.index==3" style="width: 25px; height: 25px" :src="IconImg.bronze" fit="cover"></el-image>
                                        </div>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    prop="userName"
                                    label="用户"
                                    align= "center"
                                    width="150">
                                </el-table-column>
                                <el-table-column
                                    label="接口/元素"
                                    width="130px"
                                    align= "center"
                                    prop="apiAndElementTotal">
                                </el-table-column>
                                <el-table-column
                                    label="用例总数"
                                    width="100px"
                                    align= "center"
                                    prop="caseTotal">
                                </el-table-column>
                                <el-table-column
                                    label="任务总数"
                                    width="100px"
                                    align= "center"
                                    prop="taskTotal">
                                </el-table-column>
                                <el-table-column
                                    label="工单总数"
                                    width="100px"
                                    align= "center"
                                    prop="workOrderTotal">
                                </el-table-column>
                                <el-table-column
                                    label="执行总数"
                                    width="100px"
                                    align= "center"
                                    prop="executeTotal">
                                </el-table-column>
                                </el-table>
                            </el-card>
                        </div>
                    </div>
                    <div style="margin-top:10px">
                        <el-card style="height:330px" shadow="never">
                            <span v-if="RomeData.noticeTime">公告:【{{RomeData.noticeTime}}】</span>
                            <span v-else>公告</span>
                            <div style="margin-top:10px;text-align:left;overflow:auto;height:270px;">
                                <span style="white-space: pre-line;" v-html="RomeData.notice"></span>
                            </div>
                        </el-card>
                    </div>

                </el-card>
            </el-col>
            <el-col :span="13">
                <el-card style="height:850px">
                    <div style="margin-left:65px">
                        <el-row :gutter="290">
                            <el-col :span="4">
                                <el-card class="btn" shadow="hover" @click.native="handleClick('API')">
                                    <el-image
                                        style="width: 150px; height: 150px"
                                        :src="IconImg.api"
                                        fit="cover">
                                    </el-image>
                                    <div class="btn-text">接口测试</div>
                                </el-card>
                            </el-col>
                            <el-col :span="4">
                                <el-card class="btn" shadow="hover" @click.native="handleClick('UI')">
                                    <el-image
                                        style="width: 150px; height: 150px"
                                        :src="IconImg.ui"
                                        fit="cover">
                                    </el-image>
                                    <div class="btn-text">功能测试(开发中)</div>
                                </el-card>
                            </el-col>
                            <el-col :span="4">
                                <el-card class="btn" shadow="hover" @click.native="handleClick('')">
                                    <el-image
                                        style="width: 150px; height: 150px"
                                        :src="IconImg.pts"
                                        fit="cover">
                                    </el-image>
                                    <div class="btn-text">梯度测试(未开始)</div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>
            </el-col>
        </el-row>
     </div>
</template>
<script>
import {PrintConsole} from "../../js/Logger.js";
import store from '../../../store/index.js';

import api from '@/assets/images/Choose/api.png';
import ui from '@/assets/images/Choose/ui.png';
import pts from '@/assets/images/Choose/pts.png';

import user from '@/assets/images/Choose/user.png';
import cases from '@/assets/images/Choose/case.png';
import tasks from '@/assets/images/Choose/task.png';
import total from '@/assets/images/Choose/total.png';

import gold from '@/assets/images/Choose/gold.png';
import silver from '@/assets/images/Choose/silver.png';
import bronze from '@/assets/images/Choose/bronze.png';

  export default {
    data() {
      return {
        IconImg:{
            //切换测试功能
            api:api,
            ui:ui,
            pts:pts,

            //左上角统计
            user:user,
            cases:cases,
            tasks:tasks,
            total:total,

            //列表牌
            gold:gold,//金
            silver:silver,//银
            bronze:bronze,//铜
        },
        RomeData:{
            notice:'',//公告
            noticeTime:'',
            userTotal:0,
            caseTotal:0,
            taskTotal:0,
            executeTotal:0,
            tableData:[
                // {'index':1,'userName':'古雨辰','apiTotal':1,'caseTotal':4,'taskTotal':3,'workOrderTotal':13,'executeTotal':10000},
                // {'index':2,'userName':'古雨辰','apiTotal':1,'caseTotal':4,'taskTotal':3,'workOrderTotal':13,'executeTotal':10000},
                // {'index':3,'userName':'古雨辰','apiTotal':1,'caseTotal':4,'taskTotal':3,'workOrderTotal':13,'executeTotal':10000},
                // {'index':4,'userName':'古雨辰','apiTotal':1,'caseTotal':4,'taskTotal':3,'workOrderTotal':13,'executeTotal':10000},
                // {'index':5,'userName':'古雨辰','apiTotal':1,'caseTotal':4,'taskTotal':3,'workOrderTotal':13,'executeTotal':10000},
            ],
        },
      };
    },
    beforeDestroy(){//生命周期-离开时
    },
    mounted(){
        this.SelectSysTotal();
        this.SelectUserTotal();
        this.SelectNoticeInfo();

    },
    methods: {
        SelectSysTotal(){//系统统计
            let self = this;
            self.$axios.get('/api/home/SelectSysTotal',{
                params:{
                   
                }
            }).then(res => {
               if(res.data.statusCode==2000){
                   self.RomeData.userTotal = res.data.userTotal;
                   self.RomeData.caseTotal = res.data.caseTotal;
                   self.RomeData.taskTotal = res.data.taskTotal;
                   self.RomeData.executeTotal = res.data.executeTotal;
               }else{
                   self.$message.error('主页系统统计获取失败:'+res.data.errorMsg);
               }
            }).catch(function (error) {
                console.log(error);
            })
        },
        SelectUserTotal(){//查询用户统计
            let self = this;
            self.$axios.get('/api/home/SelectUserTotal',{
                params:{
                   
                }
            }).then(res => {
               if(res.data.statusCode==2000){
                   self.RomeData.tableData = res.data.tableData;
               }else{
                   self.$message.error('主页用户统计获取失败:'+res.data.errorMsg);
               }
            }).catch(function (error) {
                console.log(error);
            })
        },
        SelectNoticeInfo(){//查询公告
            let self = this;
            self.$axios.get('/api/Notice/SelectNewNotice',{
                params:{

                }
            }).then(res => {
               if(res.data.statusCode==2000){
                   self.RomeData.noticeTime = res.data.noticeTime;
                   self.RomeData.notice = res.data.notice;
               }else{
                   self.$message.error('公告信息获取失败:'+res.data.errorMsg);
               }
            }).catch(function (error) {
                console.log(error);
            })
        },

        handleClick(val){//跳转类
            if(val=='API'){
                this.$router.push({path:'/SysType/Api/Home'});
            }else if(val=='UI'){
                this.$router.push({path:'/SysType/Ui/Home'});
            }
        },
    }
  };
</script>

<style>
.btn-text{
    font-size: 30px;
}
.btn{
    height: 250px;
    width: 250px;
}
.btn-div{
    margin-top: 15%;
    
}
.leftTotal{
    font-size: 25px;
    margin-top: 10px;
}
</style>
