<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1920px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :close-on-press-escape="false"
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写测试集"></el-step>
                    <el-step title="编写操作集"></el-step>
                    <el-step title="效验用例参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                            <div class="father" style="width: 100%; height: 650px;">
                                <div class="son" style="width: 950px; height: 200px;">
                                    <!-- <el-card style="width:1000px" shadow="never"> -->
                                    <div style="width:1000px">
                                        <el-form ref="BasicRomeData" :inline="true" :rules="BasicRomeData.rules" :model="BasicRomeData"  label-width="100px">
                                            <el-form-item prop="pageId" label="所属页面:">
                                                <el-select v-model="BasicRomeData.pageId" 
                                                clearable 
                                                placeholder="请选择" 
                                                style="width:200px;float:left;" 
                                                @click.native="GetPageNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.pageNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="funId" label="所属功能:">
                                                <el-select v-model="BasicRomeData.funId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetFunNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.funNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="environmentId" label="页面环境:">
                                                <el-select v-model="BasicRomeData.environmentId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageEnvironmentNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.environmentNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="testType" label="测试类型:">
                                                <el-select v-model="BasicRomeData.testType" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.testTypeOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="labelId" label="用例标签:">
                                                <el-select v-model="BasicRomeData.labelId" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.labelNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="priorityId" label="优先级:">
                                                <el-select v-model="BasicRomeData.priorityId" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.priorityNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                        <span style="float: left">{{ item.label }}</span>
                                                        <span style="float: right; color: #8492a6; font-size: 13px">{{ item.details }}</span>
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="caseName" label="用例名称:">
                                                <el-input v-model.trim="BasicRomeData.caseName" style="width:510px;"></el-input>
                                            </el-form-item>
                                            <el-form-item prop="caseState" label="用例状态:">
                                                <el-select v-model="BasicRomeData.caseState" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.caseStateOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item label="关联页面:">
                                                <el-select 
                                                @click.native="GetAssociatedPageNameOption()"
                                                style="width:825px"
                                                v-model="BasicRomeData.associatedPage" 
                                                multiple 
                                                placeholder="如需要在选择元素中找到别的所属页面元素,可在此选择关联相对应页面">
                                                    <el-option
                                                        v-for="item in BasicRomeData.associatedPageoOptions"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                               <!-- <el-cascader 
                                               @click.native="GetAssociatedPageNameOption()"
                                               style="width:825px"
                                               placeholder="如需要在选择元素中找到别的所属页面元素,可在此选择关联相对应页面"
                                               :options="BasicRomeData.associatedPage" :props="BasicRomeData.associatedProps" clearable></el-cascader> -->
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <div>
                            <el-table
                                ref="TestSetTableData"
                                id="TestSet" 
                                row-key="id"
                                :data="TestSetRomeData.tableData"
                                :row-class-name="tableRowClassName"
                                height="720px"
                                border>
                                <el-table-column
                                    label="序列"  
                                    type="index" 
                                    width="60" 
                                    align="center">
                                </el-table-column>
                                <el-table-column
                                    label="启用"
                                    width="70px"
                                    align= "center">
                                    <template slot-scope="scope">
                                        <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="事件名称"
                                    width="300px" 
                                    align= "center"
                                    prop="eventName">
                                </el-table-column>
                                <el-table-column
                                    label="操作类型"
                                    align= "center"
                                    width="140" 
                                    prop="elementTypeTxt">
                                </el-table-column>
                                <el-table-column
                                    label="图片对比类型"
                                    align= "center"
                                    width="140" 
                                    prop="contrastTypeText">
                                </el-table-column>
                                <el-table-column
                                    label="输入/选择"
                                    width="400px" 
                                    show-overflow-tooltip
                                    align= "center"
                                    prop="inputData">
                                </el-table-column>
                                <el-table-column
                                    label="元素动态"
                                    width="100px"
                                    align= "center">
                                    <template slot-scope="scope">
                                        <el-tag type="success" v-if="scope.row.elementDynamic==0">无更变</el-tag>
                                        <el-link type="danger" v-else-if="scope.row.elementDynamic==1" @click="OpenLifeCycleDialog(scope.row)">已更变</el-link>
                                        <el-tag type="warning" v-else-if="scope.row.elementDynamic==2">已知晓</el-tag>
                                        <el-tag type="info" v-else>无元素</el-tag>
                                    </template>
                                </el-table-column> 
                                <el-table-column label="断言操作"
                                    align= "center">
                                    <el-table-column
                                        label="断言类型"
                                        align= "center"
                                        width="120"
                                        prop="assertType">
                                    </el-table-column>
                                    <el-table-column
                                        label="断言值类型"
                                        width="120"
                                        align= "center"
                                        prop="assertValueType">
                                    </el-table-column>
                                    <el-table-column
                                        label="断言值"
                                        width="200"
                                        align= "center"
                                        prop="assertValue">
                                    </el-table-column>
                                </el-table-column>
                                <el-table-column 
                                    fixed="right"
                                    width="210" 
                                    align= "center">
                                    <template slot="header">
                                        <el-button-group>
                                            <el-button type="primary" @click="openAddCaseStepsDialog()">新增步骤</el-button>
                                            <el-dropdown @command="handleCommand">
                                                <el-button type="warning">
                                                    更多<i class="el-icon-arrow-down el-icon--right"></i>
                                                </el-button>
                                                <el-dropdown-menu slot="dropdown">
                                                    <el-dropdown-item command="AllEnable">全部启用</el-dropdown-item>
                                                    <el-dropdown-item command="AllDisable">全部禁用</el-dropdown-item>
                                                </el-dropdown-menu>
                                            </el-dropdown>
                                        </el-button-group>
                                    </template>
                                    <template slot-scope="scope">
                                        <el-button-group>
                                            <el-button
                                                size="mini"
                                                @click="openEditCaseStepsDialog(scope.$index, scope.row)">编辑</el-button>
                                            <el-button
                                                size="mini"
                                                type="danger"
                                                @click="handleTestSetDelete(scope.$index, scope.row)">删除</el-button>
                                        </el-button-group>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==2">
                        <div style="width:1300px;margin-left:300px">
                            <el-table
                                ref="OperationSetTableData"
                                id="OperationSet" 
                                row-key="id"
                                :data="OperationSetRomeData.tableData"
                                height="720px"
                                border>
                                <el-table-column
                                    label="序列"  
                                    type="index" 
                                    width="60" 
                                    align="center">
                                </el-table-column>
                                <el-table-column
                                    label="启用"
                                    width="70px"
                                    align= "center">
                                    <template slot-scope="scope">
                                        <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="操作位置"
                                    width="200px" 
                                    align= "center"
                                    prop="location">
                                    <template slot-scope="scope">
                                        <el-tag type="success" v-if="scope.row.location=='Pre'">前置操作</el-tag>
                                        <el-tag type="danger" v-else>后置操作</el-tag>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="操作类型"
                                    width="200px" 
                                    align= "center"
                                    prop="operationType">
                                </el-table-column>
                                <el-table-column
                                    label="操作数据"
                                    align= "center"
                                    prop="operationData">
                                </el-table-column>
                                <el-table-column
                                    label="备注"
                                    align= "center"
                                    width="300px" 
                                    prop="remarks">
                                </el-table-column>
                                <el-table-column 
                                    width="140px" 
                                    align= "center">
                                    <template slot="header">
                                        <el-button type="primary" @click="openAddOperationStepsDialog()">新增操作</el-button>
                                    </template>
                                    <template slot-scope="scope">
                                        <el-button-group>
                                            <el-button
                                                size="mini"
                                                @click="openEditOperationStepsDialog(scope.$index, scope.row)">编辑</el-button>
                                            <el-button
                                                size="mini"
                                                type="danger"
                                                @click="handleOperationStepsDelete(scope.$index, scope.row)">删除</el-button>
                                        </el-button-group>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </template>
                    <template v-else>
                        <div slot="header">
                            {{CharmRomeData.title}}
                        </div>
                        <div>
                            <el-table
                            v-loading="CharmRomeData.loading"
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
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" :loading="StepsRomeData.saveLoading" @click="SaveData()">保存</el-button>
            </el-drawer>
        </template>
        <template>
            <dialog-case-steps
                @closeDialog="closeCaseStepsDialog" 
                :isVisible="dialog.caseSteps.dialogVisible" 
                :dialogPara="dialog.caseSteps.dialogPara"
                @geAddtData="AddToTestStepsTable($event)"
                @geEditData="EditToTestStepsTable($event)"
                >
            </dialog-case-steps>
        </template>
        <template>
            <dialog-operation-steps
                @closeDialog="closeOperationStepsDialog" 
                :isVisible="dialog.operationSteps.dialogVisible" 
                :dialogPara="dialog.operationSteps.dialogPara"
                @geAddtData="AddToOperationStepsTable($event)"
                @geEditData="EditToOperationStepsTable($event)"
                >
            </dialog-operation-steps>
        </template>
        <template> 
            <dialog-life-cycle
                @closeDialog="closeLifeCycleDialog" 
                :isVisible="dialog.lifeCycle.dialogVisible" 
                :dialogPara="dialog.lifeCycle.dialogPara">
            </dialog-life-cycle>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import Sortable from 'sortablejs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetAssociatedPageNameItems} from "../../../../../../js/GetSelectTable.js";

