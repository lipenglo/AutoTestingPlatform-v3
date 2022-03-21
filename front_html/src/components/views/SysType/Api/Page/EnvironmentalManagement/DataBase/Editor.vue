<template>
     <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="550px">
        <div
            v-loading="loading"
            element-loading-text="拼命连接中"
            element-loading-spinner="el-icon-loading">
            <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="90px">
                <el-form-item label="DB类型:" prop="dbType" >
                    <el-select v-model="RomeData.dbType" clearable placeholder="请选择" style="width:200px;float:left">
                        <el-option
                            v-for="item in RomeData.dbTypeOption"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="IP:" prop="dataBaseIp" >
                    <el-input class="inputCss" v-model.trim="RomeData.dataBaseIp"></el-input>
                </el-form-item>
                <el-form-item label="端口:" prop="port" >
                    <el-input class="inputCss" v-model.trim="RomeData.port"></el-input>
                </el-form-item>
                <el-form-item label="用户名:" prop="userName" >
                    <el-input class="inputCss" v-model.trim="RomeData.userName"></el-input>
                </el-form-item>
                <el-form-item label="密码:" prop="passWord" >
                    <el-input class="inputCss" type="password" v-model.trim="RomeData.passWord"></el-input>
                </el-form-item>
                <el-form-item label="备注:">
                    <el-input  
                        class="inputCss"
                        type="textarea"
                        :autosize="{ minRows: 5, maxRows: 5}"
                        placeholder="请输入备注内容" v-model="RomeData.remarks">
                    </el-input>
                </el-form-item>
            
                <el-button  type="primary" @click="submitForm('RomeData')">保存</el-button>
                <!-- <el-button @click="ClearRomeData()">重置</el-button> -->
                <el-button  @click="testConnect()">测试连接</el-button>
            </el-form>
        </div>
     </el-dialog>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    data() {
        return {
            dialogTitle:"",
            loading:false,
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                dbId:'',
                dbType:'',
                dbTypeOption:[
                    {'label':'MySql','value':'MySql'}
                ],
                dataBaseIp:'',
                port:'',
                userName:'',
                passWord:'',
                remarks:'',
            },
            rules: {
                dbType:[{required: true, message: '请选择连接库类型', trigger: 'change' }],
                dataBaseIp: [
                    { required: true, message: '请输入IP地址', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
                port: [{ required: true, message: '请输入端口', trigger: 'blur' }],
                userName: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                passWord: [{ required: true, message: '请输入密码', trigger: 'blur' }],
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
                    self.RomeData.dbId = newval.dbId
                    self.RomeData.dbType =newval.dbType;
                    self.RomeData.dataBaseIp =newval.dataBaseIp;
                    self.RomeData.port =newval.port;
                    self.RomeData.userName =newval.dbUser;
                    self.RomeData.passWord =newval.dbpwd;
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
            self.RomeData.dbType='';
            self.RomeData.dataBaseIp='';
            self.RomeData.port='';
            self.RomeData.userName='';
            self.RomeData.passWord='';
            self.RomeData.remarks='';
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        testConnect(){
            let self = this;
            self.loading=true
            self.$axios.get('/api/DataBaseEnvironment/TestConnect',{
                params:{
                    "dbType":self.RomeData.dbType,
                    "dataBaseIp":self.RomeData.dataBaseIp,
                    "port":self.RomeData.port,
                    "userName":self.RomeData.userName,
                    "passWord":self.RomeData.passWord,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.$message.success('测试连接成功!');
                    self.loading=false;
                }else{
                    self.$message.error('连接失败:'+res.data.errorMsg);
                    self.loading=false;
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/DataBaseEnvironment/SaveData',Qs.stringify({
                    "dbType":self.RomeData.dbType,
                    "dataBaseIp":self.RomeData.dataBaseIp,
                    "port":self.RomeData.port,
                    "userName":self.RomeData.userName,
                    "passWord":self.RomeData.passWord,
                    'remarks':self.RomeData.remarks,
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增数据库成功');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增数据库失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/DataBaseEnvironment/EditData',Qs.stringify({
                    "dbId":self.RomeData.dbId,
                    "dbType":self.RomeData.dbType,
                    "dataBaseIp":self.RomeData.dataBaseIp,
                    "port":self.RomeData.port,
                    "userName":self.RomeData.userName,
                    "passWord":self.RomeData.passWord,
                    'remarks':self.RomeData.remarks,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改数据库成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('修改数据库失败:'+res.data.errorMsg);
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
.inputCss{
    width: 380px;
    float: left;
}
</style>
