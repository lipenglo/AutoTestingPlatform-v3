<template>
    <div ref="tab-main"  id="tab-main">
        <el-tabs type="border-card" style="height:850px">
            <el-tab-pane label="操作信息">
                <template>
                    <el-form :inline="true" class="demo-form-inline" method="post">
                        <el-form-item label="所属系统:">
                            <el-select v-model="SelectRomeData.sysType" clearable placeholder="请选择" style="width:150px;float:left;">
                                <el-option
                                    v-for="item in SelectRomeData.sysTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="提醒类别:">
                            <el-select v-model="SelectRomeData.remindType" clearable placeholder="请选择" style="width:150px;float:left;">
                                <el-option
                                    v-for="item in SelectRomeData.remindTypeOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="读取状态:">
                            <el-select v-model="SelectRomeData.isRead" clearable placeholder="请选择" style="width:150px;float:left;">
                                <el-option
                                    v-for="item in SelectRomeData.isReadOption"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <!-- <el-form-item label="事件名称:">
                            <el-input clearable v-model.trim="SelectRomeData.eventName"></el-input>
                        </el-form-item> -->
                        <el-button type="primary" @click="SelectData()">查询</el-button>
                        <el-button type="info"  @click="ClearSelectRomeData()">重置</el-button>
                    </el-form>
                </template>
                <template>
                    <el-table
                        :data="tableData"
                        height="660px"
                        border>
                        <el-table-column
                            label="ID"
                            align= "center"
                            width="80px"
                            prop="id">
                        </el-table-column>
                        <el-table-column 
                            label="详情" 
                            width="50px"
                            type="expand">
                            <template slot-scope="props">
                                <el-form label-position="left" >
                                    <el-table
                                        :data="props.row.tableItem"
                                        border>
                                        <el-table-column
                                            prop="CUFront"
                                            label="修改前"
                                            align= "center">
                                        </el-table-column>
                                        <el-table-column
                                            prop="CURear"
                                            align= "center"
                                            label="修改后">
                                        </el-table-column>
                                    </el-table>
                                </el-form>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="所属系统"
                            width="80px"
                            align= "center"
                            prop="sysType">
                        </el-table-column>  
                        <el-table-column
                            label="触发类型"
                            align= "center"
                            width="80px">
                            <template slot-scope="scope">
                                <el-tag type="success" v-if="scope.row.triggerType=='push'">推送</el-tag>
                                <el-tag type="info" v-else>系统</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="提醒类别"
                            width="100px"
                            align= "center">
                            <template slot-scope="scope">
                                <el-tag type="danger" v-if="scope.row.level==1">{{scope.row.remindType}}</el-tag>
                                <el-tag type="warning" v-else-if="scope.row.level==2">{{scope.row.remindType}}</el-tag>
                                <el-tag type="success" v-else-if="scope.row.level==3">{{scope.row.remindType}}</el-tag>
                                <el-tag v-else>{{scope.row.remindType}}</el-tag>
                            </template>
                        </el-table-column>  
                        <el-table-column
                            label="所属项目"
                            width="150px"
                            align= "center"
                            prop="toPro">
                        </el-table-column>  
                        <el-table-column
                            label="所属页面"
                            width="150px"
                            align= "center"
                            prop="toPage">
                        </el-table-column>  
                        <el-table-column
                            label="所属功能"
                            width="200px"
                            align= "center"
                            prop="toFun">
                        </el-table-column>
                        <el-table-column
                            show-overflow-tooltip
                            label="系统:(信息)/推送:(编号:工单名称)"
                            align= "center"
                            prop="info">
                        </el-table-column>
                        <!-- <el-table-column
                            label="修改信息"
                            show-overflow-tooltip
                            align= "left">
                            <template slot-scope="scope">
                                <div v-html="scope.row.editInfo"></div>
                            </template>
                        </el-table-column> -->
                        <el-table-column
                            label="操作时间"
                            width="160px"
                            align= "center"
                            prop="createTime">
                        </el-table-column>
                        <el-table-column
                            label="创建者"
                            align= "center"
                            width="150px"
                            prop="userName">
                        </el-table-column>
                        <el-table-column
                            align="center"
                            width="100px">
                            <template slot="header">
                                <el-button type="primary" @click="ReadAll()">全读</el-button>
                            </template>
                            <template slot-scope="scope" style="width:100px">
                                <el-button
                                    v-if="scope.row.is_read==0"
                                    size="mini"
                                    type="warning"
                                    @click="handleIsRead(scope.$index, scope.row)">已读
                                </el-button>
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
    </div>
</template>

<script>
import Qs from 'qs'
import store from '../../../../store/index'

export default {
    components: {

    },
    data() {
        return {
            tableData:[],
            SelectRomeData:{
                sysType:'',
                sysTypeOption:[
                    {'label':'登录','value':'LOGIN'},
                    {'label':'内置系统','value':'ALL'},
                    {'label':'Home','value':'HOME'},
                    {'label':'UI','value':'UI'},
                    {'label':'API','value':'API'},
                    {'label':'PTS','value':'PTS'},
                ],
                isRead:'',
                isReadOption:[
                    {'label':'已读','value':'1'},
                    {'label':'未读','value':'0'},
                ],
                remindType:'',
                remindTypeOption:[
                    {'label':'Error','value':'Error'},
                    {'label':'Warning','value':'Warning'},
                    {'label':'Add','value':'Add'},
                    {'label':'Edit','value':'Edit'},
                    {'label':'Update','value':'Update'},
                    {'label':'Delete','value':'Delete'},
                ],
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
        SelectData(){//刷新列表数据
            let self = this;
            self.tableData= [];
            self.$axios.get('/api/info/SelectOperationalInfo',{
                params:{
                    'sysType':self.SelectRomeData.sysType,
                    'remindType':self.SelectRomeData.remindType,
                    'isRead':self.SelectRomeData.isRead,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.tableItem=d.tableItem;
                        obj.triggerType=d.triggerType;
                        obj.level=d.level;
                        obj.remindType=d.remindType;
                        obj.sysType = d.sysType;
                        obj.toPro=d.toPro;
                        obj.toPage = d.toPage;
                        obj.toFun = d.toFun;
                        obj.info=d.info;
                        obj.editInfo = d.editInfo;
                        obj.is_read=d.is_read;
                        obj.createTime = d.createTime;
                        obj.userName = d.userName;

                        self.tableData.push(obj);
                    });
                    if(self.tableData.length==0 && self.page.current != 1){
                        self.page.current = 1;
                        self.SelectData();
                    }
                    self.page.total = res.data.Total;
                }else{
                    self.$message.error('操作信息获取失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleIsRead(index,row){
            let self = this;
            self.$axios.post('/api/info/EditOperationalInfoState',Qs.stringify({
                'oId':row.id,
            })).then(res => {
                if(res.data.statusCode==2002){
                    self.SelectData();
                }
                else{
                    self.$message.error(res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        ReadAll(){
            let self = this;
            if(self.SelectRomeData.sysType &&self.SelectRomeData.remindType){
                self.$axios.post('/api/info/SettingOperationalReadAll',Qs.stringify({
                    'sysType':self.SelectRomeData.sysType,
                    'remindType':self.SelectRomeData.remindType,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('已全部读取!');
                    this.SelectData()
                }
                else{
                    self.$message.error('操作失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$message.warning('必须选择所属系统和提醒类别!');
            }
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.sysType='';
            self.SelectRomeData.isRead='';
            self.SelectRomeData.remindType='';
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
            this.SelectData();
        },

    }
};
</script>

<style>
/* .el-table .cell {
    white-space: pre-line;
} */

</style>
