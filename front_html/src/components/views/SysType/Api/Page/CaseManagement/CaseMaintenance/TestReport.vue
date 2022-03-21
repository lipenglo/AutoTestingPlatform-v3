<template>
    <div>
        <template>
            <el-drawer
                :title="dialogTitle"
                size="1300px"
                :visible.sync="dialogVisible"
                direction="rtl"
                :before-close="dialogClose">
                <el-card 
                style="height:870px"
                v-loading="loading"
                element-loading-text="拼命返回请求信息中"
                element-loading-spinner="el-icon-loading">
                    <div>
                        <el-card style="height:250px" shadow="never">
                            <el-row>
                                <el-col :span="12">
                                    <el-row>
                                        <el-col :span="12">
                                            <div style="margin:-55px 0 0 30px;" id="EchartContainer-pie" class="EchartContainer-pie"></div>   
                                        </el-col>
                                        <el-col :span="12">
                                            <div style="margin:18px 0 0 80px;">
                                                <div style="font-size: 14px;">{{RomeData.topData.leftData.passTotal}}</div>
                                                <div style="font-size: 14px;margin:8px">{{RomeData.topData.leftData.failTotal}}</div>
                                                <div style="font-size: 14px;margin:8px">{{RomeData.topData.leftData.errorTotal}}</div>
                                                <div style="font-size: 14px;margin:8px">{{RomeData.topData.leftData.failedTotal}}</div>
                                            </div>
                                        </el-col>
                                    </el-row>
                                </el-col>
                                <el-col :span="12">
                                    <div style="text-align: left;margin:43px 0 0 -40px">
                                        <div class="TopMargin">
                                            <el-row>
                                                <el-col :span="6">
                                                    <strong>实时耗时</strong>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div><strong>{{RomeData.topData.rightData.cumulativeTime}} 秒</strong></div>
                                                </el-col>
                                            </el-row>
                                        </div>
                                        <div class="TopMargin">
                                            <el-row>
                                                <el-col :span="6">
                                                    <strong>前置操作数</strong>
                                                </el-col>
                                                <el-col :span="4">
                                                    <div>总:<strong>{{RomeData.topData.rightData.preOperationTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>成功:<strong>{{RomeData.topData.rightData.prePassTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>失败:<strong>{{RomeData.topData.rightData.preFailTotal}}</strong></div>
                                                </el-col>
                                                <!-- <el-col :span="4">
                                                    <div>错误:<strong>{{RomeData.topData.rightData.preErrorTotal}}</strong></div>
                                                </el-col> -->
                                            </el-row>
                                        </div>
                                        <div class="TopMargin">
                                            <el-row>
                                                <el-col :span="6">
                                                    <strong>后置操作数</strong>
                                                </el-col>
                                                <el-col :span="4">
                                                    <div>总:<strong>{{RomeData.topData.rightData.rearOperationTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>成功:<strong>{{RomeData.topData.rightData.rearPassTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>失败:<strong>{{RomeData.topData.rightData.rearFailTotal}}</strong></div>
                                                </el-col>
                                                <!-- <el-col :span="4">
                                                    <div>错误:<strong>{{RomeData.topData.rightData.rearErrorTotal}}</strong></div>
                                                </el-col> -->
                                            </el-row>
                                        </div>
                                        <div class="TopMargin">
                                            <el-row>
                                                <el-col :span="6">
                                                    <strong>提取数</strong>
                                                </el-col>
                                            <el-col :span="4">
                                                    <div>总:<strong>{{RomeData.topData.rightData.extractTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>成功:<strong>{{RomeData.topData.rightData.extractPassTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>失败:<strong>{{RomeData.topData.rightData.extractFailTotal}}</strong></div>
                                                </el-col>
                                            </el-row>
                                        </div>
                                        <div class="TopMargin">
                                            <el-row>
                                                <el-col :span="6">
                                                    <strong>断言数</strong>
                                                </el-col>
                                                <el-col :span="4">
                                                    <div>总:<strong>{{RomeData.topData.rightData.assertionsTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>成功:<strong>{{RomeData.topData.rightData.assertionsPassTotal}}</strong></div>
                                                </el-col>
                                                <el-col :span="5">
                                                    <div>失败:<strong>{{RomeData.topData.rightData.assertionsFailTotal}}</strong></div>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-col>
                            </el-row>
                        </el-card>
                    </div>
                    <div style="margin-top:10px">
                    <el-table
                        :data="RomeData.tableData"
                        height="570px"
                        border>
                        <el-table-column
                            label="步骤排序"
                            width="80px"
                            align= "center"
                            prop="index">
                        </el-table-column>
                        <el-table-column
                            label="测试名称"
                            width="350px"
                            align= "center"
                            prop="testName">
                        </el-table-column>
                        <el-table-column
                            label="接口类型"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.requestType=='GET'" >GET</el-tag>
                                <el-tag type="warning" v-else-if="scope.row.requestType=='POST'">POST</el-tag>
                                <el-tag type="info" v-else>{{scope.row.requestType}}</el-tag>
                            </template>
                        </el-table-column>    
                        <el-table-column
                            label="接口地址"
                            align= "center"
                            prop="apiUrl">
                        </el-table-column>
                        <el-table-column
                            label="状态码"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.code==200" >{{scope.row.code}}</el-tag>
                                <el-tag type="danger" v-else>{{scope.row.code}}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="耗时"
                            align= "center"
                            width="100px">
                            <template slot-scope="scope">
                                <div v-bind:style="{color:scope.row.timeConsuming<=5000 ? '#91cc75' : '#fac858'}">{{scope.row.timeConsuming}} ms</div>
                                <!-- <el-tag type="success">{{scope.row.timeConsuming}} ms</el-tag> -->
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="报告状态"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag v-if="scope.row.reportState=='Pass'" type="success">通过</el-tag>
                                <el-tag v-else-if="scope.row.reportState=='Fail'" type="warning">失败</el-tag>
                                <el-tag v-else type="danger">错误</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="详情"
                            align="center"
                            width="100px">
                        <template slot-scope="scope" style="width:100px">
                            <el-button
                                type="warning"
                                size="mini"
                                @click="OpendDetailsDialog(scope.$index, scope.row)">详情</el-button>
                        </template>
                        </el-table-column>
                    </el-table>
                    </div>
                </el-card>                        
            </el-drawer>
        </template>
        <template>
            <dialog-test-report
                @closeDialog="closeTestReportDialog" 
                :isVisible="dialog.testReport.dialogVisible" 
                :dialogPara="dialog.testReport.dialogPara">
            </dialog-test-report>
        </template>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import Qs from 'qs';
import store from '../../../../../../../store/index'
import {PrintConsole} from "../../../../../../js/Logger.js";
import DialogTestReport from "../ApiMaintenance/TestReport.vue";

export default {
    components: {
        DialogTestReport
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,  
            loading:false,
            MyChart_pie:'',
            socket:"",
            RomeData:{
                topData:{//头部数据
                    leftData:{
                        passTotal:0,//成功数
                        failTotal:0,//失败数
                        errorTotal:0,//错误数
                        passRate:0,//通过率
                        failedTotal:0,//未执行
                    },
                    rightData:{
                        cumulativeTime:0,//实时耗时，累计时间

                        preOperationTotal:0,
                        prePassTotal:0,
                        preFailTotal:0,
                        // preErrorTotal:0,

                        rearOperationTotal:0,
                        rearPassTotal:0,
                        rearFailTotal:0,
                        // rearErrorTotal:0,
                        
                        extractTotal:0,
                        extractPassTotal:0,
                        extractFailTotal:0,

                        assertionsTotal:0,
                        assertionsPassTotal:0,
                        assertionsFailTotal:0,
                    },
                },
                tableData:[],
            },
            dialog:{
                testReport:{//运行过程
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
            },

   
        };
    },
    props:[//main页面在引用editor时 必须声明所需要调用的属性
        'isVisible','dialogPara'
    ],
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        isVisible:{//用于监听父页面的isVisible，true时就弹出窗口
            handler(newval,oldval)
            {
                this.dialogVisible=newval;
            }
        },
        dialogPara:{
            handler(newval,oldval)
            {
                PrintConsole('newval',newval);
                this.ClearRomeData();
                this.dialogTitle = newval.dialogTitle;
                if(newval.runType=='Synchronous'){//同步时才加载 DOM
                    this.$nextTick(function () {//当DOM加载完成后才会执行这个!
                        this.MyChart_pie = echarts.init(document.getElementById('EchartContainer-pie'));//初始化
                        this.PieChart();
                    });
                }
                this.runCase(newval.runType,newval.caseId,newval.environmentId);
            }
        },
    },
    mounted(){  
        

    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.RomeData.topData.leftData.passTotal = 0;
            self.RomeData.topData.leftData.failedTotal = 0;
            self.RomeData.topData.rightData.preOperationTotal = 0;
            self.RomeData.topData.rightData.rearOperationTotal = 0;
            self.RomeData.topData.rightData.extractTotal = 0;
            self.RomeData.topData.rightData.assertionsTotal =0;
            self.RomeData.topData.rightData.passRate =0;


            self.RomeData.topData.rightData.cumulativeTime=0;
            self.RomeData.topData.rightData.preOperationTotal=0;
            self.RomeData.topData.rightData.prePassTotal=0;
            self.RomeData.topData.rightData.preFailTotal=0;
            // self.RomeData.topData.rightData.preErrorTotal=0;
            self.RomeData.topData.rightData.rearOperationTotal=0;
            self.RomeData.topData.rightData.rearPassTotal=0;
            self.RomeData.topData.rightData.rearFailTotal=0;
            // self.RomeData.topData.rightData.rearErrorTotal=0;
            self.RomeData.topData.rightData.extractTotal=0;
            self.RomeData.topData.rightData.extractPassTotal=0;
            self.RomeData.topData.rightData.extractFailTotal=0;
            self.RomeData.topData.rightData.assertionsTotal=0;
            self.RomeData.topData.rightData.assertionsPassTotal=0;
            self.RomeData.topData.rightData.assertionsFailTotal=0;

            self.RomeData.tableData=[];
        },
        PieChart(){
            let self = this;
            var option = {//设置各属性和数据
                tooltip: {
                    trigger: 'item', //通过哪种方式触发tip
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    top: 70,
                    orient: 'vertical',
                    left: 'right',
                },
                series:[{
                    name: '测试统计',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    center: ['50%', '60%'],//好像是位置
                    label:{//中间文字配置
                        normal:{
                            show:true,
                            position:'center',
                            // color:'#9A9EBA',
                            fontSize:'17px',
                            formatter:'通过率\n'+self.RomeData.topData.leftData.passRate+'%',
                            emphasis:{//中间文字显示
                                show:true
                            }
                        }
                    },
                    data:[
                        {"value": self.RomeData.topData.leftData.passTotal, "name": 'Pass', "itemStyle": {"normal": {"color": '#91cc75'}}},
                        {"value": self.RomeData.topData.leftData.failTotal, "name": 'Fail', "itemStyle": {"normal": {"color": '#fac858'}}},
                        {"value": self.RomeData.topData.leftData.errorTotal, "name": 'Error', "itemStyle": {"normal": {"color": '#ee6666'}}},
                        {"value": self.RomeData.topData.leftData.failedTotal, "name": 'Failed', "itemStyle": {"normal": {"color": '#D3D3D3'}}},
                    ],
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }] 
            };
            this.MyChart_pie.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
        runCase(runType,caseId,environmentId){
            let self = this;
            self.executeCase(runType,caseId,environmentId).then(res=>{
                if(res){
                    if(runType=="Synchronous"){
                        self.RomeData.topData.leftData.failedTotal = res.leftData.failedTotal;
                        self.RomeData.topData.rightData.preOperationTotal = res.rightData.preOperationTotal;
                        self.RomeData.topData.rightData.rearOperationTotal = res.rightData.rearOperationTotal;
                        self.RomeData.topData.rightData.extractTotal = res.rightData.extractTotal;
                        self.RomeData.topData.rightData.assertionsTotal = res.rightData.assertionsTotal;
                    
                        self.CreateSocket(res.redisKey,res.leftData.failedTotal);
                        self.loading=false;
                    }
                }else{
                    // self.dialogClose();
                }
            });
        },
        executeCase(runType,caseId,environmentId){//执行用例,先获取到用例的基本数据赋值,之后由异步继续执行
            let self = this;
            self.loading=true;
            return self.$axios.post('/api/ApiCaseMaintenance/ExecuteCase',Qs.stringify({
                'runType':runType,
                'caseId':caseId,
                'environmentId':environmentId,
            })).then(res => {
                if(res.data.statusCode==2001){
                    return res.data;
                }else{
                    self.$message.error('测试用例运行失败:'+res.data.errorMsg);
                    self.loading=false;
                    self.dialogClose();
                }
            }).catch(function (error) {
                self.$message.error('测试用例运行失败:'+error);
                console.log(error);
                self.loading=false;
                self.dialogClose();
            })
        },
        CreateSocket(redisKey,caseTotal){//创建socket连接
            let self = this;
            var socket = new WebSocket(store.state.WebSock+'/api/ApiCaseMaintenance/ReadCaseResult');
            self.socket = socket;
            
            socket.onopen = function () {
                PrintConsole('WebSocket open');//成功连接上Websocket
                var data ={};
                data.Message = 'Start';
                data.Params = {
                    'redisKey':redisKey
                }
                socket.send(JSON.stringify(data));//发送数据到服务端
                self.$message.success('任务ID:'+redisKey+',请求已建立,请耐心等待返回结果!');
            };
            socket.onmessage = function (e) {
                PrintConsole('message: ' + e.data);//打印服务端返回的数据
                let retData = JSON.parse(e.data)
                //leftData
                self.RomeData.topData.leftData.passTotal = retData.topData.leftData.passTotal;
                self.RomeData.topData.leftData.failTotal = retData.topData.leftData.failTotal;
                self.RomeData.topData.leftData.errorTotal = retData.topData.leftData.errorTotal;
                self.RomeData.topData.leftData.passRate = retData.topData.leftData.passRate;
                self.RomeData.topData.leftData.failedTotal = retData.topData.leftData.failedTotal;
                self.PieChart();

                //rightData
                self.RomeData.topData.rightData.cumulativeTime = retData.topData.rightData.runningTime;

                self.RomeData.topData.rightData.prePassTotal = retData.topData.rightData.prePassTotal;
                self.RomeData.topData.rightData.preFailTotal = self.RomeData.topData.rightData.preOperationTotal- retData.topData.rightData.prePassTotal;

                self.RomeData.topData.rightData.rearPassTotal = retData.topData.rightData.rearPassTotal;
                self.RomeData.topData.rightData.rearFailTotal = self.RomeData.topData.rightData.rearOperationTotal- retData.topData.rightData.rearPassTotal;

                self.RomeData.topData.rightData.extractPassTotal = retData.topData.rightData.extractPassTotal;
                self.RomeData.topData.rightData.extractFailTotal = self.RomeData.topData.rightData.extractTotal- retData.topData.rightData.extractPassTotal;

                self.RomeData.topData.rightData.assertionsPassTotal = retData.topData.rightData.assertionsPassTotal;
                self.RomeData.topData.rightData.assertionsFailTotal = self.RomeData.topData.rightData.assertionsTotal-retData.topData.rightData.assertionsPassTotal;

                //TableData
                let obj = {};
                obj.index = retData.tableData.index;
                obj.testName = retData.tableData.testName;
                obj.requestType = retData.tableData.requestType;
                obj.apiUrl = retData.tableData.apiUrl;
                obj.code = retData.tableData.code;
                obj.timeConsuming = retData.tableData.time;
                obj.reportState = retData.tableData.reportState;
                obj.details = retData.tableData.details;

                self.RomeData.tableData.push(obj);

                
                var data ={};
                data.Message = 'Heartbeat';
                data.Params = {
                    'time':'Date()'
                }
                socket.send(JSON.stringify(data));//发送数据到服务端
                if(caseTotal==retData.tableData.index){
                    self.$message.success('任务ID:'+redisKey+',运行完成!');
                    PrintConsole("运行完成关闭TCP连接",e);
                    socket.close(); //关闭TCP连接
                }
            };
            socket.onclose=function(e){
                PrintConsole("关闭TCP连接onclose",e);
                socket.close(); //关闭TCP连接
            };
            if (socket.readyState == WebSocket.OPEN) socket.onopen();       
        },
        closeTestReportDialog(){
            this.dialog.testReport.dialogVisible =false;
        },
        OpendDetailsDialog(index,row){
            PrintConsole(row)
            let self = this;
            self.dialog.testReport.dialogPara={
                dialogTitle:row.testName,//初始化标题
                source:'CASE',
                details:row.details,
            }
            self.dialog.testReport.dialogVisible=true;

        },
    }  
};
</script>

<style>
.el-table .cell {
    white-space: pre-line;
}
.EchartContainer-pie{
    width:450px; 
    height:270px;
}
.TopMargin{
    margin:6px 0 0 140px;
    
}
</style>
