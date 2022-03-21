<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
            <div
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading">
                <el-divider content-position="center">事件操作</el-divider>
                <div>
                    <el-form ref="RomeData" :model="RomeData" :rules="RomeData.rules" label-width="100px">
                        <el-form-item label="事件名称:"  prop="eventName">
                            <el-input v-model="RomeData.eventName" clearable placeholder="请输入事件名称,为空时取元素名称" style="width:300px;float:left"></el-input>
                        </el-form-item>
                        <!-- <el-form-item label="用例标签:">
                            <el-select v-model="RomeData.caselabelId" clearable multiple placeholder="请选择" style="width:300px;float:left" @click.native="GetCaseLabelNameOption()">
                                <el-option
                                v-for="item in tRomeData.caselabeNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item> -->
                        <div v-if="DisPlay.element">
                            <el-divider content-position="center">元素操作</el-divider>
                            <el-form-item label="选择元素:">
                                <el-select 
                                    v-model="RomeData.elementId" 
                                    filterable clearable placeholder="请选择" 
                                    style="width:300px;float:left" 
                                    @click.native="GeElementNameOption()">
                                    <el-option-group
                                        v-for="group in RomeData.elementNameOption"
                                        :key="group.label"
                                        :label="group.label">
                                        <el-option
                                            v-for="item in group.options"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-option-group>
                                </el-select>
                            </el-form-item>
                        </div>
                        <el-form-item label="元素类型:" prop="elementType">
                            <el-cascader
                                @click.native="GetElementOperationType()"
                                clearable
                                v-model="RomeData.elementType"
                                :options="RomeData.elementTypeOptions"
                                style="width:300px;float:left">
                                <template slot-scope="{ node, data }">
                                    <span>{{ data.label }}</span>
                                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                </template>
                            </el-cascader>
                        </el-form-item>
                        <div v-if="DisPlay.inputData">
                            <el-form-item label="输入/选择:">
                                <div v-if="RomeData.elementType[1]=='Upload'">
                                    <!-- <el-upload 
                                        :headers="headers"
                                        :action="RomeData.uploadToTemp"
                                        :on-success="upload_success"
                                        :on-remove="upload_remove"
                                        :limit="1"
                                        :file-list="RomeData.fileList">
                                        <el-button size="small" type="primary">点击上传</el-button>
                                    </el-upload> -->
                                </div>
                                <div v-else>
                                    <el-input v-model="RomeData.inputData" clearable style="width:300px;float:left"></el-input>
                                </div>
                            </el-form-item>
                        </div>
                        <div v-if="DisPlay.assert">
                            <el-divider content-position="center">断言操作</el-divider>
                            <el-form-item label="断言类型:">
                                <el-select v-model="RomeData.assertType" placeholder="请选择" style="width:300px;float:left">
                                    <el-option
                                    v-for="item in RomeData.assertTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="断言值类型:">
                                <el-select v-model="RomeData.assertValueType" placeholder="请选择" style="width:300px;float:left">
                                    <el-option
                                        v-for="item in RomeData.assertValueTypeOption"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="断言值:">
                                <el-input v-model="RomeData.assertValue" clearable placeholder="请输入断言值" style="width:300px;float:left"></el-input>
                            </el-form-item>
                        </div>
                        <div v-if="DisPlay.imageOperation">
                            <el-divider >图片操作</el-divider>
                            <!-- <el-form-item label="选择图片:" prop="pictureContrast">
                                <el-cascader
                                    style="width:300px"
                                    :props="{ multiple: true }"
                                    clearable
                                    v-model="RomeData.pictureContrast" placeholder="请选择"
                                    :options="RomeData.pictureContrastNameOption"
                                    @click.native="LoadContrastImgList()"
                                    @change="handleChange_pictureContrast">
                                    <template slot-scope="{ node, data }">
                                        <span>{{ data.label }}</span>
                                        <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                    </template>
                                </el-cascader>
                            </el-form-item>
                            <el-form-item label="对比类型:" prop="contrastTypeId" v-if="RomeData.disPlay.contrastType">
                                <el-select 
                                v-model="RomeData.contrastTypeId"  
                                placeholder="请选择" 
                                @click.native="LoadContrastType()"
                                style="width:300px;float:left">
                                    <el-option
                                        v-for="item in RomeData.contrastTypeNameOption"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item> -->
                        </div>
                    </el-form>
                </div>
                <div>
                    <el-button type="success" @click="AddToStepsTable()" v-if="isAddNew">保存</el-button>
                    <el-button type="warning" @click="AddToStepsTable()" v-else>修改</el-button>
                    <el-button @click="ClearRomeData('reset')">重置</el-button>
                </div>
                <el-divider >操作提示</el-divider>
                <div class="operationTips">
                    <div 
                    v-for="item in RomeData.operationTips"
                    :key="item"
                    >{{item}}</div>
                </div>
            </div>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetElementOperationTypeItems} from "../../../../../../js/GetSelectTable.js";
