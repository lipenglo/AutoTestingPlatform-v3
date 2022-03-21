<template>
    <el-drawer
        :title="dialogTitle"
        size="1500px"
        :visible.sync="dialogVisible"
        direction='rtl'
        :before-close="dialogClose">
        <div>
            <el-form :inline="true" v-if="SelectRomeData.disPlay"  method="post">
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
                <el-form-item label="元素名称:">
                    <el-input clearable v-model.trim="SelectRomeData.elementName"></el-input>
                </el-form-item>
                <el-button type="primary" @click="SelectData()">查询</el-button>
                <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
            </el-form>
        </div>
        <div>
            <el-table
                v-loading="loading"
                :data="tableData"
                height="733px"
                border>
                <el-table-column 
                    label="ID"  
                    width="80" 
                    align="center"
                    prop="id">
                </el-table-column>
                <el-table-column 
                    label="详情" 
                    width="50px"
                    type="expand">
                    <template slot-scope="props">
                        <el-form v-if="props.row.tableItem.length!=0">
                            <el-table
                                :data="props.row.tableItem"
                                border>
                                <el-table-column
                                    label="Json">
                                    <template slot-scope="scope">
                                        <el-input type="textarea" 
                                            readonly
                                            resize="none"
                                            v-model="scope.row.restoreData"
                                            :autosize="{ minRows: 20, maxRows: 20}">
                                        </el-input>
                                        <!-- <div style="white-space: pre-line;" v-html="scope.row.restoreData"></div> -->
                                    </template>
                                </el-table-column>
                                <!-- <el-table-column 
                                    label="文本信息"   
                                    align="center">
                                    <template slot-scope="scope">
                                        <div style="white-space: pre-line;text-align: left;" v-html="scope.row.textInfo"></div>
                                    </template>
                                </el-table-column> -->
                            </el-table>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column
                    label="所属页面"
                    align= "center"
                    prop="pageName">
                </el-table-column>
                <el-table-column
                    label="所属功能"
                    align= "center"
                    prop="funName">
                </el-table-column>
                <el-table-column
                    label="元素名称"
                    align= "center"
                    prop="elementName">
                </el-table-column>
                <el-table-column
                    label="操作过程"
                    width="150px"
                    align= "center">
                        <template slot-scope="scope">
                            <el-tag type="danger" v-if="scope.row.operationType=='Delete'">删除</el-tag>
                            <el-tag type="success" v-else-if="scope.row.operationType=='Add'">新增</el-tag>
                            <el-tag type="warning" v-else-if="scope.row.operationType=='Edit'">修改</el-tag>
                            <!-- <el-tag type="warning" v-else>修改</el-tag> -->
                        </template>
                </el-table-column>
                <el-table-column
                    label="修改时间"
                    width="160px"
                    align= "center"
                    prop="createTime">
                </el-table-column>
                <el-table-column
                    label="修改者"
                    width="150px"
                    align= "center"
                    prop="userName">
                </el-table-column>
                <el-table-column
                    label="操作"
                    align="center"
                    width="100px">
                    <template slot-scope="scope" style="width:100px">
                        <el-button
                            v-if="scope.row.operationType!='Delete'"
                            size="mini"
                            type="warning"
                            @click="handleRestor(scope.$index, scope.row)">恢复
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div>
            <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                @size-change="pageSizeChange"
                @current-change="handleCurrentChange"
                :current-page="page.current" 
                :total="page.total"
                :page-sizes = [12,30,50,100]
                style="margin: 20px auto auto auto;">
            </el-pagination>
        </div>
    </el-drawer>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            tableData:[],
            SelectRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                elementName:'',
                disPlay:false,
            },
            RomeData:{
                elementId:'',
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 12, // 默认每页显示的条数（可修改）
            },
          
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
                if(newval.elementId){//有id时就隐藏查询框
                    this.SelectRomeData.disPlay=false;
                    this.RomeData.elementId = newval.elementId;
                   
                }else{
                    this.SelectRomeData.disPlay=true;
                }
                
                this.SelectData();
            }
        },
        'SelectRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.SelectRomeData.funId='';
                self.SelectRomeData.funNameOption=[];
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.tableData=[];
            self.RomeData.elementId='';
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funId='';
            self.SelectRomeData.elementName='';  
            // self.SelectRomeData.operationType='';
        },
        ClearSelectRomeData(){
            let self = this;
            self.tableData=[];
            self.SelectRomeData.pageId='';
            self.SelectRomeData.funId='';
            self.SelectRomeData.elementName='';  
            // self.SelectRomeData.operationType='';
            self.SelectData();
        },
        GetPageNameOption(){
            GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                this.SelectRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.SelectRomeData.pageId){
                GetFunNameItems('UI',this.$cookies.get('proId'),this.SelectRomeData.pageId).then(d=>{
                    this.SelectRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        SelectData(){
            let self = this;
            self.loading=true;
            self.tableData= [];
            self.$axios.get('/api/UiElementMaintenance/SelectHistory',{
                params:{
                    'elementId':self.RomeData.elementId,
                    'pageId':self.SelectRomeData.pageId,
                    'funId':self.SelectRomeData.funId,
                    'elementName':self.SelectRomeData.elementName,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.pageName=d.pageName;
                        obj.funName=d.funName;
                        obj.elementName = d.elementName;
                        obj.operationType=d.operationType;
                        obj.tableItem=d.tableItem;
                        obj.createTime = d.createTime;
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
                    self.dialogClose();
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
                self.dialogClose();
            })
        },
        handleRestor(index,row){
            let message =  "注意:此恢复会查询原库中的被删除数据,如原库中无此关联数据时将会恢复失败!请确定是否恢复?";
            this.$confirm(message, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                   this.RestorData(row.id);     
                }).catch(() => {       
            });
        },
        RestorData(historyId){//恢复数据
            let self = this;
            self.$axios.post('/api/UiElementMaintenance/RestorData',Qs.stringify({
                "historyId":historyId,
            })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('元素恢复成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('元素恢复失败:'+res.data.errorMsg);
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
            self.page.current=val
            self.SelectData();
        },
    }
};
</script>

<style>
.test{
    text-align: left;
}
</style>
