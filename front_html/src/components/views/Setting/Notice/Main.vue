<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <el-tabs type="border-card" style="height:850px">
                <el-tab-pane label="公告管理">
                    <template>
                        <el-form :inline="true" class="demo-form-inline" method="post">
                            <el-form-item label="公告简介:">
                                <el-input clearable v-model.trim="SelectRomeData.abstract"></el-input>
                            </el-form-item>
                            <el-button type="primary" @click="SelectData()">查询</el-button>
                            <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                        </el-form>
                    </template>
                    <template>
                        <el-table
                            :data="tableData"
                            height="670px"
                            border>
                            <el-table-column
                                label="ID"
                                align= "center"
                                width="80px"
                                prop="id">
                            </el-table-column>
                            <el-table-column
                                label="公告简介"
                                width="300px"
                                align= "center"
                                prop="abstract">
                            </el-table-column>  
                            <el-table-column
                                label="公告信息"
                                align= "center">
                                <template slot-scope="scope">
                                    <div style="white-space: pre-line;text-align: left;" v-html="scope.row.info"></div>
                                </template>
                            </el-table-column>
                                <el-table-column
                                label="状态"
                                width="100px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.state">展示中</el-tag>
                                    <el-tag type="info" v-else>不展示</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="更新时间"
                                align= "center"
                                width="200px"
                                prop="updateTime">
                            </el-table-column>
                            <el-table-column
                                label="修改者"
                                align= "center"
                                width="200px"
                                prop="userName">
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="150px">
                            <template slot="header">
                                <el-button-group>
                                    <el-button type="primary" @click="OpenEditDialog()">新增公告</el-button>
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
                    </template>
                    <template>
                        <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                            @size-change="pageSizeChange"
                            @current-change="handleCurrentChange"
                            :current-page="page.current" 
                            :total="page.total"
                            :page-sizes = [10,30,50,100]
                            style="margin: 20px auto auto auto;">
                        </el-pagination>
                    </template>
                </el-tab-pane>
            </el-tabs>
        </template>
        <template>
            <dialog-editor
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.ediror.dialogVisible" 
                :dialogPara="dialog.ediror.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import store from '../../../../store/index';
import DialogEditor from "./Editor.vue";

export default {
    components: {
        DialogEditor
    },
    data() {
        return {
            tableData:[],
            SelectRomeData:{
              abstract:'',
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },
            dialog:{
                ediror:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    }
                },
            },
        };
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/Notice/SelectData',{
                params:{
                    'abstract':self.SelectRomeData.abstract,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                res.data.TableData.forEach(d => {
                    let obj = {};
                    obj.id =d.id;
                    obj.abstract = d.abstract;
                    obj.info = d.info;
                    obj.state = d.state;
                    obj.updateTime = d.updateTime;
                    obj.userName = d.userName;

                    self.tableData.push(obj);
                });
                if(self.tableData.length==0 && self.page.current != 1){
                    self.page.current = 1;
                    self.SelectData();
                }
                self.page.total = res.data.Total;
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.abstract='';
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
            self.page.current=val
            self.SelectData();
        },
        handleEdit(index,row){
            this.dialog.ediror.dialogPara={
                dialogTitle:"修改公告",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                noticeId:row.id,
                abstract:row.abstract,
                info:row.info,
                state:row.state,
            }
            this.dialog.ediror.dialogVisible=true;
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
        DeleteData(noticeId){
            let self = this;
            self.$axios.post('/api/Notice/DeleteData',Qs.stringify({
                'noticeId':noticeId
            })).then(res => {
                if(res.data.statusCode ==2003){
                    self.$message.success('删除成功!');
                    self.SelectData();
                }
                else{
                    self.$message.error('删除失败:'+ res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },

        //Dialog
        closeEditDialog(){
            this.dialog.ediror.dialogVisible =false;
        },
        OpenEditDialog(){
            this.dialog.ediror.dialogPara={
                dialogTitle:"新增公告",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            this.dialog.ediror.dialogVisible=true;
        },
    }
};
</script>

<style>
.test{
    
}

</style>
