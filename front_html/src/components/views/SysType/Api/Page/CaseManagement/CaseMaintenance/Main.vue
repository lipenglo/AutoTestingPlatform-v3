<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 775px;">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="所属页面:">
                            <el-select v-model="SelectRomeData.pageId" clearable placeholder="请选择" style="width:200px;" @click.native="GetPageNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.pageNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="所属功能:">
                            <el-select v-model="SelectRomeData.funId" clearable placeholder="请选择" style="width:200px;" @click.native="GetFunNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.funNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="测试类型:">
                            <el-select v-model="SelectRomeData.testType" clearable placeholder="请选择" style="width:110px;">
                                <el-option
                                    v-for="item in SelectRomeData.testTypelOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="用例标签:">
                            <el-select v-model="SelectRomeData.caseLabel" clearable placeholder="请选择" style="width:110px;">
                                <el-option
                                    v-for="item in SelectRomeData.caseLabelOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="用例状态:">
                            <el-select v-model="SelectRomeData.caseState" clearable placeholder="请选择" style="width:120px;">
                                <el-option
                                    v-for="item in SelectRomeData.caseStateOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="用例名称:">
                            <el-input clearable v-model.trim="SelectRomeData.caseName"></el-input>
                        </el-form-item>
                        <el-form-item label="关联对象:">
                            <el-select v-model="SelectRomeData.associations" clearable placeholder="请选择" style="width:80px;">
                                <el-option
                                    v-for="item in SelectRomeData.associationsOption"
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
                    <el-table
                        v-loading="loading"
                        :data="tableData"
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
                            label="步骤排序" 
                            width="50px"
                            type="expand">
                            <template slot-scope="props">
                                <el-form label-position="left" >
                                    <el-table
                                        :data="props.row.tableItem"
                                        border>
                                        <el-table-column
                                            label="步骤"
                                            prop="index"
                                            align= "center"
                                            width="100">
                                        </el-table-column>
                                        <el-table-column
                                            prop="apiName"
                                            align= "center"
                                            label="接口名称">
                                        </el-table-column>
                                        <el-table-column
                                            prop="testName"
                                            align= "center"
                                            label="测试名称">
                                        </el-table-column>
                                        <el-table-column
                                            width="100px"
                                            prop="requestType"
                                            align= "center"
                                            label="请求类型">
                                        </el-table-column>
                                        <el-table-column
                                            width="120px"
                                            prop="requestParamsType"
                                            align= "center"
                                            label="请求参数类型">
                                        </el-table-column>
                                        <el-table-column
                                            label="用例接口状态"
                                            width="130"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-tag type="success" v-if="scope.row.state" >启用</el-tag>
                                                <el-tag type="info" v-else >禁用</el-tag>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            prop="updateTime"
                                            width="200"
                                            align= "center"
                                            label="更新时间">
                                        </el-table-column>
                                    </el-table>
                                </el-form>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="优先级"
                            width="70px"
                            align= "center"
                            prop="priority">
                        </el-table-column>
                        <el-table-column
                            label="测试类型"
                            align= "center"
                            width="100px">
                            <template slot-scope="scope">
                                <el-tag type="info" v-if="scope.row.testType=='UnitTest'" >单元测试</el-tag>
                                <el-tag type="warning" v-else-if="scope.row.testType=='HybridTest'" >混合测试</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="用例名称"
                            width="300px"
                            align= "center"
                            prop="caseName">
                        </el-table-column>
                        <el-table-column
                            label="所属页面"
                            width="200px"
                            align= "center"
                            prop="pageName">
                        </el-table-column>
                        <el-table-column
                            label="所属功能"
                            width="200px"
                            align= "center"
                            prop="funName">
                        </el-table-column>
                        <el-table-column
                            label="用例标签"
                            align= "center"
                            width="120px"
                            prop="labelId">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.labelId=='CommonCase'">普通用例</el-tag>
                                <el-tag type="warning" v-else-if="scope.row.labelId=='ReturnCase'">回归用例</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="用例状态"
                            align= "center"
                            width="100px">
                            <template slot-scope="scope">
                                <el-tag type="warning" v-if="scope.row.caseState=='InDev'">研发中</el-tag>
                                <el-tag type="success" v-else-if="scope.row.caseState=='Completed'">已完成</el-tag>
                                <!-- <el-tag type="success" v-else-if="scope.row.caseState=='Completed'"><i class="el-icon-check"></i></el-tag> -->
                                <el-tag type="info" v-else>弃用</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="接口动态"
                            align= "center"
                            width="100px">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.apidynamic==false">无更变</el-tag>
                                <el-tag type="danger" v-else>已更变</el-tag>
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
                            width="160px"
                            align= "center"
                            prop="updateTime">
                        </el-table-column>
                        <el-table-column
                            show-overflow-tooltip
                            label="修改者"
                            width="150px"
                            align= "center"
                            prop="userName">
                        </el-table-column>
                        <el-table-column
                            label="创建者"
                            width="120px"
                            align= "center"
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
                                        <el-dropdown-item command="CopyCase">复制用例</el-dropdown-item>
                                        <el-dropdown-item command="CaseRestore">历史恢复(勾选/不勾选)</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </el-button-group>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                            <el-button-group>
                            <el-button
                                size="mini"
                                type="success"
                                @click="OpenRunTypeDialog(scope.$index, scope.row)">RunCase
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
                <div>
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
            </div>
        </template>
        <template>
            <dialog-editor
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
        <template>
            <dialog-run-type
                @closeDialog="closeRunTypeDialog" 
                :isVisible="dialog.runType.dialogVisible" 
                :dialogPara="dialog.runType.dialogPara"
                @Succeed="SelectData">
            </dialog-run-type>
        </template>
        <template>
            <dialog-history-info
                @closeDialog="closeHistoryInfoDialog" 
                :isVisible="dialog.historyInfo.dialogVisible" 
                :dialogPara="dialog.historyInfo.dialogPara"
                @Succeed="SelectData">
            </dialog-history-info>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";

