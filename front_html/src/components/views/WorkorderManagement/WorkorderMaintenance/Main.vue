<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 775px;">
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
                        <el-form-item label="所属功能:">
                              <el-select v-model="SelectRomeData.funId" clearable placeholder="请选择" style="width:200px;" @click.native="GetFunNameOption()">
                                <el-option
                                    v-for="item in SelectRomeData.funNameOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="我的工单:">
                              <el-select v-model="SelectRomeData.myWork" clearable placeholder="请选择" style="width:100px;">
                                <el-option
                                    v-for="item in SelectRomeData.myWorkOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </div>
                <div>
                    <el-table
                        :data="tableData"
                        height="670px"
                        border>
                        <el-table-column
                            label="编号"
                            align= "center"
                            width="100px"
                            prop="codeId">
                        </el-table-column>
                        <el-table-column
                            label="工单来源"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="primary" v-if="scope.row.workSource==0">手工录入</el-tag>
                                <el-tag type="info"  v-else>系统录入</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="工单类型"
                            width="80px"
                            align= "center"
                            prop="workType">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.workType=='Add'">新增</el-tag>
                                <el-tag type="warning"  v-else-if="scope.row.workType=='Edit'">修改</el-tag>
                                <el-tag type="danger"  v-else-if="scope.row.workType=='Delete'">删除</el-tag>
                                <el-tag type="warning"  v-else-if="scope.row.workType=='BUG'">BUG</el-tag>
                                <el-tag type="info" v-else>其他</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="所属页面/功能"
                            width="300px"
                            align= "center"
                            prop="pageNameAndfunName">
                        </el-table-column>
                        <!-- <el-table-column
                            label="所属功能"
                            width="200px"
                            align= "center"
                            prop="funName">
                        </el-table-column> -->
                        <el-table-column
                            label="工单名称"
                            align= "center"
                            prop="workName">
                        </el-table-column>
                        <el-table-column
                            label="工单信息"
                            show-overflow-tooltip
                            align= "center"
                            prop="message">
                        </el-table-column>
                        <el-table-column
                            label="工单状态"
                            width="100px"
                            align= "center"
                            prop="workState">
                            <template slot-scope="scope">
                                <el-tag type="info" v-if="scope.row.workState==0">待受理</el-tag>
                                <el-tag type="danger" v-else-if="scope.row.workState==1">受理中</el-tag>
                                <el-tag type="warning" v-else-if="scope.row.workState==2">已解决</el-tag>
                                <el-tag type="success" v-else>已关闭</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="更新时间"
                            align= "center"
                            width="160px"
                            prop="updateTime">
                        </el-table-column>   
                        <el-table-column
                            show-overflow-tooltip
                            label="创建者"
                            align= "center"
                            width="150px"
                            prop="createUserName">
                        </el-table-column>   
                        <el-table-column
                            align="center"
                            width="170px">
                        <template slot="header">
                            <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                        </template>
                        <template slot-scope="scope" style="width:100px">
                            <!-- <el-button-group> -->
                                <!-- <el-button
                                    size="mini"
                                    type="warning"
                                    @click="handleLifeCycle(scope.$index, scope.row)">生命周期
                                </el-button> -->
                                <el-button
                                    size="mini"
                                    @click="handleEdit(scope.$index, scope.row)">Edit
                                </el-button>
                                <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleDelete(scope.$index, scope.row)">Delete
                                </el-button>
                            <!-- </el-button-group> -->
                        </template>
                        </el-table-column>
                    </el-table>
                </div>
                <div style="margin-top:-10px">
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
import Qs from 'qs'
import DialogEditor from "./Editor.vue";
import {GetPageNameItems} from "../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../js/GetSelectTable.js";
// import {GetModuleNameItems} from "../../../js/intGetCommonTable.js";

export default {
    components: {
        DialogEditor,
    },
    data() {
        return {
            tableData: [],
            SelectRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                workState:'',
                workStateNameOption:[
                    {'label':'待受理','value':0},
                    {'label':'受理中','value':1},
                    {'label':'已解决','value':2},
                ],
                myWork:'My',
                myWorkOption:[
                    {'label':'我的','value':'My'},
                    {'label':'全部','value':"All"},
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
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        'SelectRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.SelectRomeData.funId='';
                self.SelectRomeData.funNameOption=[];
            }
        },
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/WorkorderManagement/SelectData',{
                params:{
                    'sysType':'API',
                    'myWork':self.SelectRomeData.myWork,
                    'proId':self.$cookies.get('proId'),
                    'pageId':self.SelectRomeData.pageId,
                    'funId':self.SelectRomeData.funId,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id = d.id;
                        obj.codeId = 'A-'+d.id;
                        obj.workSource=d.workSource;
                        obj.workType = d.workType;
                        obj.pageNameAndfunName = d.pageNameAndfunName;
                        // obj.pageName = d.pageName;
                        // obj.funName = d.funName;
                        obj.workName = d.workName;
                        obj.message=d.message;
                        obj.workState=d.workState;
                        obj.updateTime = d.updateTime;
                        obj.createUserName = d.createUserName;

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        GetPageNameOption(){
            GetPageNameItems('API',this.$cookies.get('proId')).then(d=>{
                this.SelectRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.SelectRomeData.pageId){
                GetFunNameItems('API',this.$cookies.get('proId'),this.SelectRomeData.pageId).then(d=>{
                    this.SelectRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增工单",//初始化标题
                triggerPage:'WorkorderMaintenance',//触发页面
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑工单",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                workId:row.id,
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
        // handleLifeCycle(index,row){//生命周期

        // },
        DeleteData(id){
            let self = this;
            self.$axios.post('/api/WorkorderManagement/DeleteData',Qs.stringify({
                'workId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('删除工单成功!');
                self.SelectData();
            }
            else{
                self.$message.error('删除工单失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funId='';
            self.SelectRomeData.workState='';
            self.SelectRomeData.myWork='My';
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
