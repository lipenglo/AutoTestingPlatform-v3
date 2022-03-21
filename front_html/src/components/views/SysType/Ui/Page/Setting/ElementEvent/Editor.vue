<template>
    <el-drawer
        :title="dialogTitle"
        size="1000px"
        :wrapperClosable="false"
        :close-on-press-escape="false"
        :visible.sync="dialogVisible"
        direction='rtl'
        :before-close="dialogClose">
            <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                <el-step title="维护事件信息"></el-step>
                <el-step title="编写元素操作信息"></el-step>
                <el-step title="效验元素操作"></el-step>
            </el-steps>
            <el-card 
                style="height:755px"
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading">
                <template v-if="StepsRomeData.active==0">
                    <div class="table">
                        <div class="father" style="width: 100%; height: 550px;">
                            <div class="son" style="width:900px; height: 150px;">
                                <div style="margin-top:20px;">
                                    <el-card shadow="never">
                                        <el-form ref="BaseRomeData" :inline="true" :rules="BaseRomeData.rules" :model="BaseRomeData"  label-width="100px">
                                            <el-form-item label="事件名称:" prop="eventName" >
                                                <el-input style="width:300px" v-model.trim="BaseRomeData.eventName"></el-input>
                                            </el-form-item>
                                            <el-form-item label="事件标识:" prop="eventLogo" >
                                                <el-input style="width:300px" v-model.trim="BaseRomeData.eventLogo"></el-input>
                                            </el-form-item>
                                            <el-form-item label="备注信息:">
                                                <el-input  
                                                    style="width:715px" 
                                                    type="textarea"
                                                    :autosize="{ minRows: 6, maxRows: 6}"
                                                    placeholder="请输入备注内容" v-model="BaseRomeData.remarks">
                                                </el-input>
                                            </el-form-item>
                                        </el-form>
                                    </el-card>
                                </div>
                            </div>
                        </div>
                    </div>    
                </template>
                <template v-else-if="StepsRomeData.active==1">
                    <el-table
                        id="ComponentSet" 
                        row-key="id"
                        :data="OperationRomeData.tableData"
                        height="710px"
                        border>
                        <el-table-column
                            label="序列"
                            align= "center"
                            width="80px"
                            type="index">
                        </el-table-column>
                        <el-table-column
                            label="启用"
                            width="70px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="操作名称"
                            align= "center">
                            <template slot-scope="scope">
                                <el-input v-model="scope.row.label"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="参数值"
                            align= "center">
                            <template slot-scope="scope">
                                <el-input v-model="scope.row.value"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="备注信息"
                            width="250px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-input v-model="scope.row.remarks"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column
                            align="center"
                            width="100px">
                            <template slot="header">
                                <el-button type="primary" @click="AddTable()">新增</el-button>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">Delete
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </template>
                <template v-else>
                    <div slot="header">
                        {{CharmRomeData.title}}
                    </div>
                    <div>
                        <el-table
                        :data="CharmRomeData.tableData"
                        border
                        height="660px">
                        <el-table-column
                            type="index"
                            align= "center"
                            label="Index"
                            width="100">
                        </el-table-column>
                        <el-table-column
                            prop="stepsName"
                            align= "center"
                            label="错误步骤"
                            width="200">
                        </el-table-column>
                        <el-table-column
                            prop="errorMsg"
                            align= "center"
                            label="错误信息">
                        </el-table-column>
                        <el-table-column
                            prop="updateTime"
                            align= "center"
                            label="错误时间"
                            width="200">
                        </el-table-column>
                        </el-table>
                    </div>
                </template>
            </el-card>
            <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
            <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
            <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" :disabled="StepsRomeData.saveDisabled" @click="SaveData()">保存</el-button>
      
    </el-drawer>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../../../../js/Logger.js";