import {GeElementNameItems} from "../../../../../../js/GetSelectTable.js";

export default {
    components: {

    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            RomeData:{
                id:'',
                state:true,
                pageNameList:[],
                eventName:'',
                elementId:'',//选择元素
                elementNameOption:[],
                elementType:'',//元素操作类型
                elementTypeOptions:[],
                inputData:'',
                elementDynamic:'',//元素动态
                assertType:'',//断言类型
                assertTypeOption:[
                    {'label':'等于(Equals)','value':'Equals'},
                    {'label':'不等于(NotEquals)','value':'NotEquals'},
                    {'label':'包含(Contains)','value':'Contains'},
                ],
                assertValueType:'',//断言值类型
                assertValueTypeOption:[
                    {'label':'Str','value':'Str'},
                    {'label':'List','value':'List'},
                    {'label':'Dict','value':'Dict'},
                    {'label':'Int','value':'Int'},
                    {'label':'Float','value':'Float'},
                ],
                assertValue:'',//断言值
                operationTips:[],
                rules:{
                    eventName:[
                        { required: true, message: '请输入事件名称', trigger: 'blur' },
                        { min: 1, max: 25, message: '长度在 1 到 25 个字符', trigger: 'blur' }
                    ],
                    // elementId:[{ required: true, message: '请选择元素', trigger: 'change' }],
                    elementType:[{ required: true, message: '请选择元素操作类型', trigger: 'change' }],
                    // assertType:[{ required: true, message: '请选择断言类型', trigger: 'change' }],
                    // assertValueType:[{ required: true, message: '请选择断言值类型', trigger: 'change' }],
                },
            },
            DisPlay:{
                element:true,
                inputData:false,
                assert:false,
                imageOperation:false,
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
                this.ClearRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.RomeData.id = newval.id;
                this.isAddNew = newval.isAddNew;
                this.RomeData.pageNameList = newval.pageNameList;
               

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    GeElementNameItems(self.RomeData.pageNameList).then(d=>{
                        if(d.statusCode==2000){
                            self.RomeData.elementNameOption = d.dataList;
                            GetElementOperationTypeItems().then(d=>{
                                if(d.statusCode==2000){
                                    self.RomeData.elementTypeOptions = d.dataList;
                                    
                                    self.RomeData.state=newval.state;
                                    self.RomeData.eventName=newval.eventName;
                                    self.RomeData.elementId=newval.elementId;
                                    self.RomeData.elementType=newval.elementType;
                                    self.DisPlayControls(self.RomeData.elementType[1]);
                                    self.RomeData.inputData=newval.inputData;
                                    self.RomeData.elementDynamic=newval.elementDynamic;
                                    self.RomeData.assertType=newval.assertType;
                                    self.RomeData.assertValueType=newval.assertValueType;
                                    self.RomeData.assertValue=newval.assertValue;
                                }else{
                                    self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                                }
                            });
                        }else{
                            self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                        }
                    });
                }else{
                    this.GetElementOperationType();
                }
            }
        },
        'RomeData.elementId': function (newVal,oldVal) {//选择元素后加载当前这个元素的元素类型
            let self = this;
            if(newVal!=oldVal){
                PrintConsole(self.RomeData.elementType)
                if(self.isAddNew || self.RomeData.elementType.length==0){//只有新增的时候才会查
                    self.RomeData.elementType=[];
                    if(newVal){
                        self.SelectElementType(newVal);
                    }
                }
            }
        },
        'RomeData.elementType': function (newVal,oldVal) {//选择元素后加载当前这个元素的元素类型
            if(newVal!=oldVal){
                this.DisPlayControls(newVal[1]);
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                PrintConsole('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.state=true;
            self.RomeData.eventName='';
            self.RomeData.elementId='';
            self.RomeData.elementType=[];
            self.RomeData.inputData='';
            self.RomeData.assertType='';
            self.RomeData.assertValueType='';
            self.RomeData.assertValue='';

            self.DisPlay.element=true;
            self.DisPlay.inputData=false;
            self.DisPlay.assert=false;
            self.DisPlay.imageOperation=false;
        },
        AddToStepsTable(){
            let self = this;
            let obj = {};
            obj.state=self.RomeData.state;
            obj.id=self.RomeData.id;
            obj.eventName=self.RomeData.eventName;
            obj.elementId=self.RomeData.elementId;
            obj.elementType=self.RomeData.elementType;

            let elementTypeTxt = ""
            self.RomeData.elementTypeOptions.forEach(d=>{
                let tempItem = d.children.find(item=>
                    item.value == self.RomeData.elementType[1]
                );
                // PrintConsole(d.children)
                // PrintConsole('elementTypeTxt',tempItem)
                if(tempItem){
                    elementTypeTxt = tempItem.label;
                }
            });
           
            obj.elementTypeTxt = elementTypeTxt;
            obj.inputData=self.RomeData.inputData;
            if(self.RomeData.elementId){
                if(self.isAddNew){
                    obj.elementDynamic=0;
                }else{
                    if(self.RomeData.elementDynamic==0){
                        obj.elementDynamic=0;
                    }else if(self.RomeData.elementDynamic==1){
                        obj.elementDynamic=2;
                    }else{
                        obj.elementDynamic=2;
                    }
                }
            }else{
                obj.elementDynamic=3;
            }
            
            obj.assertType=self.RomeData.assertType;
            obj.assertValueType=self.RomeData.assertValueType;
            obj.assertValue=self.RomeData.assertValue;

            if(self.isAddNew){
                self.$emit('geAddtData',obj);//回调传值
            }else{
                self.$emit('geEditData',obj);//回调传值
            }
            self.dialogClose();
        },
        GetElementOperationType(){//返回元素类型
            GetElementOperationTypeItems().then(d=>{
                if(d.statusCode==2000){
                    this.RomeData.elementTypeOptions = d.dataList;
                }else{
                    self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                }
            });
        },
        GeElementNameOption(){
            let self = this;
            GeElementNameItems(self.RomeData.pageNameList).then(d=>{
                if(d.statusCode==2000){
                    self.RomeData.elementNameOption = d.dataList;
                }else{
                    self.$message.errorMsg('列表数据获取失败:'+d.errorMsg);
                }
            });
        },
        SelectElementType(elementId){//根据元素ID查询 元素类型
            let self = this;
            self.$axios.get('/api/UiElementMaintenance/SelectElementType',{
                params:{
                    'elementId':elementId,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                   self.RomeData.elementType = res.data.elementType;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        DisPlayControls(elementType){//控件的显示及隐藏 和操作提示
            let self = this;
            PrintConsole('elementType',elementType)
            self.RomeData.operationTips =[]
            if(elementType=='Input'){
                self.DisPlay.element=true;
                self.DisPlay.inputData=true;
                self.DisPlay.assert=false;

                self.RomeData.assertType='';
                self.RomeData.assertValueType='';
                self.RomeData.assertValue='';
            }else if(elementType=='Label'){
                self.DisPlay.element=true;
                self.DisPlay.assert=true;
                self.DisPlay.inputData=false;

                self.RomeData.inputData='';
            }else if(elementType=='Click'){
                self.DisPlay.element=true;
                self.DisPlay.inputData=false;
                self.DisPlay.assert=false;

                self.RomeData.inputData='';
                self.RomeData.assertType='';
                self.RomeData.assertValueType='';
                self.RomeData.assertValue='';
            }else if(elementType=='Screenshots'){
                self.DisPlay.inputData=true;
                self.DisPlay.assert=false;
                self.DisPlay.element=false;

                self.RomeData.elementId='';
                self.RomeData.assertType='';
                self.RomeData.assertValueType='';
                self.RomeData.assertValue='';

                self.RomeData.eventName = '页面截图';
                self.RomeData.operationTips.push('1.请在输入中填写截图后的名称.');
            }else if(elementType=='Sleep'){
                self.DisPlay.inputData=true;
                self.DisPlay.element=false;
                self.DisPlay.assert=false;

                self.RomeData.elementId='';
                self.RomeData.assertType='';
                self.RomeData.assertValueType='';
                self.RomeData.assertValue='';

                if(self.RomeData.eventName){

                }else{
                    self.RomeData.eventName='进程停顿'
                }
            }else if(elementType=='HandleSwitch'){
                self.DisPlay.inputData=true;
                self.DisPlay.element=false;
                self.DisPlay.assert=false;

                self.RomeData.elementId='';
                self.RomeData.assertType='';
                self.RomeData.assertValueType='';
                self.RomeData.assertValue='';

                if(self.RomeData.eventName){

                }else{
                    self.RomeData.eventName = '切换句柄';
                }
                self.RomeData.operationTips.push('1.请在输入中填写需要切换到句柄的数值(0为第1页).');
            }
            else{
                // self.DisPlay.inputData=false;
                // self.DisPlay.assert=false;
            }
        },

    }
};
</script>

<style>
.operationTips{
    text-align: left;
}
</style>
