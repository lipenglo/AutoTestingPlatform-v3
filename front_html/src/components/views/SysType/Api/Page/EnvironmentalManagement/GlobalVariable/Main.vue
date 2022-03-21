<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 775px;">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="变量类型:">
                            <el-select v-model="SelectRomeData.globalType" clearable placeholder="请选择" style="width:200px;">
                                <el-option
                                    v-for="item in SelectRomeData.globalTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="变量名称:">
                            <el-input clearable v-model.trim="SelectRomeData.globalName"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </div>
                <div>
                    <div>
                        <el-table
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
                                label="变量类型"
                                width="150px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="info" v-if="scope.row.globalType=='0'" >普通变量</el-tag>
                                    <el-tag type="success" v-else-if="scope.row.globalType=='1'">全局变量</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="变量名称"
                                align= "center"
                                prop="globalName">
                            </el-table-column>
                            <el-table-column
                                show-overflow-tooltip
                                label="变量值"
                                align= "center"
                                prop="globalValue">
                            </el-table-column>
                            <el-table-column
                                label="备注"
                                align= "center"
                                prop="remarks">
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
                                <el-button
                                    size="mini"
                                    @click="handleEdit(scope.$index, scope.row)">Edit
                                </el-button>
                                <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">Delete
                                </el-button>
                            </template>
                            </el-table-column>
                        </el-table>
                    </div>
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
            tableData: [],
            SelectRomeData:{
                globalType:'',
                globalName:'',
                globalTypeOption:[
                    {'label':'普通变量','value':0},
                    {'label':'全局变量','value':1},
                ],
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
            self.$axios.get('/api/GlobalVariable/SelectData',{
                params:{
                    'sysType':'API',
                    'proId':self.$cookies.get('proId'),
                    'globalType':self.SelectRomeData.globalType,
                    'globalName':self.SelectRomeData.globalName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                res.data.TableData.forEach(d => {
                    let obj = {};
                    obj.id =d.id;
                    obj.globalType = d.globalType;
                    obj.globalName = d.globalName;
                    obj.globalValue = d.globalValue;
                    obj.remarks = d.remarks;
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
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增变量",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑变量",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                globalId:row.id,
                globalType:row.globalType,
                globalName:row.globalName,
                globalValue:row.globalValue,
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
            self.$axios.post('/api/GlobalVariable/DeleteData',Qs.stringify({
                'globalId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('变量删除成功!');
                self.SelectData();
            }
            else{
                self.$message.error('变量删除失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.globalName='';
            self.SelectRomeData.globalType='';
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