import Sortable from 'sortablejs';

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            StepsRomeData:{
                active:0,
                stepLength:2,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
                saveDisabled:false,
            },
            BaseRomeData:{
                eventId:'',
                eventName: '',
                eventLogo: '',
                remarks:'',
                rules: {
                    eventName: [
                        { required: true, message: '请输入事件名称', trigger: 'blur' },
                        { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
                    ],
                    eventLogo: [
                        { required: true, message: '请输入事件标识', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                }
            },
            OperationRomeData:{
                tableData:[]
            },
            CharmRomeData:{
                title:'',
                tableData:[],
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
                this.ClearStepsRomeData();
                this.ClearBaseRomeData();
                this.ClearOperationRomeData();

                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew
                
                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.BaseRomeData.eventId =newval.eventId;
                    self.LoadData(self.BaseRomeData.eventId);
                    // self.RomeData.eventName =newval.eventName;
                    // self.RomeData.eventLogo =newval.eventLogo;
                    // self.RomeData.remarks =newval.remarks;
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听步骤
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
               
            }else if(newVal==1){
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Save = false;
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
            this.$emit('Succeed');//回调查询
        },
        //导航条事件
        next() {//下一步
            let self = this;
            PrintConsole('当前',self.StepsRomeData.active)
            if(self.StepsRomeData.active==0){//基本用例数据
                // self.StepsRomeData.active++;
                this.$refs['BaseRomeData'].validate((valid) => {
                    if (valid) {//通过
                        self.StepsRomeData.active++;
                        self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                            self.rowDrop();
                        })
                    } 
                });
            }else if(self.StepsRomeData.active==1){
                self.StepsRomeData.active++;
                self.CharmEventData();
            }
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            if(self.StepsRomeData.active==0){

            }else if(self.StepsRomeData.active==3){
                self.StepsRomeData.active--;
                self.StepsRomeData.active--;
            }
            else{
                self.StepsRomeData.active--;
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
            // self.resetForm('RomeData');
            self.StepsRomeData.active= 0;
            self.StepsRomeData.disPlay_Save = false;
            self.StepsRomeData.disPlay_Next = true;
            self.StepsRomeData.saveDisabled = false;
            self.StepsRomeData.processStatus ='process';
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        submitForm(formName,id) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveData();
                } 
            });
        },


        //事件信息
        ClearBaseRomeData(){
            let self = this;
            self.BaseRomeData.eventId='';
            self.BaseRomeData.eventName='';
            self.BaseRomeData.eventLogo='';
            self.BaseRomeData.remarks='';
        },

        //操作信息
        ClearOperationRomeData(){
            let self = this;
            self.OperationRomeData.tableData=[];
        },
        AddTable(){
            let self = this;
            let obj = {};
            obj.state=true;
            obj.label ='';
            obj.value='';
            obj.remarks='';

            self.OperationRomeData.tableData.push(obj);
            self.rowDrop();
        },
        handleDelete(index,row){
            let self = this;
            self.OperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        },
        rowDrop() {//排序方法
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#ComponentSet > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.OperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.OperationRomeData.tableData.splice(newIndex, 0, currRow);
                    // console.log(self.RomeData.TableData);
                }
            });
        },

        //验证事件
        CharmEventData(){//验证API接口数据的完整性
            let self = this;
            self.StepsRomeData.saveDisabled = true;
            self.CharmRomeData.tableData = [];
            self.CharmRomeData.title = '';
            self.$axios.post('/api/UiElementEvent/CharmEventData',{
                'CharmType':self.isAddNew,
                'baseData':{
                    'eventId':self.BaseRomeData.eventId,
                    'eventName':self.BaseRomeData.eventName,
                    'eventLogo':self.BaseRomeData.eventLogo,
                },
                'OperationData':self.OperationRomeData.tableData
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.stepsName =d.stepsName;
                        obj.errorMsg = d.errorMsg;
                        obj.updateTime = d.updateTime;
                        self.CharmRomeData.tableData.push(obj);
                    });
                    if(self.CharmRomeData.tableData.length!=0){
                        self.StepsRomeData.processStatus='error';
                        self.CharmRomeData.title = '效验结果:失败,共发现错误数:'+self.CharmRomeData.tableData.length;
                    }else{
                        self.StepsRomeData.active++;
                        self.CharmRomeData.title = '效验结果:完成,请点击保存';
                        self.StepsRomeData.saveDisabled = false;
                    }
                }else{
                    self.$message.error('效验元素操作事件信息发生错误:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                self.$message.error(error);
            })
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/UiElementEvent/SaveData',{
                    'baseData':{
                        'eventName':self.BaseRomeData.eventName,
                        'eventLogo':self.BaseRomeData.eventLogo,
                        'remarks':self.BaseRomeData.remarks,
                    },
                    'OperationData':self.OperationRomeData.tableData
                }).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增元素事件成功');
                    self.dialogClose();
                }
                else{
                    self.$message.error('新增元素事件失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/UiElementEvent/EditData',{
                    'baseData':{
                        'eventId':self.BaseRomeData.eventId,
                        'eventName':self.BaseRomeData.eventName,
                        'eventLogo':self.BaseRomeData.eventLogo,
                        'remarks':self.BaseRomeData.remarks,
                    },
                    'OperationData':self.OperationRomeData.tableData
                }).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('修改元素事件成功!');
                    self.dialogClose();
                }
                else{
                    self.$message.error('修改元素事件失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        LoadData(eventId){
            let self = this;
            self.loading=true;
            self.$axios.get('/api/UiElementEvent/LoadData',{
                params:{
                  'eventId':eventId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.BaseRomeData.eventName = res.data.baseData.eventName;
                    self.BaseRomeData.eventLogo = res.data.baseData.eventLogo;
                    self.BaseRomeData.remarks = res.data.baseData.remarks;
                    self.OperationRomeData.tableData = res.data.componentTable;
                    self.loading=false;
                }else{
                    self.loading=false;
                    self.$message.error('数据加载失败:'+res.data.errorMsg);
                    self.dialogClose();
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
                self.dialogClose();
            })
        },
    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
</style>
