<template>
       <el-drawer
        :title="dialogTitle"
        size="900px"
        :visible.sync="dialogVisible"
        direction='rtl'
        :before-close="dialogClose">
        <div>
            <el-form :inline="true" v-if="SelectRomeData.disPlay"  method="post">
                <el-form-item label="任务名称:">
                    <el-input clearable v-model.trim="SelectRomeData.taskName"></el-input>
                </el-form-item>
                <el-form-item label="运行类型:">
                    <el-select v-model="SelectRomeData.runType" clearable placeholder="请选择" style="width:150px;">
                        <el-option
                            v-for="item in SelectRomeData.runTypeOption"
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
                    label="任务名称"
                    align= "center"
                    prop="taskName">
                </el-table-column>
                <el-table-column
                    label="运行类型"
                    width="150px"
                    align= "center">
                    <template slot-scope="scope">
                        <el-tag type="info" v-if="scope.row.runType=='Manual'">手动</el-tag>
                        <el-tag type="warning" v-else>自动</el-tag>
                    </template>
                </el-table-column>
                <el-table-column
                    label="运行时间"
                    width="160px"
                    align= "center"
                    prop="updateTime">
                </el-table-column>
                <el-table-column
                    label="执行人"
                    width="150px"
                    align= "center"
                    prop="userName">
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

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            tableData:[],
            SelectRomeData:{
                taskName:'',
                runType:'',
                runTypeOption:[
                    {'label':'手动','value':'Manual'},
                    {'label':'自动','value':'Auto'},
                ],
                disPlay:false,
            },
            RomeData:{
                taskId:'',
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
                if(newval.taskId){//有id时就隐藏查询框
                    this.SelectRomeData.disPlay=false;
                    this.RomeData.taskId = newval.taskId;
                   
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
            self.RomeData.taskId='';
            self.tableData=[];
            self.SelectRomeData.taskName='';  
            self.SelectRomeData.runType='';  
        },
        ClearSelectRomeData(){
            let self = this;
            self.tableData=[];
            self.SelectRomeData.taskName='';  
            self.SelectRomeData.runType='';  
            self.SelectData();
        },
        SelectData(){
            let self = this;
            self.loading=true;
            self.tableData= [];
            self.$axios.get('/api/ApiTimingTask/ExecutiveLogging',{
                params:{
                    'taskId':self.RomeData.taskId,
                    'taskName':self.SelectRomeData.taskName,
                    'runType':self.SelectRomeData.runType,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.taskName = d.taskName;
                        obj.runType=d.runType;
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
                    self.dialogClose();
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
                self.dialogClose();
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
            self.page.current=val;
            self.SelectData();
        },


    }
};
</script>

<style>

</style>
