<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 775px;">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="数据库类型:">
                            <el-select v-model="SelectRomeData.dbType" clearable placeholder="请选择" style="width:200px;float:left">
                                <el-option
                                    v-for="item in SelectRomeData.dbTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="IP:">
                            <el-input clearable v-model.trim="SelectRomeData.dataBaseIp"></el-input>
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
                        border>
                        <el-table-column
                            label="ID"
                            align= "center"
                            width="80px"
                            prop="id">
                        </el-table-column>
                        <el-table-column
                            label="数据库类型"
                            width="150px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="info">{{scope.row.dbType}}</el-tag>
                            </template>
                        </el-table-column> 
                        <el-table-column
                            label="IP"
                            align= "center"
                            prop="dataBaseIp">
                        </el-table-column>
                        <el-table-column
                            label="端口"
                            align= "center"
                            prop="port">
                        </el-table-column>
                        <el-table-column
                            label="用户名"
                            align= "center"
                            prop="dbUser">
                        </el-table-column>
                        <el-table-column
                            label="备注"
                            align= "center"
                            prop="remarks">
                        </el-table-column>
                        <el-table-column
                            label="状态"
                            width="150px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.state" >正常</el-tag>
                                <el-tag type="danger" v-else>异常</el-tag>
                            </template>
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
                            width="160px">
                        <template slot="header">
                            <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
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
    </div>
</template>

<script>
import Qs from 'qs';
import DialogEditor from "./Editor.vue";

export default {
    components: {
        DialogEditor,
    },
    data() {
        return {
            loading:false,
            tableData: [],
            SelectRomeData:{
                dbType:'',
                dbTypeOption:[
                    {'label':'MySql','value':'MySql'}
                ],
                dataBaseIp:'',
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
            self.loading=true;
            self.$axios.get('/api/DataBaseEnvironment/SelectData',{
                params:{
                    // 'proId':self.$cookies.get('proId'),
                    'dbType':self.SelectRomeData.dbType,
                    'dataBaseIp':self.SelectRomeData.dataBaseIp,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.dbType = d.dbType;
                        obj.dataBaseIp = d.dataBaseIp;
                        obj.port=d.port;
                        obj.dbUser = d.dbUser;
                        obj.dbpwd = d.dbpwd;
                        obj.remarks = d.remarks;
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
                    self.loading=false;
                }
                else{
                    self.$message.error('列表数据获取失败:'+res.data.errorMsg);
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
                dialogTitle:"新增数据库",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑数据库",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                dbId:row.id,
                dbType:row.dbType,
                dataBaseIp:row.dataBaseIp,
                port:row.port,
                dbUser:row.dbUser,
                dbpwd:row.dbpwd,
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
            self.$axios.post('/api/DataBaseEnvironment/DeleteData',Qs.stringify({
                'dbId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('数据库删除成功!');
                self.SelectData();
            }
            else{
                self.$message.error('数据库删除失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.dbType='';
            self.SelectRomeData.dataBaseIp='';
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
    }
};
</script>

<style>

</style>
