<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 785px;">
                <div>
                    <el-form :inline="true" class="demo-form-inline" method="post">
                        <el-form-item label="所属页面:">
                            <el-select v-model="SelectRomeData.pageId" clearable placeholder="请选择" style="width:150px;" @click.native="GetPageNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.pageNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="所属功能:">
                            <el-select v-model="SelectRomeData.funId" clearable placeholder="请选择" style="width:150px;" @click.native="GetFunNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.funNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="接口名称:">
                            <el-input clearable v-model="SelectRomeData.apiName"></el-input>
                        </el-form-item>
                        <el-form-item label="接口地址:">
                            <el-input clearable v-model="SelectRomeData.requestUrl"></el-input>
                        </el-form-item>
                        <el-form-item label="接口状态:">
                            <el-select v-model="SelectRomeData.apiState" clearable placeholder="请选择" style="width:100px;">
                                <el-option
                                    v-for="item in SelectRomeData.apiStateOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="关联对象:">
                            <el-select v-model="SelectRomeData.associations" clearable placeholder="请选择" style="width:100px;">
                                <el-option
                                    v-for="item in SelectRomeData.associationsOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()" >查询</el-button>
                        <el-button type="info" @click="ClearSelectRomeData()">重置</el-button>
                        <!-- <div style="float:right"> -->
                            <!-- <el-button icon="el-icon-question" circle plain @click="helpMsg()"></el-button> -->
                        <!-- </div> -->
                    </el-form>
                </div>
                <div>
                    <el-table
                        v-loading="loading"
                        :data=tableData
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
                            label="所属页面"
                            align= "center"
                            width="180px"
                            prop="pageName">
                        </el-table-column>
                        <el-table-column
                            label="所属功能"
                            align= "center"
                            width="180px"
                            prop="funName">
                        </el-table-column>
                        <el-table-column
                            label="接口名称"
                            width="300px"
                            align= "center"
                            prop="apiName">
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
                            show-overflow-tooltip
                            label="接口地址"
                            width="300px"
                            align= "center"
                            prop="requestUrl">
                        </el-table-column>
                        <el-table-column
                            label="接口状态"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="warning" v-if="scope.row.apiState=='InDev'" >研发中</el-tag>
                                <el-tag type="success" v-else-if="scope.row.apiState=='Completed'" >已完成</el-tag>
                                <el-tag type="info" v-else>弃用</el-tag>
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
                            width="170px"
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
                            label="创建者"
                            align= "center"
                            width="120px"
                            prop="createUserName">
                        </el-table-column>
                        <el-table-column
                            fixed="right"
                            align="center"
                            width="330px">
                        <template slot="header">
                            <el-button-group>  
                                <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                <el-dropdown @command="handleCommand">
                                    <el-button type="warning">
                                        更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
                                    </el-button>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item command="SwaggerImport">导入(Swagger)</el-dropdown-item>
                                        <el-dropdown-item command="SwaggerExport">导出(Swagger)-未开发</el-dropdown-item>
                                        <el-dropdown-item command="CopyApi">复制接口</el-dropdown-item>
                                        <el-dropdown-item command="HistoryBack">历史恢复(勾选/不选)</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </el-button-group>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                            <el-button-group>
                            <el-button
                                size="mini"
                                type="success"
                                @click="OpenRunTypeDialog(scope.$index, scope.row)">Request</el-button>
                            <el-button
                                type="info"
                                size="mini"
                                @click="OpenWorkOrderDialog(scope.$index, scope.row)">工单</el-button>
                            <el-button
                                type="warning"
                                size="mini"
                                @click="OpenLifeCycleDialog(scope.$index, scope.row)">生命</el-button>
                            <el-button
                                size="mini"
                                @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                            <el-button
                                size="mini"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                            </el-button-group>
                        </template>
                        </el-table-column>
                    </el-table>
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
            <dialog-work-order
                @closeDialog="closeWorkOrderDialog" 
                :isVisible="dialog.workOrder.dialogVisible" 
                :dialogPara="dialog.workOrder.dialogPara"
                @Succeed="SelectData">
            </dialog-work-order>
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
            <dialog-life-cycle
                @closeDialog="closeLifeCycleDialog" 
                :isVisible="dialog.lifeCycle.dialogVisible" 
                :dialogPara="dialog.lifeCycle.dialogPara"
                @Succeed="SelectData">
            </dialog-life-cycle>
        </template>
        <template>
            <dialog-swagger-import
                @closeDialog="closeSwaggerImportDialog" 
                :isVisible="dialog.swaggerImport .dialogVisible" 
                :dialogPara="dialog.swaggerImport.dialogPara"
                @Succeed="SelectData">
            </dialog-swagger-import>
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
import DialogWorkOrder from "../../../../../WorkorderManagement/WorkorderMaintenance/Editor.vue";
import DialogHistoryInfo from "./HistoryInfo.vue";
import DialogLifeCycle from "./LifeCycle.vue";
import DialogSwaggerImport from "./SwaggerImport.vue";


