<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="500px">
            <el-card>
                <el-form ref="RomeData" :rules="RomeData.rules" :model="RomeData"  label-width="100px">
                    <el-form-item label="用户名:" prop="userName" >
                        <el-input v-model.trim="RomeData.userName "></el-input>
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
                        <el-button style="margin: auto 80px auto auto; "  @click="resetForm('RomeData')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
    </el-dialog>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../js/Logger.js";

import {NoTokenGetRoleNameItems} from "../../js/GetSelectTable.js";

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
            RomeData:{
                userName: '',
                passWord:'',
                checkPass:'',
                nickName:'',
                emails:'',
                roleId:'',
                roleOption:[],
                rules: {
                    userName: [
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
                    ],
                    passWord: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
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
            },
        };
    },
    mounted(){

    },
    props:[//main页面在引用editor时 必须声明所需要调用的属性
        'isVisible','dialogPara'
    ],
    watch:{
        isVisible:{//用于监听父页面的isVisible，true时就弹出窗口
            handler(newval,oldval)
            {
                this.dialogVisible=newval;
                // this.resetForm('proRomeData');
            }
        },
        dialogPara:{
            handler(newval,oldval)
            {
                // console.log(newval);
                PrintConsole(newval);
                this.resetForm('RomeData');
                this.dialogTitle = newval.dialogTitle;
            }
        }
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        GetRoleNameOption(){
            NoTokenGetRoleNameItems().then(d=>{
                this.RomeData.roleOption = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        addUser(){
            let self = this;
            self.$axios.post('/api/login/registered',
            Qs.stringify({
                'userName':self.RomeData.userName,
                'passWord':self.RomeData.passWord,
                'nickName':self.RomeData.nickName,
                'emails':self.RomeData.emails,
                'roleId':self.RomeData.roleId,
            })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('注册成功,请联系管理员进行权限分配及激活操作!');
                    self.dialogVisible = false;//关闭新增弹窗
                }
                else{
                    self.$message.error('注册失败!');
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        submitForm(formName,id) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.addUser();
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
