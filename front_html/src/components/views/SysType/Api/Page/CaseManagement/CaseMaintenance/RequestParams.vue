<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1200px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :show-close="false"
            :close-on-press-escape="false"
            :before-close="dialogClose">
                <el-card v-loading="loading" shadow="never" style="height: 810px;">
                    <div>
                        <el-row>
                            <el-col :span="19">
                                <div style="float:left">
                                    <el-input placeholder="请输入接口地址" style="width:800px" v-model="RomeData.requestUrl">
                                        <el-select v-model="RomeData.requestType" slot="prepend" style="width:97px">
                                            <el-option
                                                v-for="item in RomeData.requestTypeOption"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </el-input>
                                </div>
                            </el-col>
                            <el-col :span="5">
                                <div>
                                    <el-button-group>
                                        <el-button type="primary" @click="OpenTestReportDialog()">调试接口</el-button>
                                        <el-button type="warning" @click="ReferenceOriginalSet()" >引用原设</el-button>
                                        <el-button icon="el-icon-question" circle plain @click="helpMsg()"></el-button>
                                    </el-button-group>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <div>
                        <el-tabs v-model="RomeData.activeName" @tab-click="handleClickTabs">  
                            <el-tab-pane :label="RomeData.headersName" name="Headers">
                                <div v-if="RomeData.headersRomeData.editModel=='From'">
                                    <el-table
                                        :data="RomeData.headersRomeData.tableData"
                                        border
                                        height="680px">
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
                                                v-model="RomeData.headersRomeData.bulkEdit">
                                            </el-input>
                                        </div>
                                    </el-card>
                                </div>
                            </el-tab-pane>
                            <el-tab-pane :label="RomeData.paramsName" name="Params">
                                <div v-if="RomeData.paramsRomeData.editModel=='From'">
                                    <el-table
                                        :data="RomeData.paramsRomeData.tableData"
                                        border
                                        height="680px">
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
                                                v-model="RomeData.paramsRomeData.bulkEdit">
                                            </el-input>
                                        </div>
                                    </el-card>
                                </div>
                            </el-tab-pane>
                            <el-tab-pane :label="RomeData.bodyName" name="Body">
                                <div>
                                    <el-radio-group v-model="RomeData.bodyRomeData.requestSaveType" @change="changeBodyRequestType">
                                        <el-radio label="none">none</el-radio>
                                        <el-radio label='form-data'>form-data</el-radio>
                                        <el-radio label="json">json</el-radio>
                                        <el-radio label="raw">raw</el-radio>
                                    </el-radio-group>
                                </div>
                                <div v-if="RomeData.bodyRomeData.requestSaveType=='none'">
                                    <el-card shadow="never" class="bodyRome" style="height:650px;">
                                        <div>该请求没有主体</div>
                                    </el-card>
                                </div>
                                <div v-else-if="RomeData.bodyRomeData.requestSaveType=='form-data'">
                                    <div v-if="RomeData.bodyRomeData.editModel=='From'">
                                        <el-table
                                            class="bodyRome"
                                            :data="RomeData.bodyRomeData.tableData"
                                            border
                                            height="650px">
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
                                                label="类型"
                                                width="110px"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-select v-model="scope.row.paramsType">
                                                        <el-option
                                                            v-for="item in RomeData.bodyRomeData.paramsTypeOption"
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
                                                            style="float:left;width:270px"
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
                                                    v-model="RomeData.bodyRomeData.bulkEdit">
                                                </el-input>
                                            </div>
                                        </el-card>
                                    </div>
                                </div>
                                <div v-else-if="RomeData.bodyRomeData.requestSaveType=='json'">
                                    <el-input
                                        class="bodyRome"
                                        type="textarea"
                                        :autosize="{ minRows: 29, maxRows: 29}"
                                        v-model="RomeData.bodyRomeData.jsonValue">
                                    </el-input>
                                </div>
                                <div v-else-if="RomeData.bodyRomeData.requestSaveType=='raw'">
                                    <el-input
                                        class="bodyRome"
                                        type="textarea"
                                        :autosize="{ minRows: 29, maxRows: 29}"
                                        v-model="RomeData.bodyRomeData.rawValue">
                                    </el-input>
                                </div>
                                <div v-else>
                                    <el-card shadow="never" class="bodyRome" style="height:650px;">
                                        <div>这里是上传文件地址</div>
                                    </el-card>
                                </div>
                            </el-tab-pane>
                            <el-tab-pane :label="RomeData.extractName" name="Extract">
                                <el-table
                                    :data="RomeData.extractRomeData.tableData"
                                    border
                                    height="680px">
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
                                            <el-input v-model="scope.row.key" placeholder="注意:同一接口不要使用相同变量名称,会冲突!"></el-input>
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
                            <el-tab-pane :label="RomeData.validateName" name="Validate">
                                <el-table
                                    :data="RomeData.validateRomeData.tableData"
                                    border
                                    height="680px">
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
                                                    v-for="item in RomeData.validateRomeData.validateTypeOption"
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
                                                        v-for="item in RomeData.validateRomeData.valueTypeOption"
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
                            <el-tab-pane :label="RomeData.preOperationName" name="PreOperation">
                                <el-table
                                    id="PreOperationSort"
                                    row-key="id"
                                    :data="RomeData.preOperationRomeData.tableData"
                                    border
                                    height="680px">
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
                                                <el-form ref="preOperationRomeData" :model="RomeData.preOperationRomeData" label-width="80px">
                                                    <el-form-item label="数据库:">
                                                        <el-cascader
                                                                style="float:left;width:437px"
                                                                clearable
                                                                placeholder="请选择连接的数据库" 
                                                                v-model="scope.row.dataBase"
                                                                :options="RomeData.preOperationRomeData.dataBaseOptions"
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
                            <el-tab-pane :label="RomeData.rearOperationName" name="RearOperation">
                                <el-table
                                    id="RearOperationSort"
                                    row-key="id"
                                    :data="RomeData.rearOperationRomeData.tableData"
                                    border
                                    height="680px">
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
                                                <el-form ref="rearOperationRomeData" :model="RomeData.rearOperationRomeData" label-width="80px">
                                                    <el-form-item label="数据库:">
                                                        <el-cascader
                                                                style="float:left;width:437px"
                                                                clearable
                                                                placeholder="请选择连接的数据库" 
                                                                v-model="scope.row.dataBase"
                                                                :options="RomeData.rearOperationRomeData.dataBaseOptions"
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
                </el-card>
                <div style="margin-top:10px">
                    <el-button type="info" @click="dialogClose()">取消</el-button>
                    <el-button type="success" @click="SaveData()">保存</el-button>
                </div>
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
import store from '../../../../../../../store/index';
import Sortable from 'sortablejs';
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetConnectBaseItems} from "../../../../../../js/GetSelectTable.js";

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
            uploadToTemp:store.state.BackService +'/api/upLoad/UpLoadToTempPath',
            RomeData:{
                id:'',
                environmentId:'',
                apiId:'',
                requestUrl:'',
                requestType:'GET',
                requestTypeOption:[
                    {'label':'GET','value':'GET'},
                    {'label':'POST','value':'POST'},
                ],
                activeName:'Headers',

                headersName:'Headers',
                headersRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',//显示给屏幕上看的数据
                },

                paramsName:'Params',
                paramsRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',//显示给屏幕上看的数据
                },

                bodyName:'Body',
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

                extractName:'Extract/提取',
                extractRomeData:{
                    index:0,
                    tableData:[],
                },

                validateName:'Validate/断言',
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

                preOperationName:'前置操作',
                preOperationRomeData:{
                    index:0,
                    tableData:[],
                    dataBaseOptions:[],
                },

                rearOperationName:'后置操作',
                rearOperationRomeData:{
                    index:0,
                    tableData:[],
                    dataBaseOptions:[],
                }


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
                this.ClearRomeData();
                this.RomeData.environmentId='';
                this.RomeData.apiId='';
                this.dialogTitle = newval.dialogTitle;
                this.RomeData.id = newval.id;//这是唯一值
                this.RomeData.apiId = newval.apiId;//这个不是唯一值
                this.RomeData.environmentId = newval.environmentId;
                this.getDataBaseOption();

                this.$nextTick(function () {//当DOM加载完成后才会执行这个!
                    this.assignmentData(newval.request);//查询最终列表中有没有此id的数据,如果有的话就赋值,没有的话才是全空填写
                })
                
                if(newval.synchronous){//同步开启时
                    PrintConsole('当前同步开启','正在同步数据');
                    this.LoadApiData(this.RomeData.apiId);
                }
            }
        },
        'RomeData.headersRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.headersRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.headersName='Headers';
                }else{
                    self.RomeData.headersName='Headers('+dataLength+')';
                }  
            }
        },
        'RomeData.paramsRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.paramsRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.paramsName='Params';
                }else{
                    self.RomeData.paramsName='Params('+dataLength+')';
                }
                
            }
        },
        'RomeData.bodyRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.bodyRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.bodyName='Body';
                }else{
                    self.RomeData.bodyName='Body('+dataLength+')';
                }
                
            }
        },
        'RomeData.extractRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.extractRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.extractName='Extract/提取';
                }else{
                    self.RomeData.extractName='Extract/提取('+dataLength+')';
                }
                
            }
        },
        'RomeData.validateRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.validateRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.validateName='Validate/断言';
                }else{
                    self.RomeData.validateName='Validate/断言('+dataLength+')';
                }
                
            }
        },
        'RomeData.preOperationRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.preOperationRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.preOperationName='前置操作';
                }else{
                    self.RomeData.preOperationName='前置操作('+dataLength+')';
                }
                
            }
        },
        'RomeData.rearOperationRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.RomeData.rearOperationRomeData.tableData.length;
                if(dataLength==0){
                    self.RomeData.rearOperationName='后置操作';
                }else{
                    self.RomeData.rearOperationName='后置操作('+dataLength+')';
                }
                
            }
        },
      
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        handleClickTabs(tab, event){//点击头部主体等标签
            PrintConsole(tab);
        },
        ClearRomeData(){
            PrintConsole('ClearRomeData');
            let self = this;

            self.RomeData.requestType='GET';
            self.RomeData.requestUrl='';
            self.RomeData.activeName='Headers';

            self.RomeData.headersName='Headers';
            self.RomeData.paramsName='Params';
            self.RomeData.bodyName='Body';
            self.RomeData.extractName='Extract/提取';
            self.RomeData.validateName='Validate/断言';
            self.RomeData.preOperationName='前置操作';
            self.RomeData.rearOperationName='后置操作';

            //headersRomeData
            self.RomeData.headersRomeData.tableData=[];
            self.RomeData.headersRomeData.index=0;
            self.RomeData.headersRomeData.editModel='From';

            // //paramsRomeData
            self.RomeData.paramsRomeData.tableData=[];
            self.RomeData.paramsRomeData.index=0;
            self.RomeData.paramsRomeData.editModel='From';

            //bodyRomeData
            self.RomeData.bodyRomeData.tableData=[];
            self.RomeData.bodyRomeData.index=0;
            self.RomeData.bodyRomeData.editModel='From';
            self.RomeData.bodyRomeData.requestSaveType='form-data';
            self.RomeData.bodyRomeData.rawValue = '';
            self.RomeData.bodyRomeData.jsonValue = '';

            //extractRomeData
            self.RomeData.extractRomeData.tableData=[];
            self.RomeData.extractRomeData.index=0;

            //validateRomeData
            self.RomeData.validateRomeData.tableData=[];
            self.RomeData.validateRomeData.index=0;

            //PreOperationRomeData
            self.RomeData.preOperationRomeData.tableData=[];
            self.RomeData.preOperationRomeData.index=0;

            //rearOperationRomeData
            self.RomeData.rearOperationRomeData.tableData=[];
            self.RomeData.rearOperationRomeData.index=0;
        },
        assignmentData(request){//赋值数据到页面
            let self = this;
            self.RomeData.requestType = request.requestType;
            self.RomeData.requestUrl = request.requestUrl;
            
            //headers
            request.headers.forEach(item_headers=>{
                let obj = {};
                obj.index = item_headers.index;
                obj.state =item_headers.state;
                obj.key =item_headers.key;
                obj.value=item_headers.value;
                obj.remarks=item_headers.remarks;
                self.RomeData.headersRomeData.tableData.push(obj);
                self.RomeData.headersRomeData.index+=1;
            });
            
            //params
            request.params.forEach(item_params=>{
                let obj = {};
                obj.index = item_params.index;
                obj.state =item_params.state;
                obj.key =item_params.key;
                obj.value=item_params.value;
                obj.remarks=item_params.remarks;

                self.RomeData.paramsRomeData.tableData.push(obj);
                self.RomeData.paramsRomeData.index+=1;
            });

            //body
            self.RomeData.bodyRomeData.requestSaveType = request.body.requestSaveType;
            if(self.RomeData.bodyRomeData.requestSaveType=='form-data'){
                request.body.formData.forEach(item_body=>{
                    let obj = {};
                    obj.index = item_body.index;
                    obj.state =item_body.state;
                    obj.key =item_body.key;
                    obj.paramsType=item_body.paramsType;
                    obj.value=item_body.value;
                    obj.fileList=item_body.fileList;
                    obj.remarks=item_body.remarks;

                    self.RomeData.bodyRomeData.tableData.push(obj);
                    self.RomeData.bodyRomeData.index+=1;
                });
            }else if(self.RomeData.bodyRomeData.requestSaveType=='raw'){
                self.RomeData.bodyRomeData.rawValue = request.body.rawValue;
            }else if(self.RomeData.bodyRomeData.requestSaveType=='json'){
                self.RomeData.bodyRomeData.jsonValue = request.body.jsonValue;
            }
            
            //extract
            request.extract.forEach(item_extract=>{
                let obj = {};
                obj.index = item_extract.index;
                obj.state =item_extract.state;
                obj.key =item_extract.key;
                obj.value=item_extract.value;
                obj.remarks=item_extract.remarks;

                self.RomeData.extractRomeData.tableData.push(obj);
                self.RomeData.extractRomeData.index+=1;
            });
            
            //validate
            request.validate.forEach(item_validate=>{
                let obj = {};
                obj.index = item_validate.index;
                obj.state =item_validate.state;
                obj.checkName =item_validate.checkName;
                obj.validateType=item_validate.validateType;
                obj.valueType=item_validate.valueType;
                obj.expectedResults=item_validate.expectedResults;
                obj.remarks=item_validate.remarks;

                self.RomeData.validateRomeData.tableData.push(obj);
                self.RomeData.validateRomeData.index+=1;
            });
            
            //preOperation
            request.preOperation.forEach(item_preOperation=>{
                let obj = {};
                obj.index = item_preOperation.index;
                obj.state =item_preOperation.state;
                obj.operationType =item_preOperation.operationType;
                obj.methodsName=item_preOperation.methodsName;
                obj.dataBase=item_preOperation.dataBase;
                obj.sql=item_preOperation.sql;
                obj.remarks=item_preOperation.remarks;

                self.RomeData.preOperationRomeData.tableData.push(obj);
                self.RomeData.preOperationRomeData.index+=1;
            });
            
            //rearOperation
            request.rearOperation.forEach(item_rearOperation=>{
                let obj = {};
                obj.index = item_rearOperation.index;
                obj.state =item_rearOperation.state;
                obj.operationType =item_rearOperation.operationType;
                obj.methodsName=item_rearOperation.methodsName;
                obj.dataBase=item_rearOperation.dataBase;
                obj.sql=item_rearOperation.sql;
                obj.remarks=item_rearOperation.remarks;

                self.RomeData.rearOperationRomeData.tableData.push(obj);
                self.RomeData.rearOperationRomeData.index+=1;
            });
            
            PrintConsole('赋值到页面');
        },
        LoadApiData(apiId){//加载接口的数据
            let self = this;
            self.$axios.get('/api/ApiCaseMaintenance/LoadData',{
                params:{
                  'apiId':apiId
                }
            }).then(res => {
               if(res.data.statusCode==2000){
                    self.RomeData.requestType=res.data.apiInfo.requestType;
                    self.RomeData.requestUrl=res.data.apiInfo.requestUrl;
                
                    //headers
                    res.data.apiInfo.request.headers.forEach(item_headers=>{
                        let tempCaseTable = self.RomeData.headersRomeData.tableData.find(item=>
                            item_headers.key == item.key
                        );
                        if(tempCaseTable){
                            PrintConsole('headers-当前key存在不会同步此Key:',item_headers.key);
                        }else{
                            let obj = {};
                            obj.index = item_headers.index;
                            obj.state =item_headers.state;
                            obj.key =item_headers.key;
                            obj.value='';
                            obj.remarks=item_headers.remarks;

                            self.RomeData.headersRomeData.tableData.push(obj);
                            self.RomeData.headersRomeData.index+=1
                        }
                    });

                    //params
                    res.data.apiInfo.request.params.forEach(item_params=>{
                        let tempCaseTable = self.RomeData.paramsRomeData.tableData.find(item=>
                            item_params.key == item.key
                        );
                        if(tempCaseTable){
                            PrintConsole('params-当前key存在不会同步此Key:',item_params.key);
                        }else{
                            let obj = {};
                            obj.index = item_params.index;
                            obj.state =item_params.state;
                            obj.key =item_params.key;
                            obj.value='';
                            obj.remarks=item_params.remarks;

                            self.RomeData.paramsRomeData.tableData.push(obj);
                            self.RomeData.paramsRomeData.index+=1
                        }
                    });

                    //body
                    self.RomeData.bodyRomeData.requestSaveType = res.data.apiInfo.request.body.requestSaveType;
                    if(res.data.apiInfo.request.body.requestSaveType=='form-data'){
                        res.data.apiInfo.request.body.bodyData.forEach(item_body=>{
                            let tempCaseTable = self.RomeData.bodyRomeData.tableData.find(item=>
                                item_body.key == item.key
                            );
                            if(tempCaseTable){
                                PrintConsole('body-当前key存在不会同步此Key:',item_body.key);
                            }else{
                                let obj = {};
                                obj.index = item_body.index;
                                obj.state =item_body.state;
                                obj.key =item_body.key;
                                obj.paramsType=item_body.paramsType;
                                obj.value='';
                                obj.fileList=item_body.fileList;
                                obj.remarks=item_body.remarks;

                                self.RomeData.bodyRomeData.tableData.push(obj);
                                self.RomeData.bodyRomeData.index+=1
                            }
                        });
                    }else if(res.data.apiInfo.request.body.requestSaveType=='raw'){
                        self.RomeData.bodyRomeData.rawValue = res.data.apiInfo.request.body.bodyData;
                    }else if(res.data.apiInfo.request.body.requestSaveType=='json'){
                        self.RomeData.bodyRomeData.jsonValue = res.data.apiInfo.request.body.bodyData;
                    }            
               }else{
                   self.$message.error('数据获取失败:',res.data.errorMsg);
               }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ReferenceOriginalSet(){
            let self = this;
            self.$confirm('引用原接口设置,会清空当前您所填写的参数,请确定是否引用?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                self.ClearRomeData();
                self.loading=true;
                self.$axios.get('/api/ApiIntMaintenance/LoadData',{
                    params:{
                        'apiId':self.RomeData.apiId
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.requestType=res.data.apiInfo.requestType;
                        self.RomeData.requestUrl=res.data.apiInfo.currentRequestUrl;
                    
                        //headers
                        res.data.apiInfo.request.headers.forEach(item_headers=>{
                            let obj = {};
                            obj.index = item_headers.index;
                            obj.state =item_headers.state;
                            obj.key =item_headers.key;
                            obj.value=item_headers.value;
                            obj.remarks=item_headers.remarks;

                            self.RomeData.headersRomeData.tableData.push(obj);
                            self.RomeData.headersRomeData.index+=1;
                        });

                        //params
                        res.data.apiInfo.request.params.forEach(item_params=>{
                            let obj = {};
                            obj.index = item_params.index;
                            obj.state =item_params.state;
                            obj.key =item_params.key;
                            obj.value=item_params.value;
                            obj.remarks=item_params.remarks;
                            self.RomeData.paramsRomeData.tableData.push(obj);

                            self.RomeData.paramsRomeData.index+=1;
                        });

                        //body
                        self.RomeData.bodyRomeData.requestSaveType = res.data.apiInfo.request.body.requestSaveType;
                        if(res.data.apiInfo.request.body.requestSaveType=='form-data'){
                            res.data.apiInfo.request.body.bodyData.forEach(item_body=>{
                                let obj = {};
                                obj.index = item_body.index;
                                obj.state =item_body.state;
                                obj.key =item_body.key;
                                obj.paramsType=item_body.paramsType;
                                obj.value=item_body.value;
                                obj.fileList=[];
                                obj.remarks=item_body.remarks;

                                self.RomeData.bodyRomeData.tableData.push(obj);
                                self.RomeData.bodyRomeData.index+=1;
                            });
                        }else if(res.data.apiInfo.request.body.requestSaveType=='raw'){
                            self.RomeData.bodyRomeData.rawValue = res.data.apiInfo.request.body.bodyData;
                        }else if(res.data.apiInfo.request.body.requestSaveType=='json'){
                            self.RomeData.bodyRomeData.jsonValue = res.data.apiInfo.request.body.bodyData;
                        }
                
                        //extract
                        res.data.apiInfo.request.extract.forEach(item_extract=>{
                            let obj = {};
                            obj.index = item_extract.index;
                            obj.state =item_extract.state;
                            obj.key =item_extract.key;
                            obj.value=item_extract.value;
                            obj.remarks=item_extract.remarks;

                            self.RomeData.extractRomeData.tableData.push(obj);
                            self.RomeData.extractRomeData.index+=1;
                        });

                        //validate
                        res.data.apiInfo.request.validate.forEach(item_validate=>{
                            let obj = {};
                            obj.index = item_validate.index;
                            obj.state =item_validate.state;
                            obj.checkName =item_validate.checkName;
                            obj.validateType=item_validate.validateType;
                            obj.valueType=item_validate.valueType;
                            obj.expectedResults=item_validate.expectedResults;
                            obj.remarks=item_validate.remarks;

                            self.RomeData.validateRomeData.tableData.push(obj);
                            self.RomeData.validateRomeData.index+=1;
                        });

                        //preOperation
                        self.getDataBaseOption();
                        res.data.apiInfo.request.preOperation.forEach(item_preOperation=>{
                            let obj = {};
                            obj.index = item_preOperation.index;
                            obj.state =item_preOperation.state;
                            obj.operationType =item_preOperation.operationType;
                            obj.methodsName=item_preOperation.methodsName;
                            obj.dataBase=item_preOperation.dataBase;
                            obj.sql=item_preOperation.sql;
                            obj.remarks=item_preOperation.remarks;

                            self.RomeData.preOperationRomeData.tableData.push(obj);
                            self.RomeData.preOperationRomeData.index+=1;
                        });

                        //rearOperation
                        res.data.apiInfo.request.rearOperation.forEach(item_rearOperation=>{
                            let obj = {};
                            obj.index = item_rearOperation.index;
                            obj.state =item_rearOperation.state;
                            obj.operationType =item_rearOperation.operationType;
                            obj.methodsName=item_rearOperation.methodsName;
                            obj.dataBase=item_rearOperation.dataBase;
                            obj.sql=item_rearOperation.sql;
                            obj.remarks=item_rearOperation.remarks;

                            self.RomeData.rearOperationRomeData.tableData.push(obj);
                            self.RomeData.rearOperationRomeData.index+=1;
                        });
                        self.loading=false;
                    }else{
                        self.$message.error('数据加载失败:',res.data.errorMsg);
                        self.loading=false;
                    }
                }).catch(function (error) {
                    console.log(error);
                    self.loading=false;
                })
            }).catch(function (error){     
                console.log(error);   
            }); 
        },
        //测试请求
        closeTestReportDialog(){
            this.dialog.testReport.dialogVisible =false;
        },
        OpenTestReportDialog(index,row){
            let self = this;
            self.dialog.testReport.dialogPara={
                dialogTitle:self.dialogTitle,//初始化标题
                source:'API',
                isTest:true,
                testSendData:{
                    'BasicInfo':{
                        'proId':self.$cookies.get('proId'),
                        'environmentId':self.RomeData.environmentId,
                    },
                    'ApiInfo':{
                        'requestType':self.RomeData.requestType,
                        'requestUrlRadio':1,
                        'requestUrl':{
                            'url1':self.RomeData.requestUrl,
                            'url2':'',
                            'url3':'',
                        },
                        'request':{
                            'headers':self.RomeData.headersRomeData.tableData,
                            'params':self.RomeData.paramsRomeData.tableData,
                            'body':{
                                'requestSaveType':self.RomeData.bodyRomeData.requestSaveType,
                                'formData':self.RomeData.bodyRomeData.tableData,
                                'raw':self.RomeData.bodyRomeData.rawValue,
                                'json':self.RomeData.bodyRomeData.jsonValue,
                            },
                            'extract':self.RomeData.extractRomeData.tableData,
                            'validate':self.RomeData.validateRomeData.tableData,
                            'preOperation':self.RomeData.preOperationRomeData.tableData,
                            'rearOperation':self.RomeData.rearOperationRomeData.tableData,
                        }
                    }
                }
            }
            self.dialog.testReport.dialogVisible=true;
        },

        //headersRomeData
        CreateNewHeadersData(){
            let self = this;
            let obj = {};
            obj.index = self.RomeData.headersRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.RomeData.headersRomeData.tableData.push(obj);
            self.RomeData.headersRomeData.index+=1;
            PrintConsole('CreateNewHeadersData',obj);
        },
        handleHeadersDelete(index,row){
            PrintConsole('handleHeadersDelete',row);
            let self = this;
            self.RomeData.headersRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.headersRomeData.tableData.forEach((item,i)=>{
                self.RomeData.headersRomeData.tableData[i].index = i;
            });

            self.RomeData.headersRomeData.index -=1 ;
        },
        cancelHeadersBulkEdit(){//批量修改模式下的取消
            this.RomeData.headersRomeData.editModel='From';
            this.RomeData.headersRomeData.showBulkEdit ='';
            this.RomeData.headersRomeData.actualBulkEdit ='';
        },
        changesHeadersEditModel(){
            let self = this;
            if(self.RomeData.headersRomeData.editModel=='From'){
                self.RomeData.headersRomeData.editModel='Bulk';
                self.RomeData.headersRomeData.bulkEdit ='';
                self.RomeData.headersRomeData.tableData.forEach(item=>{
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
                    self.RomeData.headersRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.RomeData.headersRomeData.bulkEdit.split('\n'));

                self.RomeData.headersRomeData.editModel='From';
                self.RomeData.headersRomeData.tableData=[];
                self.RomeData.headersRomeData.index = 0
                let bulkEdit = self.RomeData.headersRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.RomeData.headersRomeData.index;
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
                        self.RomeData.headersRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.RomeData.headersRomeData.tableData);
            }
        },

        //paramsRomeData
        CreateNewParamsData(){
            let self = this;
            let obj = {};
            obj.index = self.RomeData.paramsRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.RomeData.paramsRomeData.tableData.push(obj);
            self.RomeData.paramsRomeData.index+=1;
            PrintConsole('CreateNewParamsData',self.RomeData.paramsRomeData.tableData);
        },
        handleParamsDelete(index,row){
            PrintConsole('handleParamsDelete',row);
            let self = this;
            self.RomeData.paramsRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.paramsRomeData.tableData.forEach((item,i)=>{
                self.RomeData.paramsRomeData.tableData[i].index = i;
            });

            self.RomeData.paramsRomeData.index -=1 ;
        },
        cancelParamsBulkEdit(){//批量修改模式下的取消
            this.RomeData.paramsRomeData.editModel='From';
            this.RomeData.paramsRomeData.showBulkEdit ='';
            this.RomeData.paramsRomeData.actualBulkEdit ='';
        },
        changesParamsEditModel(){
            let self = this;
            if(self.RomeData.paramsRomeData.editModel=='From'){
                self.RomeData.paramsRomeData.editModel='Bulk';
                self.RomeData.paramsRomeData.bulkEdit ='';
                self.RomeData.paramsRomeData.tableData.forEach(item=>{
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
                    self.RomeData.paramsRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.RomeData.paramsRomeData.bulkEdit.split('\n'));

                self.RomeData.paramsRomeData.editModel='From';
                self.RomeData.paramsRomeData.tableData=[];
                self.RomeData.paramsRomeData.index = 0
                let bulkEdit = self.RomeData.paramsRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.RomeData.paramsRomeData.index;
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
                        self.RomeData.paramsRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.RomeData.paramsRomeData.tableData);
            }
        },

        //bodyRomeDta
        changeBodyRequestType(val){
            PrintConsole(val);
            let self = this;
            if(val=='json'){
                let tempData = self.RomeData.headersRomeData.tableData.find(item=>
                    item.key == 'Content-Type'
                );
                if(tempData){
                    PrintConsole(tempData);
                }else{
                    let obj = {};
                    obj.index = self.RomeData.headersRomeData.index;
                    obj.state = true;
                    obj.key = 'Content-Type';
                    obj.value='application/json';
                    obj.remarks='';

                    self.RomeData.headersRomeData.tableData.push(obj);
                    self.RomeData.headersRomeData.index+=1;
                }
            }
        },
        CreateNewBodyData(){
            let self = this;
            let obj = {};
            obj.index = self.RomeData.bodyRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.paramsType = 'Text';
            obj.value='';
            obj.fileList=[];
            obj.remarks='';

            self.RomeData.bodyRomeData.tableData.push(obj);
            self.RomeData.bodyRomeData.index+=1;
            PrintConsole('CreateNewBodyData',self.RomeData.bodyRomeData.tableData);
        },
        handleBodyDelete(index,row){
            PrintConsole('handleBodyDelete',row);
            let self = this;
            self.RomeData.bodyRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.bodyRomeData.tableData.forEach((item,i)=>{
                self.RomeData.bodyRomeData.tableData[i].index = i;
            });

            self.RomeData.bodyRomeData.index -=1 ;
        },
        cancelBodyBulkEdit(){//批量修改模式下的取消
            this.RomeData.bodyRomeData.editModel='From';
            this.RomeData.bodyRomeData.showBulkEdit ='';
            this.RomeData.bodyRomeData.actualBulkEdit ='';
        },
        changesBodyEditModel(){
            let self = this;
            if(self.RomeData.bodyRomeData.editModel=='From'){
                self.RomeData.bodyRomeData.editModel='Bulk';
                self.RomeData.bodyRomeData.bulkEdit ='';
                self.RomeData.bodyRomeData.tableData.forEach(item=>{
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
                    self.RomeData.bodyRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.RomeData.bodyRomeData.bulkEdit.split('\n'));

                self.RomeData.bodyRomeData.editModel='From';
                self.RomeData.bodyRomeData.tableData=[];
                self.RomeData.bodyRomeData.index = 0
                let bulkEdit = self.RomeData.bodyRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.RomeData.bodyRomeData.index;
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
                        self.RomeData.bodyRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.RomeData.bodyRomeData.tableData);
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
            self.RomeData.bodyRomeData.deleteFileList.push({
                'dirName':dirName,
                'fileName':fileName
            });
            PrintConsole('deleteFileList',self.RomeData.bodyRomeData.deleteFileList);
        },

        //extractRomeData
        CreateNewExtractData(){
            let self = this;
            let obj = {};
            obj.index = self.RomeData.extractRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.RomeData.extractRomeData.tableData.push(obj);
            self.RomeData.extractRomeData.index+=1;
            PrintConsole('CreateNewExtractData',self.RomeData.extractRomeData.tableData);
        },
        handleExtractDelete(index,row){
            PrintConsole('handleExtractDelete',row);
            let self = this;
            self.RomeData.extractRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.extractRomeData.tableData.forEach((item,i)=>{
                self.RomeData.extractRomeData.tableData[i].index = i;
            });
            self.RomeData.extractRomeData.index -=1 ;
        },

        //validateRomeData
        GetExtractKeyName(){//获取提取中的key值
            let self = this;
            let checkOptions = [];
            self.RomeData.extractRomeData.tableData.forEach(e =>{
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
            obj.index = self.RomeData.validateRomeData.index;
            obj.state = true;
            obj.checkName = '';
            obj.validateType='';
            obj.valueType='';//断言值类型
            obj.expectedResults='';
            obj.remarks='';

            self.RomeData.validateRomeData.tableData.push(obj);
            self.RomeData.validateRomeData.index+=1;
            PrintConsole('CreateNewValidateData',self.RomeData.validateRomeData.tableData);
        },
        handleValidateDelete(index,row){
            PrintConsole('handleValidateDelete',row);
            let self = this;
            self.RomeData.validateRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.validateRomeData.tableData.forEach((item,i)=>{
                self.RomeData.validateRomeData.tableData[i].index = i;
            });
            self.RomeData.validateRomeData.index -=1 ;
        },

        //前置操作
        handlePreOperationCommand(command){
            PrintConsole('handlePreOperationCommand:',command);
            this.CreateNewPreOperationData(command);
        },
        CreateNewPreOperationData(operationType){
            let self = this;
            let obj = {};
            obj.id = self.RomeData.preOperationRomeData.index;
            obj.index = self.RomeData.preOperationRomeData.index;
            obj.state = true;
            obj.operationType = operationType;
            obj.methodsName='';
            obj.dataBase='';
            obj.sql='';

            obj.remarks='';

            self.RomeData.preOperationRomeData.tableData.push(obj);
            self.RomeData.preOperationRomeData.index+=1;
            self.rowDropPreOperation();
            PrintConsole('CreateNewMethodsData',self.RomeData.preOperationRomeData.tableData);
        },
        handlePreOperationDelete(index,row){
            PrintConsole('handlePreOperationDelete',row);
            let self = this;
            self.RomeData.preOperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.preOperationRomeData.tableData.forEach((item,i)=>{
                self.RomeData.preOperationRomeData.tableData[i].index = i;
            });
            self.RomeData.preOperationRomeData.index -=1 ;
        },
        rowDropPreOperation() {//加载可拖动效果
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#PreOperationSort > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.RomeData.preOperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.RomeData.preOperationRomeData.tableData.splice(newIndex, 0, currRow);
                    self.SortPreOperation();
                }
            });
        },
        SortPreOperation(){//调用 每次拖动完成后调用重新排序
            let self = this;
            self.RomeData.preOperationRomeData.tableData.forEach((d,index)=>{
                self.RomeData.preOperationRomeData.tableData[index].rowNum = index;
            });
            PrintConsole('SortPreOperation:重新排序',self.RomeData.preOperationRomeData.tableData);
        },
        getDataBaseOption(){//加载数据库环境的IP及以下可用的库名
            GetConnectBaseItems().then(d=>{
                if(d.statusCode==2000){
                    this.RomeData.preOperationRomeData.dataBaseOptions = d.dataList;
                    this.RomeData.rearOperationRomeData.dataBaseOptions = d.dataList;
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
            obj.id = self.RomeData.rearOperationRomeData.index;
            obj.index = self.RomeData.rearOperationRomeData.index;
            obj.state = true;
            obj.operationType = operationType;
            obj.methodsName='';
            obj.dataBase='';
            obj.sql='';

            obj.remarks='';

            self.RomeData.rearOperationRomeData.tableData.push(obj);
            self.RomeData.rearOperationRomeData.index+=1;
            self.rowDropRearOperation();
            PrintConsole('CreateNewRearOperationData',self.RomeData.rearOperationRomeData.tableData);
        },
        handleRearOperationDelete(index,row){
            PrintConsole('handleRearOperationDelete',row);
            let self = this;
            self.RomeData.rearOperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.RomeData.rearOperationRomeData.tableData.forEach((item,i)=>{
                self.RomeData.rearOperationRomeData.tableData[i].index = i;
            });
            self.RomeData.rearOperationRomeData.index -=1 ;
        },
        rowDropRearOperation() {//加载可拖动效果
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#RearOperationSort > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.RomeData.rearOperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.RomeData.rearOperationRomeData.tableData.splice(newIndex, 0, currRow);
                    self.SortRearOperation();
                }
            });
        },
        SortRearOperation(){//调用 每次拖动完成后调用重新排序
            let self = this;
            self.RomeData.rearOperationRomeData.tableData.forEach((d,index)=>{
                self.RomeData.rearOperationRomeData.tableData[index].rowNum = index;
            });
            PrintConsole('SortRearOperation:重新排序',self.RomeData.rearOperationRomeData.tableData);
        },

        SaveData(){
            let self = this;
            if(self.RomeData.requestUrl==''){
                self.$message.warning('不可保存空请求');
            }else{
                let obj = {}
                obj.id = self.RomeData.id;
                obj.apiId = self.RomeData.apiId;
                obj.requestType = self.RomeData.requestType;
                obj.requestUrl = self.RomeData.requestUrl;
                obj.headers = self.RomeData.headersRomeData.tableData;
                obj.params = self.RomeData.paramsRomeData.tableData;
                obj.body = {
                    'requestSaveType':self.RomeData.bodyRomeData.requestSaveType,
                    'formData':self.RomeData.bodyRomeData.tableData,
                    'rawValue':self.RomeData.bodyRomeData.rawValue,
                    'jsonValue':self.RomeData.bodyRomeData.jsonValue,
                    'deleteFileList':self.RomeData.bodyRomeData.deleteFileList,
                };
                obj.extract = self.RomeData.extractRomeData.tableData;
                obj.validate = self.RomeData.validateRomeData.tableData;
                obj.preOperation = self.RomeData.preOperationRomeData.tableData;
                obj.rearOperation = self.RomeData.rearOperationRomeData.tableData;

                self.$emit('getData',obj);//回调传值
                self.dialogClose();
            }
        },
     
    }
};
</script>

<style>

</style>
