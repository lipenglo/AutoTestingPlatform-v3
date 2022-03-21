<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1200px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写接口信息"></el-step>
                    <el-step title="效验接口参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                            <div class="father" style="width: 100%; height: 550px;">
                                <div class="son" style="width:1100px; height: 150px;">
                                    <div style="margin-top:20px;">
                                        <el-card shadow="never">
                                            <el-form ref="BasicRomeData" :inline="true" :rules="BasicRomeData.rules" :model="BasicRomeData"  label-width="100px">
                                                <el-form-item label="接口名称:" prop="apiName">
                                                    <el-input placeholder="请输入接口名称" v-model="BasicRomeData.apiName" style="width:550px;"></el-input>
                                                </el-form-item>
                                                <el-form-item label="接口状态:" prop="apiState">
                                                    <el-select v-model="BasicRomeData.apiState" clearable placeholder="请选择" >
                                                        <el-option
                                                            v-for="item in BasicRomeData.apiStateOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="所属页面:" prop="pageId">
                                                    <el-select v-model="BasicRomeData.pageId" clearable placeholder="请选择" @click.native="GetPageNameOption()">
                                                        <el-option
                                                            v-for="item in BasicRomeData.pageNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="所属功能:" prop="funId">
                                                    <el-select v-model="BasicRomeData.funId" clearable placeholder="请选择" @click.native="GetFunNameOption()">
                                                        <el-option
                                                            v-for="item in BasicRomeData.funNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="页面环境:" prop="environmentId">
                                                    <el-select v-model="BasicRomeData.environmentId" clearable placeholder="请选择" @click.native="GetPageEnvironmentNameOption()">
                                                        <el-option
                                                            v-for="item in BasicRomeData.environmentNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="指派To:">
                                                    <el-cascader 
                                                        placeholder="可不填,默认为当前用户"
                                                        @click.native="GetassignedUserNameOption()"
                                                        v-model="BasicRomeData.assignedUserId" 
                                                        :options="BasicRomeData.assignedUserNameOptions" 
                                                        :show-all-levels="false" 
                                                        clearable>
                                                        <template slot-scope="{ node, data }">
                                                            <span>{{ data.label }}</span>
                                                            <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                                        </template>
                                                    </el-cascader>
                                                </el-form-item>
                                                <el-form-item label="关联To:">
                                                    <el-cascader 
                                                        placeholder="被关联者将会在此接口变动时收到变动提醒!"
                                                        @click.native="GetUserNameOption()"
                                                        style="width:550px;"
                                                        v-model="BasicRomeData.pushTo" 
                                                        :options="BasicRomeData.userNameOptions" 
                                                        :props="BasicRomeData.props" 
                                                        :show-all-levels="false" 
                                                        clearable>
                                                        <template slot-scope="{ node, data }">
                                                            <span>{{ data.label }}</span>
                                                            <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                                        </template>
                                                    </el-cascader>
                                                </el-form-item>
                                            </el-form>
                                        </el-card>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <div>
                            <el-row>
                                <el-col :span="16">
                                    <div v-if="EditApiRomeData.requestUrlRadio==1">
                                        <el-input placeholder="请输入接口地址"  v-model="EditApiRomeData.requestUrl1">
                                            <el-select v-model="EditApiRomeData.requestType" slot="prepend" style="width:97px">
                                                <el-option
                                                    v-for="item in EditApiRomeData.requestTypeOption"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-input>
                                    </div>
                                    <div v-else-if="EditApiRomeData.requestUrlRadio==2">
                                        <el-input placeholder="请输入接口地址"  v-model="EditApiRomeData.requestUrl2">
                                            <el-select v-model="EditApiRomeData.requestType" slot="prepend" style="width:97px">
                                                <el-option
                                                    v-for="item in EditApiRomeData.requestTypeOption"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-input>
                                    </div>
                                    <div v-else>
                                        <el-input placeholder="请输入接口地址"  v-model="EditApiRomeData.requestUrl3">
                                            <el-select v-model="EditApiRomeData.requestType" slot="prepend" style="width:97px">
                                                <el-option
                                                    v-for="item in EditApiRomeData.requestTypeOption"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-input>
                                    </div>
                                </el-col>
                                <el-col :span="2">
                                    <div>
                                        <el-button type="success" @click="OpenTestReportDialog()">Send</el-button>
                                    </div>
                                </el-col>
                                <el-col :span="6">
                                    <div>
                                        <el-radio-group v-model="EditApiRomeData.requestUrlRadio">
                                            <el-radio-button :label="1">URL:1</el-radio-button>
                                            <el-radio-button :label="2">URL:2</el-radio-button>
                                            <el-radio-button :label="3">URL:3</el-radio-button>
                                        </el-radio-group>
                                    </div>
                                </el-col>
                               
                            </el-row>
                        </div>
                        <div>
                            <el-tabs v-model="EditApiRomeData.activeName" @tab-click="handleClick">
                                <el-tab-pane :label="EditApiRomeData.headersName" name="Headers">
                                    <div v-if="EditApiRomeData.headersRomeData.editModel=='From'">
                                        <el-table
                                            :data="EditApiRomeData.headersRomeData.tableData"
                                            border
                                            height="610">
                                            <el-table-column
                                                label="启用"
                                                width="70px"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="参数名"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="参数值"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="备注"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                align="center"
                                                width="120px">
                                            <template slot="header">
                                                <el-button-group>
                                                    <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewHeadersData()"></el-button>
                                                    <el-button type="warning" size="mini" @click="changesHeadersEditModel()">Bulk</el-button>
                                                </el-button-group>
                                            </template>
                                            <template slot-scope="scope" style="width:100px">
                                                <el-button
                                                    size="mini"
                                                    icon="el-icon-delete"
                                                    type="danger"
                                                    @click="handleHeadersDelete(scope.$index, scope.row)"></el-button>
                                            </template>
                                            </el-table-column>
                                        </el-table>
                                    </div>
                                    <div v-else>
                                        <el-card>
                                            <div slot="header" style="height:20px">
                                                <el-row style="margin-top:-8px">
                                                    <el-col :span="12">
                                                        <div style="float:left;margin-top:3px">
                                                            <span style="font-size:15px">格式:启用状态,参数名,参数值,备注</span>
                                                        </div>
                                                        </el-col>
                                                    <el-col :span="12">
                                                        <div style="float:right">
                                                            <el-button type="primary" size="mini" @click="changesHeadersEditModel()">确定</el-button>
                                                            <el-button size="mini" @click="cancelHeadersBulkEdit()">取消</el-button>
                                                        </div>
                                                    </el-col>
                                                </el-row>
                                            </div>
                                            <div>
                                                <el-input
                                                    type="textarea"
                                                    :autosize="{ minRows: 24, maxRows: 24}"
                                                    v-model="EditApiRomeData.headersRomeData.bulkEdit">
                                                </el-input>
                                            </div>
                                        </el-card>
                                    </div>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.paramsName" name="Params">
                                    <div v-if="EditApiRomeData.paramsRomeData.editModel=='From'">
                                        <el-table
                                            :data="EditApiRomeData.paramsRomeData.tableData"
                                            border
                                            height="610">
                                            <el-table-column
                                                label="启用"
                                                width="70px"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="参数名"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="参数值"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="备注"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                align="center"
                                                width="120px">
                                            <template slot="header">
                                                <el-button-group>
                                                    <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewParamsData()"></el-button>
                                                    <el-button type="warning" size="mini" @click="changesParamsEditModel()">Bulk</el-button>
                                                </el-button-group>
                                            </template>
                                            <template slot-scope="scope" style="width:100px">
                                                <el-button
                                                    size="mini"
                                                    icon="el-icon-delete"
                                                    type="danger"
                                                    @click="handleParamsDelete(scope.$index, scope.row)"></el-button>
                                            </template>
                                            </el-table-column>
                                        </el-table>
                                    </div>
                                    <div v-else>
                                        <el-card>
                                            <div slot="header" style="height:20px">
                                                <el-row style="margin-top:-8px">
                                                    <el-col :span="12">
                                                        <div style="float:left;margin-top:3px">
                                                            <span style="font-size:15px">格式:启用状态,参数名,参数值,备注</span>
                                                        </div>
                                                        </el-col>
                                                    <el-col :span="12">
                                                        <div style="float:right">
                                                            <el-button type="primary" size="mini" @click="changesParamsEditModel()">确定</el-button>
                                                            <el-button size="mini" @click="cancelParamsBulkEdit()">取消</el-button>
                                                        </div>
                                                    </el-col>
                                                </el-row>
                                                
                                            </div>
                                            <div>
                                                <el-input
                                                    type="textarea"
                                                    :autosize="{ minRows: 24, maxRows: 24}"
                                                    v-model="EditApiRomeData.paramsRomeData.bulkEdit">
                                                </el-input>
                                            </div>
                                        </el-card>
                                    </div>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.bodyName" name="Body">
                                    <div>
                                        <el-radio-group v-model="EditApiRomeData.bodyRomeData.requestSaveType" @change="changeBodyRequestType">
                                            <el-radio label="none">none</el-radio>
                                            <el-radio label='form-data'>form-data</el-radio>
                                            <el-radio label='json'>json</el-radio>
                                            <el-radio label="raw">raw</el-radio>
                                        </el-radio-group>
                                    </div>
                                    <div v-if="EditApiRomeData.bodyRomeData.requestSaveType=='none'">
                                        <el-card shadow="never" class="bodyRome" style="height:580px;">
                                            <div>该请求没有主体</div>
                                        </el-card>
                                    </div>
                                    <div v-else-if="EditApiRomeData.bodyRomeData.requestSaveType=='form-data'">
                                        <div v-if="EditApiRomeData.bodyRomeData.editModel=='From'">
                                            <el-table
                                                class="bodyRome"
                                                :data="EditApiRomeData.bodyRomeData.tableData"
                                                border
                                                height="582">
                                                <el-table-column
                                                    label="启用"
                                                    width="70px"
                                                    align= "center">
                                                    <template slot-scope="scope">
                                                        <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                    </template>
                                                </el-table-column>
                                                <el-table-column
                                                    label="参数名"
                                                    width="250px"
                                                    align= "center">
                                                    <template slot-scope="scope">
                                                        <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                                                    </template>
                                                </el-table-column>
                                                <el-table-column
                                                    label="类型"
                                                    width="110px"
                                                    align= "center">
                                                    <template slot-scope="scope">
                                                        <el-select v-model="scope.row.paramsType">
                                                            <el-option
                                                                v-for="item in EditApiRomeData.bodyRomeData.paramsTypeOption"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value">
                                                            </el-option>
                                                        </el-select>
                                                    </template>
                                                </el-table-column>
                                                <el-table-column
                                                    label="参数值"
                                                    align= "center">
                                                    <template slot-scope="scope">
                                                        <div v-if="scope.row.paramsType=='Text'">
                                                            <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                                                        </div>
                                                        <div v-else>
                                                            <el-upload
                                                                style="float:left;width:300px"
                                                                :headers="headers"
                                                                :action="uploadToTemp"
                                                                :file-list="scope.row.fileList"
                                                                :limit='1'
                                                                :on-success="(value)=> upload_success(scope.row.fileList,value)"
                                                                :on-remove="(value)=> upload_remove(scope.row.fileList,value)">
                                                                <el-button size="small" type="primary">点击上传</el-button>
                                                            </el-upload>
                                                        </div>
                                                    </template>
                                                </el-table-column>
                                                <el-table-column
                                                    label="备注"
                                                    width="300px"
                                                    align= "center">
                                                    <template slot-scope="scope">
                                                        <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                    </template>
                                                </el-table-column>
                                                <el-table-column
                                                    align="center"
                                                    width="120px">
                                                <template slot="header">
                                                    <el-button-group>
                                                        <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewBodyData()"></el-button>
                                                        <el-button type="warning" size="mini" @click="changesBodyEditModel()">Bulk</el-button>
                                                    </el-button-group>
                                                </template>
                                                <template slot-scope="scope" style="width:100px">
                                                    <el-button
                                                        size="mini"
                                                        icon="el-icon-delete"
                                                        type="danger"
                                                        @click="handleBodyDelete(scope.$index, scope.row)"></el-button>
                                                </template>
                                                </el-table-column>
                                            </el-table>
                                        </div>
                                        <div v-else>
                                            <el-card style="margin-top:5px">
                                                <div slot="header" style="height:20px;">
                                                    <el-row style="margin-top:-8px">
                                                        <el-col :span="12">
                                                            <div style="float:left;margin-top:3px">
                                                                <span style="font-size:15px">格式:启用状态,参数名,参数值,备注</span>
                                                            </div>
                                                            </el-col>
                                                        <el-col :span="12">
                                                            <div style="float:right">
                                                                <el-button type="primary" size="mini" @click="changesBodyEditModel()">确定</el-button>
                                                                <el-button size="mini" @click="cancelBodyBulkEdit()">取消</el-button>
                                                            </div>
                                                        </el-col>
                                                    </el-row>
                                                </div>
                                                <div>
                                                    <el-input
                                                        type="textarea"
                                                        :autosize="{ minRows: 23, maxRows: 23}"
                                                        v-model="EditApiRomeData.bodyRomeData.bulkEdit">
                                                    </el-input>
                                                </div>
                                            </el-card>
                                        </div>
                                    </div>
                                    <div v-else-if="EditApiRomeData.bodyRomeData.requestSaveType=='json'">
                                        <el-input
                                            class="bodyRome"
                                            type="textarea"
                                            :autosize="{ minRows: 27, maxRows: 27}"
                                            v-model="EditApiRomeData.bodyRomeData.jsonValue">
                                        </el-input>
                                    </div>
                                    <div v-else-if="EditApiRomeData.bodyRomeData.requestSaveType=='raw'">
                                        <el-input
                                            class="bodyRome"
                                            type="textarea"
                                            :autosize="{ minRows: 27, maxRows: 27}"
                                            v-model="EditApiRomeData.bodyRomeData.rawValue">
                                        </el-input>
                                    </div>
                                    <div v-else>
                                        <!-- <el-card shadow="never" class="bodyRome" style="height:580px;">
                                            <div>这里是上传文件地址</div>
                                        </el-card> -->
                                    </div>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.extractName" name="Extract">
                                    <el-table
                                        :data="EditApiRomeData.extractRomeData.tableData"
                                        border
                                        height="610">
                                        <el-table-column
                                            label="启用"
                                            width="70px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="变量名称"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.key" placeholder="变量名称"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="提取表达式"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.value" placeholder="例:$.statuscode,$.key[0],$.table[0].name"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="备注"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            align="center"
                                            width="120px">
                                        <template slot="header">
                                            <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewExtractData()"></el-button>
                                        </template>
                                        <template slot-scope="scope" style="width:100px">
                                            <el-button
                                                size="mini"
                                                icon="el-icon-delete"
                                                type="danger"
                                                @click="handleExtractDelete(scope.$index, scope.row)"></el-button>
                                        </template>
                                        </el-table-column>
                                    </el-table>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.validateName" name="Validate">
                                    <el-table
                                        :data="EditApiRomeData.validateRomeData.tableData"
                                        border
                                        height="610">
                                        <el-table-column
                                            label="启用"
                                            width="70px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="提取变量名称"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-autocomplete
                                                    v-model="scope.row.checkName"
                                                    :fetch-suggestions="fetchSuggestionsValidate"
                                                    placeholder="请输入提取变量名称">
                                                </el-autocomplete>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="断言类型"
                                            width="170px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-select  v-model="scope.row.validateType" placeholder="请选择">
                                                    <el-option
                                                        v-for="item in EditApiRomeData.validateRomeData.validateTypeOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="断言值类型"
                                            width="120px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-select v-model="scope.row.valueType"  placeholder="请选择">
                                                        <el-option
                                                            v-for="item in EditApiRomeData.validateRomeData.valueTypeOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="预期结果"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.expectedResults" placeholder="预期结果"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="备注"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            align="center"
                                            width="65px">
                                        <template slot="header">
                                            <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewValidateData()"></el-button>
                                        </template>
                                        <template slot-scope="scope" style="width:100px">
                                        <el-button
                                            size="mini"
                                            icon="el-icon-delete"
                                            type="danger"
                                            @click="handleValidateDelete(scope.$index, scope.row)"></el-button>
                                        </template>
                                        </el-table-column>
                                    </el-table>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.preOperationName" name="PreOperation">
                                    <el-table
                                        id="PreOperationSort"
                                        row-key="id"
                                        :data="EditApiRomeData.preOperationRomeData.tableData"
                                        border
                                        height="610">
                                        <el-table-column
                                            label="启用"
                                            width="70px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
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
                                            label="操作数据"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <div v-if="scope.row.operationType=='Methods'">
                                                    <el-input v-model.trim="scope.row.methodsName" placeholder="输入DebugTalk文件中需要调用的方法"></el-input>
                                                </div>
                                                <div v-else-if="scope.row.operationType=='DataBase'">
                                                    <el-form ref="preOperationRomeData" :model="EditApiRomeData.preOperationRomeData" label-width="80px">
                                                        <el-form-item label="数据库:">
                                                            <el-cascader
                                                                style="float:left;width:437px"
                                                                clearable
                                                                placeholder="请选择连接的数据库" 
                                                                v-model="scope.row.dataBase"
                                                                :options="EditApiRomeData.preOperationRomeData.dataBaseOptions"
                                                                @click.native="getDataBaseOption()">
                                                                <template slot-scope="{ node, data }">
                                                                    <span>{{ data.label }}</span>
                                                                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                                                </template>
                                                            </el-cascader>
                                                        </el-form-item>
                                                        <el-form-item label="SQL:">
                                                            <el-input
                                                                type="textarea"
                                                                :autosize="{ minRows: 3, maxRows: 3}"
                                                                v-model="scope.row.sql"
                                                                placeholder="SQL">
                                                            </el-input>
                                                        </el-form-item>
                                                    </el-form>
                                                </div>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="备注"
                                            width="300px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            align="center"
                                            width="100px">
                                        <template slot="header">
                                            <el-dropdown @command="handlePreOperationCommand">
                                                <el-button type="warning" size="mini" icon="el-icon-circle-plus-outline">
                                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                                </el-button>
                                                <el-dropdown-menu slot="dropdown">
                                                    <el-dropdown-item command="Methods">方法函数</el-dropdown-item>
                                                    <el-dropdown-item command="DataBase">数据库操作</el-dropdown-item>
                                                </el-dropdown-menu>
                                            </el-dropdown>
                                        </template>
                                        <template slot-scope="scope" style="width:100px">
                                            <el-button
                                                size="mini"
                                                icon="el-icon-delete"
                                                type="danger"
                                                @click="handlePreOperationDelete(scope.$index, scope.row)"></el-button>
                                        </template>
                                        </el-table-column>
                                    </el-table>
                                </el-tab-pane>
                                <el-tab-pane :label="EditApiRomeData.rearOperationName" name="RearOperation">
                                    <el-table
                                        id="RearOperationSort"
                                        row-key="id"
                                        :data="EditApiRomeData.rearOperationRomeData.tableData"
                                        border
                                        height="610">
                                        <el-table-column
                                            label="启用"
                                            width="70px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
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
                                            label="操作数据"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <div v-if="scope.row.operationType=='Methods'">
                                                    <el-input v-model.trim="scope.row.methodsName" placeholder="输入DebugTalk文件中需要调用的方法"></el-input>
                                                </div>
                                                <div v-else-if="scope.row.operationType=='DataBase'">
                                                    <el-form ref="rearOperationRomeData" :model="EditApiRomeData.rearOperationRomeData" label-width="80px">
                                                        <el-form-item label="数据库:">
                                                            <el-cascader
                                                                style="float:left;width:437px"
                                                                clearable
                                                                placeholder="请选择连接的数据库" 
                                                                v-model="scope.row.dataBase"
                                                                :options="EditApiRomeData.rearOperationRomeData.dataBaseOptions"
                                                                @click.native="getDataBaseOption()">
                                                                <template slot-scope="{ node, data }">
                                                                    <span>{{ data.label }}</span>
                                                                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                                                </template>
                                                            </el-cascader>
                                                        </el-form-item>
                                                        <el-form-item label="SQL:">
                                                            <el-input
                                                                type="textarea"
                                                                :autosize="{ minRows: 3, maxRows: 3}"
                                                                v-model="scope.row.sql"
                                                                placeholder="SQL">
                                                            </el-input>
                                                        </el-form-item>
                                                    </el-form>
                                                </div>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="备注"
                                            width="300px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            align="center"
                                            width="100px">
                                        <template slot="header">
                                            <el-dropdown @command="handleRearOperationCommand">
                                                <el-button type="warning" size="mini" icon="el-icon-circle-plus-outline">
                                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                                </el-button>
                                                <el-dropdown-menu slot="dropdown">
                                                    <el-dropdown-item command="Methods">方法函数</el-dropdown-item>
                                                    <el-dropdown-item command="DataBase">数据库操作</el-dropdown-item>
                                                </el-dropdown-menu>
                                            </el-dropdown>
                                        </template>
                                        <template slot-scope="scope" style="width:100px">
                                            <el-button
                                                size="mini"
                                                icon="el-icon-delete"
                                                type="danger"
                                                @click="handleRearOperationDelete(scope.$index, scope.row)"></el-button>
                                        </template>
                                        </el-table-column>
                                    </el-table>
                                </el-tab-pane>
                            </el-tabs>
                        </div>
                    </template>
                    <template v-else>
                        <div slot="header">
                            {{CharmRomeData.title}}
                        </div>
                        <div>
                            <el-table
                            :data="CharmRomeData.tableData"
                            border
                            height="660px">
                            <el-table-column
                                type="index"
                                align= "center"
                                label="Index"
                                width="100">
                            </el-table-column>
                            <el-table-column
                                prop="stepsName"
                                align= "center"
                                label="错误步骤"
                                width="200">
                            </el-table-column>
                            <el-table-column
                                prop="errorMsg"
                                align= "center"
                                label="错误信息">
                            </el-table-column>
                            <el-table-column
                                prop="updateTime"
                                align= "center"
                                label="错误时间"
                                width="200">
                            </el-table-column>
                            </el-table>
                        </div>
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="DataSave()">保存</el-button>
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
import Sortable from 'sortablejs';
import Qs from 'qs';
import store from '../../../../../../../store/index';

