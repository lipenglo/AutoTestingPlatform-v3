<template>
    <el-drawer
    :title="dialogTitle"
    size="750px"
    :wrapperClosable="false"
    :visible.sync="dialogVisible"
    direction='rtl'
    :before-close="dialogClose">
        <el-tabs 
        type="border-card" 
        v-model="activeName" 
        @tab-click="handleClick" 
        style="height:870px"
        v-loading="loading"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading">
            <el-tab-pane label="基本信息" name="basicInfo">
                <div class="table">
                    <div class="father" style="width: 100%; height: 600px;">
                        <div class="son" style="width: 650px; height: 450px;">
                            <el-form ref="RomeData" :inline="true" :rules="rules" :model="RomeData"  label-width="100px">
                                <el-form-item label="工单类型:" prop="workType">
                                    <el-select v-model="RomeData.workType" clearable placeholder="请选择" style="width:200px;float:left;">
                                        <el-option
                                            v-for="item in RomeData.workTypeNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="工单状态:" prop="workState">
                                    <el-select v-model="RomeData.workState" clearable placeholder="请选择" style="width:200px;float:left;">
                                        <el-option
                                            v-for="item in RomeData.workStateNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="所属页面:" prop="pageId">
                                    <el-select v-model="RomeData.pageId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageNameOption()">
                                        <el-option
                                            v-for="item in RomeData.pageNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="所属功能:" prop="funId">
                                    <el-select v-model="RomeData.funId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetFunNameOption()">
                                        <el-option
                                            v-for="item in RomeData.funNameOption"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="工单名称:" prop="workName">
                                    <el-input v-model.trim="RomeData.workName" style="width:515px"></el-input>
                                </el-form-item>
                                <div>
                                    <el-form-item label="工单信息:">
                                        <el-input type="textarea" 
                                        :autosize="{ minRows: 10, maxRows: 10}"
                                        v-model="RomeData.message"
                                        style="width:515px"></el-input>
                                    </el-form-item>
                                </div>
                                <el-form-item label="工单关联人:">
                                    <el-cascader 
                                        @click.native="GetUserNameOption()"
                                        style="width:515px"
                                        v-model="RomeData.pushTo" 
                                        :options="RomeData.userNameOptions" 
                                        :props="RomeData.props" 
                                        :show-all-levels="false" 
                                        clearable>
                                        <template slot-scope="{ node, data }">
                                            <span>{{ data.label }}</span>
                                            <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                                        </template>
                                    </el-cascader>
                                </el-form-item>
                                <div>
                                    <el-button type="primary" @click="submitForm('RomeData')">确定</el-button>
                                    <el-button @click="ClearRomeData()">重置</el-button>
                                </div>
                            </el-form>
                        </div>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane label="历史回复信息" name="historyInfo" v-if="isAddNew==false">
                <div style=" height:760px;overflow:auto">
                    <el-timeline style="text-align: left;">
                        <el-timeline-item 
                        placement="top"
                        v-for="(activity, index) in RomeData.historyInfo"
                        :key="index"
                        :timestamp="activity.timestamp">
                        <el-card style="width:600px">
                            <h4>{{activity.title}}</h4>
                            <p v-html="activity.content" style="white-space: pre-line;"></p>
                        </el-card>
                        </el-timeline-item>
                    </el-timeline>
                </div>
            </el-tab-pane>
            <el-tab-pane label="生命周期" name="lifeCycle" v-if="isAddNew==false">
                <div style=" height:760px;overflow:auto">
                    <el-timeline style="text-align: left;">
                        <el-timeline-item 
                        placement="top"
                        v-for="(activity, index) in RomeData.activities"
                        :key="index"
                        :timestamp="activity.timestamp">
                        <el-card style="width:600px">
                            <h4>{{activity.title}}</h4>
                            <p v-html="activity.content" style="white-space: pre-line;"></p>
                        </el-card>
                        </el-timeline-item>
                    </el-timeline>
                </div>
                <!-- <el-timeline>
                    <el-timeline-item
                        v-for="(activity, index) in RomeData.activities"
                        :key="index"
                        :timestamp="activity.timestamp">
                        {{activity.content}}
                    </el-timeline-item>
                </el-timeline> -->
            </el-tab-pane>
        <!-- <el-card style="height:860px">
            <template>
                
            </template>
        </el-card> -->
        </el-tabs>
    </el-drawer>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../js/Logger.js";
import {GetPageNameItems} from "../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../js/GetSelectTable.js";
import {GetUserNameItems} from "../../../js/GetSelectTable.js";

