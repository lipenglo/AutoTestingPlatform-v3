<template>
    <div ref="tab-main"  id="tab-main">
        <el-tabs type="border-card" style="height:850px">
            <el-tab-pane label="角色管理">
                <template>
                    <el-form :inline="true" class="demo-form-inline" method="post">
                        <el-form-item label="角色名称:">
                            <el-input clearable v-model.trim="SelectRomeData.roleName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </template>
                <template>
                    <el-table
                        :data="tableData"
                        height="596px"
                        border>
                        <el-table-column
                            label="ID"
                            align= "center"
                            width="80px"
                            prop="id">
                        </el-table-column>
                        <el-table-column
                            label="角色名称"
                            width="300px"
                            align= "center"
                            prop="roleName">
                        </el-table-column>  
                        <el-table-column
                            label="绑定用户"
                            align= "center"
                            prop="bindUsers">
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
                            width="200px">
                        <template slot="header">
                            <el-button-group>
                                <el-button type="primary" @click="OpenEditDialog()">新增角色</el-button>
                            </el-button-group>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                            <el-button-group>
                                <el-button
                                    size="mini"
                                    type="warning"
                                    @click="OpenPermissionsDialog(scope.$index, scope.row)">权限
                                </el-button>
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
        <template>
            <dialog-editor
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.ediror.dialogVisible" 
                :dialogPara="dialog.ediror.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
        </template>
        <template>
            <dialog-permissions
                @closeDialog="closePermissionsDialog" 
                :isVisible="dialog.permissions.dialogVisible" 
                :dialogPara="dialog.permissions.dialogPara"
                @Succeed="SelectData">
            </dialog-permissions>
        </template>
    </div>
</template>

<script>
import Qs from 'qs'
import store from '../../../../store/index'
import DialogEditor from "./Editor.vue"
import DialogPermissions from "./Permissions.vue"

export default {
    components: {
        DialogEditor,DialogPermissions,
    },
    data() {
        return {
            tableData:[],
            multipleSelection:[],
            SelectRomeData:{
                roleName:'',
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
                permissions:{//权限
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
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
            self.$axios.get('/api/role/SelectData',{
                params:{
                    'roleName':self.SelectRomeData.roleName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                res.data.TableData.forEach(d => {
                    let obj = {};
                    obj.id =d.id;
                    obj.roleName = d.roleName;
                    obj.bindUsers = d.bindUsers;
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

        handleEdit(index,row){
            this.dialog.ediror.dialogPara={
                dialogTitle:"编辑角色",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                roleId:row.id,
                roleName:row.roleName,
            }
            this.dialog.ediror.dialogVisible=true;
        },
        DeleteData(roleId){
            let self = this;
            self.$axios.post('/api/role/DeleteData',Qs.stringify({
                'roleId':roleId
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
        handleDelete(index,row){
            this.$confirm('如该角色下有绑定用户,删除角色后绑定用户会成为游客,请确定是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.DeleteData(row.id);     
                }).catch(() => {       
            });
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.roleName='';
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

        //Dialog
        closeEditDialog(){
            this.dialog.ediror.dialogVisible =false;
        },
        OpenEditDialog(){
            this.dialog.ediror.dialogPara={
                dialogTitle:"新增角色",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            this.dialog.ediror.dialogVisible=true;
        },

        closePermissionsDialog(){
            this.dialog.permissions.dialogVisible =false;
        },
        OpenPermissionsDialog(index,row){
            this.dialog.permissions.dialogPara={
                dialogTitle:"修改权限",//初始化标题
                roleId:row.id,//初始化是否新增\修改
            }
            this.dialog.permissions.dialogVisible=true;
        },

    }
};
</script>

<style>


</style>
