<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div
            v-loading="loading"
            element-loading-text="拼命加载中"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.8)">
                <el-row>
                    <el-col :span="2">
                        <el-menu
                            default-active="0"
                            class="MainMenu"
                            @select="handleSelect"
                            @open="handleOpen"
                            @close="handleClose"
                            background-color="#545c64"
                            text-color="#fff"
                            active-text-color="#ffd04b">
                            <el-menu-item index="0">
                                <i class="el-icon-menu"></i>
                                <span slot="title">总览</span>
                            </el-menu-item>
                            <el-menu-item index="1">
                                <i class="el-icon-receiving"></i>
                                <span slot="title">套件</span>
                            </el-menu-item>
                            <el-menu-item index="2">
                                <i class="el-icon-document"></i>
                                <span slot="title">日志</span>
                            </el-menu-item>
                            <!-- <el-menu-item></el-menu-item>
                            <el-menu-item></el-menu-item>
                            <el-menu-item></el-menu-item>
                            <el-menu-item index="10" v-if="isCollapse">
                                <i class="el-icon-arrow-right"></i>
                                <span slot="title">展开</span>
                            </el-menu-item>
                            <el-menu-item index="11" v-else>
                                <i class="el-icon-arrow-left"></i>
                                <span slot="title">折叠</span>
                            </el-menu-item> -->
                        </el-menu>
                    </el-col>
                    <el-col :span="21">
                        <el-card class="MainCard" v-show="OverviewRomeData.disPlay">
                            <div>
                                <el-row :gutter="20">
                                    <el-col :span="11">
                                        <el-card shadow="never" style="height:300px">
                                            <el-row>
                                                <el-col :span='24'>
                                                    <h2 style="margin-top:-10px;float:left">{{OverviewRomeData.titleClass.reportName}}</h2>
                                                    <div style="margin-top:-10px;margin-left:10px;float:left">
                                                        <el-tag v-if="OverviewRomeData.titleClass.reportStatus=='Pass'" type="success">通过</el-tag>
                                                        <el-tag v-else type="warning">未通过</el-tag>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='24'>
                                                    <div style="float:left">
                                                        <span><b>创建时间:</b>{{OverviewRomeData.titleClass.createTime}}</span>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='24'>
                                                    <div style="float:left;margin-top:5px">
                                                        <span><b>耗时时长:</b>{{OverviewRomeData.titleClass.runningTime}} ms</span>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='24'>
                                                    <div style="float:left;margin-top:5px">
                                                        <span><b>创建人:</b>{{OverviewRomeData.titleClass.createUserName}}</span>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                            <el-row>
                                                <el-col :span='12'>
                                                    <div style="margin:10px 0px 0px 60px">
                                                        <el-row>
                                                            <el-col :span='24'>
                                                                <div>
                                                                    <h1>{{OverviewRomeData.titleClass.total}}</h1>
                                                                </div>
                                                            </el-col>
                                                        </el-row>
                                                        <el-row>
                                                            <el-col :span='24'>
                                                                <div style="margin-top:-20px">
                                                                    <span v-if="RomeData.reportType=='API'">独立接口</span>
                                                                    <span v-else-if="RomeData.reportType=='CASE'">独立接口</span>
                                                                    <span v-else-if="RomeData.reportType=='TASK'">测试用例</span>
                                                                    <span v-else-if="RomeData.reportType=='BATCH'">定时任务</span>
                                                                </div>
                                                            </el-col>
                                                        </el-row>
                                                    </div>
                                                </el-col>
                                                <el-col :span='12'>
                                                    <!-- <el-card> -->
                                                    <!-- </el-card> -->
                                                    <div style="margin-top:-130px;margin-left:-120px;" id="EchartContainer-pie" class="EchartContainer-pie"></div>   
                                                </el-col>
                                            </el-row>
                                        </el-card>
                                    </el-col>
                                    <el-col :span="13">
                                        <el-card shadow="never" style="height:300px;width:910px">
                                            <div style="margin-top:-10px" id="EchartContainer-trend" class="EchartContainer-trend"></div>   
                                        </el-card>
                                    </el-col>
                                </el-row>
                            </div>
                            <div style="margin-top:20px">
                                <el-row :gutter="20">
                                    <el-col :span="11">
                                        <el-card shadow="never" style="height:570px">
                                            <div slot="header" style="text-align: left;">
                                                <span v-if="RomeData.reportType=='API'">独立接口</span>
                                                <span v-else-if="RomeData.reportType=='CASE'">独立接口</span>
                                                <span v-else-if="RomeData.reportType=='TASK'">测试用例</span>
                                                <span v-else-if="RomeData.reportType=='BATCH'">定时任务</span>
                                                <span style="color: darkgray;">总共{{OverviewRomeData.dataTable.length}}项</span>
                                            </div>
                                            <div>
                                                <el-table
                                                    style="margin-top:-20px"
                                                    :data="OverviewRomeData.dataTable"
                                                    height="513px">
                                                    <el-table-column
                                                        label="ID"
                                                        align= "center"
                                                        width="70px"
                                                        prop="id">
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="名称"
                                                        align= "center"
                                                        prop="name">
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="统计"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-tag type="success">Pass:{{scope.row.passTotal}}</el-tag>
                                                            <el-tag type="warning">Fail:{{scope.row.failTotal}}</el-tag>
                                                            <el-tag type="danger">Error:{{scope.row.errorTotal}}</el-tag>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="通过率"
                                                        width="80px"
                                                        align= "center"
                                                        prop="passRate">
                                                    </el-table-column>
                                                </el-table>
                                            </div>
                                        </el-card>
                                    </el-col>
                                    <el-col :span="13">
                                        <div>
                                            <el-card shadow="never" style="height:570px">
                                                <div slot="header" style="text-align: left;">
                                                    <span>警示信息</span>
                                                    <span style="color: darkgray;">总共{{OverviewRomeData.warningDataTable.length}}项</span>
                                                </div>
                                                <div>
                                                    <el-table
                                                        style="margin-top:-20px"
                                                        :data="OverviewRomeData.warningDataTable"
                                                        height="513px">
                                                        <el-table-column
                                                            label="ID"
                                                            align= "center"
                                                            width="70px"
                                                            prop="id">
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="触发类型"
                                                            width="100px"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-tag type="info" v-if="scope.row.triggerType=='Warning'">Warning</el-tag>
                                                                <el-tag type="danger" v-else-if="scope.row.triggerType=='Error'">Error</el-tag>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="名称"
                                                            width="300px"
                                                            align= "center"
                                                            prop="taskName">
                                                        </el-table-column>
                                                        <el-table-column
                                                            show-overflow-tooltip
                                                            label="信息"
                                                            align= "center"
                                                            prop="info">
                                                        </el-table-column>
                                                    </el-table>
                                                </div>
                                            </el-card>
                                        </div>
                                    </el-col>
                                </el-row>
                            </div>
                        </el-card>
                        <el-card class="MainCard" v-show="SuiteRomeData.disPlay">
                            <el-row :gutter="5">
                                <el-col :span="10">
                                    <el-card shadow="never" style="height:890px">
                                        <div>
                                            <el-button-group>
                                                <el-button type="info" @click="AllShrink()">概要&nbsp;{{OverviewRomeData.titleClass.passRate}}%</el-button>
                                                <el-button type="danger" @click="AllSelect('Error')">错误&nbsp;{{OverviewRomeData.titleClass.errorTotal}}</el-button>
                                                <el-button type="warning" @click="AllSelect('Fail')">失败&nbsp;{{OverviewRomeData.titleClass.failTotal}}</el-button>
                                                <el-button type="success" @click="AllSelect('Pass')">成功&nbsp;{{OverviewRomeData.titleClass.passTotal}}</el-button>
                                                <el-button type="primary" @click="AllExpand()">所有&nbsp;{{OverviewRomeData.titleClass.allTotal}}</el-button>
                                            </el-button-group>
                                        </div>
                                        <div style="margin-top:10px">
                                            <el-input placeholder="输入关键字进行过滤" v-model="filterText" clearable>
                                            </el-input>
                                            <el-tree 
                                                ref="tree"
                                                node-key="id"
                                                @node-click="handleNodeClick"
                                                :filter-node-method="filterNode"
                                                :data="SuiteRomeData.leftRomeData.tableData" 
                                                :props="SuiteRomeData.leftRomeData.defaultProps"
                                                :default-expanded-keys="SuiteRomeData.leftRomeData.expandedList">
                                                <span class="custom-tree-node" slot-scope="{ node ,data }">
                                                    <el-row :gutter="20">
                                                        <el-col :span="18">
                                                            <div style="width:600px;">
                                                                <el-row>
                                                                    <el-col :span="2">
                                                                        <div v-if="data.layerType=='API'">
                                                                            <el-tag size="mini" type='success' v-if="data.reportStatus=='Pass'"><i class="el-icon-check"></i></el-tag>
                                                                            <el-tag size="mini" type='warning' v-else-if="data.reportStatus=='Fail'"><i class="el-icon-close"></i></el-tag>
                                                                            <el-tag size="mini" type='danger' v-else><i class="el-icon-close"></i></el-tag>
                                                                        </div>
                                                                    </el-col>
                                                                    <el-col :span="12">
                                                                        <div style="float:left">
                                                                            <span v-if="data.layerType=='API'">接口:{{ node.label }}</span>
                                                                            <span v-else-if="data.layerType=='CASE'">测试用例:{{ node.label }}</span>
                                                                            <span v-else-if="data.layerType=='TASK'">定时任务:{{ node.label }}</span>
                                                                        </div>
                                                                    </el-col>
                                                                    <el-col :span="5">
                                                                        <div v-if="data.layerType=='API'">
                                                                            <el-tag size="mini" type='success' v-if="data.code=='200'">{{data.code}}</el-tag>
                                                                            <el-tag size="mini" type='danger' v-else>{{data.code}}</el-tag>
                                                                        </div>
                                                                    </el-col>
                                                                    <el-col :span="5">
                                                                        <div v-if="data.layerType=='API'" style="float:left">
                                                                            <el-tag size="mini" type='info'>{{data.time}} ms</el-tag>
                                                                        </div>
                                                                    </el-col>
                                                                </el-row>
                                                            </div>
                                                        </el-col>
                                                        <el-col :span="6">
                                                            <div style="float:right" v-if="data.layerType!='API'">
                                                                <el-tag type="success" size="mini">{{data.passTotal}}</el-tag>
                                                                <el-tag type="warning" size="mini">{{data.failTotal}}</el-tag>
                                                                <el-tag type="danger" size="mini">{{data.errorTotal}}</el-tag>
                                                            </div>
                                                        </el-col>
                                                    </el-row>
                                                </span>
                                            </el-tree>
                                        </div>
                                    </el-card>
                                </el-col>
                                <el-col :span="14">
                                    <el-card shadow="never" style="height:890px">
                                        <div 
                                        v-if="SuiteRomeData.rightRomeData.disPlay"
                                        v-loading="SuiteRomeData.rightRomeData.loading"
                                        element-loading-text="拼命加载中"
                                        element-loading-spinner="el-icon-loading"
                                        element-loading-background="rgba(0, 0, 0, 0.8)">
                                            <el-tabs v-model="SuiteRomeData.rightRomeData.activeName">
                                                <el-tab-pane label="返回主体" name="ResponseInfo">
                                                    <el-input type="textarea" 
                                                        readonly
                                                        resize="none"
                                                        v-model="SuiteRomeData.rightRomeData.ApiInfo.responseInfo"
                                                        :autosize="{ minRows:37, maxRows: 37}"
                                                        >
                                                    </el-input>
                                                </el-tab-pane>
                                                <el-tab-pane label="Headers" name="Headers">
                                                    <el-collapse v-model="SuiteRomeData.rightRomeData.ApiInfo.headersActiveNames">
                                                        <el-collapse-item  name="General">
                                                            <template slot="title"><b>General</b></template>
                                                            <el-table
                                                            :data="SuiteRomeData.rightRomeData.ApiInfo.generalTableData"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column>
                                                                <template slot-scope="scope">
                                                                    <div v-if="scope.row.key=='Status Code:'">
                                                                        <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                        <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                    </div>
                                                                    <div v-else>
                                                                        <span>{{scope.row.value}}</span>
                                                                    </div>
                                                                </template>
                                                            </el-table-column>
                                                            </el-table>
                                                        </el-collapse-item>
                                                        <el-collapse-item name="responseHeaders">
                                                            <template slot="title"><b>response Headers</b></template>
                                                            <el-table
                                                            :data="SuiteRomeData.rightRomeData.ApiInfo.responseHeaders" 
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </el-collapse-item>
                                                        <el-collapse-item name="RequestHeaders" v-if="SuiteRomeData.rightRomeData.ApiInfo.requestHeaders.length!=0">
                                                            <template slot="title"><b>Request Headers</b></template>
                                                            <el-table
                                                            :data="SuiteRomeData.rightRomeData.ApiInfo.requestHeaders" 
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                label=""
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </el-collapse-item>
                                                        <el-collapse-item name="RequestParameters" v-if="SuiteRomeData.rightRomeData.ApiInfo.requestData.length!=0">
                                                            <template slot="title"><b>Request Parameters</b></template>
                                                            <el-table
                                                            :data="SuiteRomeData.rightRomeData.ApiInfo.requestData"
                                                            height="665px"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </el-collapse-item>
                                                    </el-collapse>
                                                </el-tab-pane>
                                                <el-tab-pane label="前/后置操作" name="operation" v-if="SuiteRomeData.rightRomeData.TestResults.operationTabelData.length!=0">
                                                    <div>
                                                        <el-table
                                                        :data="SuiteRomeData.rightRomeData.TestResults.operationTabelData"
                                                        height="800px">
                                                        <el-table-column
                                                            align="center"
                                                            label="操作位置"
                                                            width="150px">
                                                            <template slot-scope="scope">
                                                                <el-tag type="success" v-if="scope.row.operatingPosition=='Pre'">前置操作</el-tag>
                                                                <el-tag type="danger" v-else>后置操作</el-tag>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="操作类型"
                                                            width="150px"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-tag type="info">{{scope.row.operationType}}</el-tag>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            align="center"
                                                            width='200px'
                                                            label="调用名称"
                                                            prop="callName">
                                                        </el-table-column>
                                                        <el-table-column
                                                            align="center"
                                                            label="调用结果"
                                                            prop="callResults">
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
                                                    </div>
                                                </el-tab-pane>
                                                <el-tab-pane label="测试结果" name="Results" v-if="SuiteRomeData.rightRomeData.TestResults.extractTabelData.length!=0">
                                                    <el-collapse v-model="SuiteRomeData.rightRomeData.TestResults.testResultsActiveNames">
                                                        <el-collapse-item  name="提取结果">
                                                            <template slot="title"><b>提取结果</b></template>
                                                            <el-table
                                                            :data="SuiteRomeData.rightRomeData.TestResults.extractTabelData">
                                                            <el-table-column
                                                                align="center"
                                                                prop="key"
                                                                label="变量名称"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                width='100px'
                                                                label="提取值类型"
                                                                prop="valueType">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="提取值"
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </el-collapse-item>
                                                        <el-collapse-item  name="断言结果">
                                                            <template slot="title"><b>断言结果</b></template>
                                                            <el-table
                                                            :data="SuiteRomeData.rightRomeData.TestResults.validateResults">
                                                            <el-table-column
                                                                align="center"
                                                                prop="checkName"
                                                                label="检查值"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="期望结果"
                                                                prop="retCheckOut">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                width="150px"
                                                                label="比较类型"
                                                                prop="validateType">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="实际返回"
                                                                prop="retExtractorOut">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="测试结果"
                                                                width="100px">
                                                                <template slot-scope="scope">
                                                                    <el-tag type="success" v-if="scope.row.results">通过</el-tag>
                                                                    <el-tag type="warning" v-else>失败</el-tag>
                                                                </template>
                                                            </el-table-column>
                                                            </el-table>
                                                        </el-collapse-item>
                                                    </el-collapse>
                                                </el-tab-pane>
                                                <el-tab-pane label="警告信息" name="ErrorMsg" v-if="SuiteRomeData.rightRomeData.TestResults.errorTableData.length!=0">
                                                    <el-table
                                                        :data="SuiteRomeData.rightRomeData.TestResults.errorTableData">
                                                        <el-table-column
                                                            label="触发时间"
                                                            width="160px"
                                                            align= "center"
                                                            prop="createTime">
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="名称"
                                                            width="200px"
                                                            align= "center"
                                                            prop="errorName">
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="信息"
                                                            align= "center"
                                                            prop="errorInfo">
                                                        </el-table-column>
                                                    </el-table>
                                                </el-tab-pane>
                                            </el-tabs>
                                        </div>
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </template>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import {PrintConsole} from "../../../../../js/Logger.js";
export default {
    data() {
        return {
            loading:false,
            filterText:'',
            RomeData:{
                testReportId:'',
                reportType:'',
                // reportType:'API',
            },
            OverviewRomeData:{//总览
                disPlay:true,
                //标题类
                titleClass:{
                    // reportName:'测试接口报告',
                    // reportStatus:'Pass',
                    // createTime:'2020-01-01 12:22:33',
                    // runningTime:'20',
                    // total:'100',
                    // createUserName:'lipenglo',
                    // passTotal:1,
                    // failTotal:2,
                    // errorTotal:3,
                    // allTotal:10,
                    // passRate:'33',

                    reportName:'',
                    reportStatus:'',
                    createTime:'',
                    runningTime:'',
                    total:0,//这里的为主页的总数显示
                    createUserName:'',
                    passTotal:0,
                    failTotal:0,
                    errorTotal:0,
                    allTotal:0,//这里的为按钮所有的显示
                    passRate:0,
                },
                trendChart:{//趋势图
                    // reportIdList:['#1', '#12', '#33', '#34', '#35', '#36', '#40'],
                    // passList:[120, 132, 101, 134, 90, 230, 210],
                    // failList:[220, 182, 191, 234, 290, 330, 310],
                    // errorList:[150, 232, 201, 154, 190, 330, 410],

                    reportIdList:[],//这里的ID以当前reportId的类型来查询
                    passList:[],
                    failList:[],
                    errorList:[],
                },
                dataTable:[//当前接口，用例，定时任务，批量任务的简要列表,Id为接口或用例的ID
                    // {'id':1,'name':'测试登录接口','passTotal':1,'failTotal':2,'errorTotal':3,'passRate':'30%'},
                ],
                warningDataTable:[//警示信息
                    // {'id':1,'triggerType':'Warning','name':'测试登录接口','info':'我警告你','updateTime':'2020-22-11 12:22:32'},
                    // {'id':1,'triggerType':'Error','name':'测试登录接口','info':'我出错误了你大爷的','updateTime':'2020-22-11 12:22:32'},
                ],
            },
            SuiteRomeData:{//套件
                disPlay:false,
                leftRomeData:{
                    // filterText:'',
                    //这里的ID为item的ID
                    tableData:[
                        // {label: '测试定时任务',id:'1',layerType:'TASK',children: [
                        //     {label: '测试登录',id:'1',layerType:'CASE',children: 
                        //     [
                        //         {label: '登录登录登录登录登录登录登',layerType:'API',id:'1',reportStatus:'Pass','code':200,'time':3},
                        //         {label: '查询',layerType:'API',id:'2',reportStatus:'Fail','code':400,'time':4},
                        //         {label: '删除',layerType:'API',id:'3',reportStatus:'Error','code':500,'time':20},
                        //     ]}
                        // ]}, 
                        // {label: '测试登录',id:'1',layerType:'CASE',children: [
                        //     {label: '查询',layerType:'API',id:'2',reportStatus:'Fail','code':400,'time':4},
                        // ]},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                        // {label: '查询1',layerType:'API',id:'2',reportStatus:'Pass','code':400,'time':4},
                    ],
                    tempTableData:[],//在按钮查询时用来保存查询前的数据保存
                    expandedList:[],//展开列表
                    defaultProps:{
                        children: 'children',
                        label: 'label'
                    }
                },
                rightRomeData:{
                    loading:false,
                    disPlay:false,
                    activeName:'ResponseInfo',
                    ApiInfo:{//接口的信息
                        generalTableData:[],
                        headersActiveNames: [],//如果需要全部展开，就把name放在这里
                        requestHeaders:[],
                        requestData:[],
                        // requestFile:[],
                        responseHeaders:[],
                        responseInfo:'',
                    },
                    TestResults:{
                        testResultsActiveNames: ['提取结果','断言结果'],//如果需要全部展开，就把name放在这里
                        extractTabelData:[],//请求提取
                        validateResults:[],
                        operationTabelData:[],
                        errorTableData:[],
                    },

                }
            }
        };
    },
    watch:{
        filterText(val) {
            this.$refs.tree.filter(val);
        }
    },
    mounted(){
        PrintConsole('query',this.$route.query);
        this.clearRomeData();
        this.clearOverviewRomeData();
        this.clearSuiteRomeData();
        this.clearApiRomeData();
        

        this.RomeData.testReportId = this.$route.query.testReportId;
        this.RomeData.reportType = this.$route.query.reportType;
        this.loadReportData(this.RomeData.testReportId);


        // this.PieChart(this.OverviewRomeData.titleClass.passRate);
        // this.TrendChart();

    },
    methods: {
        //菜单 固定值
        handleOpen(key, keyPath) {
            PrintConsole(key, keyPath);
        },
        handleClose(key, keyPath) {
            PrintConsole(key, keyPath);
        },
        handleSelect(key, keyPath){
            PrintConsole(key, keyPath);
            if(key=='0'){
                this.OverviewRomeData.disPlay=true;
                this.SuiteRomeData.disPlay=false;
            }else if(key=='1'){
              this.SuiteRomeData.disPlay=true;
              this.OverviewRomeData.disPlay=false;
            }
        },

        // 初始化
        clearRomeData(){
            let self = this;
            self.RomeData.testReportId='';
            self.RomeData.reportType='';
        },
        clearOverviewRomeData(){
            let self = this;
            self.OverviewRomeData.titleClass.reportName='';
            self.OverviewRomeData.titleClass.reportStatus='';
            self.OverviewRomeData.titleClass.createTime='';
            self.OverviewRomeData.titleClass.runningTime='';
            self.OverviewRomeData.titleClass.createUserName='';
            self.OverviewRomeData.titleClass.total=0;
            self.OverviewRomeData.titleClass.passTotal=0;
            self.OverviewRomeData.titleClass.failTotal=0;
            self.OverviewRomeData.titleClass.errorTotal=0;
            self.OverviewRomeData.titleClass.allTotal=0;
            self.OverviewRomeData.titleClass.passRate=0;

            self.OverviewRomeData.trendChart.reportIdList=[];
            self.OverviewRomeData.trendChart.passList=[];
            self.OverviewRomeData.trendChart.failList=[];
            self.OverviewRomeData.trendChart.errorList=[];

            self.OverviewRomeData.trendChart.dataTable=[];
            self.OverviewRomeData.trendChart.warningDataTable=[];
        },
        clearSuiteRomeData(){
            let self = this;
            self.filterText='';
            self.SuiteRomeData.leftRomeData.tableData=[];
        },
        clearApiRomeData(){
            let self = this;
            self.SuiteRomeData.rightRomeData.activeName='ResponseInfo';
            self.SuiteRomeData.rightRomeData.loading=false;

            self.SuiteRomeData.rightRomeData.ApiInfo.generalTableData = [];
            self.SuiteRomeData.rightRomeData.ApiInfo.requestHeaders = [];
            self.SuiteRomeData.rightRomeData.ApiInfo.requestData = [];
            self.SuiteRomeData.rightRomeData.ApiInfo.requestFile= [];
            self.SuiteRomeData.rightRomeData.ApiInfo.responseHeaders=[];
            self.SuiteRomeData.rightRomeData.ApiInfo.responseInfo='';

            self.SuiteRomeData.rightRomeData.TestResults.extractTabelData =[];
            self.SuiteRomeData.rightRomeData.TestResults.validateResults = [];
            self.SuiteRomeData.rightRomeData.TestResults.operationTabelData = [];
            self.SuiteRomeData.rightRomeData.TestResults.errorTableData =[];
        },

        //点击节点
        handleNodeClick(data){
            PrintConsole(data);
            let self = this;
            self.SuiteRomeData.rightRomeData.disPlay=true;
            if(data.layerType=="API"){
                self.clearApiRomeData();
                self.SuiteRomeData.rightRomeData.loading=true;
                self.$axios.get('/api/ApiTestReport/LoadReportApi',{//请求接口数据
                    params:{
                        'reportItemId':data.id
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.SuiteRomeData.rightRomeData.ApiInfo.generalTableData = res.data.TableData.general;
                        self.SuiteRomeData.rightRomeData.ApiInfo.requestHeaders = res.data.TableData.requestHeaders;
                        self.SuiteRomeData.rightRomeData.ApiInfo.requestData = res.data.TableData.requestData;
                        self.SuiteRomeData.rightRomeData.ApiInfo.responseHeaders = res.data.TableData.responseHeaders;
                        self.SuiteRomeData.rightRomeData.ApiInfo.responseInfo = res.data.TableData.responseInfo;

                        self.SuiteRomeData.rightRomeData.TestResults.extractTabelData= res.data.TableData.extract;
                        self.SuiteRomeData.rightRomeData.TestResults.validateResults = res.data.TableData.validateResults;
                        self.SuiteRomeData.rightRomeData.TestResults.operationTabelData = res.data.TableData.operationData;
                        self.SuiteRomeData.rightRomeData.TestResults.errorTableData = res.data.TableData.errorTableData;

                        self.SuiteRomeData.rightRomeData.loading = false;
                    }
                    else{
                        self.$message.error('接口步骤获取失败:'+ res.data.errorMsg);
                        self.SuiteRomeData.rightRomeData.loading = false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.SuiteRomeData.rightRomeData.loading = false;
                })
            }     
        },
        filterNode(value, data){//查询使用
            PrintConsole(data)
            if (!value) return true;
                return data.label.indexOf(value) !== -1;
        },
        //按钮组
        AllExpand(){//展开
            let self = this;
            //复原数据
            self.SuiteRomeData.leftRomeData.tableData = self.SuiteRomeData.leftRomeData.tempTableData;
            self.SuiteRomeData.leftRomeData.tableData.forEach(d=>{
                if(self.RomeData.reportType=="API"){
                    self.SuiteRomeData.leftRomeData.expandedList.push(d.id);
                }else{
                    d.children.forEach(item=>{
                        // PrintConsole(item)
                        self.SuiteRomeData.leftRomeData.expandedList.push(item.id);
                    })
                }
            });
        },
        AllShrink(){//收缩
            let self = this;
            //复原数据
            self.SuiteRomeData.leftRomeData.tableData = self.SuiteRomeData.leftRomeData.tempTableData;
            if(self.RomeData.reportType=="BATCH"){
                this.$refs.tree.$children[0].node.parent.childNodes[0].expanded=false;
            }else if(self.RomeData.reportType=="TASK"){
                this.$refs.tree.$children[0].node.parent.childNodes.forEach(d=>{
                    d.expanded=false;
                });

            }

        },
        AllSelect(value){
            let self = this;
            let tempData = [];
            // PrintConsole('tempTableData',self.SuiteRomeData.leftRomeData.tempTableData)
            //复原数据
            self.SuiteRomeData.leftRomeData.tableData = self.SuiteRomeData.leftRomeData.tempTableData;

            self.SuiteRomeData.leftRomeData.tableData.forEach(item=>{
                PrintConsole(item)
                if(item.reportStatus == value){
                    tempData.push(item)
                }
            });
            self.SuiteRomeData.leftRomeData.tableData = tempData;
        },


        loadReportData(testReportId){
            let self = this;
            self.loading=true;
            self.$axios.get('/api/ApiTestReport/loadReportData',{//请求接口数据
                params:{
                    'testReportId':testReportId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    //总览
                    //左上角
                    self.OverviewRomeData.titleClass.reportName = res.data.overview.titleClass.reportName;
                    self.OverviewRomeData.titleClass.reportStatus = res.data.overview.titleClass.reportStatus;
                    self.OverviewRomeData.titleClass.createTime = res.data.overview.titleClass.createTime;
                    self.OverviewRomeData.titleClass.runningTime = res.data.overview.titleClass.runningTime;
                    self.OverviewRomeData.titleClass.createUserName = res.data.overview.titleClass.createUserName;
                    self.OverviewRomeData.titleClass.total = res.data.overview.titleClass.allTotal;
                    let passTotal = res.data.overview.titleClass.passTotal;
                    let failTotal = res.data.overview.titleClass.failTotal;
                    let errorTotal = res.data.overview.titleClass.errorTotal;
                    self.OverviewRomeData.titleClass.passTotal = passTotal;
                    self.OverviewRomeData.titleClass.failTotal = failTotal;
                    self.OverviewRomeData.titleClass.errorTotal = errorTotal;
                    self.OverviewRomeData.titleClass.passRate = res.data.overview.titleClass.passRate;
                    self.OverviewRomeData.titleClass.allTotal = passTotal+failTotal+errorTotal;

                    self.PieChart(self.OverviewRomeData.titleClass.passRate);

                    //右上角
                    self.OverviewRomeData.trendChart.reportIdList= res.data.overview.trendChart.reportIdList;
                    self.OverviewRomeData.trendChart.passList= res.data.overview.trendChart.passList;
                    self.OverviewRomeData.trendChart.failList= res.data.overview.trendChart.failList;
                    self.OverviewRomeData.trendChart.errorList= res.data.overview.trendChart.errorList;
                    self.TrendChart();

                    //左下角列表
                    self.OverviewRomeData.dataTable = res.data.overview.reportBriefItemData;
                    
                    //右下角列表
                    self.OverviewRomeData.warningDataTable = res.data.overview.warngigInfo;

                    //套件
                    self.SuiteRomeData.leftRomeData.tableData = res.data.suite.tableData;
                    self.SuiteRomeData.leftRomeData.tempTableData = res.data.suite.tableData;


                    self.loading = false;
                }
                else{
                    self.$message.error('报告骤获取失败:'+ res.data.errorMsg);
                    self.loading = false;
                }
            }).catch(function (error) {
                console.log(error);
                // self.loading = false;
            })

        },
        PieChart(passRate){//通过率
            let self = this;
            var MyChart_pie = echarts.init(document.getElementById('EchartContainer-pie'));//初始化
            var option = {//设置各属性和数据
                tooltip: {
                    trigger: 'item', //通过哪种方式触发tip
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
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
                                formatter:'通过率\n'+passRate+'%',
                                emphasis:{//中间文字显示
                                    show:true
                                }
                            }
                        },
                        data:[
                            {"value": self.OverviewRomeData.titleClass.passTotal, "name": 'Pass', "itemStyle": {"normal": {"color": '#91cc75'}}},
                            {"value": self.OverviewRomeData.titleClass.failTotal, "name": 'Fail', "itemStyle": {"normal": {"color": '#fac858'}}},
                            {"value": self.OverviewRomeData.titleClass.errorTotal, "name": 'Error', "itemStyle": {"normal": {"color": '#ee6666'}}},
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
            MyChart_pie.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
        TrendChart(){//趋势图
            let self = this;
            var MyChart_trend = echarts.init(document.getElementById('EchartContainer-trend'));//初始化
            var option = {
                title: {
                    text: '历史趋势图:近100条数据'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    }
                },
                // legend: {
                //     data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
                // },
                // toolbox: {
                //     feature: {
                //     saveAsImage: {}
                //     }
                // },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: self.OverviewRomeData.trendChart.reportIdList
                    }
                ],
                yAxis: [
                    {
                    type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'Pass',
                        type: 'line',
                        stack: 'Total',
                        color: '#91cc75',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: self.OverviewRomeData.trendChart.passList
                    },
                    {
                        name: 'Fail',
                        type: 'line',
                        stack: 'Total',
                        color: '#fac858',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: self.OverviewRomeData.trendChart.failList
                    },
                    {
                        name: 'Error',
                        type: 'line',
                        color: '#ee6666',
                        stack: 'Total',
                        areaStyle: {},
                        emphasis: {
                            focus: 'series'
                        },
                        data: self.OverviewRomeData.trendChart.errorList
                    },
                ]
            };


            MyChart_trend.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
    }
};
</script>

<style>
.MainMenu{
    height: 930px;
}
.MainCard{
    height: 928px;
    width: 1740px;
}

.EchartContainer-pie{
    width:600px; 
    height:270px;
    
}

.EchartContainer-trend{
    width:900px; 
    height:280px;
    /* color: darkgray; */
    
    
}
</style>