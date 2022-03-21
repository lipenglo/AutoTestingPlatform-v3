<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 775px;">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="任务名称:">
                            <el-input clearable v-model.trim="SelectRomeData.taskName"></el-input>
                        </el-form-item>
                        <el-form-item label="报告状态:">
                            <el-select v-model="SelectRomeData.reportState" clearable placeholder="请选择" style="width:120px;">
                                <el-option
                                    v-for="item in SelectRomeData.reportStateOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </div>
                <div>
                    <div>
                        <el-table
                            v-loading="loading"
                            :data="RomeData.tableData"
                            height="670px"
                            border
                            ref="multipleTable"
                            @selection-change="handleSelectionChange"
                            @row-click="handleRowClick">
                            <el-table-column
                                type="selection"
                                align= "center"
                                width="50">
                            </el-table-column>
                            <el-table-column
                                label="ID"
                                align= "center"
                                width="80px"
                                prop="id">
                            </el-table-column>
                            <el-table-column
                                label="任务名称"
                                width="300px"
                                align= "center"
                                prop="taskName">
                            </el-table-column>
                            <el-table-column
                                label="定时配置"
                                width="200px"
                                align= "center"
                                prop="timingConfig">
                            </el-table-column>
                            <el-table-column
                                label="用例数量"
                                width="100px"
                                align= "center"
                                prop="taskSetTotal">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="备注"
                                width="300px"
                                align= "center"
                                prop="remarks">
                            </el-table-column>      
                            <el-table-column
                                label="任务状态"
                                width="100px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.taskStatus" >启用</el-tag>
                                    <el-tag type="danger" v-else>禁用</el-tag>
                                </template>
                            </el-table-column>          
                            <el-table-column
                                label="最后报告时间"
                                width="160px"
                                align= "center">
                                <template slot-scope="scope">
                                    <span type="success" v-if="scope.row.lastReportTime" >{{scope.row.lastReportTime}}</span>
                                    <el-tag v-else>无最新数据</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="最后报告状态"
                                width="110px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.lastReportStatus=='Pass'" >Pass</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.lastReportStatus=='Fail'">Fail</el-tag>
                                    <el-tag type="danger" v-else-if="scope.row.lastReportStatus=='Error'">Error</el-tag>
                                    <el-tag v-else>无最新数据</el-tag>
                                </template>
                            </el-table-column> 
                            <el-table-column
                                label="通过率"
                                width="80px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-button type="text" @click="openReport(scope.row.id)">{{scope.row.passRate}}</el-button>
                                </template>
                            </el-table-column> 
                            <el-table-column
                                label="更新时间"
                                align= "center"
                                width="200px"
                                prop="updateTime">
                            </el-table-column>   
                            <el-table-column
                                show-overflow-tooltip
                                label="修改者"
                                align= "center"
                                width="150px"
                                prop="userName">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="创建者"
                                align= "center"
                                width="150px"
                                prop="createUserName">
                            </el-table-column>   
                            <el-table-column
                                fixed="right"
                                align="center"
                                width="240px">
                            <template slot="header">
                                <el-button-group>
                                    <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                    <el-dropdown @command="handleCommand">
                                        <el-button type="warning">
                                            更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                        </el-button>
                                        <el-dropdown-menu slot="dropdown">
                                            <el-dropdown-item command="ExecutiveLogging">执行记录</el-dropdown-item>
                                            <el-dropdown-item command="CopyTask">复制定时任务(未开发)</el-dropdown-item>
                                            <el-dropdown-item command="TaskRestore">历史恢复(勾选/不勾选)</el-dropdown-item>
                                        </el-dropdown-menu>
                                    </el-dropdown>
                                </el-button-group>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button-group>
                                    <el-button
                                        :loading="buttonLoading"
                                        size="mini"
                                        type="success"
                                        @click="runTask(scope.$index, scope.row)">RunTask
                                    </el-button>
                                    <el-button
                                        size="mini"
                                        @click="handleEdit(scope.$index, scope.row)">Edit
                                    </el-button>
                                    <el-button
                                        size="mini"
                                        type="danger"
                                        @click="handleDelete(scope.$index, scope.row)">Delete
                                    </el-button>
                                </el-button-group>
                            </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
                <div style="margin-top:-10px">
                    <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                        @size-change="pageSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page="page.current" 
                        :total="page.total"
                        :page-sizes = [10,30,50,100]
                        style="margin: 20px auto auto auto;">
                    </el-pagination>
                </div>
            </div>
        </template>
        <template>
            <dialog-editor
                @closeDialog="CloseEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
        <template>
            <dialog-history-info
                @closeDialog="closeHistoryInfoDialog" 
                :isVisible="dialog.historyInfo.dialogVisible" 
                :dialogPara="dialog.historyInfo.dialogPara"
                @Succeed="SelectData">
            </dialog-history-info>
        </template>
        <template>
            <dialog-run-log
                @closeDialog="closeRunLogDialog" 
                :isVisible="dialog.runLog.dialogVisible" 
                :dialogPara="dialog.runLog.dialogPara"
                @Succeed="SelectData">
            </dialog-run-log>
        </template>
    </div>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../../../../js/Logger.js";

import DialogEditor from "./Editor.vue";
import DialogHistoryInfo from "./HistoryInfo.vue";
import DialogRunLog from "./RunLog.vue"