import DialogCaseSteps from "./CaseSteps.vue";
import DialogOperationSteps from "./OperationSteps.vue";
import DialogLifeCycle from "../ElementMaintenance/LifeCycle.vue";


export default {
    components: {
        DialogCaseSteps,DialogOperationSteps,DialogLifeCycle
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:4,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
                saveLoading:true,
            },
            BasicRomeData:{//基本信息
                caseId:'',
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                environmentId:'',
                environmentNameOption:[],
                testType:'',
                testTypeOption:[
                    {'label':'功能测试','value':'Function'},
                    {'label':'冒烟测试','value':'Smoke'},
                ],
                labelId:'',
                labelNameOption:[
                    {'label':'普通用例','value':'CommonCase'},
                    {'label':'回归用例','value':'ReturnCase'},
                ],
                priorityId:'',//优先级
                priorityNameOption:[
                    {'label':'P0','value':'P0','details':'最高'},
                    {'label':'P1','value':'P1','details':'高'},
                    {'label':'P2','value':'P2','details':'中'},
                    {'label':'P3','value':'P3','details':'低'},
                ],
                caseState:'',
                caseStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                caseName:'',
                associatedPage:[],//关联页面
                associatedPageoOptions:[],
                // associatedProps: { multiple: true },
                rules:{
                    pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                    environmentId:[{ required: true, message: '请选择页面环境', trigger: 'change' }],
                    testType:[{ required: true, message: '请选择测试类型', trigger: 'change' }],
                    labelId:[{ required: true, message: '请选择用例标签', trigger: 'change' }],
                    priorityId:[{ required: true, message: '请选择优先级', trigger: 'change' }],
                    caseName:[
                        { required: true, message: '请输入用例名称', trigger: 'blur' },
                        { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
                    ],
                    caseState:[{ required: true, message: '请选择用例状态', trigger: 'change' }],
                },
            },
            TestSetRomeData:{//测试集
                tableData:[],
            },
            OperationSetRomeData:{//操作集
                tableData:[],
            },
            CharmRomeData:{
                loading:false,
                title:'',
                tableData:[],
            },
            dialog:{
                caseSteps:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                operationSteps:{
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
                }
            },
        };
    },
    mounted(){

    },
    computed:{//计算属性

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
                this.ClearTestSetRomeData();
                this.ClearCharmRomeData();
                this.ClearOperationStepsRomeData();
                
                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                    this.BasicRomeData.caseId = newval.caseId;
                    this.LoadCaseData(this.BasicRomeData.caseId);
                  
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听所属项目有变化
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
            }else if(newVal==1){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Next = true;
            }else if(newVal==2){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Next = true;
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
                //每次切换所属页面的时候看下关联页面列表中有没有存在当前的，如果有就把关联页面中当前的给去掉
                self.BasicRomeData.associatedPage.forEach((item,index) =>{
                    if(item==newVal){
                        self.BasicRomeData.associatedPage.splice(index,1)
                    }
                });

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
            if(self.StepsRomeData.active==0){//基本用例数据
                // self.StepsRomeData.active++;
                // self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                //     self.TestSetRowDrop();
                // })
                this.$refs['BasicRomeData'].validate((valid) => {
                    if (valid) {//通过
                        self.StepsRomeData.active++;
                        self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                            self.TestSetRowDrop();
                        })
                    } 
                });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
                self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                    self.OperationStepsRowDrop();
                })
            }else if(self.StepsRomeData.active==2){
                self.StepsRomeData.active++;
                self.CharmCaseData();
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else if(self.StepsRomeData.active==2){
                self.StepsRomeData.active--;
                self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                    self.TestSetRowDrop();
                })
            }else if(self.StepsRomeData.active==4){
                self.StepsRomeData.active--;
                self.StepsRomeData.active--;
            }
            else{
                self.StepsRomeData.active--;
            }
            // PrintConsole('步骤',self.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
            // self.resetForm('RomeData');
            self.StepsRomeData.active= 0;
            self.StepsRomeData.disPlay_Save = false;
            self.StepsRomeData.disPlay_Next = true;
            self.StepsRomeData.processStatus ='process';
            self.StepsRomeData.saveLoading = true;
        },
        returnToMain(){
            let self = this;
            self.dialogVisible = false;//关闭新增弹窗
            self.$emit('closeDialog');
            self.$emit('Succeed');//回调查询   
        },

        //基础信息
        ClearBasicRomeData(){
            let self = this;
            self.resetForm('BasicRomeData');
            self.BasicRomeData.pageId='';
            self.BasicRomeData.funId='';
            self.BasicRomeData.environmentId='';
            self.BasicRomeData.testType='';
            self.BasicRomeData.labelId='';
            self.BasicRomeData.priorityId='';
            self.BasicRomeData.caseState='';
            self.BasicRomeData.caseName='';
            self.BasicRomeData.associatedPage=[];
        },
        GetPageNameOption(){
            GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            this.BasicRomeData.funNameOption = [];
            if(this.BasicRomeData.pageId){
                GetFunNameItems('UI',this.$cookies.get('proId'),this.BasicRomeData.pageId).then(d=>{
                    this.BasicRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetAssociatedPageNameOption(){//关联页面
            if(this.BasicRomeData.pageId){
                GetAssociatedPageNameItems('UI',this.BasicRomeData.pageId).then(d=>{
                    if(d.statusCode==2000){
                        this.BasicRomeData.associatedPageoOptions = d.dataList;
                    }else{
                        self.$message.error('关联页面数据获取失败:'+d.errorMsg);
                    }
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
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                PrintConsole('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },

        //测试集
        ClearTestSetRomeData(){
            let self = this;
            self.TestSetRomeData.tableData=[];
        },
        handleCommand(command){
            PrintConsole(command);
            if(command=='AllEnable'){
                this.updateStepsTableState(true);
            }else if(command=='AllDisable'){
                this.updateStepsTableState(false);
            }
        },
        tableRowClassName({row, rowIndex}) {//禁用时 当前行显示为高亮
            if (row.state === false) {
                return 'warning-row';
            }
            return '';
        },
        closeCaseStepsDialog(){
            this.dialog.caseSteps.dialogVisible =false;
        },
        openAddCaseStepsDialog(){//打开新增
            let self = this;
            let pageNameList = [];
            if(self.BasicRomeData.pageId){
                pageNameList.push(self.BasicRomeData.pageId);
            }
            self.BasicRomeData.associatedPage.forEach(d=>{
                pageNameList.push(d);
            });
            
            self.dialog.caseSteps.dialogPara={
                dialogTitle:"新增步骤",//初始化标题
                isAddNew:true,//初始化是否新增\修改
                id:self.TestSetRomeData.tableData.length+1,
                pageNameList:pageNameList.join(',')
            }
            self.dialog.caseSteps.dialogVisible=true;
        },
        openEditCaseStepsDialog(index,row){//打开编辑
            let self = this;
            let pageNameList = [];
            if(self.BasicRomeData.pageId){
                pageNameList.push(self.BasicRomeData.pageId);
            }
            self.BasicRomeData.associatedPage.forEach(d=>{
                pageNameList.push(d);
            });

            self.dialog.caseSteps.dialogPara={
                dialogTitle:"编辑步骤",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                id:row.id,
                pageNameList:pageNameList.join(','),

                state:row.state,
                eventName:row.eventName,
                elementId:row.elementId,
                elementType:row.elementType,
                inputData:row.inputData,
                elementDynamic:row.elementDynamic,
                assertType:row.assertType,
                assertValueType:row.assertValueType,
                assertValue:row.assertValue,
            }
            self.dialog.caseSteps.dialogVisible=true;
        },
        handleTestSetDelete(index,row){//删除数据
            this.$confirm('请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.TestSetRomeData.tableData.splice(index,1);
                }).catch(() => {       
            });
        },
        AddToTestStepsTable(val){//添加步骤数据到列表中-回调传值
            PrintConsole('回调-AddToTestStepsTable',val);
            let self = this;
            self.TestSetRomeData.tableData.push(val);
          
            self.TestSetRowDrop();
        },
        EditToTestStepsTable(val){//修改步骤数据到列表中-回调传值
            PrintConsole('回调-EditToTestStepsTable',val);
            let self = this;
            let tempSetTable = self.TestSetRomeData.tableData.find(item=>
                item.id == val.id
            );
            if(tempSetTable){
                tempSetTable.eventName=val.eventName;
                tempSetTable.elementId=val.elementId;
                tempSetTable.elementType=val.elementType;
                tempSetTable.elementTypeTxt=val.elementTypeTxt;
                
                tempSetTable.inputData=val.inputData;
                tempSetTable.elementDynamic=val.elementDynamic;
                tempSetTable.assertType=val.assertType;
                tempSetTable.assertValueType=val.assertValueType;
                tempSetTable.assertValue=val.assertValue;

            }
            self.TestSetRowDrop();
        },
        TestSetRowDrop() {//排序方法
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#TestSet > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.TestSetRomeData.tableData.splice(oldIndex, 1)[0];
                    self.TestSetRomeData.tableData.splice(newIndex, 0, currRow);
                    // console.log(self.RomeData.TableData);
                }
            });
        },
        updateStepsTableState(state){//全部启用或禁用
            let self = this;
            self.TestSetRomeData.tableData.forEach((d,i)=>{
                self.TestSetRomeData.tableData[i].state=state;
            });
        },
        OpenLifeCycleDialog(row){//打开接口生命周期
            let self = this;
            self.dialog.lifeCycle.dialogPara={
                dialogTitle:row.elementName+'(生命周期)',//初始化标题
                elementId:row.elementId,
            }
            self.dialog.lifeCycle.dialogVisible=true;
        },
        closeLifeCycleDialog(){
            this.dialog.lifeCycle.dialogVisible =false;
        },

        //操作集
        ClearOperationStepsRomeData(){
            let self = this;
            self.OperationSetRomeData.tableData = [];
        },
        AddToOperationStepsTable(val){
            PrintConsole('回调-AddToOperationStepsTable',val);
            let self = this;
            val.state = true;
            if(val.operationType=="TestCase"){
                val.operationData = val.caseName;
            }else if(val.operationType=="Methods"){
                val.operationData = val.methodsName;
            }else if(val.operationType=="DataBase"){
                val.operationData = val.dataBaseName;
            }
            self.OperationSetRomeData.tableData.push(val)
            self.OperationStepsRowDrop();
        },
        EditToOperationStepsTable(val){
            PrintConsole('回调-EditToOperationStepsTable',val);
            let tempData = this.OperationSetRomeData.tableData.find(item=>
                item.id == val.id
            );
            if(tempData){
                tempData.location=val.location;
                tempData.operationType=val.operationType;
                tempData.methodsName=val.methodsName;
                tempData.caseId=val.caseId;
                tempData.dataBaseId=val.dataBaseId;
                tempData.sql=val.sql;

                if(val.operationType=="TestCase"){
                    tempData.operationData = val.caseName;
                }else if(val.operationType=="Methods"){
                    tempData.operationData = val.methodsName;
                }else if(val.operationType=="DataBase"){
                    tempData.operationData = val.dataBaseName;
                }
                tempData.remarks=val.remarks;
            }
            this.OperationStepsRowDrop();
        },
        closeOperationStepsDialog(){
            this.dialog.operationSteps.dialogVisible =false;
        },
        openAddOperationStepsDialog(){
            let self = this; 
            let pageNameList = [];
            if(self.BasicRomeData.pageId){
                pageNameList.push(self.BasicRomeData.pageId);
            }
            self.BasicRomeData.associatedPage.forEach(d=>{
                pageNameList.push(d);
            });
            self.dialog.operationSteps.dialogPara={
                dialogTitle:"新增操作",//初始化标题
                isAddNew:true,//初始化是否新增\修改
                currentCaseId:self.BasicRomeData.caseId,
                id:self.OperationSetRomeData.tableData.length+1,
                pageNameList:pageNameList.join(',')
            }
            self.dialog.operationSteps.dialogVisible=true;
        },
        openEditOperationStepsDialog(index,row){
            let self = this; 
            let pageNameList = [];
            if(self.BasicRomeData.pageId){
                pageNameList.push(self.BasicRomeData.pageId);
            }
            self.BasicRomeData.associatedPage.forEach(d=>{
                pageNameList.push(d);
            });
            self.dialog.operationSteps.dialogPara={
                dialogTitle:"编辑操作",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                currentCaseId:self.BasicRomeData.caseId,
                id:row.id,
                location:row.location,
                operationType:row.operationType,
                caseId:row.caseId,
                methodsName:row.methodsName,
                dataBaseId:row.dataBaseId,
                sql:row.sql,
                remarks:row.remarks,
                pageNameList:pageNameList.join(','),
            }
            self.dialog.operationSteps.dialogVisible=true;
        },
        handleOperationStepsDelete(index,row){
              this.$confirm('请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.OperationSetRomeData.tableData.splice(index,1);
                }).catch(() => {       
            });
        },
        OperationStepsRowDrop() {//排序方法
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#OperationSet > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.OperationSetRomeData.tableData.splice(oldIndex, 1)[0];
                    self.OperationSetRomeData.tableData.splice(newIndex, 0, currRow);
                    // console.log(self.RomeData.TableData);
                }
            });
        },


        //效验和保存加载
        ClearCharmRomeData(){
            let self =this;
            self.CharmRomeData.title='';
            self.CharmRomeData.tableData=[];
        },
        CharmCaseData(){//验证
            let self = this;
            self.CharmRomeData.tableData = [];
            self.CharmRomeData.title = '';
            self.CharmRomeData.loading=true;
            self.StepsRomeData.saveLoading = true;
            self.$axios.post('/api/UiCaseMaintenance/CharmCaseData',{
                'CharmType':self.isAddNew,
                'BasicData':{
                    'proId':self.$cookies.get('proId'),
                    'caseId':self.BasicRomeData.caseId,
                    'pageId':self.BasicRomeData.pageId,
                    'funId':self.BasicRomeData.funId,
                    'environmentId':self.BasicRomeData.environmentId,
                    'testType':self.BasicRomeData.testType,
                    'labelId':self.BasicRomeData.labelId,
                    'caseName':self.BasicRomeData.caseName,
                },
                'TestSet':self.TestSetRomeData.tableData,
                'OperationSet':self.OperationSetRomeData.tableData

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
                        self.StepsRomeData.saveLoading=false;
                    }
                    self.CharmRomeData.loading=false;
                }else{
                    self.$message.error('效验用例信息发生错误:'+res.data.errorMsg);
                    self.CharmRomeData.title='效验用例信息发生错误:'+res.data.errorMsg;
                    self.StepsRomeData.processStatus='error';
                    self.CharmRomeData.loading=false;
                }
            }).catch(function (error) {
                console.log(error);
                self.CharmRomeData.title=error;
                self.StepsRomeData.processStatus='error';
                self.CharmRomeData.loading=false;
            })
        },

        SaveData(){//保存接口
            let self = this;
            if(self.CharmRomeData.tableData.length==0){
                if(self.isAddNew){  
                    self.$axios.post('/api/UiCaseMaintenance/SaveData',{
                        'BasicData':{
                            'proId':self.$cookies.get('proId'),
                            'pageId':self.BasicRomeData.pageId,
                            'funId':self.BasicRomeData.funId,
                            'environmentId':self.BasicRomeData.environmentId,
                            'testType':self.BasicRomeData.testType,
                            'labelId':self.BasicRomeData.labelId,
                            'priorityId':self.BasicRomeData.priorityId,
                            'caseName':self.BasicRomeData.caseName,
                            'caseState':self.BasicRomeData.caseState,
                            'associatedPage':self.BasicRomeData.associatedPage,
                        },
                        'TestSet':self.TestSetRomeData.tableData,
                        'OperationSet':self.OperationSetRomeData.tableData
                    }).then(res => {
                        if(res.data.statusCode==2001){
                            self.$message.success('新增用例成功!');
                            self.returnToMain();
                        
                        }else{
                            self.$message.error('保存失败'+res.data.errorMsg);
                        }
                    }).catch(function (error) {
                        console.log(error);
                    })
                }else{
                    self.$axios.post('/api/UiCaseMaintenance/EditData',{
                        'BasicData':{
                            'caseId':self.BasicRomeData.caseId,
                            'proId':self.$cookies.get('proId'),
                            'pageId':self.BasicRomeData.pageId,
                            'funId':self.BasicRomeData.funId,
                            'environmentId':self.BasicRomeData.environmentId,
                            'testType':self.BasicRomeData.testType,
                            'labelId':self.BasicRomeData.labelId,
                            'priorityId':self.BasicRomeData.priorityId,
                            'caseName':self.BasicRomeData.caseName,
                            'caseState':self.BasicRomeData.caseState,
                            'associatedPage':self.BasicRomeData.associatedPage,
                        },
                        'TestSet':self.TestSetRomeData.tableData,
                        'OperationSet':self.OperationSetRomeData.tableData
                    }).then(res => {
                        if(res.data.statusCode==2002){
                            self.$message.success('修改用例成功!');
                            self.returnToMain();
                        
                        }else{
                            self.$message.error('修改用例失败'+res.data.errorMsg);
                        }
                    }).catch(function (error) {
                        console.log(error);
                    })
                }
            }else{
                self.$message.warning('请先修改错误数据后,在进行保存!');
            }
        },
        LoadCaseData(caseId){
            let self = this;
            self.loading=true;
            self.$axios.get('/api/UiCaseMaintenance/LoadCaseData',{
                params:{
                    'caseId':caseId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                        self.BasicRomeData.pageNameOption = d;
                        self.BasicRomeData.pageId = res.data.basicData.pageId;
                        GetFunNameItems('UI',this.$cookies.get('proId'),this.BasicRomeData.pageId).then(d=>{
                            self.BasicRomeData.funNameOption = d;
                            self.BasicRomeData.funId = res.data.basicData.funId;
                            GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(d=>{
                                self.BasicRomeData.environmentNameOption = d;
                                self.BasicRomeData.environmentId = res.data.basicData.environmentId;
                                GetAssociatedPageNameItems('UI',this.BasicRomeData.pageId).then(d=>{
                                    if(d.statusCode==2000){
                                        self.BasicRomeData.associatedPageoOptions = d.dataList;
                                        self.BasicRomeData.associatedPage = res.data.basicData.associatedPage;

                                        self.BasicRomeData.testType = res.data.basicData.testType;
                                        self.BasicRomeData.labelId = res.data.basicData.labelId;
                                        self.BasicRomeData.priorityId = res.data.basicData.priorityId;
                                        self.BasicRomeData.caseName = res.data.basicData.caseName;
                                        self.BasicRomeData.caseState = res.data.basicData.caseState;

                                        self.TestSetRomeData.tableData = res.data.testSet;
                                        self.OperationSetRomeData.tableData = res.data.operationSet;


                                        self.loading=false;
                                    }else{
                                        self.$message.error('关联页面数据获取失败:'+d.errorMsg);
                                    }
                                });
                            });
                        });
                    });
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                    self.dialogClose();
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
                self.dialogClose();
            })
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

.el-table .warning-row {
    background: oldlace;
}
</style>
