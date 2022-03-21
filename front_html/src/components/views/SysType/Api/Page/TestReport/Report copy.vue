<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div ref="tab-second" class="flex-layout" id="tab-second">
                <el-row>
                    <el-col :span="10">
                        <el-row class="TopTitle">
                            <el-col :span="24">
                                <h1>{{RomeData.TopData.reportName}}</h1>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>创建时间:</strong>
                                    <el-tag>{{RomeData.TopData.createTime}}</el-tag>
                                </div>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>耗时时长:</strong>
                                    <el-tag type="success">{{RomeData.TopData.runningTime}}</el-tag>
                                </div>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>测试统计:</strong>
                                    <el-tag type="success">成功:{{RomeData.TopData.passTotal}}</el-tag>&nbsp;&nbsp;
                                    <el-tag type="warning">失败:{{RomeData.TopData.failTotal}}</el-tag>&nbsp;&nbsp;
                                    <el-tag type="danger">错误:{{RomeData.TopData.errorTotal}}</el-tag>&nbsp;
                                </div>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>测试结果:</strong>
                                    <el-tag v-if="RomeData.TopData.reportStatus=='Pass'" type="success">通过</el-tag>
                                    <el-tag v-else type="warning">未通过</el-tag>
                                </div>
                            </el-col>
                        </el-row>
                    </el-col>
                    <el-card shadow="never" style="height:250px">
                        <el-col :span="7">
                            <div style="margin-top:-10px" id="EchartContainer-bar" class="EchartContainer-bar"></div>   
                        </el-col>
                        <el-col :span="7">
                            <div style="margin-top:-55px;margin-left:200px" id="EchartContainer-pie" class="EchartContainer-pie"></div>   
                        </el-col>
                    </el-card>
                </el-row>
                <div style="margin-top:-10px">
                    <el-divider></el-divider>
                </div>
                <div style="margin-top:-15px">
                    <template>
                        <el-tabs tab-position="left" @tab-click="handleClick_firstMenu"> 
                            <el-tab-pane  v-for="pane in RomeData.firstList" :key="pane.name" :label="pane.label" :name="pane.name">
                                <div v-if="RomeData.reportType=='API' || RomeData.reportType=='CASE'">
                                    <el-collapse>
                                        <div v-loading="loading">
                                            <template>
                                                <el-tabs v-model="RomeData.activeName">
                                                    <el-tab-pane label="返回主体" name="ResponseInfo">
                                                        <el-input type="textarea" 
                                                            readonly
                                                            resize="none"
                                                            v-model="RomeData.ApiInfo.responseInfo"
                                                            :autosize="{ minRows: 26, maxRows: 26}"
                                                            >
                                                        </el-input>
                                                    </el-tab-pane>
                                                    <el-tab-pane label="Headers" name="Headers">
                                                        <el-collapse v-model="RomeData.ApiInfo.headersActiveNames">
                                                            <el-collapse-item  name="General">
                                                                <template slot="title"><b>General</b></template>
                                                                <el-table
                                                                :data="RomeData.ApiInfo.generalTableData"
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
                                                                :data="RomeData.ApiInfo.responseHeaders" 
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
                                                            <el-collapse-item name="RequestHeaders" v-if="RomeData.ApiInfo.requestHeaders.length!=0">
                                                                <template slot="title"><b>Request Headers</b></template>
                                                                <el-table
                                                                :data="RomeData.ApiInfo.requestHeaders" 
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
                                                            <el-collapse-item name="RequestParameters" v-if="RomeData.ApiInfo.requestData.length!=0">
                                                                <template slot="title"><b>Request Parameters</b></template>
                                                                <el-table
                                                                :data="RomeData.ApiInfo.requestData"
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
                                                    <el-tab-pane label="前/后置操作" name="operation" v-if="RomeData.TestResults.operationTabelData.length!=0">
                                                        <div>
                                                            <el-table
                                                            :data="RomeData.TestResults.operationTabelData"
                                                           >
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
                                                    <el-tab-pane label="测试结果" name="Results" v-if="RomeData.TestResults.extractTabelData.length!=0">
                                                        <el-collapse v-model="RomeData.TestResults.testResultsActiveNames">
                                                            <el-collapse-item  name="提取结果">
                                                                <template slot="title"><b>提取结果</b></template>
                                                                <el-table
                                                                :data="RomeData.TestResults.extractTabelData">
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
                                                                :data="RomeData.TestResults.validateResults">
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
                                                    <el-tab-pane label="错误信息" name="ErrorMsg" v-if="RomeData.TestResults.errorTableData.length!=0">
                                                        <el-table
                                                            :data="RomeData.TestResults.errorTableData">
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
                                            </template>
                                        </div>
                                    </el-collapse>
                                </div>
                                <div v-else-if="RomeData.reportType=='TASK'">
                                    <el-tabs tab-position="left" @tab-click="handleClick_secondMenu"> 
                                        <el-tab-pane v-for="pane in RomeData.secondList" :key="pane.name" :label="pane.label" :name="pane.name" v-loading="loading">
                                            <el-collapse>
                                                <div v-loading="loading" v-if="RomeData.disPlay_second">
                                                    <template>
                                                        <el-tabs v-model="RomeData.activeName">
                                                            <el-tab-pane label="返回主体" name="ResponseInfo">
                                                                <el-input type="textarea" 
                                                                    readonly
                                                                    resize="none"
                                                                    v-model="RomeData.ApiInfo.responseInfo"
                                                                    :autosize="{ minRows: 26, maxRows: 26}"
                                                                    >
                                                                </el-input>
                                                            </el-tab-pane>
                                                            <el-tab-pane label="Headers" name="Headers">
                                                                <el-collapse v-model="RomeData.ApiInfo.headersActiveNames">
                                                                    <el-collapse-item  name="General">
                                                                        <template slot="title"><b>General</b></template>
                                                                        <el-table
                                                                        :data="RomeData.ApiInfo.generalTableData"
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
                                                                        :data="RomeData.ApiInfo.responseHeaders" 
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
                                                                    <el-collapse-item name="RequestHeaders" v-if="RomeData.ApiInfo.requestHeaders.length!=0">
                                                                        <template slot="title"><b>Request Headers</b></template>
                                                                        <el-table
                                                                        :data="RomeData.ApiInfo.requestHeaders" 
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
                                                                    <el-collapse-item name="RequestParameters" v-if="RomeData.ApiInfo.requestData.length!=0">
                                                                        <template slot="title"><b>Request Parameters</b></template>
                                                                        <el-table
                                                                        :data="RomeData.ApiInfo.requestData"
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
                                                            <el-tab-pane label="前/后置操作" name="operation" v-if="RomeData.TestResults.operationTabelData.length!=0">
                                                                <div>
                                                                    <el-table
                                                                    :data="RomeData.TestResults.operationTabelData"
                                                                >
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
                                                            <el-tab-pane label="测试结果" name="Results" v-if="RomeData.TestResults.extractTabelData.length!=0">
                                                                <el-collapse v-model="RomeData.TestResults.testResultsActiveNames">
                                                                    <el-collapse-item  name="提取结果">
                                                                        <template slot="title"><b>提取结果</b></template>
                                                                        <el-table
                                                                        :data="RomeData.TestResults.extractTabelData">
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
                                                                        :data="RomeData.TestResults.validateResults">
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
                                                            <el-tab-pane label="错误信息" name="ErrorMsg" v-if="RomeData.TestResults.errorTableData.length!=0">
                                                                <el-table
                                                                    :data="RomeData.TestResults.errorTableData">
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
                                                    </template>
                                                </div>
                                            </el-collapse>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                                <div v-else>
                                    <el-tabs tab-position="left" @tab-click="handleClick_secondMenu"> 
                                        <el-tab-pane v-for="pane in RomeData.secondList" :key="pane.name" :label="pane.label" :name="pane.name" v-loading="loading">
                                            <el-tabs tab-position="left" @tab-click="handleClick_thirdMenu"> 
                                                <el-tab-pane v-for="pane in RomeData.thirdList" :key="pane.name" :label="pane.label" :name="pane.name" v-loading="loading">
                                                    <el-collapse>
                                                        <div v-loading="loading" v-if="RomeData.disPlay_fourth">
                                                            <template>
                                                                <el-tabs v-model="RomeData.activeName">
                                                                    <el-tab-pane label="返回主体" name="ResponseInfo">
                                                                        <el-input type="textarea" 
                                                                            readonly
                                                                            resize="none"
                                                                            v-model="RomeData.ApiInfo.responseInfo"
                                                                            :autosize="{ minRows: 26, maxRows: 26}"
                                                                            >
                                                                        </el-input>
                                                                    </el-tab-pane>
                                                                    <el-tab-pane label="Headers" name="Headers">
                                                                        <el-collapse v-model="RomeData.ApiInfo.headersActiveNames">
                                                                            <el-collapse-item  name="General">
                                                                                <template slot="title"><b>General</b></template>
                                                                                <el-table
                                                                                :data="RomeData.ApiInfo.generalTableData"
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
                                                                                :data="RomeData.ApiInfo.responseHeaders" 
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
                                                                            <el-collapse-item name="RequestHeaders" v-if="RomeData.ApiInfo.requestHeaders.length!=0">
                                                                                <template slot="title"><b>Request Headers</b></template>
                                                                                <el-table
                                                                                :data="RomeData.ApiInfo.requestHeaders" 
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
                                                                            <el-collapse-item name="RequestParameters" v-if="RomeData.ApiInfo.requestData.length!=0">
                                                                                <template slot="title"><b>Request Parameters</b></template>
                                                                                <el-table
                                                                                :data="RomeData.ApiInfo.requestData"
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
                                                                    <el-tab-pane label="前/后置操作" name="operation" v-if="RomeData.TestResults.operationTabelData.length!=0">
                                                                        <div>
                                                                            <el-table
                                                                            :data="RomeData.TestResults.operationTabelData"
                                                                        >
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
                                                                    <el-tab-pane label="测试结果" name="Results" v-if="RomeData.TestResults.extractTabelData.length!=0">
                                                                        <el-collapse v-model="RomeData.TestResults.testResultsActiveNames">
                                                                            <el-collapse-item  name="提取结果">
                                                                                <template slot="title"><b>提取结果</b></template>
                                                                                <el-table
                                                                                :data="RomeData.TestResults.extractTabelData">
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
                                                                                :data="RomeData.TestResults.validateResults">
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
                                                                    <el-tab-pane label="错误信息" name="ErrorMsg" v-if="RomeData.TestResults.errorTableData.length!=0">
                                                                        <el-table
                                                                            :data="RomeData.TestResults.errorTableData">
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
                                                            </template>
                                                        </div>
                                                    </el-collapse>
                                                </el-tab-pane>
                                            </el-tabs>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                            </el-tab-pane>
                        </el-tabs>
                    </template>
                </div>
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
            RomeData:{
                testReportId:'',
                reportType:'',
                TopData:{//头部数据
                    reportName:'',//报告标题
                    createTime:'',//开始时间
                    runningTime:'',//运行时长
                    passTotal:'',//成功数
                    failTotal:'',//失败数
                    errorTotal:'',//错误数
                    passRate:0,//通过率
                },
                activeName:'ResponseInfo',
                firstList:[],//1级菜单列表
                secondList:[],//2级菜单列表
                thirdList:[],//3级菜单列表

                disPlay_second:false,//第2层
                disPlay_fourth:false,//第4层

                ApiInfo:{
                    //接口的信息
                    generalTableData:[],
                    headersActiveNames: [],//如果需要全部展开，就把name放在这里
                    requestHeaders:[],
                    requestData:[],
                    requestFile:[],
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
        };
    },
    mounted(){
        PrintConsole('query',this.$route.query);
        this.RomeData.testReportId = this.$route.query.testReportId;
        this.RomeData.reportType = this.$route.query.reportType;
        this.openFullScreen();
        this.loadReportData(this.RomeData.testReportId);
        // this.BarChart();
        // this.PieChart();


    },
    methods: {
        openFullScreen() {//全屏加载显示
            this.loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
        },
        BarChart(){
            let self = this;
            var MyChart_bar = echarts.init(document.getElementById('EchartContainer-bar'));//初始化
            var option = {//设置各属性和数据
                title: {
                    show: true, //显示折线图
                    //   text: '各应用折线图:', //标题文字
                    left: 50, //配置title的位置
                    top:-10,
                    padding: [20,20,5,10] //title的padding值
                },
                tooltip: {
                    trigger: 'axis' //通过哪种方式触发tip
                },
                //图例，选择要显示的项目
                legend:{
                    left:'center',
                    data:['Pass','Fail','Error']//注意要和数据的name相对应
                },
                xAxis: {
                    type:'category',
                    data: ['本次执行接口步骤统计'],
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {  
                        show: true,  
                        interval: 'auto',  
                        formatter: '{value}'  
                    },  
                    // splitLine: {//y轴横线图
                    //     show: true
                    // }
                },
                series: [
                    {"name": 'Pass',"data": [self.RomeData.TopData.passTotal],"type": 'bar',"itemStyle": {
                        "normal": {"color": '#91cc75'}}, 
                        "label": {'normal': {'show': 'true', 'position': 'top'}}
                    },
                    {"name": 'Fail',"data": [self.RomeData.TopData.failTotal],"type": 'bar',"itemStyle": {
                        "normal": {"color": '#fac858'}}, 
                        "label": {'normal': {'show': 'true', 'position': 'top'}}
                    },
                    {"name": 'Error',"data": [self.RomeData.TopData.errorTotal],"type": 'bar',"itemStyle": {
                        "normal": {"color": '#ee6666'}}, 
                        "label": {'normal': {'show': 'true', 'position': 'top'}}
                    },

                ]
            };
            MyChart_bar.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
        PieChart(passRate){
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
                            {"value": self.RomeData.TopData.passTotal, "name": 'Pass', "itemStyle": {"normal": {"color": '#91cc75'}}},
                            {"value": self.RomeData.TopData.failTotal, "name": 'Fail', "itemStyle": {"normal": {"color": '#fac858'}}},
                            {"value": self.RomeData.TopData.errorTotal, "name": 'Error', "itemStyle": {"normal": {"color": '#ee6666'}}},
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
        ClearApiInfoResultsRomeData(){
            let self = this;
            self.RomeData.activeName='ResponseInfo';
            self.RomeData.secondList=[];
            self.RomeData.thirdList = [];

            self.RomeData.disPlay_second=false;
            self.RomeData.disPlay_fourth=false;


            self.RomeData.ApiInfo.generalTableData = [];
            self.RomeData.ApiInfo.requestHeaders = [];
            self.RomeData.ApiInfo.requestData = [];
            self.RomeData.ApiInfo.requestFile= [];
            self.RomeData.ApiInfo.responseHeaders=[];
            self.RomeData.ApiInfo.responseInfo='';

            self.RomeData.TestResults.extractTabelData =[];
            self.RomeData.TestResults.validateResults = [];
            self.RomeData.TestResults.operationTabelData = [];
            self.RomeData.TestResults.errorTableData =[];

        },
        handleClick_firstMenu(tab, event){//点击1级名称加载2层数据
            PrintConsole(tab, event);
            let self = this;
            self.loading=true;
            self.RomeData.disPlay_second=false;
            self.ClearApiInfoResultsRomeData();
            if(self.RomeData.reportType=='API' || self.RomeData.reportType=='CASE'){
                self.disPlay_second=true;
                self.$axios.get('/api/ApiTestReport/LoadReportApi',{//请求接口数据
                    params:{
                        'reportItemId':tab.name
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.ApiInfo.generalTableData = res.data.TableData.general;
                        self.RomeData.ApiInfo.requestHeaders = res.data.TableData.requestHeaders;
                        self.RomeData.ApiInfo.requestData = res.data.TableData.requestData;
                        // self.NewRomeData.RequestFile = res.data.TableData.requestFile;

                        self.RomeData.ApiInfo.responseHeaders = res.data.TableData.responseHeaders;
                        self.RomeData.ApiInfo.responseInfo = res.data.TableData.responseInfo;

                        self.RomeData.TestResults.extractTabelData= res.data.TableData.extract;
                        self.RomeData.TestResults.validateResults = res.data.TableData.validateResults;
                        self.RomeData.TestResults.operationTabelData = res.data.TableData.operationData;
                        self.RomeData.TestResults.errorTableData = res.data.TableData.errorTableData;

                        self.loading = false;
                    }
                    else{
                        self.$message.error('接口步骤获取失败:'+ res.data.errormsg);
                        self.loading = false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading = false;
                })
            }else{
            // }else if(self.RomeData.reportType=='TASK'){
                self.$axios.get('/api/ApiTestReport/loadReportCase',{//请求接口数据
                    params:{
                        'reportType':self.RomeData.reportType,
                        'testReportId':self.RomeData.testReportId,
                        'id':tab.name
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                         //列表2层数据加载
                        res.data.secondList.forEach(d=>{
                            let obj = {};
                            let lebel = '';
                            if(d.reportStatus=='Fail'){
                                lebel='<失败>---'+d.name;
                            }else if(d.reportStatus=='Error'){
                                lebel='<错误>---'+d.name;
                            }else{
                                lebel=d.name;
                            }
                            // obj.id = d.id;
                            obj.name = String(d.id);
                            obj.label = lebel;
                            // obj.reportStatus = d.reportStatus;

                            self.RomeData.secondList.push(obj);
                        });
                        self.loading = false;
                    }
                    else{
                        self.$message.error('用例步骤获取失败:'+ res.data.errormsg);
                        self.loading = false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading = false;
                })
            }
        },
        handleClick_secondMenu(tab,event){
            PrintConsole('handleClick_secondMenu',tab)
            let self = this;
            if(self.RomeData.reportType=='API' ||self.RomeData.reportType== 'CASE'||self.RomeData.reportType=='TASK'){
                self.loading=true;
                self.RomeData.disPlay_second=true;
                self.$axios.get('/api/ApiTestReport/LoadReportApi',{//请求接口数据
                    params:{
                        'reportItemId':tab.name
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.ApiInfo.generalTableData = res.data.TableData.general;
                        self.RomeData.ApiInfo.requestHeaders = res.data.TableData.requestHeaders;
                        self.RomeData.ApiInfo.requestData = res.data.TableData.requestData;
                        // self.NewRomeData.RequestFile = res.data.TableData.requestFile;

                        self.RomeData.ApiInfo.responseHeaders = res.data.TableData.responseHeaders;
                        self.RomeData.ApiInfo.responseInfo = res.data.TableData.responseInfo;

                        self.RomeData.TestResults.extractTabelData= res.data.TableData.extract;
                        self.RomeData.TestResults.validateResults = res.data.TableData.validateResults;
                        self.RomeData.TestResults.operationTabelData = res.data.TableData.operationData;
                        self.RomeData.TestResults.errorTableData = res.data.TableData.errorTableData;

                        self.loading = false;
                    }
                    else{
                        self.$message.error('接口步骤获取失败:'+ res.data.errormsg);
                        self.loading = false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading = false;
                })
            }else{
                self.RomeData.thirdList=[]
                self.loading=true;
                self.$axios.get('/api/ApiTestReport/loadReportCase',{//请求接口数据
                    params:{
                        'reportType':'TASK',
                        'testReportId':self.RomeData.testReportId,
                        'id':tab.name
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                         //列表2层数据加载
                        res.data.secondList.forEach(d=>{
                            let obj = {};
                            let lebel = '';
                            if(d.reportStatus=='Fail'){
                                lebel='<失败>---'+d.name;
                            }else if(d.reportStatus=='Error'){
                                lebel='<错误>---'+d.name;
                            }else{
                                lebel=d.name;
                            }
                            obj.name = String(d.id);
                            obj.label = lebel;

                            self.RomeData.thirdList.push(obj);
                        });
                        self.loading = false;
                    }
                    else{
                        self.$message.error('用例步骤获取失败:'+ res.data.errormsg);
                        self.loading = false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading = false;
                })
            }
        },
        handleClick_thirdMenu(tab,event){
            PrintConsole(tab);
            let self = this;
            self.loading=true;
            self.RomeData.disPlay_fourth=true;
                self.$axios.get('/api/ApiTestReport/LoadReportApi',{//请求接口数据
                    params:{
                        'reportItemId':tab.name
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.ApiInfo.generalTableData = res.data.TableData.general;
                        self.RomeData.ApiInfo.requestHeaders = res.data.TableData.requestHeaders;
                        self.RomeData.ApiInfo.requestData = res.data.TableData.requestData;
                        // self.NewRomeData.RequestFile = res.data.TableData.requestFile;

                        self.RomeData.ApiInfo.responseHeaders = res.data.TableData.responseHeaders;
                        self.RomeData.ApiInfo.responseInfo = res.data.TableData.responseInfo;

                        self.RomeData.TestResults.extractTabelData= res.data.TableData.extract;
                        self.RomeData.TestResults.validateResults = res.data.TableData.validateResults;
                        self.RomeData.TestResults.operationTabelData = res.data.TableData.operationData;
                        self.RomeData.TestResults.errorTableData = res.data.TableData.errorTableData;

                        self.loading = false;
                    }
                    else{
                        self.$message.error('接口步骤获取失败:'+ res.data.errormsg);
                        self.loading = false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading = false;
                })
        },
        loadReportData(testReportId){
            let self = this;
            // self.$store.commit("addToken",tokey)//把token信息放到vuex中
            self.$axios.get('/api/ApiTestReport/loadReportData',{//请求接口数据
                params:{
                    'testReportId':testReportId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.TopData.reportName = res.data.topData.reportName;
                    self.RomeData.TopData.createTime = res.data.topData.createTime;
                    self.RomeData.TopData.runningTime = res.data.topData.runningTime+'s';
                    self.RomeData.TopData.reportStatus = res.data.topData.reportStatus;

                    self.RomeData.TopData.passTotal = res.data.topData.passTotal;
                    self.RomeData.TopData.failTotal = res.data.topData.failTotal;
                    self.RomeData.TopData.errorTotal = res.data.topData.errorTotal;

                    self.BarChart();
                    self.PieChart(res.data.topData.passRate);


                    //列表1层数据加载
                    res.data.firstList.forEach(d=>{
                        let obj = {};
                        let lebel = '';
                        if(d.reportStatus=='Fail'){
                            lebel='<失败>---'+d.name;
                        }else if(d.reportStatus=='Error'){
                            lebel='<错误>---'+d.name;
                        }else{
                            lebel=d.name;
                        }
                        obj.name = String(d.id);
                        obj.label = lebel;

                        self.RomeData.firstList.push(obj);
                    });
                    self.loading.close();
                }
                else{
                    self.$message.error('报告获取失败:'+ res.data.errorMsg);
                    self.loading.close();
                }
            }).catch(function (error) {
                console.log(error);
                self.loading.close();
            })
        },
    }
};
</script>

<style>
.flex-layout{
    /* text-align:center;
    float:center; */
    margin:0 auto;
    width:1700px; 
}
.TopTitle{
    text-align:left;
    margin-left: 50px;
}
.TopMargin{
    margin:5px 0;
}
.EchartContainer-bar{
    width:600px; 
    height:270px;
} 
.EchartContainer-pie{
    width:600px; 
    height:270px;
}
</style>