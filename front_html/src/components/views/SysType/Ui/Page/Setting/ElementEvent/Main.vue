<template>
    <div>
        <template>
            <div style="height: 775px;">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="事件名称:">
                            <el-input clearable v-model.trim="SelectRomeData.eventName"></el-input>
                        </el-form-item>
                        <el-form-item label="事件名称:">
                            <el-input clearable v-model.trim="SelectRomeData.eventLogo"></el-input>
                        </el-form-item>
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </div>
                <div style="margin-top:-15px;">
                    <el-table
                        v-loading="loading"
                        :data="tableData"
                        height="680px"
                        border>
                        <el-table-column
                            label="ID"
                            align= "center"
                            width="80px"
                            prop="id">
                        </el-table-column>
                        <el-table-column
                            label="事件名称"
                            width="250px"
                            align= "center"
                            prop="eventName">
                        </el-table-column>
                        <el-table-column
                            label="事件标识"
                            width="200px"
                            align= "center"
                            prop="eventLogo">
                        </el-table-column>
                        <el-table-column
                            label="元素组件"
                            width="500px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag 
                                v-for="item in scope.row.component" 
                                :key="item.id" 
                                :type="item.state ? 'success':'info'" 
                                style="margin:5px 5px">{{item.label}}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="备注"
                            align= "center"
                            width="300px"
                            prop="remarks">
                        </el-table-column>
                        <el-table-column
                            label="更新时间"
                            width="160px"
                            align= "center"
                            prop="updateTime">
                        </el-table-column>
                        <el-table-column
                            label="修改者"
                            width="160px"
                            align= "center"
                            prop="userName">
                        </el-table-column>
                        <el-table-column
                            fixed="right"
                            align="center"
                            width="200px">
                        <template slot="header">
                            <el-button-group>
                                <el-button type="primary" @click="OpenEditDialog()">新增</el-button>
                                <el-button type="warning" @click="OpenSequencingDialog()">事件排序</el-button>
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
        <template>
            <dialog-event-sequencing
                @closeDialog="closeSequencingDialog" 
                :isVisible="dialog.sequencing.dialogVisible" 
                :dialogPara="dialog.sequencing.dialogPara"
                @Succeed="SelectData">
            </dialog-event-sequencing>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from '../../../../../../js/Logger';
import DialogEditor from "./Editor.vue";
import DialogEventSequencing from "./EventSequencing.vue";

export default {
    components: {
       DialogEditor,DialogEventSequencing
    },
    data() {
        return {
            loading:false,
            tableData: [],
            SelectRomeData:{
                eventName:'',
                eventLogo:'',
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
                sequencing:{
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
      
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){
            let self = this;
            self.loading=true;
            self.tableData= [];
            self.$axios.get('/api/UiElementEvent/SelectData',{
                params:{
                    'eventName':self.SelectRomeData.eventName,
                    'eventLogo':self.SelectRomeData.eventLogo,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.eventName=d.eventName;
                        obj.eventLogo=d.eventLogo;
                        obj.remarks = d.remarks;
                        obj.component=d.component;

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
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.eventName='';
            self.SelectRomeData.eventLogo='';
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

        //编辑、新增
        closeEditDialog(){
            this.dialog.editor.dialogVisible =false;
        },
        OpenEditDialog(){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"新增元素操作",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.editor.dialogVisible=true;
        },
        handleEdit(index,row){
            let self = this;
            self.dialog.editor.dialogPara={
                dialogTitle:"编辑元素操作",//初始化标题
                isAddNew:false,//初始化是否新增\修改
                eventId:row.id,
                eventName:row.eventName,
                eventLogo:row.eventLogo,
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
            self.$axios.post('/api/UiElementEvent/DeleteData',Qs.stringify({
                'eventId':id,
            })).then(res => {
            if(res.data.statusCode ==2003){
                self.$message.success('删除元素事件成功!');
                self.SelectData();
            }
            else{
                self.$message.error('删除元素事件失败:'+ res.data.errorMsg);
            }
            }).catch(function (error) {
                console.log(error);
            })
        },

        //事件排序
        closeSequencingDialog(){
            this.dialog.sequencing.dialogVisible =false;
        },
        OpenSequencingDialog(){
            let self = this;
            self.dialog.sequencing.dialogPara={
                dialogTitle:"事件排序",//初始化标题
                isAddNew:true,//初始化是否新增\修改
            }
            self.dialog.sequencing.dialogVisible=true;
        },
    }
};
</script>

<style>

</style>