import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetUserNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetConnectBaseItems} from "../../../../../../js/GetSelectTable.js";
import DialogTestReport from "./TestReport.vue";

export default {
    components: {
        DialogTestReport
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            uploadToTemp:store.state.BackService +'/api/upLoad/UpLoadToTempPath',
            StepsRomeData:{
                active:0,
                stepLength:2,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            BasicRomeData:{
                apiId:'',
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                environmentId:'',//页面环境
                environmentNameOption:[],
                apiName:'',
                apiState:'',
                apiStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                assignedUserId:'',//指派用户
                assignedUserNameOptions:[],
                props: { multiple: true },
                pushTo:[],//关联To用户
                userNameOptions:[],
                rules:{
                    pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                    environmentId:[{ required: true, message: '请选择环境地址', trigger: 'change' }],
                    apiName:[
                        { required: true, message: '请输入接口名称', trigger: 'blur' },
                        { min: 1, max: 30, message: '长度在 1 到 30 个字符', trigger: 'blur' }
                    ],
                    apiState:[{ required: true, message: '请选择状态', trigger: 'change' }],
                },
            },
            EditApiRomeData:{
                requestUrlRadio:1,//备选1 2 3
                requestUrl1:'',
                requestUrl2:'',
                requestUrl3:'',
                requestType:'GET',
                requestTypeOption:[
                    {'label':'GET','value':'GET'},
                    {'label':'POST','value':'POST'},
                ],
                activeName:'Headers',
                headersName:'Headers',
                paramsName:'Params',
                bodyName:'Body',
                extractName:'Extract/提取',
                validateName:'Validate/断言',
                preOperationName:'前置操作',
                rearOperationName:'后置操作',
                headersRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',//显示给屏幕上看的数据
                },
                paramsRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',//显示给屏幕上看的数据
                },
                bodyRomeData:{
                    index:0,
                    tableData:[],
                    paramsTypeOption:[
                        {'label':'Text','value':'Text'},
                        {'label':'File','value':'File'},
                    ],
                    editModel:'From',
                    bulkEdit:'',
                    requestSaveType:'form-data',//请求保存类型，none,form-data,json,raw
                    rawValue:'',
                    jsonValue:'',
                    deleteFileList:[],
                },
                extractRomeData:{
                    index:0,
                    tableData:[],
                },
                validateRomeData:{
                    index:0,
                    tableData:[],
                    validateTypeOption:[//断言类型
                        {label: 'equals(==)', value: 'equals'},
                        {label: 'contains(In)',value: 'contains'},
                        {label: 'not_equals(!=)', value: 'not_equals'},
                    ],
                    valueTypeOption:[//对比值类型
                        {label: 'String',value: 'str'},
                        {label: 'Int',value: 'int'},
                        {label: 'Float',value: 'float'},
                        {label: 'Bool',value: 'bool'},
                        {label: 'List',value: 'list'}
                    ],
                },
                preOperationRomeData:{
                    index:0,
                    tableData:[],
                    dataBaseOptions:[],
                },
                rearOperationRomeData:{
                    index:0,
                    tableData:[],
                    dataBaseOptions:[],
                }
            },
            CharmRomeData:{
                title:'',
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
    mounted(){

    },
    computed:{//计算属性
        headers(){//用来把token放到头部
            return {
                'Token': this.$cookies.get('token')
            }
        },
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
                PrintConsole(newval);
                this.ClearStepsRomeData();
                this.ClearBasicRomeData();
                this.ClearEditApiRomeData();
                this.ClearCharmRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.BasicRomeData.apiId = newval.apiId;
                    self.LoadData(newval.apiId).then(d=>{
                        if(d.statusCode==2000){
                            GetPageNameItems('API',this.$cookies.get('proId')).then(dd=>{
                                self.BasicRomeData.pageNameOption = dd;
                                self.BasicRomeData.pageId = d.basicInfo.pageId;
                                GetFunNameItems('API',this.$cookies.get('proId'),self.BasicRomeData.pageId).then(dd=>{
                                    self.BasicRomeData.funNameOption = dd;
                                    self.BasicRomeData.funId = d.basicInfo.funId;
                                    GetUserNameItems().then(dd=>{
                                        self.BasicRomeData.assignedUserNameOptions = dd;
                                        self.BasicRomeData.assignedUserId = d.basicInfo.assignedUserId;
                                        GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(dd=>{
                                            self.BasicRomeData.environmentNameOption = dd;
                                            self.BasicRomeData.environmentId = d.basicInfo.environmentId;
                                            self.BasicRomeData.apiName = d.basicInfo.apiName;
                                            self.BasicRomeData.apiState = d.basicInfo.apiState;
                                            GetUserNameItems().then(dd=>{
                                                self.BasicRomeData.userNameOptions = dd;
                                                self.BasicRomeData.pushTo = d.basicInfo.pushTo;

                                                self.EditApiRomeData.requestType = d.apiInfo.requestType;
                                                self.EditApiRomeData.requestUrlRadio = d.apiInfo.requestUrlRadio;
                                                self.EditApiRomeData.requestUrl1 =  d.apiInfo.requestUrl1;
                                                self.EditApiRomeData.requestUrl2 =  d.apiInfo.requestUrl2;
                                                self.EditApiRomeData.requestUrl3 =  d.apiInfo.requestUrl3;
                                                //headers
                                                d.apiInfo.request.headers.forEach(item_headers=>{
                                                    let obj = {};
                                                    obj.index = item_headers.index;
                                                    obj.state =item_headers.state;
                                                    obj.key =item_headers.key;
                                                    obj.value=item_headers.value;
                                                    obj.remarks=item_headers.remarks;
                                                    self.EditApiRomeData.headersRomeData.tableData.push(obj);
                                                });
                                                self.EditApiRomeData.headersRomeData.index=d.apiInfo.request.headers.length+1;

                                                //params
                                                d.apiInfo.request.params.forEach(item_params=>{
                                                    let obj = {};
                                                    obj.index = item_params.index;
                                                    obj.state =item_params.state;
                                                    obj.key =item_params.key;
                                                    obj.value=item_params.value;
                                                    obj.remarks=item_params.remarks;
                                                    self.EditApiRomeData.paramsRomeData.tableData.push(obj);
                                                });
                                                self.EditApiRomeData.paramsRomeData.index=d.apiInfo.request.params.length+1;

                                                //body
                                                self.EditApiRomeData.bodyRomeData.requestSaveType = d.apiInfo.request.body.requestSaveType;
                                                if(d.apiInfo.request.body.requestSaveType=='form-data'){
                                                    d.apiInfo.request.body.bodyData.forEach(item_body=>{
                                                        let obj = {};
                                                        obj.index = item_body.index;
                                                        obj.state =item_body.state;
                                                        obj.key =item_body.key;
                                                        obj.paramsType =item_body.paramsType;
                                                        obj.value=item_body.value;
                                                        obj.fileList=item_body.fileList;
                                                        obj.remarks=item_body.remarks;
                                                        self.EditApiRomeData.bodyRomeData.tableData.push(obj);
                                                    });
                                                    self.EditApiRomeData.bodyRomeData.index=d.apiInfo.request.body.bodyData.length+1;
                                                }else if(d.apiInfo.request.body.requestSaveType=='raw'){
                                                    self.EditApiRomeData.bodyRomeData.rawValue = d.apiInfo.request.body.bodyData;
                                                }else if(d.apiInfo.request.body.requestSaveType=='json'){
                                                    self.EditApiRomeData.bodyRomeData.jsonValue = d.apiInfo.request.body.bodyData;
                                                }

                                                //extract
                                                d.apiInfo.request.extract.forEach(item_extract=>{
                                                    let obj = {};
                                                    obj.index = item_extract.index;
                                                    obj.state =item_extract.state;
                                                    obj.key =item_extract.key;
                                                    obj.value=item_extract.value;
                                                    obj.remarks=item_extract.remarks;
                                                    self.EditApiRomeData.extractRomeData.tableData.push(obj);
                                                });
                                                self.EditApiRomeData.extractRomeData.index=d.apiInfo.request.extract.length+1;

                                                //validate
                                                d.apiInfo.request.validate.forEach(item_validate=>{
                                                    let obj = {};
                                                    obj.index = item_validate.index;
                                                    obj.state =item_validate.state;
                                                    obj.checkName =item_validate.checkName;
                                                    obj.validateType=item_validate.validateType;
                                                    obj.valueType=item_validate.valueType;
                                                    obj.expectedResults=item_validate.expectedResults;
                                                    obj.remarks=item_validate.remarks;
                                                    self.EditApiRomeData.validateRomeData.tableData.push(obj);
                                                });
                                                self.EditApiRomeData.validateRomeData.index=d.apiInfo.request.validate.length+1;

                                                //preOperation
                                                self.getDataBaseOption()
                                                d.apiInfo.request.preOperation.forEach(item_preOperation=>{
                                                    let obj = {};
                                                    obj.index = item_preOperation.index;
                                                    obj.state =item_preOperation.state;
                                                    obj.operationType =item_preOperation.operationType;
                                                    obj.methodsName=item_preOperation.methodsName;
                                                    obj.dataBase=item_preOperation.dataBase;
                                                    obj.sql=item_preOperation.sql;
                                                    obj.remarks=item_preOperation.remarks;

                                                    self.EditApiRomeData.preOperationRomeData.tableData.push(obj);
                                                });
                                                self.EditApiRomeData.preOperationRomeData.index=d.apiInfo.request.preOperation.length+1;

                                                //rearOperation
                                                d.apiInfo.request.rearOperation.forEach(item_rearOperation=>{
                                                    let obj = {};
                                                    obj.index = item_rearOperation.index;
                                                    obj.state =item_rearOperation.state;
                                                    obj.operationType =item_rearOperation.operationType;
                                                    obj.methodsName=item_rearOperation.methodsName;
                                                    obj.dataBase=item_rearOperation.dataBase;
                                                    obj.sql=item_rearOperation.sql;
                                                    obj.remarks=item_rearOperation.remarks;

                                                    self.EditApiRomeData.rearOperationRomeData.tableData.push(obj);
                                                });
                                                self.EditApiRomeData.rearOperationRomeData.index=d.apiInfo.request.rearOperation.length+1;
                                            });
                                            self.loading=false;
                                        });
                                    });
                                });
                            });
                        }else{
                            self.$message.error('获取数据失败:'+d.errorMsg);
                            self.loading=false;
                        }
                    });
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听步骤
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
               
            }else if(newVal==1){
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Save = false;
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
        'BasicRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.BasicRomeData.funId='';
                self.BasicRomeData.funNameOption=[];
            }
        },
        'EditApiRomeData.headersRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.headersRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.headersName='Headers';
                }else{
                    self.EditApiRomeData.headersName='Headers('+dataLength+')';
                }
                
            }
        },
        'EditApiRomeData.paramsRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.paramsRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.paramsName='Params';
                }else{
                    self.EditApiRomeData.paramsName='Params('+dataLength+')';
                }
                
            }
        },
        'EditApiRomeData.bodyRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.bodyRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.bodyName='Body';
                }else{
                    self.EditApiRomeData.bodyName='Body('+dataLength+')';
                }
                
            }
        },
        'EditApiRomeData.extractRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.extractRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.extractName='Extract/提取';
                }else{
                    self.EditApiRomeData.extractName='Extract/提取('+dataLength+')';
                }
                
            }
        },
        'EditApiRomeData.validateRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.validateRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.validateName='Validate/断言';
                }else{
                    self.EditApiRomeData.validateName='Validate/断言('+dataLength+')';
                }
                
            }
        },
        'EditApiRomeData.preOperationRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.preOperationRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.preOperationName='前置操作';
                }else{
                    self.EditApiRomeData.preOperationName='前置操作('+dataLength+')';
                }
                
            }
        },
        'EditApiRomeData.rearOperationRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditApiRomeData.rearOperationRomeData.tableData.length;
                if(dataLength==0){
                    self.EditApiRomeData.rearOperationName='后置操作';
                }else{
                    self.EditApiRomeData.rearOperationName='后置操作('+dataLength+')';
                }
                
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        //导航条事件
        next() {//下一步
            let self = this;
            PrintConsole('当前',self.StepsRomeData.active)
            if(self.StepsRomeData.active==0){//基本用例数据
                // self.StepsRomeData.active++;
                this.$refs['BasicRomeData'].validate((valid) => {
                    if (valid) {//通过
                        self.StepsRomeData.active++;
                    } 
                });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
                self.CharmApiData();
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else if(self.StepsRomeData.active==3){
                self.StepsRomeData.active--;
                self.StepsRomeData.active--;
            }
            else{
                self.StepsRomeData.active--;
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
            // self.resetForm('RomeData');
            self.StepsRomeData.active= 0;
            self.StepsRomeData.disPlay_Save = false;
            self.StepsRomeData.disPlay_Next = true;
            self.StepsRomeData.processStatus ='process';
        },
        returnToMain(){
            let self = this;
            self.dialogVisible = false;//关闭新增弹窗
            self.$emit('closeDialog');
            self.$emit('Succeed');//回调查询   
        },

        //基本信息
        ClearBasicRomeData(){
            let self = this;
            self.resetForm('BasicRomeData');
            self.BasicRomeData.pageId='';
            self.BasicRomeData.funId='';
            self.BasicRomeData.environmentId='';
            self.BasicRomeData.apiName='';
            self.BasicRomeData.apiState='';
            self.BasicRomeData.assignedUserId='';
            self.BasicRomeData.pushTo=[];
            PrintConsole('BasicRomeData','清除');
        
        },
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.BasicRomeData.pageId){
                GetFunNameItems('API',this.$cookies.get('proId'),this.BasicRomeData.pageId).then(d=>{
                    this.BasicRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetPageEnvironmentNameOption(){
            GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.environmentNameOption = d;
            });
        },
        GetUserNameOption(){//关联
            GetUserNameItems().then(d=>{
                this.BasicRomeData.userNameOptions = d;
            });
        },
        GetassignedUserNameOption(){//指派
            GetUserNameItems().then(d=>{
                this.BasicRomeData.assignedUserNameOptions = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                PrintConsole('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },

        //编辑接口信息
        ClearEditApiRomeData(){
            let self = this;
            self.EditApiRomeData.requestType='GET';
            self.EditApiRomeData.requestUrlRadio=1;
            self.EditApiRomeData.requestUrl1='';
            self.EditApiRomeData.requestUrl2='';
            self.EditApiRomeData.requestUrl3='';
            self.EditApiRomeData.activeName='Headers';
            self.EditApiRomeData.headersName='Headers';
            self.EditApiRomeData.paramsName='Params';
            self.EditApiRomeData.bodyName='Body';
            self.EditApiRomeData.extractName='Extract/提取';
            self.EditApiRomeData.validateName='Validate/断言';
            self.EditApiRomeData.preOperationName='前置操作';
            self.EditApiRomeData.rearOperationName='后置操作';

            //headersRomeData
            self.EditApiRomeData.headersRomeData.tableData=[];
            self.EditApiRomeData.headersRomeData.index=0;
            self.EditApiRomeData.headersRomeData.editModel='From';

            //paramsRomeData
            self.EditApiRomeData.paramsRomeData.tableData=[];
            self.EditApiRomeData.paramsRomeData.index=0;
            self.EditApiRomeData.paramsRomeData.editModel='From';

            //bodyRomeData
            self.EditApiRomeData.bodyRomeData.tableData=[];
            self.EditApiRomeData.bodyRomeData.index=0;
            self.EditApiRomeData.bodyRomeData.editModel='From';
            self.EditApiRomeData.bodyRomeData.requestSaveType='form-data';
            self.EditApiRomeData.bodyRomeData.rawValue = '';
            self.EditApiRomeData.bodyRomeData.jsonValue = '';
            self.EditApiRomeData.bodyRomeData.deleteFileList = [];

            //extractRomeData
            self.EditApiRomeData.extractRomeData.tableData=[];
            self.EditApiRomeData.extractRomeData.index=0;

            //validateRomeData
            self.EditApiRomeData.validateRomeData.tableData=[];
            self.EditApiRomeData.validateRomeData.index=0;

            //PreOperationRomeData
            self.EditApiRomeData.preOperationRomeData.tableData=[];
            self.EditApiRomeData.preOperationRomeData.index=0;

            //rearOperationRomeData
            self.EditApiRomeData.rearOperationRomeData.tableData=[];
            self.EditApiRomeData.rearOperationRomeData.index=0;
        },
        handleClick(tab, event){
            PrintConsole(tab);
            if(tab.name=='PreOperation'){
                this.rowDropPreOperation();
            }
        },

        //headersRomeData
        CreateNewHeadersData(){
            let self = this;
            let obj = {};
            obj.index = self.EditApiRomeData.headersRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditApiRomeData.headersRomeData.tableData.push(obj);
            self.EditApiRomeData.headersRomeData.index+=1;
        },
        handleHeadersDelete(index,row){
            PrintConsole('handleHeadersDelete',row);
            let self = this;
            self.EditApiRomeData.headersRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.headersRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.headersRomeData.tableData[i].index = i;
            });

            self.EditApiRomeData.headersRomeData.index -=1 ;
        },
        cancelHeadersBulkEdit(){//批量修改模式下的取消
            this.EditApiRomeData.headersRomeData.editModel='From';
            this.EditApiRomeData.headersRomeData.showBulkEdit ='';
            this.EditApiRomeData.headersRomeData.actualBulkEdit ='';
        },
        changesHeadersEditModel(){
            let self = this;
            if(self.EditApiRomeData.headersRomeData.editModel=='From'){
                self.EditApiRomeData.headersRomeData.editModel='Bulk';
                self.EditApiRomeData.headersRomeData.bulkEdit ='';
                self.EditApiRomeData.headersRomeData.tableData.forEach(item=>{
                    PrintConsole('changesHeadersBulkState',item);
                    let rowData=item.state+',';
                    if(item.key){
                        rowData+=item.key+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.value){
                        rowData+=item.value+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.remarks){
                        rowData+=item.remarks;
                    }
                    rowData+='\n';
                    self.EditApiRomeData.headersRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.EditApiRomeData.headersRomeData.bulkEdit.split('\n'));

                self.EditApiRomeData.headersRomeData.editModel='From';
                self.EditApiRomeData.headersRomeData.tableData=[];
                self.EditApiRomeData.headersRomeData.index = 0
                let bulkEdit = self.EditApiRomeData.headersRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.EditApiRomeData.headersRomeData.index;
                        if(data[0]=="true"){
                            obj.state = true;
                        }else{
                            obj.state = false;
                        }
                        obj.key = data[1];
                        obj.value = data[2];
                        if(data.length==4){
                            obj.remarks = data[3];
                        }else{
                            obj.remarks ='';
                        }
                        // PrintConsole(obj);
                        self.EditApiRomeData.headersRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.EditApiRomeData.headersRomeData.tableData);
            }
        },

        //paramsRomeData
        CreateNewParamsData(){
            let self = this;
            let obj = {};
            obj.index = self.EditApiRomeData.paramsRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditApiRomeData.paramsRomeData.tableData.push(obj);
            self.EditApiRomeData.paramsRomeData.index+=1;
            PrintConsole('CreateNewParamsData',self.EditApiRomeData.paramsRomeData.tableData);
        },
        handleParamsDelete(index,row){
            PrintConsole('handleParamsDelete',row);
            let self = this;
            self.EditApiRomeData.paramsRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.paramsRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.paramsRomeData.tableData[i].index = i;
            });

            self.EditApiRomeData.paramsRomeData.index -=1 ;
        },
        cancelParamsBulkEdit(){//批量修改模式下的取消
            this.EditApiRomeData.paramsRomeData.editModel='From';
            this.EditApiRomeData.paramsRomeData.showBulkEdit ='';
            this.EditApiRomeData.paramsRomeData.actualBulkEdit ='';
        },
        changesParamsEditModel(){
            let self = this;
            if(self.EditApiRomeData.paramsRomeData.editModel=='From'){
                self.EditApiRomeData.paramsRomeData.editModel='Bulk';
                self.EditApiRomeData.paramsRomeData.bulkEdit ='';
                self.EditApiRomeData.paramsRomeData.tableData.forEach(item=>{
                    PrintConsole('changesParamsEditModel',item);
                    let rowData=item.state+',';
                    if(item.key){
                        rowData+=item.key+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.value){
                        rowData+=item.value+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.remarks){
                        rowData+=item.remarks;
                    }
                    rowData+='\n';
                    self.EditApiRomeData.paramsRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.EditApiRomeData.paramsRomeData.bulkEdit.split('\n'));

                self.EditApiRomeData.paramsRomeData.editModel='From';
                self.EditApiRomeData.paramsRomeData.tableData=[];
                self.EditApiRomeData.paramsRomeData.index = 0
                let bulkEdit = self.EditApiRomeData.paramsRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.EditApiRomeData.paramsRomeData.index;
                        if(data[0]=="true"){
                            obj.state = true;
                        }else{
                            obj.state = false;
                        }
                        obj.key = data[1];
                        obj.value = data[2];
                        if(data.length==4){
                            obj.remarks = data[3];
                        }else{
                            obj.remarks ='';
                        }
                        // PrintConsole(obj);
                        self.EditApiRomeData.paramsRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.EditApiRomeData.paramsRomeData.tableData);
            }
        },

        //bodyRomeDta
        changeBodyRequestType(val){
            PrintConsole(val);
            let self = this;
            if(val=='json'){
                let tempData = self.EditApiRomeData.headersRomeData.tableData.find(item=>
                    item.key == 'Content-Type'
                );
                if(tempData){
                    PrintConsole(tempData);
                }else{
                    let obj = {};
                    obj.index = self.EditApiRomeData.headersRomeData.index;
                    obj.state = true;
                    obj.key = 'Content-Type';
                    obj.value='application/json';
                    obj.remarks='';

                    self.EditApiRomeData.headersRomeData.tableData.push(obj);
                    self.EditApiRomeData.headersRomeData.index+=1;
                }
            }
        },
        CreateNewBodyData(){
            let self = this;
            let obj = {};
            obj.index = self.EditApiRomeData.bodyRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.paramsType = 'Text';
            obj.value='';
            obj.fileList=[];
            obj.remarks='';

            self.EditApiRomeData.bodyRomeData.tableData.push(obj);
            self.EditApiRomeData.bodyRomeData.index+=1;
            PrintConsole('CreateNewBodyData',self.EditApiRomeData.bodyRomeData.tableData);
        },
        handleBodyDelete(index,row){
            PrintConsole('handleBodyDelete',row);
            let self = this;
            self.EditApiRomeData.bodyRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.bodyRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.bodyRomeData.tableData[i].index = i;
            });

            self.EditApiRomeData.bodyRomeData.index -=1 ;
        },
        cancelBodyBulkEdit(){//批量修改模式下的取消
            this.EditApiRomeData.bodyRomeData.editModel='From';
            this.EditApiRomeData.bodyRomeData.showBulkEdit ='';
            this.EditApiRomeData.bodyRomeData.actualBulkEdit ='';
        },
        changesBodyEditModel(){
            let self = this;
            if(self.EditApiRomeData.bodyRomeData.editModel=='From'){
                self.EditApiRomeData.bodyRomeData.editModel='Bulk';
                self.EditApiRomeData.bodyRomeData.bulkEdit ='';
                self.EditApiRomeData.bodyRomeData.tableData.forEach(item=>{
                    PrintConsole('changesBodyEditModel',item);
                    let rowData=item.state+',';
                    if(item.key){
                        rowData+=item.key+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.value){
                        rowData+=item.value+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.remarks){
                        rowData+=item.remarks;
                    }
                    rowData+='\n';
                    self.EditApiRomeData.bodyRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.EditApiRomeData.bodyRomeData.bulkEdit.split('\n'));

                self.EditApiRomeData.bodyRomeData.editModel='From';
                self.EditApiRomeData.bodyRomeData.tableData=[];
                self.EditApiRomeData.bodyRomeData.index = 0
                let bulkEdit = self.EditApiRomeData.bodyRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.EditApiRomeData.bodyRomeData.index;
                        if(data[0]=="true"){
                            obj.state = true;
                        }else{
                            obj.state = false;
                        }
                        obj.key = data[1];
                        obj.value = data[2];
                        if(data.length==4){
                            obj.remarks = data[3];
                        }else{
                            obj.remarks ='';
                        }
                        // PrintConsole(obj);
                        self.EditApiRomeData.bodyRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.EditApiRomeData.bodyRomeData.tableData);
            }
        },
        upload_success(fileList,value){
            PrintConsole('fileList',fileList);
            PrintConsole('value',value);
            fileList.push({
                'name':value['fileList'][0]['fileName'],
                'url':store.state.nginxUrl+'Temp/'+value['fileList'][0]['fileName']}
            )
        },
        upload_remove(fileList, value){//在保存和修改的时候传过去
            PrintConsole('fileList',fileList);
            PrintConsole('value',value);
            let self = this;
            fileList.splice(0, 1);

            let splitStr = value.url.split('/');
            let dirName = splitStr[splitStr.length-2]
            let fileName = splitStr[splitStr.length-1]
            self.EditApiRomeData.bodyRomeData.deleteFileList.push({
                'dirName':dirName,
                'fileName':fileName
            });
            PrintConsole('deleteFileList',self.EditApiRomeData.bodyRomeData.deleteFileList);
        },

        //extractRomeData
        CreateNewExtractData(){
            let self = this;
            let obj = {};
            obj.index = self.EditApiRomeData.extractRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditApiRomeData.extractRomeData.tableData.push(obj);
            self.EditApiRomeData.extractRomeData.index+=1;
            PrintConsole('CreateNewExtractData',self.EditApiRomeData.extractRomeData.tableData);
        },
        handleExtractDelete(index,row){
            PrintConsole('handleExtractDelete',row);
            let self = this;
            self.EditApiRomeData.extractRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.extractRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.extractRomeData.tableData[i].index = i;
            });
            self.EditApiRomeData.extractRomeData.index -=1 ;
        },

        //validateRomeData
        GetExtractKeyName(){//获取提取中的key值
            let self = this;
            let checkOptions = [];
            self.EditApiRomeData.extractRomeData.tableData.forEach(e =>{
                if(e.state){
                    let obj ={};
                    obj.label = e.key;
                    obj.value = e.key;
                    checkOptions.push(obj);
                }
            })
            PrintConsole('GetExtractKeyName',checkOptions);
            return checkOptions
        },
        createFilterValidate(queryString) {
            return (restaurant) => {
                return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
        fetchSuggestionsValidate(queryString, cb){//断言点击输入框会加载断言的数据
            var restaurants = this.GetExtractKeyName();
            var results = queryString ? restaurants.filter(this.createFilterValidate(queryString)) : restaurants;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        CreateNewValidateData(){
            let self = this;
            let obj = {};
            obj.index = self.EditApiRomeData.validateRomeData.index;
            obj.state = true;
            obj.checkName = '';
            obj.validateType='';
            obj.valueType='';//断言值类型
            obj.expectedResults='';
            obj.remarks='';

            self.EditApiRomeData.validateRomeData.tableData.push(obj);
            self.EditApiRomeData.validateRomeData.index+=1;
            PrintConsole('CreateNewValidateData',self.EditApiRomeData.validateRomeData.tableData);
        },
        handleValidateDelete(index,row){
            PrintConsole('handleValidateDelete',row);
            let self = this;
            self.EditApiRomeData.validateRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.validateRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.validateRomeData.tableData[i].index = i;
            });
            self.EditApiRomeData.validateRomeData.index -=1 ;
        },

        //前置操作
        handlePreOperationCommand(command){
            PrintConsole('handlePreOperationCommand:',command);
            this.CreateNewPreOperationData(command);
        },
        CreateNewPreOperationData(operationType){
            let self = this;
            let obj = {};
            obj.id = self.EditApiRomeData.preOperationRomeData.index;
            obj.index = self.EditApiRomeData.preOperationRomeData.index;
            obj.state = true;
            obj.operationType = operationType;
            obj.methodsName='';
            obj.dataBase='';
            obj.sql='';

            obj.remarks='';

            self.EditApiRomeData.preOperationRomeData.tableData.push(obj);
            self.EditApiRomeData.preOperationRomeData.index+=1;
            self.rowDropPreOperation();
            PrintConsole('CreateNewMethodsData',self.EditApiRomeData.preOperationRomeData.tableData);
        },
        handlePreOperationDelete(index,row){
            PrintConsole('handlePreOperationDelete',row);
            let self = this;
            self.EditApiRomeData.preOperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.preOperationRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.preOperationRomeData.tableData[i].index = i;
            });
            self.EditApiRomeData.preOperationRomeData.index -=1 ;
        },
        rowDropPreOperation() {//加载可拖动效果
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#PreOperationSort > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.EditApiRomeData.preOperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.EditApiRomeData.preOperationRomeData.tableData.splice(newIndex, 0, currRow);
                    self.SortPreOperation();
                }
            });
        },
        SortPreOperation(){//调用 每次拖动完成后调用重新排序
            let self = this;
            self.EditApiRomeData.preOperationRomeData.tableData.forEach((d,index)=>{
                self.EditApiRomeData.preOperationRomeData.tableData[index].rowNum = index;
            });
            PrintConsole('SortPreOperation:重新排序',self.EditApiRomeData.preOperationRomeData.tableData);
        },
        getDataBaseOption(){//加载数据库环境的IP及以下可用的库名
            GetConnectBaseItems().then(d=>{
                if(d.statusCode==2000){
                    this.EditApiRomeData.preOperationRomeData.dataBaseOptions = d.dataList;
                    this.EditApiRomeData.rearOperationRomeData.dataBaseOptions = d.dataList;
                }else{
                    this.$message.error('数据库环境加载失败:'+d.errorMsg);
                }
            });
        },

        //后置操作
        handleRearOperationCommand(command){
            PrintConsole('handleRearOperationCommand:',command);
            this.CreateNewRearOperationData(command);
        },
        CreateNewRearOperationData(operationType){
            let self = this;
            let obj = {};
            obj.id = self.EditApiRomeData.rearOperationRomeData.index;
            obj.index = self.EditApiRomeData.rearOperationRomeData.index;
            obj.state = true;
            obj.operationType = operationType;
            obj.methodsName='';
            obj.dataBase='';
            obj.sql='';

            obj.remarks='';

            self.EditApiRomeData.rearOperationRomeData.tableData.push(obj);
            self.EditApiRomeData.rearOperationRomeData.index+=1;
            self.rowDropRearOperation();
            PrintConsole('CreateNewRearOperationData',self.EditApiRomeData.rearOperationRomeData.tableData);
        },
        handleRearOperationDelete(index,row){
            PrintConsole('handleRearOperationDelete',row);
            let self = this;
            self.EditApiRomeData.rearOperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditApiRomeData.rearOperationRomeData.tableData.forEach((item,i)=>{
                self.EditApiRomeData.rearOperationRomeData.tableData[i].index = i;
            });
            self.EditApiRomeData.rearOperationRomeData.index -=1 ;
        },
        rowDropRearOperation() {//加载可拖动效果
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#RearOperationSort > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.EditApiRomeData.rearOperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.EditApiRomeData.rearOperationRomeData.tableData.splice(newIndex, 0, currRow);
                    self.SortRearOperation();
                }
            });
        },
        SortRearOperation(){//调用 每次拖动完成后调用重新排序
            let self = this;
            self.EditApiRomeData.rearOperationRomeData.tableData.forEach((d,index)=>{
                self.EditApiRomeData.rearOperationRomeData.tableData[index].rowNum = index;
            });
            PrintConsole('SortRearOperation:重新排序',self.EditApiRomeData.rearOperationRomeData.tableData);
        },

        //验证事件
        ClearCharmRomeData(){
            let self =this;
            self.CharmRomeData.title='';
            self.CharmRomeData.tableData=[];
        },
        CharmApiData(){//验证API接口数据的完整性
            let self = this;
            self.CharmRomeData.tableData = [];
            self.CharmRomeData.title = '';
            self.$axios.post('/api/ApiIntMaintenance/CharmApiData',{
                'CharmType':self.isAddNew,
                'BasicInfo':{
                    'apiId':self.BasicRomeData.apiId,
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.BasicRomeData.pageId,
                    'funId':self.BasicRomeData.funId,
                    'apiName':self.BasicRomeData.apiName,
                },
                'ApiInfo':{
                    'requestType':self.EditApiRomeData.requestType,
                    'requestUrlRadio':self.EditApiRomeData.requestUrlRadio,
                    'requestUrl':{
                        'url1':self.EditApiRomeData.requestUrl1,
                        'url2':self.EditApiRomeData.requestUrl2,
                        'url3':self.EditApiRomeData.requestUrl3,
                    },
                    'request':{
                        'headers':self.EditApiRomeData.headersRomeData.tableData,
                        'params':self.EditApiRomeData.paramsRomeData.tableData,
                        'body':{
                            'requestSaveType':self.EditApiRomeData.bodyRomeData.requestSaveType,
                            'formData':self.EditApiRomeData.bodyRomeData.tableData,
                            'raw':self.EditApiRomeData.bodyRomeData.rawValue,
                            'json':self.EditApiRomeData.bodyRomeData.jsonValue,
                        },
                        'extract':self.EditApiRomeData.extractRomeData.tableData,
                        'validate':self.EditApiRomeData.validateRomeData.tableData,
                        'preOperation':self.EditApiRomeData.preOperationRomeData.tableData,
                        'rearOperation':self.EditApiRomeData.rearOperationRomeData.tableData,
                    }
                },
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.stepsName =d.stepsName;
                        obj.errorMsg = d.errorMsg;
                        obj.updateTime = d.updateTime;
                        self.CharmRomeData.tableData.push(obj);
                    });
                    if(self.CharmRomeData.tableData.length!=0){
                        self.StepsRomeData.processStatus='error';
                        self.CharmRomeData.title = '效验结果:失败,共发现错误数:'+self.CharmRomeData.tableData.length;
                    }else{
                        self.StepsRomeData.active++;
                        self.CharmRomeData.title = '效验结果:完成,请点击保存';
                    }
                }else{
                    self.$message.error('效验接口信息发生错误:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },

        //保存事件
        DataSave(){//保存接口
            let self = this;
            if(self.CharmRomeData.tableData.length==0){
                if(self.isAddNew){  
                    self.$axios.post('/api/ApiIntMaintenance/SaveData',{
                        'BasicInfo':{
                            'proId':self.$cookies.get('proId'),
                            'pageId':self.BasicRomeData.pageId,
                            'funId':self.BasicRomeData.funId,
                            'apiName':self.BasicRomeData.apiName,
                            'environmentId':self.BasicRomeData.environmentId,
                            'apiState':self.BasicRomeData.apiState,
                            'assignedUserId':self.BasicRomeData.assignedUserId,
                            'pushTo':self.BasicRomeData.pushTo,
                        },
                        'ApiInfo':{
                            'requestType':self.EditApiRomeData.requestType,
                            'requestUrlRadio':self.EditApiRomeData.requestUrlRadio,
                            'requestUrl':{
                                'url1':self.EditApiRomeData.requestUrl1,
                                'url2':self.EditApiRomeData.requestUrl2,
                                'url3':self.EditApiRomeData.requestUrl3,
                            },
                            'request':{
                                'headers':self.EditApiRomeData.headersRomeData.tableData,
                                'params':self.EditApiRomeData.paramsRomeData.tableData,
                                'body':{
                                    'requestSaveType':self.EditApiRomeData.bodyRomeData.requestSaveType,
                                    'formData':self.EditApiRomeData.bodyRomeData.tableData,
                                    'raw':self.EditApiRomeData.bodyRomeData.rawValue,
                                    'json':self.EditApiRomeData.bodyRomeData.jsonValue,
                                    'deleteFileList':self.EditApiRomeData.bodyRomeData.deleteFileList,
                                },
                                'extract':self.EditApiRomeData.extractRomeData.tableData,
                                'validate':self.EditApiRomeData.validateRomeData.tableData,
                                'preOperation':self.EditApiRomeData.preOperationRomeData.tableData,
                                'rearOperation':self.EditApiRomeData.rearOperationRomeData.tableData,
                            }
                        },
                    }).then(res => {
                        if(res.data.statusCode==2001){
                            self.$message.success('新增接口成功!');
                            self.returnToMain();
                        
                        }else{
                            self.$message.error('接口保存失败'+res.data.errorMsg);
                        }
                    }).catch(function (error) {
                        console.log(error);
                    })
                }else{
                    self.$axios.post('/api/ApiIntMaintenance/EditData',{
                       'BasicInfo':{
                            'apiId':self.BasicRomeData.apiId,
                            'proId':self.$cookies.get('proId'),
                            'pageId':self.BasicRomeData.pageId,
                            'funId':self.BasicRomeData.funId,
                            'apiName':self.BasicRomeData.apiName,
                            'environmentId':self.BasicRomeData.environmentId,
                            'apiState':self.BasicRomeData.apiState,
                            'assignedUserId':self.BasicRomeData.assignedUserId,
                            'pushTo':self.BasicRomeData.pushTo,
                        },
                        'ApiInfo':{
                            'requestType':self.EditApiRomeData.requestType,
                            'requestUrlRadio':self.EditApiRomeData.requestUrlRadio,
                            'requestUrl':{
                                'url1':self.EditApiRomeData.requestUrl1,
                                'url2':self.EditApiRomeData.requestUrl2,
                                'url3':self.EditApiRomeData.requestUrl3,
                            },
                            'request':{
                                'headers':self.EditApiRomeData.headersRomeData.tableData,
                                'params':self.EditApiRomeData.paramsRomeData.tableData,
                                'body':{
                                    'requestSaveType':self.EditApiRomeData.bodyRomeData.requestSaveType,
                                    'formData':self.EditApiRomeData.bodyRomeData.tableData,
                                    'raw':self.EditApiRomeData.bodyRomeData.rawValue,
                                    'json':self.EditApiRomeData.bodyRomeData.jsonValue,
                                    'deleteFileList':self.EditApiRomeData.bodyRomeData.deleteFileList,
                                },
                                'extract':self.EditApiRomeData.extractRomeData.tableData,
                                'validate':self.EditApiRomeData.validateRomeData.tableData,
                                'preOperation':self.EditApiRomeData.preOperationRomeData.tableData,
                                'rearOperation':self.EditApiRomeData.rearOperationRomeData.tableData,
                            }
                        },
                    }).then(res => {
                        if(res.data.statusCode==2002){
                            self.$message.success('修改接口成功!');
                            self.returnToMain();
                        
                        }else{
                            self.$message.error('修改接口失败'+res.data.errorMsg);
                        }
                    }).catch(function (error) {
                        console.log(error);
                    })
                }
            }else{
                self.$message.warning('请先修改错误数据后,在进行保存!');
            }
        },
        LoadData(apiId){
            let self = this;
            self.loading=true;
            return self.$axios.get('/api/ApiIntMaintenance/LoadData',{
                params:{
                  'apiId':apiId
                }
            }).then(res => {
                return res.data;
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },

        //测试请求
        closeTestReportDialog(){
            this.dialog.testReport.dialogVisible =false;
        },
        OpenTestReportDialog(index,row){
            let self = this;
            self.dialog.testReport.dialogPara={
                dialogTitle:self.BasicRomeData.apiName,//初始化标题
                isTest:true,
                source:'API',
                testSendData:{
                    'BasicInfo':{
                        'proId':self.$cookies.get('proId'),
                        'environmentId':self.BasicRomeData.environmentId,
                    },
                    'ApiInfo':{
                        'requestType':self.EditApiRomeData.requestType,
                        'requestUrlRadio':self.EditApiRomeData.requestUrlRadio,
                        'requestUrl':{
                            'url1':self.EditApiRomeData.requestUrl1,
                            'url2':self.EditApiRomeData.requestUrl2,
                            'url3':self.EditApiRomeData.requestUrl3,
                        },
                        'request':{
                            'headers':self.EditApiRomeData.headersRomeData.tableData,
                            'params':self.EditApiRomeData.paramsRomeData.tableData,
                            'body':{
                                'requestSaveType':self.EditApiRomeData.bodyRomeData.requestSaveType,
                                'formData':self.EditApiRomeData.bodyRomeData.tableData,
                                'raw':self.EditApiRomeData.bodyRomeData.rawValue,
                                'json':self.EditApiRomeData.bodyRomeData.jsonValue,

                            },
                            'extract':self.EditApiRomeData.extractRomeData.tableData,
                            'validate':self.EditApiRomeData.validateRomeData.tableData,
                            'preOperation':self.EditApiRomeData.preOperationRomeData.tableData,
                            'rearOperation':self.EditApiRomeData.rearOperationRomeData.tableData,
                        }
                    }
                }
            }
            self.dialog.testReport.dialogVisible=true;
        },

    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
.bodyRome{
    margin-top:10px;
}
</style>
