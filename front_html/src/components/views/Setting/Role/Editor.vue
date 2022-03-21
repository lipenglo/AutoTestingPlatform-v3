<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="500px">
        <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="100px"  @submit.native.prevent>
            <el-form-item label="角色名称:" prop="roleName" >
                <el-input v-model.trim="RomeData.roleName "></el-input>
            </el-form-item>
            <el-form-item>
                <el-button style="margin: auto 20px auto auto; " type="primary" @click="submitForm('RomeData')">保存</el-button>
                <el-button style="margin: auto 80px auto auto; "  @click="ClearRomeData()">重置</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../js/Logger.js";
import store from '../../../../store/index'

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                roleId:'',
                roleName: '',
            },
            rules: {
                roleName: [
                    { required: true, message: '请输入角色名称', trigger: 'blur' },
                    { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
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
                    self.RomeData.roleId = newval.roleId;
                    self.RomeData.roleName = newval.roleName;
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
            this.resetForm('RomeData');
            self.RomeData.roleId = '';
            self.RomeData.roleName = '';
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/role/SaveData',Qs.stringify({
                    'roleName':self.RomeData.roleName,
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增角色成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增角色失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/role/EditData',Qs.stringify({
                    'roleId':self.RomeData.roleId,
                    'roleName':self.RomeData.roleName,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改角色成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('修改角色失败:'+res.data.errorMsg);
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

</style>