import DialogEditor from "./Editor.vue";
import DialogRunType from "./RunType.vue";
import DialogHistoryInfo from "./HistoryInfo.vue";

export default {
    components: {
        DialogEditor,DialogRunType,DialogHistoryInfo
    },
    data() {
        return {
            multipleSelection:[],
            loading:false,
            tableData: [
                // {'priority':'P0','testType':'UnitTest','caseName':'测试登录','pageName':'测试页面','funName':'测试功能','caseLabel':'CommonCase','Apidynamic':false,'caseState':'InDev','updateTime':'2021-12-12 14:13:22','userName':'lipenglo'},
                // {'priority':'P1','testType':'HybridTest','caseName':'测试登录','pageName':'测试页面','funName':'测试功能','caseLabel':'RetentCase','Apidynamic':true,'caseState':'Completed','updateTime':'2021-12-12 14:13:22','userName':'lipenglo'}
            ],
            SelectRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                testType:'',
                testTypelOption:[
                    {'label':'单元测试','value':'UnitTest'},
                    {'label':'混合测试','value':'HybridTest'},
                ],
                caseLabel:'',
                caseLabelOption:[
                    {'label':'普通用例','value':'CommonCase'},
                    {'label':'回归用例','value':'ReturnCase'},
                ],
                caseState:'',
                caseStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                caseName:'',
                associations:'',
                associationsOption:[
                    {'label':'我','value':'My'},
                    {'label':'全部','value':''},
                ],
            },
            RomeData:{
         
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
                runType:{
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
            }
           
        };
    },
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        'SelectRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.SelectRomeData.funId='';
                self.SelectRomeData.funNameOption=[];
            }
        },
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){
            let self = this;
            self.tableData= [];
            self.loading=true;
            self.$axios.get('/api/ApiCaseMaintenance/SelectData',{
                params:{
                    "proId":self.$cookies.get('proId'),
                    "pageId":self.SelectRomeData.pageId,
                    "funId":self.SelectRomeData.funId,
                    'testType':self.SelectRomeData.testType,
                    "labelId":self.SelectRomeData.caseLabel,
                    "caseState":self.SelectRomeData.caseState,
                    'caseName':self.SelectRomeData.caseName,
                    'associations':self.SelectRomeData.associations,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.tableItem=d.tableItem;
                        obj.priority=d.priority;
                        obj.testType = d.testType;
                        obj.caseName = d.caseName;
                        obj.pageName=d.pageName;
                        obj.funName=d.funName;
                        obj.labelId = d.labelId;
                        obj.apidynamic=d.apidynamic;
                        obj.caseState = d.caseState;
                        obj.passRate = d.passRate+'%';
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;     
                        obj.createUserName = d.createUserName;     

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funId='';
            self.SelectRomeData.testType='';
            self.SelectRomeData.caseLabel='';
            self.SelectRomeData.caseState='';
            self.SelectRomeData.caseName='';
            self.SelectRomeData.associations='';
            self.SelectData();
        },
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.SelectRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            this.SelectRomeData.funNameOption = [];
            if(this.SelectRomeData.pageId){
                GetFunNameItems('API',this.$cookies.get('proId'),this.SelectRomeData.pageId).then(d=>{
                    this.SelectRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
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
        handleCommand(command){
            PrintConsole(command);
            if(command=='CopyCase'){
                this.copyCase();
            }else if(command=='CaseRestore'){
                this.OpenHistoryInfoDialog();
            }
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
            self.page.current=val
            self.SelectData();
        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增用例",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑用例",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                caseId:row.id,
            }
            self.dialog.editor.dialogVisible=true;
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
            self.$axios.post('/api/ApiCaseMaintenance/DeleteData',Qs.stringify({
                'caseId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('用例删除成功!');
                self.SelectData();
            }
            else{
                self.$message.error('用例删除失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        closeRunTypeDialog(){
            this.dialog.runType.dialogVisible =false;
        },
        OpenRunTypeDialog(index,row){
            let self = this;
            self.dialog.runType.dialogPara={
                dialogTitle:'选择运行',//初始化标题
                caseId:row.id,
                caseName:row.caseName,
            }
            self.dialog.runType.dialogVisible=true;
        },
        copyCase(){
            let self = this;
            if(self.multipleSelection.length!=1){
                self.$message.warning('请勾选1条用例进行复制操作');
            }else{
                self.loading=true;
                self.$axios.get('/api/ApiCaseMaintenance/CopyCase',{
                    params:{
                        'caseId':self.multipleSelection[0]
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.$message.success('复制成功');
                        self.loading=false;
                        self.SelectData();
                    }else{
                        self.$message.error('复制失败:'+res.data.errorMsg);
                        self.loading=false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading=false;
                })
            }
        },
        SelectLastReport(taskId){
            let self = this;
            return self.$axios.get('/api/ApiTestReport/SelectLastReport',{
                params:{
                    "taskId":taskId,
                    'reportType':'CASE'
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
        openReport(caseId){
            this.SelectLastReport(caseId).then(testReportId=>{
                PrintConsole(testReportId)
                if(testReportId){
                    let routeUrl = this.$router.resolve({
                        name: "Api_Report",
                        query: {
                            testReportId:testReportId,
                            reportType:'CASE'
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
                    caseId:self.multipleSelection[0],
                }
                self.dialog.historyInfo.dialogVisible=true;
            }
        },
       
    }
};
</script>

<style>

</style>
