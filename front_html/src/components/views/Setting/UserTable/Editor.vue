<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="500px">
        <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="100px">
            <el-form-item label="用户名:" prop="userName" >
                <el-input :disabled="RomeData.userNameInput" v-model.trim="RomeData.userName "></el-input>
            </el-form-item>
            <el-form-item label="密码:" prop="passWord">
                <el-input  show-password v-model.trim="RomeData.passWord"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="RomeData.checkPass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="昵称:" prop="nickName">
                <el-input  v-model.trim="RomeData.nickName"></el-input>
            </el-form-item>
            <el-form-item label="Email:">
                <el-input v-model.trim="RomeData.emails"></el-input>
            </el-form-item>
            <el-form-item label="入加角色:" prop="roleId">
                <el-select v-model="RomeData.roleId" clearable placeholder="请选择" style="float:left" @click.native="GetRoleNameOption()">
                    <el-option
                        v-for="item in RomeData.roleOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button style="margin: auto 20px auto auto; " type="primary" @click="submitForm('RomeData')">保存</el-button>
                <el-button style="margin: auto 80px auto auto; "  @click="ClearRomeData()">重置</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script>
import {PrintConsole} from "../../../js/Logger.js";
import Qs from 'qs'
import store from '../../../../store/index';
import {GetRoleNameItems} from "../../../js/GetSelectTable.js";

export default {
    data() {
        var validatecheckPass = (rule, value, callback) => {//验证2次密码相同
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.RomeData.passWord) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        };
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                userId:'',
                userName: '',
                userNameInput:false,
                passWord:'',
                checkPass:'',
                nickName:'',
                emails:'',
                roleId:'',
                roleOption:[],
            },
            rules: {
                userName: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
                ],
                passWord: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
                ],
                checkPass: [
                    { validator: validatecheckPass, trigger: 'blur' }
                ],
                nickName: [
                    { required: true, message: '请输入昵称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
                roleId:[
                    { required: true, message: '请选择加入角色', trigger: 'change' }
                ]
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
                    self.RomeData.userNameInput = true;
                    self.RomeData.userId=newval.userId;
                    self.RomeData.userName=newval.userName;
                    self.RomeData.nickName=newval.nickName;
                    self.RomeData.emails=newval.emails;
                    self.GetRoleNameOption();
                    self.RomeData.roleId = newval.roleId;
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
            self.RomeData.userId='';
            self.RomeData.userName='';
            self.RomeData.userNameInput=false;
            self.RomeData.nickName='';
            self.RomeData.emails='';
            self.RomeData.roleId='';
        },
        GetRoleNameOption(){
            GetRoleNameItems().then(d=>{
                this.RomeData.roleOption = d;
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
                self.$axios.post('/api/userManagement/InternalRegistered',Qs.stringify({
                    'userName':self.RomeData.userName,
                    'passWord':self.RomeData.passWord,
                    'nickName':self.RomeData.nickName,
                    'emails':self.RomeData.emails,
                    'roleId':self.RomeData.roleId,
                })).then(res => {
                    if(res.data.statusCode==2001){
                        self.$message.success('注册成功,请联系管理员进行权限分配及激活操作!');
                        self.dialogVisible = false;//关闭新增弹窗
                        self.$emit('closeDialog');
                        self.$emit('Succeed');//回调查询
                    }
                    else{
                        self.$message.error(res.data.errorMsg);
                    }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/userManagement/EditData',Qs.stringify({
                    'userId':self.RomeData.userId,
                    'passWord':self.RomeData.passWord,
                    'nickName':self.RomeData.nickName,
                    'emails':self.RomeData.emails,
                    'roleId':self.RomeData.roleId,
                })).then(res => {
                    if(res.data.statusCode==2002){
                        self.$message.success('用户修改成功!');
                        self.dialogVisible = false;//关闭新增弹窗
                        self.$emit('closeDialog');
                        self.$emit('Succeed');//回调查询
                    }
                    else{
                        self.$message.error(res.data.errorMsg);
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
.el-table-column{
    width: 400px;
}
.el-input {
    float:left;
    /* width:300px; */
}
</style>
