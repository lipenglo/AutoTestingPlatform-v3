<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="700px">
        <el-form ref="RomeData" :rules="rules" :model="RomeData"  label-width="90px">
            <el-form-item label="公告简介:" prop="abstract" >
                <el-input v-model.trim="RomeData.abstract "></el-input>
            </el-form-item>
            <el-form-item label="公告信息:">
                <el-input
                    type="textarea"
                    :autosize="{ minRows: 15, maxRows: 15}"
                    placeholder="请输入内容"
                    v-model="RomeData.info">
                </el-input>
            </el-form-item>
            <el-form-item label="展示状态:" prop="state">
                <div style='float:left'>
                    <el-switch
                        v-model="RomeData.state"
                        active-color="#13ce66"
                        inactive-color="#ff4949"
                        active-text="关闭"
                        inactive-text="开启">
                    </el-switch>
                <!-- <el-radio-group v-model="RomeData.state">
                    <el-radio label="展示"></el-radio>
                    <el-radio label="不展示"></el-radio>
                </el-radio-group> -->
                </div>
            </el-form-item>
            <el-button type="primary" @click="submitForm('RomeData')">保存</el-button>
            <el-button @click="ClearRomeData()">重置</el-button>
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
                noticeId:'',
                abstract: '',
                info:'',
                state:false,
            },
            rules: {
                abstract: [
                    { required: true, message: '请输入公告简介', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
                state: [
                    { required: true, message: '请选择展示状态', trigger: 'change' }
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
                    self.RomeData.noticeId = newval.noticeId;
                    self.RomeData.abstract = newval.abstract;
                    self.RomeData.info = newval.info;
                    self.RomeData.state = newval.state;
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
            self.RomeData.noticeId = '';
            self.RomeData.abstract = '';
            self.RomeData.info = '';
            self.RomeData.state = false;
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/Notice/SaveData',Qs.stringify({
                    'abstract':self.RomeData.abstract,
                    'info':self.RomeData.info,
                    'state':self.RomeData.state,
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增公告成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增公告失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/Notice/EditData',Qs.stringify({
                    'noticeId':self.RomeData.noticeId,
                    'abstract':self.RomeData.abstract,
                    'info':self.RomeData.info,
                    'state':self.RomeData.state,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改公告成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('修改公告失败:'+res.data.errorMsg);
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
