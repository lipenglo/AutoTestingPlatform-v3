<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="500px">
        <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="85px" @submit.native.prevent>
            <el-form-item label="环境名称:" prop="environmentName" >
                <el-input v-model.trim="RomeData.environmentName "></el-input>
            </el-form-item>
            <el-form-item label="环境地址:" prop="environmentUrl" >
                <el-input v-model.trim="RomeData.environmentUrl "></el-input>
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
import Qs from 'qs'
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                environmentId:'',
                environmentName: '',
                environmentUrl: '',
                remarks:'',
            },
            rules: {
                proId:[{ required: true, message: '请选择所属项目', trigger: 'change' }],
                environmentName: [
                    { required: true, message: '请输入环境名称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
                environmentUrl: [
                    { required: true, message: '请输入环境地址', trigger: 'blur' },
                    { min: 1, max: 200, message: '长度在 1 到 200 个字符', trigger: 'blur' }
                ],
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
                    self.RomeData.environmentId =newval.environmentId;
                    self.RomeData.environmentName =newval.environmentName;
                    self.RomeData.environmentUrl =newval.environmentUrl;
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
            self.RomeData.environmentName = '';
            self.RomeData.environmentUrl = '';
            self.RomeData.remarks='';
            
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/PageEnvironment/SaveData',Qs.stringify({
                    'sysType':'UI',
                    'proId':self.$cookies.get('proId'),
                    'environmentName':self.RomeData.environmentName,
                    'environmentUrl':self.RomeData.environmentUrl,
                    'remarks':self.RomeData.remarks,
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增环境成功');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增环境失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/PageEnvironment/EditData',Qs.stringify({
                    'sysType':'UI',
                    'environmentId':self.RomeData.environmentId,
                    'proId':self.$cookies.get('proId'),
                    'environmentName':self.RomeData.environmentName,
                    'environmentUrl':self.RomeData.environmentUrl,
                    'remarks':self.RomeData.remarks,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('环境修改成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('环境修改失败:'+res.data.errorMsg);
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