export default {
    components: {
       
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            activeName:'basicInfo',
            loading:false,
            RomeData:{
                workId:'',
                workType:'',
                workTypeNameOption:[
                    {'label':'新增','value':'Add'},
                    {'label':'修改','value':'Edit'},
                    {'label':'删除','value':'Delete'},
                    {'label':'BUG','value':'BUG'},
                    {'label':'其他','value':'Other'},
                ],
                workState:'',
                workStateNameOption:[
                    {'label':'待受理','value':0},
                    {'label':'受理中','value':1},
                    {'label':'已解决','value':2},
                    {'label':'已关闭','value':3},
                ],
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                workName:'',
                message:'',
                props: { multiple: true },
                pushTo:[],
                userNameOptions:[],
                reverse:false,
                activities:[],
                historyInfo:[
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                    // {'timestamp':'2022-21-21 12:11:11','title':'lipenglo(古雨辰):回复','content':'不要你管,我自己改了'},
                ],
            },
            rules:{
                workType:[{required: true, message: '请选择工单类型', trigger: 'change' }],
                workState:[{required: true, message: '请选择工单状态', trigger: 'change' }],
                pageId:[{required: true, message: '请选择所属页面', trigger: 'change' }],
                funId:[{required: true, message: '请选择所属功能', trigger: 'change' }],
                workName: [
                    { required: true, message: '请输入工单名称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
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
                this.isAddNew = newval.isAddNew
                if(newval.triggerPage=='ApiMaintenance'){
                    let self = this;
                    self.RomeData.workType=newval.workType;
                    self.RomeData.workState=newval.workState;
                    GetPageNameItems('API',self.$cookies.get('proId')).then(d=>{
                        self.RomeData.pageNameOption = d;
                        self.RomeData.pageId=newval.pageId;
                        GetFunNameItems('API',self.$cookies.get('proId'),self.RomeData.pageId).then(d=>{
                            self.RomeData.funNameOption = d;
                            self.RomeData.funId=newval.funId;
                            self.RomeData.workName=newval.workName;
                            GetUserNameItems().then(d=>{
                                self.RomeData.userNameOptions = d;
                                self.RomeData.pushTo=newval.createUserId;
                            });

                        });
                    });
                    
                }else{      
                    if(newval.isAddNew==false){//进入编辑状态
                        let self = this;
                        self.RomeData.workId=newval.workId;
                        self.LoadEditData(newval.workId).then(d=>{
                            if(d.statusCode==2000){
                                self.RomeData.workType = d.dataTabel.workType;
                                self.RomeData.workState = d.dataTabel.workState;
                                GetPageNameItems('API',this.$cookies.get('proId')).then(dd=>{
                                    self.RomeData.pageNameOption = dd;
                                    self.RomeData.pageId = d.dataTabel.pageId;
                                    GetFunNameItems('API',this.$cookies.get('proId'),this.RomeData.pageId).then(dd=>{
                                        self.RomeData.funNameOption = dd;
                                        self.RomeData.funId = d.dataTabel.funId;
                                        self.RomeData.workName = d.dataTabel.workName;
                                        // self.RomeData.message = d.dataTabel.message;
                                        self.RomeData.historyInfo = d.dataTabel.historyInfo;
                                        GetUserNameItems().then(dd=>{
                                            self.RomeData.userNameOptions = dd;
                                            self.RomeData.pushTo = d.dataTabel.pushTo;
                                        });
                                    });
                                });
                            }else{
                                self.$message.error('获取数据失败:'+d.errorMsg);
                            }
                        });
                    }
                }
            }
        },
        'RomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.RomeData.funId='';
                self.RomeData.funNameOption=[];
            }
        },
     
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        handleClick(tab, event) {
            PrintConsole(tab);
            if(tab.name=="lifeCycle"){
                this.SelectLifeCycle();
            }
        },
        SelectLifeCycle(){//查询生命周期
            let self = this;
            self.loading=true;
            self.$axios.get('/api/WorkorderManagement/SelectLifeCycle',{
                params:{
                    'workId':self.RomeData.workId,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.activities=res.data.dataTabel;
                    
                    self.loading=false;
                }else{
                    self.$message.error('获取生命周期失败:'+res.data.errorMsg);
                    self.loading=false;
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.activeName='basicInfo';
            self.RomeData.workType='';
            self.RomeData.workState='';
            self.RomeData.pageId='';
            self.RomeData.funId='';
            self.RomeData.workName='';
            self.RomeData.message='';
            self.RomeData.pushTo=[];
            self.RomeData.historyInfo=[];
        },
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.RomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.RomeData.pageId){
                GetFunNameItems(this.$cookies.get('proId'),this.RomeData.pageId).then(d=>{
                    this.RomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetUserNameOption(){
            GetUserNameItems().then(d=>{
                this.RomeData.userNameOptions = d;
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
                self.$axios.post('/api/WorkorderManagement/SaveData',Qs.stringify({
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.RomeData.pageId,
                    'funId':self.RomeData.funId,
                    'workType':self.RomeData.workType,
                    'workState':self.RomeData.workState,
                    'workName':self.RomeData.workName,
                    'message':self.RomeData.message,
                    'pushTo':self.RomeData.pushTo.toString(),
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增工单成功');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增工单失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/WorkorderManagement/EditData',Qs.stringify({
                    'workId':self.RomeData.workId,
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.RomeData.pageId,
                    'funId':self.RomeData.funId,
                    'workType':self.RomeData.workType,
                    'workState':self.RomeData.workState,
                    'workName':self.RomeData.workName,
                    'message':self.RomeData.message,
                    'pushTo':self.RomeData.pushTo.toString(),
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改工单成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('修改工单失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        LoadEditData(workId){
            let self = this;
            self.loading=true;
            return self.$axios.get('/api/WorkorderManagement/LoadData',{
                params:{
                    'workId':workId
                }
            }).then(res => {
                self.loading=false;
                return res.data
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        submitForm(formName) {//保存
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
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
.test{
    text-align: left;
}
</style>
