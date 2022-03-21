<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div class="MainCard">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="所属页面:">
                            <el-select v-model="SelectRomeData.pageId" clearable placeholder="请选择" style="width:200px;" @click.native="GetPageNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.pageNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="功能名称:">
                            <el-input clearable v-model.trim="SelectRomeData.funName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </div>
                <div>
                    <el-table
                        v-loading="loading"
                        :data="tableData"
                        height="619px"
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
                            align= "center"
                            width="80px"
                            prop="id">
                        </el-table-column>
                        <el-table-column
                            label="所属页面"
                            align= "center"
                            prop="pageName">
                        </el-table-column>
                        <el-table-column
                            label="功能名称"
                            align= "center"
                            prop="funName">
                        </el-table-column>
                        <el-table-column
                            label="备注"
                            align= "center"
                            prop="remarks">
                        </el-table-column>         
                        <el-table-column
                            label="元素数量"
                            width="100px"
                            align= "center"
                            prop="elementTotal">
                        </el-table-column>
                        <el-table-column
                            label="更新时间"
                            align= "center"
                            width="200px"
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
                            width="200px">
                        <template slot="header">
                            <el-button-group>
                                <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                <el-button type="warning" @click="OpenHistoryInfoDialog()">历史恢复</el-button>
                            </el-button-group>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                            <el-button-group>
                                <el-button
                                    size="mini"
                                    @click="handleEdit(scope.$index, scope.row)">Edit
                                </el-button>
                                <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">Delete
                                </el-button>
                            </el-button-group>
                        </template>
                        </el-table-column>
                    </el-table>
                </div>
                <div style="margin-top:30px">
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
import DialogEditor from "./Editor.vue";
import {GetPageNameItems} from "../../../../../js/GetSelectTable.js";
import DialogHistoryInfo from "./HistoryInfo.vue";

export default {
    components: {
        DialogEditor,DialogHistoryInfo
    },
    data() {
        return {
            loading:false,
            tableData: [],
            multipleSelection:[],
            SelectRomeData:{
                pageId:'',
                pageNameOption:[],
                funName:'',
            },
            RomeData:{
    
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
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
     
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.loading=true;
            self.tableData= [];
            self.$axios.get('/api/FunManagement/SelectData',{
                params:{
                    'sysType':'UI',
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.SelectRomeData.pageId,
                    'funName':self.SelectRomeData.funName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.pageId=d.pageId;
                        obj.pageName = d.pageName;
                        obj.funName = d.funName;
                        obj.remarks = d.remarks;
                        obj.elementTotal = d.elementTotal;
                        obj.updateTime = d.updateTime;
                        obj.userName = d.userName;

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
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
        GetPageNameOption(){
            GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                this.SelectRomeData.pageNameOption = d;
            });
        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增功能",//初始化标题
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
                funId:self.multipleSelection[0],
            }
            self.dialog.historyInfo.dialogVisible=true;
        }
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑功能",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                funId:row.id,
                pageId:row.pageId,
                funName:row.funName,
                remarks:row.remarks,
            }
            self.dialog.editor.dialogVisible=true;
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
            self.$axios.post('/api/FunManagement/DeleteData',Qs.stringify({
                'sysType':'UI',
                'funId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('删除功能成功!');
                self.SelectData();
            }
            else{
                self.$message.error('删除功能失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funName='';
            self.SelectData();
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
