<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="900px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="编写定位信息"></el-step>
                    <el-step title="效验元素参数"></el-step>
                </el-steps>
                <el-card 
                    style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                            <div class="father" style="width: 100%; height: 550px;">
                                <div class="son" style="width:800px; height: 150px;">
                                    <div style="margin-top:20px;">
                                        <el-card shadow="never">
                                            <el-form ref="BaseRomeData" :rules="BaseRomeData.rules" :inline="true" :model="BaseRomeData"  label-width="85px">
                                                <el-form-item label="所属页面:" prop="pageId">
                                                    <el-select v-model="BaseRomeData.pageId" clearable placeholder="请选择" style="float:left" @click.native="GetPageNameOption()">
                                                        <el-option
                                                            v-for="item in BaseRomeData.pageNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="所属功能:" prop="funId">
                                                    <el-select v-model="BaseRomeData.funId" clearable placeholder="请选择" style="float:left" @click.native="GetFunNameOption()">
                                                        <el-option
                                                            v-for="item in BaseRomeData.funNameOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                                <el-form-item label="元素名称:" prop="elementName">
                                                    <el-input style="width:535px" clearable v-model.trim="BaseRomeData.elementName"></el-input>
                                                </el-form-item>
                                                <el-form-item label="元素类型:" prop="elementType">
                                                    <el-cascader
                                                        @click.native="GetElementOperationType()"
                                                        clearable
                                                        v-model="BaseRomeData.elementType"
                                                        :options="BaseRomeData.elementTypeOption"
                                                        style="float:left;">
                                                        <template slot-scope="{ node, data }">
                                                            <span>{{ data.label }}</span>
                                                            <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                                        </template>
                                                    </el-cascader>
                                                </el-form-item>
                                                <el-form-item label="元素状态:" prop="elementState">
                                                    <el-select v-model="BaseRomeData.elementState" placeholder="请选择" style="float:left">
                                                        <el-option
                                                            v-for="item in BaseRomeData.elementStateOption"
                                                            :key="item.value"
                                                            :label="item.label"
                                                            :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                            </el-form>
                                        </el-card>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <el-table
                            :data="LocationRomeData.tableData"
                            height="720px"
                            border>
                            <el-table-column
                                label="启用"
                                width="70px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="定位类型"
                                align= "center"
                                width="120">
                                <template slot-scope="scope">
                                    <el-select
                                        v-model="scope.row.targetingType" clearable placeholder="请选择">
                                        <el-option
                                            v-for="item in LocationRomeData.targetingTypeOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="定位地址"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.targetingPath"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="备注信息"
                                width="250px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.remarks"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="100px">
                                <template slot="header">
                                    <el-button type="primary" @click="AddTable()">新增</el-button>
                                </template>
                                <template slot-scope="scope" style="width:100px">
                                    <el-button
                                        size="mini"
                                        type="danger"
                                        @click="handleDelete(scope.$index, scope.row)">Delete
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
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
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" :disabled="StepsRomeData.saveDisabled" @click="SaveData()">保存</el-button>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetElementOperationTypeItems} from "../../../../../../js/GetSelectTable.js";