export default {
    components: {
        DialogEditor,DialogHistoryInfo,DialogRunLog
    },
    data() {
        return {
            loading:false,
            buttonLoading:false,
            multipleSelection:[],
            SelectRomeData:{
                taskName:'',
                reportState:'',
                reportStateOption:[
                    {'label':'Pass','value':'Pass'},
                    {'label':'Fail','value':'Fail'},
                    {'label':'Error','value':'Error'},
                ],
            },
            RomeData:{
                tableData: [
                    // {'id':'1','taskName':'测试任务','timingConfig':'* * * * *','taskTotal':8,'remarks':'这是备注啊','taskStatus':true,'lastReportTime':'2021-22-22 12:22:21',
                    // 'lastReportStatus':'Pass','updateTime':'2021-22-22 12:22:21','userName':'liepnglo(古雨辰)','createUserName':'lipenglo'},
                    // {'id':'2','taskName':'测试任务','timingConfig':'* * * * *','taskTotal':8,'remarks':'这是备注啊','taskStatus':false,'lastReportTime':'2021-22-22 12:22:21',
                    // 'lastReportStatus':'Fail','updateTime':'2021-22-22 12:22:21','userName':'liepnglo(古雨辰)','createUserName':'lipenglo'},
                ],
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },
            dialog:{
                editor:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                historyInfo:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                runLog:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
            },
          
        };
    },
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
     
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.loading=true;
            self.RomeData.tableData= [];
            self.$axios.get('/api/ApiTimingTask/SelectData',{
                params:{
                    'proId':self.$cookies.get('proId'),
                    'taskName':self.SelectRomeData.taskName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.taskName=d.taskName;
                        obj.timingConfig=d.timingConfig;
                        obj.taskSetTotal=d.taskSetTotal;
                        obj.remarks = d.remarks;
                        obj.taskStatus = d.taskStatus;
                        obj.lastReportTime = d.lastReportTime;
                        obj.lastReportStatus = d.lastReportStatus;
                        obj.passRate=d.passRate+'%';
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;
                        obj.createUserName = d.createUserName;

                        self.RomeData.tableData.push(obj);
                    });
                    if(self.RomeData.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        CloseEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增定时任务",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑定时任务",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                taskId:row.id,
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleRowClick(row, column, event){//点击行选择勾选框
            this.$refs.multipleTable.toggleRowSelection(row);
        },
        handleSelectionChange(val){//勾选数据时触发
            // console.log(val)
            this.multipleSelection=[];
            val.forEach(d =>{
                this.multipleSelection.push(d.id);
            }); 
        },
        handleDelete(index,row){
            this.$confirm('请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                   this.DeleteData(row.id);     
                }).catch(() => {       
            });
        },
        DeleteData(id){
            let self = this;
            self.$axios.post('/api/ApiTimingTask/DeleteData',Qs.stringify({
                'taskId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('删除定时任务成功!');
                self.SelectData();
            }
            else{
                self.$message.error('删除定时任务失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleCommand(command){
            PrintConsole(command);
            if(command=='TaskRestore'){
                this.OpenHistoryInfoDialog();
            }else if(command=='ExecutiveLogging'){
                this.OpenRunLogDialog();
            }
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.taskName='';
            self.SelectRomeData.reportState='';
            self.SelectData();
        },
        pageSizeChange(pageSize) {
            let self = this;
            self.page.current = 1;
            self.page.pageSize = pageSize;
        },
        // 显示第几页
        handleCurrentChange(val) {
            let self = this;
            // 改变默认的页数
            self.page.current=val;
            self.SelectData();
        },
        SelectLastReport(taskId){
            let self = this;
            return self.$axios.get('/api/ApiTestReport/SelectLastReport',{
                params:{
                    "taskId":taskId,
                    'reportType':'TASK'
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    return res.data.testReportId;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    return null;
                }
            }).catch(function (error) {
                console.log(error);
                return null;
            })
        },
        openReport(taskId){
            this.SelectLastReport(taskId).then(testReportId=>{
                PrintConsole(testReportId)
                if(testReportId){
                    let routeUrl = this.$router.resolve({
                        name: "Api_Report",
                        query: {
                            testReportId:testReportId,
                            reportType:'TASK'
                        }
                    });
                    window.open(routeUrl.href, '_blank');
                }
            });
        },

        //历史恢复
        closeHistoryInfoDialog(){
            this.dialog.historyInfo.dialogVisible =false;
        },
        OpenHistoryInfoDialog(){
            let self = this;
            if(self.multipleSelection.length>1){
                self.$message.warning('只可勾选1条数据或不勾选数据进行历史查看及恢复!');
            }else{
                self.dialog.historyInfo.dialogPara={
                    dialogTitle:"历史恢复",//初始化标题
                    taskId:self.multipleSelection[0],
                }
                self.dialog.historyInfo.dialogVisible=true;
            }
        },
        runTask(index,row){
            let self = this;
            self.buttonLoading=true;
            self.$axios.post('/api/ApiTimingTask/ExecuteTask',Qs.stringify({
                'taskId':row.id,
            })).then(res => {
            if(res.data.statusCode ==2001){
                self.$message.success('定时任务已启动,任务ID:'+res.data.celeryTaskId+',请稍后在测试报告页面查看结果!');
                self.buttonLoading=false;
            }
            else{
                self.$message.error('定时任务启动失败:'+ res.data.errorMsg);
                self.buttonLoading=false;
            }
            }).catch(function (error) {
                console.log(error);
                self.buttonLoading=false;
            })
        },

        //执行记录
        closeRunLogDialog(){
            this.dialog.runLog.dialogVisible =false;
        },
        OpenRunLogDialog(){
            let self = this;
            self.dialog.runLog.dialogPara={
                dialogTitle:"执行记录",//初始化标题
                taskId:self.multipleSelection[0],
            }
            self.dialog.runLog.dialogVisible=true;
        },
    }
};
</script>

<style>

</style>
