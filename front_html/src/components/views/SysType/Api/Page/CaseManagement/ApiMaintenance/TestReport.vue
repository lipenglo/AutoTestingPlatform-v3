<template>
   <el-drawer
        :title="dialogTitle"
        size="1000px"
        :visible.sync="dialogVisible"
        direction="rtl"
        :before-close="dialogClose">
        <el-card 
            style="height:865px"
            v-loading="loading"
            element-loading-text="拼命返回请求信息中"
            element-loading-spinner="el-icon-loading">
            <div>
                <el-form ref="RomeData" :model="RomeData" label-width="80px">
                    <el-form-item label="请求地址:">
                        <span style="float:left">{{RomeData.requestUrl}}</span>
                    </el-form-item>
                    <el-form-item label="请求类型:">
                        <span style="float:left">{{RomeData.requestType}}</span>
                    </el-form-item>
                </el-form>
            </div>
            <div  style="margin-top:-20px">
                <el-divider></el-divider>
            </div>
            <div>
                <el-row style="font-size:13px">
                    <el-col :span="3">
                        <div>
                            <!-- <div v-bind:style="{color:scope.row.is_activation == 1 ? 'chartreuse' : 'red'}">{{scope.row.is_activation == 0 ? '否' : '是'}}</div> -->
                            <span>状态码:</span>
                            <span v-bind:style="{color:RomeData.stateCode == 200 ? 'chartreuse' : 'red'}">{{RomeData.stateCode}}</span>
                            <el-divider direction="vertical"></el-divider>
                        </div>
                    </el-col>
                    <el-col :span="2">
                        <div>
                            <span>耗时:{{RomeData.time}}</span>
                            <el-divider direction="vertical"></el-divider>
                        </div>
                    </el-col>
                    <el-col :span="4">
                        <div style="margin-top:-8px">
                            <span>报告状态:</span>
                            <el-tag v-if="RomeData.reportState=='Pass'" type="success">通过</el-tag>
                            <el-tag v-else-if="RomeData.reportState=='Fail'" type="warning">失败</el-tag>
                            <el-tag v-else type="danger">错误</el-tag>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <div style="margin-top:-10px">
                <el-divider></el-divider>
            </div>
            <div>
                <el-tabs v-model="RomeData.activeName">
                    <el-tab-pane label="文档信息" name="docInfo">
                        <div style=" height:570px;overflow:auto">
                            <div>
                                <div slot="header" style="text-align: left;">
                                    <el-tag type="info">基础信息</el-tag>
                                </div>
                                <div style="margin-top:15px;margin-left:-15px">
                                    <el-row>
                                        <el-col :span="2">
                                            <el-tag type="success" v-if="RomeData.requestType=='GET'" >GET</el-tag>
                                            <el-tag type="warning" v-else-if="RomeData.requestType=='POST'">POST</el-tag>
                                            <el-tag type="info" v-else>{{RomeData.requestType}}</el-tag>
                                        </el-col>
                                        <el-col :span="22">
                                            <span style="float:left;margin-top:6px;margin-left:-8px">{{docInfoRomeData.originalUrl}}</span>
                                        </el-col>
                                    </el-row>
                                </div>
                            </div>
                            <el-divider></el-divider>
                            <div style="margin-top:10px">
                                <div slot="header" style="text-align:left;">
                                    <el-tag type="info">请求Headers</el-tag>
                                </div>
                                <div>
                                    <el-table
                                        :data="docInfoRomeData.headersTableData"
                                        style="width: 100%">
                                        <el-table-column
                                            prop="key"
                                            width="400px"
                                            label="名称">
                                        </el-table-column>
                                        <el-table-column
                                            prop="value"
                                            label="值">
                                        </el-table-column>
                                    </el-table>
                                </div>
                            </div>
                            <el-divider></el-divider>
                            <div style="margin-top:10px">
                                <div slot="header" style="text-align: left;">
                                    <el-tag type="info">请求主体</el-tag>
                                </div>
                                <div>
                                    <el-table
                                        :data="docInfoRomeData.requestDataTableData"
                                        style="width: 100%">
                                        <el-table-column
                                            prop="key"
                                            width="400px"
                                            label="参数名">
                                        </el-table-column>
                                        <el-table-column
                                            prop="value"
                                            label="参数值">
                                        </el-table-column>
                                    </el-table>
                                </div>
                            </div>
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="返回主体" name="responseBody">
                        <el-input type="textarea" 
                            readonly
                            resize="none"
                            v-model="RomeData.responseText"
                            :autosize="{ minRows: 27, maxRows: 27}"
                            >
                        </el-input>
                    </el-tab-pane>
                    <el-tab-pane :label="RomeData.responseHeadersName" name="ResponseHeaders">
                        <el-table
                            :data="RomeData.responseHeadersTableData"
                            height="580px"
                            style="width: 100%">
                            <el-table-column
                                width="400px"
                                prop="key"
                                label="名称">
                            </el-table-column>
                            <el-table-column
                                prop="value"
                                label="值">
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane :label="RomeData.ExtractResultsName" name="ExtractResults" v-if="RomeData.extractTableData.length!=0">
                        <el-table
                            :data="RomeData.extractTableData"
                            height="580px"
                            style="width: 100%">
                            <el-table-column
                                align="center"
                                width="200px"
                                prop="key"
                                label="参数名">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="100px"
                                prop="valueType"
                                label="值类型">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                prop="value"
                                label="参数值">
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane :label="RomeData.AssertionResultsName" name="AssertionResults" v-if="RomeData.assertionTableData.length!=0">
                        <el-table
                            :data="RomeData.assertionTableData"
                            height="580px"
                            border
                            style="width: 100%">
                            <el-table-column
                                align="center"
                                prop="checkName"
                                label="检查值">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                prop="retCheckOut"
                                label="预期结果">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                prop="validateType"
                                width="150px"
                                label="比较类型">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                prop="retExtractorOut"
                                label="实际返回">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="100px"
                                label="结果">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.results" >通过</el-tag>
                                    <el-tag type="warning" v-else >失败</el-tag>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane :label="RomeData.preOperationName" name="PreOperation" v-if="RomeData.preOperationTableData!=0">
                        <el-table
                            :data="RomeData.preOperationTableData"
                            border
                            height="610">
                            <el-table-column
                                label="操作类型"
                                width="150px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="info">{{scope.row.operationType}}</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="调用名称"
                                width="200px"
                                align= "center"
                                prop="callName">
                            </el-table-column>
                            <el-table-column
                                label="调用结果"
                                align= "center">
                                <template slot-scope="scope">
                                    <div style="text-align:left;white-space:pre-line;">{{scope.row.callResults}}</div>
                                </template>
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="100px"
                                label="结果">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.resultsState">通过</el-tag>
                                    <el-tag type="warning" v-else >失败</el-tag>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane :label="RomeData.rearOperationName" name="RearOperation" v-if="RomeData.rearOperationTableData!=0">
                        <el-table
                            :data="RomeData.rearOperationTableData"
                            border
                            height="610">
                            <el-table-column
                                label="操作类型"
                                width="150px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="info">{{scope.row.operationType}}</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="调用名称"
                                width="200px"
                                align= "center"
                                prop="callName">
                            </el-table-column>
                            <el-table-column
                                label="调用结果"
                                align= "center">
                                <template slot-scope="scope">
                                    <div style="text-align:left;white-space:pre-line;">{{scope.row.callResults}}</div>
                                </template>
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="100px"
                                label="结果">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.resultsState">通过</el-tag>
                                    <el-tag type="warning" v-else >失败</el-tag>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane  :label="RomeData.errorInfoName" name="errorInfo" v-if="RomeData.errorInfoTableData!=0">
                        <el-table
                            :data="RomeData.errorInfoTableData"
                            border
                            height="610">
                            <el-table-column
                                label="触发时间"
                                width="160px"
                                align= "center"
                                prop="createTime">
                            </el-table-column>
                            <el-table-column
                                label="错误名称"
                                width="200px"
                                align= "center"
                                prop="errorName">
                            </el-table-column>
                            <el-table-column
                                label="错误信息"
                                align= "center"
                                prop="errorInfo">
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-card>
    </el-drawer>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    components: {
        
    },
    data() {
        return {
        dialogTitle:"",
        dialogVisible:false,  
        loading:true,

        RomeData:{  
            requestUrl:'Null',
            requestType:'Null',
            stateCode:'Null',
            time:'Null',
            reportState:'Null',

            activeName:'responseBody',
            responseHeadersName:'返回Headers',
            ExtractResultsName:'提取结果',
            AssertionResultsName:'断言结果',
            preOperationName:'前置操作',
            rearOperationName:'后置操作',
            errorInfoName:'错误信息',
    
            responseText:'',
            responseHeadersTableData:[],
            extractTableData:[],
            assertionTableData:[],
            preOperationTableData:[],
            rearOperationTableData:[],
            errorInfoTableData:[],

        },
        docInfoRomeData:{
            originalUrl:'',
            headersTableData:[],
            requestDataTableData:[],
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
                if(newval.source=="API"){
                    this.RequestApi(
                        newval.isTest,
                        newval.apiId,
                        newval.environmentId,
                        newval.testSendData);
                }else{
                    this.assignmentDataToPage(newval.details);
                }
            }
        },
        'RomeData.responseHeadersTableData': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.responseHeadersTableData.length;
                if(dataLength==0){
                    self.RomeData.responseHeadersName='返回Headers';
                }else{
                    self.RomeData.responseHeadersName='返回Headers('+dataLength+')';
                }
            }
        },
        'RomeData.extractTableData': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.extractTableData.length;
                if(dataLength==0){
                    self.RomeData.ExtractResultsName='提取结果';
                }else{
                    self.RomeData.ExtractResultsName='提取结果('+dataLength+')';
                }
            }
        },
        'RomeData.assertionTableData': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.assertionTableData.length;
                if(dataLength==0){
                    self.RomeData.AssertionResultsName='断言结果';
                }else{
                    self.RomeData.AssertionResultsName='断言结果('+dataLength+')';
                }
            }
        },
        'RomeData.preOperationTableData': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.preOperationTableData.length;
                if(dataLength==0){
                    self.RomeData.preOperationName='前置操作';
                }else{
                    self.RomeData.preOperationName='前置操作('+dataLength+')';
                }
            }
        },
        'RomeData.rearOperationTableData': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.rearOperationTableData.length;
                if(dataLength==0){
                    self.RomeData.rearOperationName='后置操作';
                }else{
                    self.RomeData.rearOperationName='后置操作('+dataLength+')';
                }
            }
        },
        'RomeData.errorInfoTableData': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.errorInfoTableData.length;
                if(dataLength==0){
                    self.RomeData.errorInfoName='错误信息';
                }else{
                    self.RomeData.errorInfoName='错误信息('+dataLength+')';
                }
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
            self.RomeData.requestUrl='Null';
            self.RomeData.requestType='Null';
            self.RomeData.stateCode='Null';
            self.RomeData.time='Null';
            self.RomeData.reportState='Null';

            self.RomeData.activeName='responseBody';
            self.RomeData.responseText="";
            self.RomeData.responseHeadersTableData=[];
            self.RomeData.extractTableData=[];
            self.RomeData.assertionTableData=[];
            self.RomeData.preOperationTableData=[];
            self.RomeData.rearOperationTableData=[];
            self.RomeData.errorInfoTableData=[];

            self.docInfoRomeData.originalUrl='';
            self.docInfoRomeData.headersTableData=[];
            self.docInfoRomeData.requestDataTableData=[];
        },
        RequestApi(isTest,apiId,environmentId,testSendData){
            let self = this;
            self.loading=true;
            if(isTest){
                self.$axios.post('/api/ApiIntMaintenance/SendTestRequest',{
                    'testSendData':testSendData,
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.requestUrl = res.data.request.requestUrl;
                        self.RomeData.requestType = res.data.request.requestType;
                        self.RomeData.stateCode = res.data.response.responseCode;

                        self.RomeData.time = res.data.response.time;
                        self.RomeData.reportState = res.data.response.reportState;

                        self.docInfoRomeData.originalUrl = res.data.request.apiUrl;
                        self.docInfoRomeData.headersTableData = res.data.request.headersList;
                        self.docInfoRomeData.requestDataTableData = res.data.request.requestDataList;

                        self.RomeData.responseText = res.data.response.content;
                        self.RomeData.responseHeadersTableData = res.data.response.responseHeaders;

                        self.RomeData.extractTableData = res.data.response.extractTable;
                        self.RomeData.assertionTableData = res.data.response.assertionTable;
                        self.RomeData.preOperationTableData= res.data.response.preOperationTable;
                        self.RomeData.rearOperationTableData= res.data.response.rearOperationTable;

                        self.RomeData.errorInfoTableData = res.data.response.errorInfoTable;
                        self.loading=false;
                    }else{
                        self.$message.error('接口请求失败'+res.data.errorMsg);
                        self.loading=false;
                        self.dialogClose();
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading=false;
                    self.dialogClose();
                })
            }else{
                self.$axios.post('/api/ApiIntMaintenance/SendRequest',Qs.stringify({
                    'apiId':apiId,
                    'environmentId':environmentId,
                })).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.requestUrl = res.data.request.requestUrl;
                        self.RomeData.requestType = res.data.request.requestType;
                        self.RomeData.stateCode = res.data.response.responseCode;

                        self.RomeData.time = res.data.response.time;
                        self.RomeData.reportState = res.data.response.reportState;

                        self.docInfoRomeData.originalUrl = res.data.request.apiUrl;
                        self.docInfoRomeData.headersTableData = res.data.request.headersList;
                        self.docInfoRomeData.requestDataTableData = res.data.request.requestDataList;

                        self.RomeData.responseText = res.data.response.content;
                        self.RomeData.responseHeadersTableData = res.data.response.responseHeaders;

                        self.RomeData.extractTableData = res.data.response.extractTable;
                        self.RomeData.assertionTableData = res.data.response.assertionTable;
                        self.RomeData.preOperationTableData= res.data.response.preOperationTable;
                        self.RomeData.rearOperationTableData= res.data.response.rearOperationTable;

                        self.RomeData.errorInfoTableData = res.data.response.errorInfoTable;
                        self.loading=false;
                    }else{
                        self.$message.error('接口请求失败'+res.data.errorMsg);
                        self.loading=false;
                        self.dialogClose();
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading=false;
                    self.dialogClose();
                })
            }
        },
        assignmentDataToPage(details){//赋值数据到页面
            let self = this;

            self.RomeData.requestUrl = details.requestUrl;
            self.RomeData.requestType = details.requestType;
            self.RomeData.stateCode = details.code;

            self.RomeData.time = details.time;
            self.RomeData.reportState = details.reportState;

            self.docInfoRomeData.originalUrl = details.originalUrl;
            self.docInfoRomeData.headersTableData = details.headersTableData;
            self.docInfoRomeData.requestDataTableData = details.requestDataTableData;

            self.RomeData.responseText = details.responseText;
            self.RomeData.responseHeadersTableData = details.responseHeadersTableData;

            self.RomeData.extractTableData = details.extractTableData;
            self.RomeData.assertionTableData = details.assertionTableData;
            self.RomeData.preOperationTableData= details.preOperationTableData;
            self.RomeData.rearOperationTableData= details.rearOperationTableData;

            self.RomeData.errorInfoTableData = details.errorInfoTableData;
            self.loading=false;
        },
        
    }  
};
</script>

<style>
.test{
    text-align: left;
}
</style>
