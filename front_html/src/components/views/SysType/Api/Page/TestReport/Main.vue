<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div style="height: 775px;">
                <div>
                    <el-form :inline="true"  method="post">
                        <el-form-item label="报告名称:">
                            <el-input clearable v-model.trim="SelectRomeData.reportName"></el-input>
                        </el-form-item>
                        <el-form-item label="报告类型:">
                            <el-select v-model="SelectRomeData.reportType" clearable placeholder="请选择" style="width:200px;">
                                <el-option
                                    v-for="item in SelectRomeData.reportTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="报告状态:">
                            <el-select v-model="SelectRomeData.reportStatus" clearable placeholder="请选择" style="width:150px;">
                                <el-option
                                    v-for="item in SelectRomeData.reportStatusOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="队列状态:">
                            <el-select v-model="SelectRomeData.queueStatus" clearable placeholder="请选择" style="width:200px;">
                                <el-option
                                    v-for="item in SelectRomeData.queueStatusOption"
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
                                label="报告名称"
                                align= "center"
                                prop="reportName">
                            </el-table-column>
                             <el-table-column
                                label="报告类型"
                                width="150px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag v-if="scope.row.reportType=='API'" >接口</el-tag>
                                    <el-tag type="success" v-else-if="scope.row.reportType=='CASE'" >测试用例</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.reportType=='TASK'" >定时任务</el-tag>
                                    <el-tag type="danger" v-else-if="scope.row.reportType=='BATCH'" >批量任务</el-tag>
                                </template>
                            </el-table-column>         
                           <el-table-column
                                label="队列状态"
                                width="150px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="info" v-if="scope.row.queueStatus==0" >未开始</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.queueStatus==1">执行中</el-tag>
                                    <el-tag type="success" v-else-if="scope.row.queueStatus==2">已结束</el-tag>
                                    <el-tag type="danger" v-else>数据缺损</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="执行进度"
                                width="150px"
                                align= "center"
                                prop="runningProgress">
                            </el-table-column>   
                            <el-table-column
                                label="报告状态"
                                width="150px"
                                align= "center">
                                <template slot-scope="scope">
                                    <el-tag type="success" v-if="scope.row.reportStatus=='Pass'" >Pass</el-tag>
                                    <el-tag type="warning" v-else-if="scope.row.reportStatus=='Fail'">Fail</el-tag>
                                    <el-tag type="danger" v-else-if="scope.row.reportStatus=='Error'">Error</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="耗费时间"
                                align= "center"
                                width="100px"
                                prop="runningTime">
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
                                label="操作"
                                align="center"
                                width="230px">
                            <template slot-scope="scope" style="width:100px">
                              <el-button-group>
                                <el-button
                                    size="mini"
                                    type="warning"
                                    @click="handleReport(scope.$index, scope.row)">详情
                                </el-button>
                                <el-button
                                    size="mini"
                                    type="success"
                                    @click="handleLog(scope.$index, scope.row)">Log(未做)
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
    </div>
</template>

<script>

import Qs from 'qs';
export default {
    components: {
        
    },
    data() {
        return {
            tableData: [],
            SelectRomeData:{
                reportName:'',
                reportType:'',
                reportTypeOption:[
                    {'label':'接口','value':'API'},
                    {'label':'测试用例','value':'CASE'},
                    {'label':'定时任务','value':'TASK'},
                    {'label':'批量任务','value':'BATCH'},
                ],
                queueStatus:'',//报告队列状态
                queueStatusOption:[
                    {'label':'未开始','value':'0'},
                    {'label':'执行中','value':'1'},
                    {'label':'已结束','value':'2'},
                ],
                reportStatus:'',
                reportStatusOption:[
                    {'label':'Pass','value':'Pass'},
                    {'label':'Fail','value':'Fail'},
                    {'label':'Error','value':'Error'},
                ],
            },
            RomeData:{
    
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
            },

        };
    },
    mounted(){
        this.SelectData();

    },
    methods: {
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.reportName='';
            self.SelectRomeData.reportType='';
            self.SelectRomeData.queueStatus='';
            self.SelectRomeData.reportStatus='';

            self.SelectData();
        },
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/ApiTestReport/SelectData',{
                params:{
                    'proId':self.$cookies.get('proId'),
                    'reportName':self.SelectRomeData.reportName,
                    'reportType':self.SelectRomeData.reportType,
                    'reportStatus':self.SelectRomeData.reportStatus,
                    'queueStatus':self.SelectRomeData.queueStatus,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                res.data.TableData.forEach(d => {
                    let obj = {};
                    obj.id =d.id;
                    obj.reportName = d.reportName;
                    obj.reportType = d.reportType;
                    obj.queueStatus = d.queueStatus;
                    obj.runningProgress = d.runningProgress;
                    obj.reportStatus = d.reportStatus;
                    if(d.runningTime!=null){
                        obj.runningTime=d.runningTime+' ms';
                    }else{
                        obj.runningTime='';
                    }
                    
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
            self.$axios.post('/api/ApiTestReport/DeleteData',Qs.stringify({
                "sysType":'API',
                'testReportId':id,
            })).then(res => {
                if(res.data.statusCode ==2003){
                    self.$message.success('测试报告删除成功!');
                    self.SelectData();
                }
                else{
                    self.$message.error('测试报告删除失败:'+ res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleReport(index,row){
            let routeUrl = this.$router.resolve({
                name: "Api_Report",
                query: {
                    testReportId:row.id,
                    reportType:row.reportType,
                }
            });
            window.open(routeUrl.href, '_blank');
        },
    }
};
</script>

<style>

</style>
