<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height:760px;">
                <div style="margin-top:15px">
                    <div>
                        <el-form :inline="true"  method="post">
                            <el-form-item label="项目名称:">
                                <el-input clearable v-model.trim="RomeData.proName"></el-input>
                            </el-form-item>
                            <el-button type="primary" @click="SelectData()">查询</el-button>
                            <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                        </el-form>
                    </div>
                    <div>
                        <el-table
                            v-loading="loading"
                            :data="RomeData.tableData"
                            height="596px"
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
                                label="ID"
                                prop="id"
                                align= "center"
                                width="80px">
                            </el-table-column>
                            <el-table-column 
                                label="详情" 
                                width="50px"
                                type="expand">
                                <template slot-scope="props">
                                    <el-form label-position="left" >
                                        <el-table
                                            :data="props.row.tableItem"
                                            border>
                                            <el-table-column
                                                label="关联成员"
                                                align= "center">
                                                <template slot-scope="scope">
                                                    <el-tag type="info" style="margin:0 5px"
                                                        v-for="item in scope.row.bindMembers"
                                                        :index="item.id" :key="item.name"
                                                        >{{item.name}}
                                                    </el-tag>
                                                </template>
                                            </el-table-column>
                                            <el-table-column
                                                label="创建人"
                                                align= "center"
                                                width="160px"
                                                prop="createUserName">
                                            </el-table-column>
                                            <el-table-column
                                                label="创建时间"
                                                width="160px"
                                                prop="createTime"
                                                align= "center">
                                            </el-table-column>
                                        </el-table>
                                    </el-form>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="项目名称"
                                align= "center"
                                prop="proName">
                            </el-table-column>
                            <el-table-column
                                label="备注"
                                width="300px"
                                align= "center"
                                prop="remarks">
                            </el-table-column>
                            <el-table-column
                                label="接口数量"
                                width="80px"
                                align= "center"
                                prop="apiTotal">
                            </el-table-column>
                            <el-table-column
                                label="单元/混合"
                                width="100px"
                                align= "center"
                                prop="caseTotal">
                            </el-table-column>
                            <el-table-column
                                label="定时任务"
                                width="80px"
                                align= "center"
                                prop="taskTotal">
                            </el-table-column>
                            <el-table-column
                                label="批量任务"
                                width="80px"
                                align= "center"
                                prop="batchTotal">
                            </el-table-column>
                            <el-table-column
                                label="本周执行"
                                width="100px"
                                align= "center"
                                prop="performWeekTotal">
                            </el-table-column>
                            <el-table-column
                                label="历史执行"
                                width="100px"
                                align= "center"
                                prop="perforHistoryTotal">
                            </el-table-column>
                            <el-table-column
                                label="更新时间"
                                align= "center"
                                width="160px"
                                prop="updateTime">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="修改者"
                                align= "center"
                                width="150px"
                                prop="userName">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="255px">
                                <template slot="header">
                                    <el-button-group>
                                        <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                        <el-button type="warning" @click="OpenHistoryInfoDialog()">历史恢复</el-button>
                                    </el-button-group>
                                </template>
                                <template slot-scope="scope" style="width:100px">
                                    <el-button-group>
                                        <el-button
                                            :disabled="scope.row.isEnterInto"
                                            size="mini"
                                            type="success"
                                            @click="handleEnterInto(scope.$index, scope.row)">进入
                                        </el-button>
                                        <el-button
                                            :disabled="scope.row.isMembers"
                                            size="mini"
                                            type="warning"
                                            @click="handleMembers(scope.$index, scope.row)">成员
                                        </el-button>
                                        <el-button
                                            :disabled="scope.row.isEdit"
                                            size="mini"
                                            @click="handleEdit(scope.$index, scope.row)">Edit
                                        </el-button>
                                        <el-button
                                            :disabled="scope.row.isDelete"
                                            size="mini"
                                            type="danger"
                                            @click="handleDelete(scope.$index, scope.row)">Delete
                                        </el-button>
                                    </el-button-group>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                    <div style="margin-top:40px">
                        <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                            @size-change="pageSizeChange"
                            @current-change="handleCurrentChange"
                            :current-page="page.current" 
                            :total="page.total"
                            :page-sizes = [10,30,50,100]
                            style="margin: 20px auto auto auto;">
                        </el-pagination>
                    </div>
                </div>
            </div>
        </template>
        <template>
            <dialog-editor
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
        <template>
            <dialog-members
                @closeDialog="closeMembersDialog" 
                :isVisible="dialog.members.dialogVisible" 
                :dialogPara="dialog.members.dialogPara"
                @Succeed="SelectData">
            </dialog-members>
        </template>
        <template>
            <dialog-history-info
                @closeDialog="closeHistoryInfoDialog" 
                :isVisible="dialog.historyInfo.dialogVisible" 
                :dialogPara="dialog.historyInfo.dialogPara"
                @Succeed="SelectData">
            </dialog-history-info>
        </template>
    </div>