export default {
    components: {

    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:2,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
                saveDisabled:false,
            },
            BaseRomeData:{
                elementId:'',
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                elementName:'',
                elementType:'',
                elementTypeOption:[],
                elementState:true,
                elementStateOption:[
                    {'label':'启用','value':true},
                    {'label':'禁用','value':false},
                ],
                rules:{
                    pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                    elementType:[{ required: true, message: '请选择元素类型', trigger: 'change' }],
                    elementName: [
                        { required: true, message: '请输入元素名称', trigger: 'blur' },
                        { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                    ],
                    elementState:[{ required: true, message: '请选择元素状态', trigger: 'change' }],
                },
            },
            LocationRomeData:{
                targetingTypeOption:[
                    {'label':'Id','value':'Id'},
                    {'label':'Name','value':'Name'},
                    {'label':'Css','value':'Css'},
                    {'label':'Text','value':'Text'},
                    {'label':'Xpath','value':'Xpath'},
                    {'label':'坐标','value':'Coordinate'},
                ],
                tableData:[],
            },
            CharmRomeData:{
                title:'',
                tableData:[],
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
                this.ClearBaseRomeData();
                this.ClearLocationRomeData();
                this.ClearCharmRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.BaseRomeData.elementId=newval.elementId;
                    self.LoadData(self.BaseRomeData.elementId);
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
        'BaseRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.BaseRomeData.funId='';
                self.BaseRomeData.funNameOption=[];
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
                this.$refs['BaseRomeData'].validate((valid) => {
                    if (valid) {//通过
                        self.StepsRomeData.active++;
                    } 
                });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
                self.CharmElementData();
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
            self.StepsRomeData.saveDisabled = false;
            self.StepsRomeData.processStatus ='process';
        },
        returnToMain(){
            let self = this;
            self.$emit('closeDialog');
            self.$emit('Succeed');//回调查询   
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        submitForm(formName,id) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveData();
                } 
            });
        },

        //基础信息
        ClearBaseRomeData(){
            let self = this;
            self.resetForm('BaseRomeData');
            self.BaseRomeData.elementId='';
            self.BaseRomeData.pageId='';
            self.BaseRomeData.funId='';
            self.BaseRomeData.elementName='';
            self.BaseRomeData.elementType='';
            self.BaseRomeData.tableData=[];
            self.BaseRomeData.elementState=true;
        },
        GetPageNameOption(){
            GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                this.BaseRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.BaseRomeData.pageId){
                GetFunNameItems('UI',this.$cookies.get('proId'),this.BaseRomeData.pageId).then(d=>{
                    this.BaseRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetElementOperationType(){
            GetElementOperationTypeItems().then(d=>{
                if(d.statusCode==2000){
                    this.BaseRomeData.elementTypeOption = d.dataList;
                }else{
                    self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                }
            });
        },

        //定位信息
        ClearLocationRomeData(){
            let self = this;
            self.LocationRomeData.tableData = [];
        },
        AddTable(){
            let self = this;
            let obj = {};
            obj.state=true;
            obj.targetingType ='';
            obj.targetingPath='';
            obj.remarks='';

            self.LocationRomeData.tableData.push(obj);
        },
        handleDelete(index,row){
            let self = this;
            self.LocationRomeData.tableData.splice(index, 1)//删除列表中的数据
        },

        //验证事件
        ClearCharmRomeData(){
            let self =this;
            self.CharmRomeData.title='';
            self.CharmRomeData.tableData=[];
        },
        CharmElementData(){//验证API接口数据的完整性
            let self = this;
            self.StepsRomeData.saveDisabled = true;
            self.CharmRomeData.tableData = [];
            self.CharmRomeData.title = '';
            self.$axios.post('/api/UiElementMaintenance/CharmElementData',{
                'CharmType':self.isAddNew,
                'baseData':{
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.BaseRomeData.pageId,
                    'funId':self.BaseRomeData.funId,
                    'elementId':self.BaseRomeData.elementId,
                    'elementName':self.BaseRomeData.elementName,
                    'elementType':self.BaseRomeData.elementType,
                },
                'locationData':self.LocationRomeData.tableData
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
                        self.StepsRomeData.saveDisabled = false;
                    }
                }else{
                    self.$message.error('效验元素信息发生错误:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                self.$message.error(error);
            })
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){  
                self.$axios.post('/api/UiElementMaintenance/SaveData',{
                    'baseData':{
                        'proId':self.$cookies.get('proId'),
                        'pageId':self.BaseRomeData.pageId,
                        'funId':self.BaseRomeData.funId,
                        'elementName':self.BaseRomeData.elementName,
                        'elementType':self.BaseRomeData.elementType,
                        'elementState':self.BaseRomeData.elementState,
                    },
                    'elementLocation':self.LocationRomeData.tableData
                }).then(res => {
                    if(res.data.statusCode==2001){
                        self.$message.success('新增元素成功!');
                        self.returnToMain();
                    
                    }else{
                        self.$message.error('新增元素失败'+res.data.errorMsg);
                    }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/UiElementMaintenance/EditData',{
                    'baseData':{
                        'elementId':self.BaseRomeData.elementId,
                        'proId':self.$cookies.get('proId'),
                        'pageId':self.BaseRomeData.pageId,
                        'funId':self.BaseRomeData.funId,
                        'elementName':self.BaseRomeData.elementName,
                        'elementType':self.BaseRomeData.elementType,
                        'elementState':self.BaseRomeData.elementState,
                    },
                    'elementLocation':self.LocationRomeData.tableData
                }).then(res => {
                    if(res.data.statusCode==2002){
                        self.$message.success('修改元素成功!');
                        self.returnToMain();
                    }else{
                        self.$message.error('修改元素败'+res.data.errorMsg);
                    }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        LoadData(elementId){
            let self = this;
            self.loading=true;
            self.$axios.get('/api/UiElementMaintenance/LoadData',{
                params:{
                  'elementId':elementId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                        self.BaseRomeData.pageNameOption = d;
                        self.BaseRomeData.pageId=res.data.baseData.pageId;
                        GetFunNameItems('UI',this.$cookies.get('proId'),this.BaseRomeData.pageId).then(d=>{
                            self.BaseRomeData.funNameOption = d;
                            self.BaseRomeData.funId=res.data.baseData.funId;
                            GetElementOperationTypeItems().then(d=>{
                                if(d.statusCode==2000){
                                    self.BaseRomeData.elementTypeOption = d.dataList;

                                    self.BaseRomeData.elementName=res.data.baseData.elementName;
                                    self.BaseRomeData.elementType=res.data.baseData.elementType;
                                    self.LocationRomeData.tableData = res.data.locationTable;
                                    self.loading=false;
                                }else{
                                    self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                                }
                            });
                        });
                    });
                }else{
                    self.loading=false;
                    self.$message.error('数据加载失败:'+res.data.errorMsg);
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
</style>
