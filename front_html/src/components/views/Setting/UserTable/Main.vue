<template>
     <div ref="tab-main"  id="tab-main">
         <template>
            <el-tabs type="border-card" style="height:850px">
                <el-tab-pane label="用户管理">
                    <template>
                        <el-form :inline="true" class="demo-form-inline" method="post">
                            <el-form-item label="用户名称:">
                                <el-input clearable v-model.trim="SelectRomeData.userName"></el-input>
                            </el-form-item>
                            <el-form-item label="账号状态:">
                                <el-select v-model="SelectRomeData.isLock" clearable placeholder="请选择" style="width:150px;">
                                    <el-option
                                        v-for="item in SelectRomeData.lockOption"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="激活状态:">
                                <el-select v-model="SelectRomeData.isActivation" clearable placeholder="请选择" style="width:150px;">
                                    <el-option
                                        v-for="item in SelectRomeData.activationOption"
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
                                label="头像"
                                align= "center"
                                width="100px">
                                <template slot-scope="scope">
                                    <el-avatar :size="50" fit="fill" :src="scope.row.userImage"></el-avatar>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="用户名"
                                align= "center"
                                prop="userName">
                            </el-table-column>
                            <el-table-column
                                label="昵称"
                                align= "center"
                                prop="nickName">
                            </el-table-column>
                            <el-table-column
                                label="Email"
                                align= "center"
                                prop="emails">
                            </el-table-column>         
                            <el-table-column
                                label="角色权限"
                                align= "center"
                                width="110px">
                                <template slot-scope="scope">
                                    <el-tag type="info" v-if="scope.row.roleName=='游客'">{{scope.row.roleName}}</el-tag>
                                    <el-tag type="success"  v-else>{{scope.row.roleName}}</el-tag>
                                </template>
                            </el-table-column>   
                            <el-table-column
                                label="激活状态"
                                align= "center"
                                width="100px">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.is_activation==1">激活</el-tag>
                                    <el-tag type="danger" v-else>未激活</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="是否禁用"
                                align= "center"
                                width="100px">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.is_lock==0">正常</el-tag>
                                    <el-tag type="warning" v-else>禁用</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                align="center"
                                width="260px">
                            <template slot="header">
                                <el-button type="primary" @click="openEditDialog()">新增</el-button>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button-group>
                                    <el-button
                                        v-if="scope.row.is_activation==0"
                                        size="mini"
                                        type="success"
                                        @click="handleActivation(scope.$index, scope.row)">激活
                                    </el-button>
                                    <el-button
                                        v-if="scope.row.is_lock==0"
                                        size="mini"
                                        type="info"
                                        @click="editIsLockState(scope.$index, scope.row,'1')">禁用
                                    </el-button>
                                    <el-button
                                        v-else
                                        size="mini"
                                        type="success"
                                        @click="editIsLockState(scope.$index, scope.row,'0')">启用
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
         </template>
         <template>
            <dialog-editor
                @closeDialog="closeEditDialog" 
                :isVisible="dialog.editor.dialogVisible" 
                :dialogPara="dialog.editor.dialogPara"
                @Succeed="SelectData">
            </dialog-editor>
         </template>
     </div>
</template>

<script>
import Qs from 'qs'
import DialogEditor from "./Editor.vue";

export default {
    components: {
        DialogEditor,
    },
    data() {
        return {
            tableData: [],
            multipleSelection: [],//勾选后被存进来的数据id
            SelectRomeData:{
                userName:'',
                isLock:'',
                lockOption:[
                    {'label':'正常','value':'0'},
                    {'label':'禁用','value':'1'},
                ],
                isActivation:'',
                activationOption:[
                    {'label':'激活','value':'1'},
                    {'label':'未激活','value':'0'},
                ],

            },
            RomeData:{
                id:'',
                userName: '',
                nickName:'',
                emails:'',
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
                }
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
            self.$axios.get('/api/userManagement/SelectData',{
                params:{
                    'userName':self.SelectRomeData.userName,
                    'isLock':self.SelectRomeData.isLock,
                    'isActivation':self.SelectRomeData.isActivation,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                res.data.TableData.forEach(d => {
                    let obj = {};
                    obj.id =d.id;
                    obj.userImage = 'data:image/png;base64,'+ d.userImage;
                    obj.userName = d.userName;
                    obj.nickName = d.nickName;
                    obj.emails = d.emails;
                    obj.roldId = d.roldId;
                    obj.roleName = d.roleName;
                    obj.is_lock = d.is_lock;
                    obj.is_activation = d.is_activation;

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
        handleActivation(index, row){//激活
            let self = this;
            self.$axios.post('/api/userManagement/UserActivation',Qs.stringify({
                'userId':row.id,
            })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('激活完成!');
                    self.SelectData();
                }
                else{
                    self.$message.error('激活失败:'+res.data.errormsg);
                    }
                }).catch(function (error) {
                    console.log(error);
            })
        },
        editIsLockState(index,row,state){//修改启用或禁用的状态
            let self = this;
            self.$axios.post('/api/userManagement/EditIsLockState',Qs.stringify({
                'userId':row.id,
                'state':state
            })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('用户状态修改成功!');
                    self.SelectData();
                }
                else{
                    self.$message.error('用户状态修改失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
            })
        },
        DeleteData(userId){
            let self = this;
            self.$axios.post('/api/userManagement/DeleteData',Qs.stringify({
                'userId':userId
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
        handleEdit(index,row){
            this.dialog.editor.dialogPara={
                dialogTitle:"编辑用户",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                userId:row.id,
                userName: row.userName,
                nickName:row.nickName,
                emails:row.emails,
                roleId:row.roldId,
            }
            this.dialog.editor.dialogVisible=true;
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
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.userName='';
            self.SelectRomeData.isLock='';
            self.SelectRomeData.isActivation='';
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
        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        openEditDialog(){
            this.dialog.editor.dialogPara={
                dialogTitle:"新增用户",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            this.dialog.editor.dialogVisible=true;
        },
    }
};
</script>

<style>
.el-table-column{
    width: 400px;
}
.el-input {
    float:left;
    /* width:300px; */
}
</style>
