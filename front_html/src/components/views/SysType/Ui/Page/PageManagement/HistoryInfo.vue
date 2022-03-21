<template>
    <el-drawer
        :title="dialogTitle"
        size="1100px"
        :visible.sync="dialogVisible"
        direction='rtl'
        :before-close="dialogClose">
        <div>
            <el-form :inline="true" v-if="SelectRomeData.disPlay"  method="post">
                <el-form-item label="页面名称:">
                    <el-input clearable v-model.trim="SelectRomeData.pageName"></el-input>
                </el-form-item>
                <el-form-item label="操作类型:">
                    <el-select v-model="SelectRomeData.operationType" clearable placeholder="请选择" style="width:150px;">
                        <el-option
                            v-for="item in SelectRomeData.operationTypeOption"
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
                        <el-form label-position="left" v-if="props.row.tableItem.length!=0">
                            <el-table
                                :data="props.row.tableItem"
                                border>
                                <el-table-column
                                    label="原始信息">
                                    <template slot-scope="scope">
                                        <div style="white-space: pre-line;" v-html="scope.row.restoreData"></div>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column
                    label="页面名称"
                    align= "center"
                    prop="pageName">
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
import {PrintConsole} from "../../../../../js/Logger.js";

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            tableData:[],
            SelectRomeData:{
                pageName:'',
                disPlay:false,
                operationType:'',
                operationTypeOption:[
                    {'label':'Add','value':'Add'},
                    {'label':'Edit','value':'Edit'},
                    {'label':'Delete','value':'Delete'},
                ],
            },
            RomeData:{
                pageId:'',
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
                if(newval.pageId){//有id时就隐藏查询框
                    this.SelectRomeData.disPlay=false;
                    this.RomeData.pageId = newval.pageId;
                   
                }else{
                    this.SelectRomeData.disPlay=true;
                }
                
                this.SelectData();
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
            self.RomeData.pageId='';
            self.SelectRomeData.pageName='';
            self.SelectRomeData.operationType='';
        },
        ClearSelectRomeData(){
            let self = this;
            self.tableData=[];
            self.SelectRomeData.pageName='';
            self.SelectRomeData.operationType='';
            self.SelectData();
        },
        SelectData(){
            let self = this;
            self.loading=true;
            self.tableData= [];
            self.$axios.get('/api/PageManagement/SelectHistory',{
                params:{
                    'sysType':'UI',
                    'pageId':self.RomeData.pageId,
                    'pageName':self.SelectRomeData.pageName,
                    'operationType':self.SelectRomeData.operationType,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.pageName = d.pageName;
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
            self.$axios.post('/api/PageManagement/RestorData',Qs.stringify({
                "historyId":historyId,
            })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('页面恢复成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('页面恢复失败:'+res.data.errorMsg);
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

</style>
