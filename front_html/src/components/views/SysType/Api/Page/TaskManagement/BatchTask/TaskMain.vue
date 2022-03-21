<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="1100px">
            <template>
                <el-form :inline="true"  method="post">
                    <el-form-item label="定时任务名称:">
                        <el-input clearable v-model.trim="RomeData.taskName"></el-input>
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
                        label="任务名称"
                        align= "center"
                        prop="taskName">
                    </el-table-column>
                    <el-table-column
                        label="用例数量"
                        width="100px"
                        align= "center"
                        prop="caseTotal">
                    </el-table-column>
                    <el-table-column
                        label="任务状态"
                        width="100px"
                        align= "center">
                        <template slot-scope="scope">
                            <el-tag type="success" v-if="scope.row.taskStatus" >启用</el-tag>
                            <el-tag type="danger" v-else>禁用</el-tag>
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
            <div style="margin-top:20px;margin-left:880px;">
                <el-button type="info"  @click="dialogClose()">取消</el-button>
                <el-button type="success" @click="AddToSortCaseTable()">{{RomeData.buttonConfirm}}</el-button>
            </div>
    </el-dialog>
</template>

<script>
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                taskName:'',
                tableData:[],
                multipleSelection:[],
                buttonConfirm:'确认',
                passTaskId:[],
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
                this.RomeData.passTaskId = newval.passTaskId;
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
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        SelectData(){
            let self = this;
            self.RomeData.tableData= [];
            self.loading=true;
            self.$axios.get('/api/ApiBatchTask/SelectTaskData',{
                params:{
                    "proId":self.$cookies.get('proId'),
                    "taskName":self.RomeData.taskName,
                    "passTaskId":self.RomeData.passTaskId.join(','),//需要忽略不显示在页面上的数据
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.taskName =d.taskName;
                        obj.caseTotal =d.caseTotal;
                        obj.taskState =d.taskState;
                        obj.passRate = d.passRate+'%';
                        obj.userName = d.userName;   
                        obj.updateTime = d.updateTime;   

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
                self.$message.warning('未选择1条接任务数据进行保存!');
            }else{
                // console.log(self.RomeData.multipleSelection)
                self.$emit('getData',self.RomeData.multipleSelection);//回调传值
                self.dialogClose();
            }
        },
        ClearRomeData(){
            let self = this;
            self.RomeData.taskName='';
            self.RomeData.passCaseId=[];
        },

    }
};
</script>

<style>

</style>
