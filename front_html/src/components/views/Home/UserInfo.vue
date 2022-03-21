<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="550px">
        <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="85px" @submit.native.prevent>
            <el-form-item  label="用户名:">
                <el-input :disabled="true" v-model.trim="RomeData.userName"></el-input>
            </el-form-item>
            <el-form-item  label="昵称:">
                <el-input v-model.trim="RomeData.nickName"></el-input>
            </el-form-item>
            <el-form-item  label="邮件:">
                <el-input v-model.trim="RomeData.emails"></el-input>
            </el-form-item>
            <el-form-item  label="密码:" prop="pwd">
                <el-input show-password v-model.trim="RomeData.pwd" ></el-input>
            </el-form-item>
            <el-form-item  label="确认密码:" prop="confirmPwd">
                <el-input show-password v-model.trim="RomeData.confirmPwd" ></el-input>
            </el-form-item>
            <el-form-item  label="个人图片:">
                <el-upload
                    style="float:left"
                    :headers="headers"
                    :action="RomeData.uploadToTemp"
                    :file-list="RomeData.fileList"
                    list-type="picture-card"
                    :limit='1'
                    :on-success="upload_success"
                    :on-remove="upload_remove"
                    :before-upload="beforeAvatarUpload">
                    <i class="el-icon-plus"></i>
                </el-upload>
            </el-form-item>
            <div>
                <el-button type="primary" @click="submitForm('RomeData')">保存</el-button>
                <el-button >重置</el-button>
            </div>
        </el-form>
    </el-dialog>
</template>

<script>
import Qs from 'qs'
import store from '../../../store/index'
import {PrintConsole} from "../../js/Logger.js";

export default {
    data() {
        var validatePass_pwd = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else {
            if (this.RomeData.confirmPwd !== '') {
                this.$refs.RomeData.validateField('confirmPwd');
            }
                callback();
            }
        };
        var validatePass_confirmPwd = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.RomeData.pwd) {
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
                dialogVisible: false,
                uploadToTemp:store.state.BackService +'/api/upLoad/UpLoadToTempPath',
                userName:'',
                nickName:'',
                emails:'',
                pwd:'',
                confirmPwd:'',
                fileList:[],
                deleteFileList:[],
            },
            rules: {
                pwd: [{ required: true,validator: validatePass_pwd, trigger: 'blur' },],
                confirmPwd: [{ required: true,validator: validatePass_confirmPwd, trigger: 'blur' }],

            }
        };
    },
    mounted(){
        
    },
    computed:{//计算属性
        headers(){//用来把token放到头部
            return {
                'Token': this.$cookies.get('token')
            }
        },
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
                this.LoadUserInfo();
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        beforeAvatarUpload(file) {
            const isJPG = file.type === 'image/jpeg';
            const isLt2M = file.size / 1024 / 1024 < 2;

            if (!isJPG) {
            this.$message.error('上传头像图片只能是 JPG 格式!');
            }
            if (!isLt2M) {
            this.$message.error('上传头像图片大小不能超过 2MB!');
            }
            return isJPG && isLt2M;
        },
        upload_success(response, file, fileList){
            let self = this;
            //这里的url地址要是网络地址，不然页面上只会加载一个白的图片
            self.RomeData.fileList.push({
                'name':response['file']['fileName'],
                'url':store.state.nginxUrl+'Temp/'+response['file']['fileName']}
            );
          
        },
        upload_remove(file, fileList){
            let self = this;
            PrintConsole(file);
            self.RomeData.deleteFileList.push({'name':file.name,'url':file.url});
            self.RomeData.fileList=[];
        },
        LoadUserInfo(){//基本信息及权限信息
            let self = this;
            self.$axios.get('/api/home/LoadUserInfo', {
                params:{}
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.userName=res.data.baseInfo.userName;
                    self.RomeData.nickName=res.data.baseInfo.nickName;
                    self.RomeData.emails=res.data.baseInfo.emails;
                    if(res.data.baseInfo.userImg){
                        self.RomeData.fileList = res.data.baseInfo.fileList;
                    }
                
                }else{
                    self.$message.error('用户数据获取失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.userName='';
            self.RomeData.nickName='';
            self.RomeData.pwd='';
            self.RomeData.confirmPwd='';
            self.RomeData.emails='';
            self.RomeData.fileList=[];
            self.RomeData.deleteFileList=[];
        },
        SaveUserInfo(){
            let self = this;
            self.$axios.post('/api/home/SaveUserInfo',{
                'nickName':self.RomeData.nickName,
                'emails':self.RomeData.emails,
                'password':self.RomeData.pwd,
                'fileList':self.RomeData.fileList,
                'deleteFileList':self.RomeData.deleteFileList,
            }).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('更新完成-请退出当前账户后查看更新!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    // self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('更新失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })  
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        submitForm(formName) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveUserInfo();
                } 
            });
        },
    }
};
</script>

<style>

</style>