export default {
    components: {
        DialogEditor,DialogRunType,DialogWorkOrder,DialogHistoryInfo,DialogLifeCycle,DialogSwaggerImport
    },
    data() {
        return {
            loading:false,
            tableData: [],
            multipleSelection:[],
            SelectRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                apiName:'',
                requestUrl:'',
                apiState:'',
                apiStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
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
                workOrder:{
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
                lifeCycle:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                swaggerImport:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                }
            },
           
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
            self.$axios.get('/api/ApiIntMaintenance/SelectData',{
                params:{
                    "proId":self.$cookies.get('proId'),
                    "pageId":self.SelectRomeData.pageId,
                    "funId":self.SelectRomeData.funId,
                    "apiName":self.SelectRomeData.apiName,
                    "requestUrl":self.SelectRomeData.requestUrl,
                    'apiState':self.SelectRomeData.apiState,
                    'associations':self.SelectRomeData.associations,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.pageId=d.pageId;
                        obj.pageName = d.pageName;
                        obj.funId = d.funId;
                        obj.funName=d.funName;
                        obj.apiName = d.apiName;
                        obj.requestType = d.requestType;
                        obj.requestUrl = d.requestUrl;
                        obj.apiState =d.apiState;
                        obj.associationMy=d.associationMy;
                        obj.passRate=d.passRate+'%';
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;
                        obj.createUserId = d.createUserId;        
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
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.SelectRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.SelectRomeData.pageId){
                GetFunNameItems('API',this.$cookies.get('proId'),this.SelectRomeData.pageId).then(d=>{
                    this.SelectRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funId='';
            self.SelectRomeData.apiName='';
            self.SelectRomeData.requestUrl='';
            self.SelectRomeData.apiState='';
            self.SelectRomeData.associations='';
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
            self.page.current=val
            self.SelectData();
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
            self.$axios.post('/api/ApiIntMaintenance/DeleteData',Qs.stringify({
                'apiId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('接口删除成功!');
                self.SelectData();
            }
            else{
                self.$message.error('接口删除失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑接口",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                apiId:row.id,
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
        SelectLastReport(taskId){
            let self = this;
            return self.$axios.get('/api/ApiTestReport/SelectLastReport',{
                params:{
                    "taskId":taskId,
                    'reportType':'API'
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
        openReport(apiId){
            this.SelectLastReport(apiId).then(testReportId=>{
                PrintConsole(testReportId)
                if(testReportId){
                    let routeUrl = this.$router.resolve({
                        name: "Api_Report",
                        query: {
                            testReportId:testReportId,
                            reportType:'API'
                        }
                    });
                    window.open(routeUrl.href, '_blank');
                }
            });
        },

        //更多操作
        handleCommand(command){//更多菜单
            PrintConsole(command);
            if(command=='CopyApi'){
                this.CopyApi();
            }else if(command=='HistoryBack'){
                this.OpenHistoryInfoDialog();
            }else if(command=='SwaggerImport'){
                this.OpenSwaggerImportDialog();
            }
        },
        CopyApi(){
            let self = this;
            if(self.multipleSelection.length==0){
                self.$message.warning('请勾选1条数据进行复制操作!');
            }else{
                self.loading=true;
                self.$axios.get('/api/ApiIntMaintenance/CopyApi',{
                    params:{
                        'apiId':self.multipleSelection[0]
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.$message.success('接口复制成功!');
                        self.SelectData();
                        self.loading=false;
                    }else{
                        self.$message.error('获取数据失败:'+res.data.errorMsg);
                        self.loading=false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading=false;
                })
            }
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
                    apiId:self.multipleSelection[0],
                }
                self.dialog.historyInfo.dialogVisible=true;
            }
        },
        //导入
        closeSwaggerImportDialog(){
            this.dialog.swaggerImport.dialogVisible =false;
        },
        OpenSwaggerImportDialog(){
            let self = this;
            self.dialog.swaggerImport.dialogPara={
                dialogTitle:"导入(Swagger)",//初始化标题
            }
            self.dialog.swaggerImport.dialogVisible=true;
        },

        //编辑、新增
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增接口",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },

        //运行类型
        closeRunTypeDialog(){
            this.dialog.runType.dialogVisible =false;
        },
        OpenRunTypeDialog(index,row){
            let self = this;
            self.dialog.runType.dialogPara={
                dialogTitle:'选择运行',//初始化标题
                apiId:row.id,
                apiName:row.apiName,
            }
            self.dialog.runType.dialogVisible=true;
        },

        //工单
        closeWorkOrderDialog(){
            this.dialog.workOrder.dialogVisible =false;
        },
        OpenWorkOrderDialog(index,row){
            let self = this;
            self.dialog.workOrder.dialogPara={
                dialogTitle:'新增工单',//初始化标题
                isAddNew:true,
                triggerPage:'ApiMaintenance',//触发页面
                workType:'Other',
                workState:0,
                pageId:row.pageId,
                funId:row.funId,
                workName:row.apiName,
                createUserId:row.createUserId
            }
            self.dialog.workOrder.dialogVisible=true;
        },


        //生命周期
        closeLifeCycleDialog(){
            this.dialog.lifeCycle.dialogVisible =false;
        },
        OpenLifeCycleDialog(index,row){//生命
            let self = this;
            self.dialog.lifeCycle.dialogPara={
                dialogTitle:row.apiName+'(生命周期)',//初始化标题
                apiId:row.id,
            }
            self.dialog.lifeCycle.dialogVisible=true;
        },
    }
};
</script>

<style>
body {
    margin: 0;
}

</style>
