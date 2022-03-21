<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="500px">
        <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="85px" @submit.native.prevent>
            <el-form-item label="所属页面:" prop="pageId">
                <el-select v-model="RomeData.pageId" clearable placeholder="请选择" style="width:200px;float:left" @click.native="GetPageNameOption()">
                    <el-option
                        v-for="item in RomeData.pageNameOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="功能名称:" prop="funName" >
                <el-input v-model.trim="RomeData.funName "></el-input>
            </el-form-item>
            <el-form-item label="备注:">
                <el-input  
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 4}"
                    placeholder="请输入备注内容" v-model="RomeData.remarks">
                </el-input>
            </el-form-item>
            <el-button  type="primary" @click="submitForm('RomeData')">保存</el-button>
            <el-button @click="ClearRomeData()">重置</el-button>
        </el-form>
    </el-dialog>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../js/GetSelectTable.js";

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                funId:'',
                pageId:'',
                pageNameOption:[],
                funName:'',
                remarks:'',
            },
            rules: {
                funName: [
                    { required: true, message: '请输入功能名称', trigger: 'blur' },
                    { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
                ],
                pageId:[{required: true, message: '请选择所属页面', trigger: 'change' }]
            }
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
                this.isAddNew = newval.isAddNew
                
                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.GetPageNameOption();
                    self.RomeData.funId = newval.funId;
                    self.RomeData.pageId =newval.pageId;
                    self.RomeData.funName =newval.funName;
                    self.RomeData.remarks =newval.remarks;
                }
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.pageId='';
            self.RomeData.funName='';
            self.RomeData.remarks='';
        },
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.RomeData.pageNameOption = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/FunManagement/SaveData',Qs.stringify({
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.RomeData.pageId,
                    'funName':self.RomeData.funName,
                    'remarks':self.RomeData.remarks,
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增功能成功');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增功能失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/FunManagement/EditData',Qs.stringify({
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'funId':self.RomeData.funId,
                    'pageId':self.RomeData.pageId,
                    'funName':self.RomeData.funName,
                    'remarks':self.RomeData.remarks,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改功能成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('修改功能失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        submitForm(formName,id) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveData();
                } 
            });
        },
    }
};
</script>

<style>
.Item-Button{
    margin-left: -30px;
}
</style>
