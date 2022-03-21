<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="450px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
            <div style="text-align: left;">
                <el-form ref="RomeData" :inline="true" :rules="RomeData.rules" :model="RomeData"  label-width="100px">
                    <el-form-item prop="location" label="操作位置:">
                        <el-select v-model="RomeData.location" clearable placeholder="请选择操作位置" style="width:150px;float:left;" >
                            <el-option
                                v-for="item in RomeData.locationOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="operationType" label="操作类型:">
                        <el-select v-model="RomeData.operationType" clearable placeholder="请选择操作位置" style="width:300px;float:left;" >
                            <el-option
                                v-for="item in RomeData.operationTypeOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="选择用例:" v-if="RomeData.operationType=='TestCase'">
                        <el-cascader 
                        clearable
                        :options="RomeData.caseNameOption" 
                        v-model="RomeData.caseId" 
                        placeholder="请选择需要运行的用例" 
                        style="width:300px;float:left;"
                        @click.native="GetCaseNameOption()"
                        @change="changeCase">
                            <template slot-scope="{ node, data }">
                                <span>{{ data.label }}</span>
                                <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                            </template>
                        </el-cascader>
                    </el-form-item>
                    <el-form-item label="输入方法:" v-else-if="RomeData.operationType=='Methods'">
                        <el-input v-model="RomeData.methodsName" clearable placeholder="输入方法函数名称" style="width:300px;float:left;"></el-input>
                    </el-form-item>
                    <div v-else-if="RomeData.operationType=='DataBase'">
                        <el-form-item label="选择DB:" >
                            <el-cascader
                                style="float:left;width:300px;"
                                clearable
                                placeholder="请选择连接的数据库" 
                                v-model="RomeData.dataBaseId"
                                :options="RomeData.dataBaseOptions"
                                @click.native="getDataBaseOption()"
                                @change="changeDataBase">
                                <template slot-scope="{ node, data }">
                                    <span>{{ data.label }}</span>
                                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                </template>
                            </el-cascader>
                        </el-form-item>
                        <el-form-item label="SQL:">
                            <el-input  
                                v-model="RomeData.sql"  style="float:left;width:300px;" clearable placeholder="请输入正确的SQL语句" 
                                type="textarea"></el-input>
                        </el-form-item>
                    </div>
                    <el-form-item label="备注:">
                            <el-input  
                                style="width:300px"
                                type="textarea"
                                :autosize="{ minRows: 6, maxRows: 6}"
                                placeholder="请输入内容"
                                v-model="RomeData.remarks"></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div>
                <el-button type="success" @click="AddToOperationTable(isAddNew)" v-if="isAddNew">保存</el-button>
                <el-button type="warning" @click="AddToOperationTable(isAddNew)" v-else>修改</el-button>
                <el-button @click="ClearRomeData('reset')">重置</el-button>  
            </div>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetUiCaseNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetConnectBaseItems} from "../../../../../../js/GetSelectTable.js";

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
                currentCaseId:'',
                
                location:'',//位置
                locationOption:[
                    {'label':'前置操作','value':'Pre'},
                    {'label':'后置操作','value':'Rear'},
                ],
                operationType:'',
                operationTypeOption:[
                    {'label':'测试用例','value':'TestCase'},
                    {'label':'方法函数','value':'Methods'},
                    {'label':'数据库操作','value':'DataBase'},
                ],
                caseId:'',
                caseName:'',
                caseNameOption:[],
                methodsName:'',
                dataBaseId:'',
                dataBaseName:'',
                sql:'',
                dataBaseOptions:[],
                remarks:'',
                pageNameList:[],
                rules:{
                    location:[{ required: true, message: '请选择操作位置', trigger: 'change' }],
                    operationType:[{ required: true, message: '请选择操作类型', trigger: 'change' }],
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
                this.ClearRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;
                this.RomeData.currentCaseId=newval.currentCaseId;
                this.RomeData.id=newval.id;
                this.RomeData.pageNameList=newval.pageNameList;

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    GetUiCaseNameItems(self.$cookies.get('proId'),self.RomeData.pageNameList,self.RomeData.currentCaseId).then(d=>{
                        self.RomeData.caseNameOption = d.dataList;

                        self.RomeData.location=newval.location;
                        self.RomeData.operationType=newval.operationType;
                        self.RomeData.methodsName=newval.methodsName;
                        self.RomeData.caseId=newval.caseId;
                        self.RomeData.dataBaseId=newval.dataBaseId;
                        self.RomeData.sql=newval.sql;
                        self.RomeData.remarks=newval.remarks;
                    });
                   
                }
            }
        },
        'RomeData.operationType': function (newVal,oldVal) {//选择元素后加载当前这个元素的元素类型
            if(newVal!=oldVal){
                PrintConsole(newVal);
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
            self.RomeData.location='';
            self.RomeData.operationType='';
            self.RomeData.caseId='';
            self.RomeData.methodsName='';
            self.RomeData.dataBaseId='';
            self.RomeData.sql='';
            self.RomeData.remarks='';
        },
        AddToOperationTable(val){
            let self = this;
            let obj = {};
            obj.id=self.RomeData.id;
            obj.location = self.RomeData.location;
            obj.operationType = self.RomeData.operationType;
            obj.caseId = self.RomeData.caseId;
            if(self.RomeData.caseId.length==0){
                obj.caseName = '';
            }else{
                obj.caseName = self.RomeData.caseName;
            }
            obj.methodsName = self.RomeData.methodsName;
            obj.dataBaseId = self.RomeData.dataBaseId;
            obj.dataBaseName = self.RomeData.dataBaseName;
            obj.sql = self.RomeData.sql;
            obj.remarks = self.RomeData.remarks;
            if(val){
                self.$emit('geAddtData',obj);//回调传值
            }else{
                self.$emit('geEditData',obj);//回调传值
            }
            self.dialogClose();
        },
        GetCaseNameOption(){//加载用例列表,根据页面Id及需要排除的用例id
            GetUiCaseNameItems(this.$cookies.get('proId'),this.RomeData.pageNameList,this.RomeData.currentCaseId).then(d=>{
                this.RomeData.caseNameOption = d.dataList;
            });
            
        },
        changeCase(val){//选中用例后触发
            // PrintConsole(val);
            let self = this;
            let tempCaseTable = self.RomeData.caseNameOption.find(item=>
                item.value == val[0]
            );
            if(tempCaseTable){
                PrintConsole('tempCaseTable',tempCaseTable)
                let tempChildren = tempCaseTable.children.find(item=>
                    item.value == val[1]
                );
                if(tempChildren){
                    PrintConsole('tempChildren',tempChildren)
                    self.RomeData.caseName = tempChildren.label;
                }else{
                    self.RomeData.caseName = '';
                }
            }else{
                self.RomeData.caseName = '';
            }
        },
        changeDataBase(val){//选中DB后触发
            // PrintConsole(val);
            let self = this;
            let tempDbTable = self.RomeData.dataBaseOptions.find(item=>
                item.value == val[0]
            );
            if(tempDbTable){
                PrintConsole('tempDbTable',tempDbTable)
                let tempChildren = tempDbTable.children.find(item=>
                    item.value == val[1]
                );
                if(tempChildren){
                    PrintConsole('tempChildren',tempChildren)
                    self.RomeData.dataBaseName = tempChildren.label;
                }else{
                    self.RomeData.dataBaseName = '';
                }
            }else{
                self.RomeData.dataBaseName = '';
            }
        },
        getDataBaseOption(){//加载数据库环境的IP及以下可用的库名
            GetConnectBaseItems().then(d=>{
                if(d.statusCode==2000){
                    this.RomeData.dataBaseOptions = d.dataList;
                }else{
                    this.$message.error('数据库环境加载失败:'+d.errorMsg);
                }
            });
        },

    }
};
</script>

<style>
.test{
    text-align: left;
}
</style>
