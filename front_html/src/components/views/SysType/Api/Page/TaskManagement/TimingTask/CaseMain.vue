<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="1500px">
            <template>
                <el-form :inline="true"  method="post">
                    <el-form-item label="所属页面:">
                        <el-select v-model="RomeData.pageId" clearable placeholder="请选择" style="width:200px;" @click.native="GetPageNameOption()">
                            <el-option
                                v-for="item in RomeData.pageNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="所属功能:">
                        <el-select v-model="RomeData.funId" clearable placeholder="请选择" style="width:200px;" @click.native="GetFunNameOption()">
                            <el-option
                                v-for="item in RomeData.funNameOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button type="primary" @click="SelectData()">查询</el-button>
                    <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                </el-form>
            </template>
            <template>
                <el-table
                    v-loading="loading"
                    :data="RomeData.tableData"
                    height="510px"
                    border
                    ref="multipleTable"
                    @selection-change="handleSelectionChange"
                    @row-click="handleRowClick">
                    <el-table-column
                        type="selection"
                        align= "center"
                        width="50">
                    </el-table-column>
                    <el-table-column
                        label="测试类型"
                        align= "center"
                        width="100px">
                        <template slot-scope="scope">
                            <el-tag type="info" v-if="scope.row.testType=='UnitTest'" >单元测试</el-tag>
                            <el-tag type="warning" v-else-if="scope.row.testType=='HybridTest'" >混合测试</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column
                        label="用例名称"
                        align= "center"
                        prop="caseName">
                    </el-table-column>
                    <el-table-column
                        label="所属页面"
                        width="200px"
                        align= "center"
                        prop="pageName">
                    </el-table-column>
                    <el-table-column
                        label="所属功能"
                        width="200px"
                        align= "center"
                        prop="funName">
                    </el-table-column>
                    <el-table-column
                        label="接口数量"
                        width="100px"
                        align= "center"
                        prop="apiTotal">
                    </el-table-column>
                    <el-table-column
                        label="接口状态"
                        align= "center"
                        width="100">
                        <template slot-scope="scope">
                            <el-tag type="warning" v-if="scope.row.caseState=='InDev'" >研发中</el-tag>
                            <el-tag type="success" v-else-if="scope.row.caseState=='Completed'" >已完成</el-tag>
                            <el-tag type="info" v-else>弃用</el-tag>
                        </template>
                    </el-table-column>
                     <el-table-column
                        label="通过率"
                        width="100px"
                        align= "center"
                        prop="passRate">
                    </el-table-column>
                    <el-table-column
                        label="修改者"
                        width="150px"
                        align= "center"
                        prop="userName">
                    </el-table-column>
                    <el-table-column
                        label="更新时间"
                        width="160px"
                        align= "center"
                        prop="updateTime">
                    </el-table-column>
                </el-table>
            </template>
            <div style="margin-top:20px;margin-left:950px;">
                <el-button type="info"  @click="dialogClose()">取消</el-button>
                <el-button type="success" @click="AddToSortCaseTable()">{{RomeData.buttonConfirm}}</el-button>
            </div>
    </el-dialog>
</template>

<script>
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                tableData:[],
                multipleSelection:[],
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                buttonConfirm:'确认',
                passCaseId:[],
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
                this.RomeData.passCaseId = newval.passCaseId;
                this.SelectData();
            }
        },
        'RomeData.multipleSelection': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                if(newVal==0){
                    self.RomeData.buttonConfirm='确认';
                }else{
                    self.RomeData.buttonConfirm='确认('+self.RomeData.multipleSelection.length+')';
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
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.RomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            this.RomeData.funNameOption = [];
            if(this.RomeData.pageId){
                GetFunNameItems('API',this.$cookies.get('proId'),this.RomeData.pageId).then(d=>{
                    this.RomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        SelectData(passCaseId){
            let self = this;
            self.RomeData.tableData= [];
            self.loading=true;
            self.$axios.get('/api/ApiTimingTask/SelectCaseData',{
                params:{
                    "proId":self.$cookies.get('proId'),
                    "pageId":self.RomeData.pageId,
                    "funId":self.RomeData.funId,
                    "passCaseId":self.RomeData.passCaseId.join(','),//需要忽略不显示在页面上的数据
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.testType =d.testType;
                        obj.pageName =d.pageName;
                        obj.funName =d.funName;
                        obj.caseName = d.caseName;
                        obj.apiTotal=d.apiTotal;
                        obj.caseState = d.caseState;
                        obj.passRate=d.passRate+'%';
                        obj.userName = d.userName;   
                        obj.updateTime=d.updateTime;

                        self.RomeData.tableData.push(obj);
                    });
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                    self.dialogClose();
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
                self.dialogClose();
            })
        },
        handleRowClick(row, column, event){//点击行选择勾选框
          this.$refs.multipleTable.toggleRowSelection(row);
        },
        handleSelectionChange(val){//勾选数据时触发
            // console.log(val)
            this.RomeData.multipleSelection=[];
            val.forEach(d =>{
                this.RomeData.multipleSelection.push(d);
            }); 
        },
        AddToSortCaseTable(){
            let self = this;
            if(self.RomeData.multipleSelection.length==0){
                self.$message.warning('未选择1条接用例数据进行保存!');
            }else{
                // console.log(self.RomeData.multipleSelection)
                self.$emit('getData',self.RomeData.multipleSelection);//回调传值
                self.dialogClose();
            }
        },
        ClearSelectRomeData(){
            let self = this;
            self.RomeData.pageId='';
            self.RomeData.funId='';
            self.SelectData();
        },
        ClearRomeData(){
            let self = this;
            self.RomeData.pageId='';
            self.RomeData.funId='';
            self.RomeData.passCaseId=[];
        },

    }
};
</script>

<style>

</style>