</template>

<script>
import Qs from 'qs'
import { PrintConsole } from '../../../../js/Logger';

import DialogEditor from "./Editor.vue";
import DialogMembers from "./Members.vue";
import DialogHistoryInfo from "./HistoryInfo.vue";

export default {
    components: {
        DialogEditor,DialogMembers,DialogHistoryInfo
    },
    data() {
        return {
            loading:false,
            multipleSelection:[],
            RomeData:{
                proName:'',
                tableData:[],
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },
            dialog:{
                editor:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                members:{//成员
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
                historyInfo:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                }
            },
        };
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        ClearSelectRomeData(){
            let self = this;
            self.RomeData.proName='';

            self.SelectData();
        },
        handleRowClick(row, column, event){//点击行选择勾选框
          this.$refs.multipleTable.toggleRowSelection(row);
        },
        handleSelectionChange(val){//勾选数据时触发
            // console.log(val)
            this.multipleSelection=[];
            val.forEach(d =>{
                this.multipleSelection.push(d.id);
            }); 
        },
        SelectData(){
            let self = this;
            self.loading=true;
            self.RomeData.tableData= [];
            self.$axios.get('/api/ProjectManagement/SelectData',{
                params:{
                    'sysType':'API',
                    'proName':self.RomeData.proName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.proName = d.proName;
                        obj.remarks = d.remarks;
                        // obj.bindMembers=d.bindMembers;
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;
                        // obj.createUserName = d.createUserName;
                        obj.isEnterInto=d.isEnterInto;
                        obj.isMembers=d.isMembers;
                        obj.isEdit = d.isEdit;
                        obj.isDelete = d.isDelete;
                        obj.apiTotal=d.apiTotal;
                        obj.caseTotal=d.caseTotal;
                        obj.taskTotal=d.taskTotal;
                        obj.batchTotal=d.batchTotal;
                        obj.performWeekTotal=d.performWeekTotal;
                        obj.perforHistoryTotal=d.perforHistoryTotal;
                        obj.tableItem=d.tableItem;

                        self.RomeData.tableData.push(obj);
                    });
                    if(self.RomeData.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增项目",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        closeHistoryInfoDialog(){
            this.dialog.historyInfo.dialogVisible =false;
        },
        OpenHistoryInfoDialog(){
            let self = this;
            if(self.multipleSelection.length>1){
                self.$message.warning('只可勾选1条数据或不勾选数据进行历史查看及恢复!');
            }else{
                self.dialog.historyInfo.dialogPara={
                    dialogTitle:"历史恢复",//初始化标题
                    proId:self.multipleSelection[0],
                }
                self.dialog.historyInfo.dialogVisible=true;
            }
        },
        closeMembersDialog(){
            this.dialog.members.dialogVisible =false;
        },
        handleEnterInto(index,row){//进入
            let self = this;
            self.$axios.get('/api/ProjectManagement/VerifyEnterInto',{
                params:{
                    'sysType':'API',
                    'proId':row.id,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.$cookies.set('proId',row.id,"0") 
                    self.$cookies.set('proName',row.proName,"0") 
                    self.$router.push({path:'/SysType/Api/Page/Home'});
                }else{
                    self.$message.error('验证进入项目权限失败:'+res.data.errorMsg);
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleMembers(index,row){
            let self = this;
            self.dialog.members.dialogPara={
                dialogTitle:"成员维护",//初始化标题
                proId:row.id,
            }
            self.dialog.members.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑项目",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                proId:row.id,
                proName:row.proName,
                remarks:row.remarks,
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleDelete(index,row){
            this.$confirm('请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                   this.DeleteData(row.id);     
                }).catch(() => {       
            });
        },
        DeleteData(id){
            let self = this;
            self.$axios.post('/api/ProjectManagement/DeleteData',Qs.stringify({
                "sysType":'API',
                'proId':id,
            })).then(res => {
                if(res.data.statusCode ==2003){
                    self.$message.success('项目删除成功!');
                    self.SelectData();
                }
                else{
                    self.$message.error('项目删除失败:'+ res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        pageSizeChange(pageSize) {
            let self = this;
            self.page.current = 1;
            self.page.pageSize = pageSize;
        },
        // 显示第几页
        handleCurrentChange(val) {
            let self = this;
            // 改变默认的页数
            self.page.current=val;
            self.SelectData();
        },
       
    }
};
</script>

<style>
</style>
