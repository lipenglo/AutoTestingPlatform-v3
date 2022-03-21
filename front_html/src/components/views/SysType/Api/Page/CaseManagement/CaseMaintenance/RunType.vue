<template>
    <div>
        <template>
            <el-dialog
                :title="dialogTitle"
                :visible.sync="dialogVisible"
                :close-on-click-modal=false
                :before-close="dialogClose"
                width="400px">
                <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="100px" @submit.native.prevent>
                    <el-form-item label="选择环境:" >
                        <el-select v-model="RomeData.environmentId" clearable placeholder="默认为原用例环境" style="float:left" @click.native="GetPageEnvironmentNameOption()">
                            <el-option
                                v-for="item in RomeData.environmentNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="运行方式:" prop="runType">
                        <el-select v-model="RomeData.runType" placeholder="请选择运行方式" style="float:left">
                            <el-option
                                v-for="item in RomeData.runTypeOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button  type="primary" @click="submitForm('RomeData')">运行</el-button>
                    <el-button @click="ClearRomeData()">重置</el-button>
                </el-form>
            </el-dialog>
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
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";
import DialogTestReport from "./TestReport.vue";

export default {
    components: {
        DialogTestReport
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            loading:false,
            RomeData:{
                caseId:'',
                caseName:'',
                environmentId:'',
                environmentNameOption:[],
                runType:'',
                runTypeOptions:[
                    {'label':'同步(显示执行过程)','value':'Synchronous'},
                    {'label':'异步(不会显示执行过程)','value':'Asynchronous'},
                ],
            },
            rules:{
                runType:[{required: true, message: '请选择运行方式', trigger: 'change' }]
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
                this.RomeData.caseId=newval.caseId;
                this.RomeData.caseName=newval.caseName;
            },
        }
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.environmentId='';
            self.RomeData.runType='';
        },
        GetPageEnvironmentNameOption(){
            GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(d=>{
                this.RomeData.environmentNameOption = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.OpenTestReportDialog();
                } 
            });
        },
        //运行过程
        closeTestReportDialog(){
            this.dialog.testReport.dialogVisible =false;
        },
        OpenTestReportDialog(index,row){
            let self = this;
            self.dialog.testReport.dialogPara={
                dialogTitle:self.RomeData.caseName,//初始化标题
                runType:self.RomeData.runType,
                caseId:self.RomeData.caseId,
                environmentId:self.RomeData.environmentId,
            }
            if(self.RomeData.runType=="Synchronous"){
                self.dialog.testReport.dialogVisible=true;
            }else{
                self.$message.success('异步任务指令已发出,请稍后在测试报告中查看结果!');
            }
            self.dialogClose();
        },
    }
};
</script>

<style>

</style>
