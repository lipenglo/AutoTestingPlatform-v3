<template>
    <el-dialog
        title="推送提醒"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="1600px">
        <template>
            <el-form :inline="true" class="demo-form-inline" method="post">
                <el-form-item label="系统类型:">
                    <el-select v-model="SelectRomeData.sysType" clearable placeholder="请选择" style="width:150px;float:left;">
                        <el-option
                            v-for="item in SelectRomeData.sysTypeOption"
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
            :data="RomeData.tableData"
            height="550px"
            border>
            <el-table-column
                label="系统类型"
                width="100px"
                align= "center"
                prop="sysType">
            </el-table-column>
            <el-table-column
                label="触发类型"
                align= "center"
                width="100px">
                <template slot-scope="scope">
                    <el-tag type="success" v-if="scope.row.triggerType=='Manual'">手动</el-tag>
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
                </template>
            </el-table-column>  
            <el-table-column
                label="所属来源"
                align= "center"
                prop="sourcePath">
            </el-table-column>
            <!-- <el-table-column
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
            </el-table-column> -->
            <el-table-column
                label="系统:(信息)/推送:(编号:工单名称)"
                align= "center"
                prop="info">
            </el-table-column>
            <!-- <el-table-column
                label="修改信息"
                align= "center"
                prop="editInfo">
            </el-table-column> -->
            <el-table-column
                show-overflow-tooltip
                label="推送者"
                align= "center"
                width="150px"
                prop="userName">
            </el-table-column>   
            <el-table-column
                label="创建时间"
                align= "center"
                width="200px"
                prop="createTime">
            </el-table-column>   
            <el-table-column
                align="center"
                width="100px">
                <template slot="header">
                    <el-button type="primary" @click="handleIsRead('','','ALL')">全读</el-button>
                </template>
                <template slot-scope="scope" style="width:100px">
                    <el-button
                        v-if="scope.row.is_read==0"
                        size="mini"
                        type="warning"
                        @click="handleIsRead(scope.$index, scope.row,'1')">已读
                    </el-button>
                    <el-button v-else size="mini" type="info" disabled>已读</el-button>
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
    </el-dialog>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../js/Logger.js";
export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            SelectRomeData:{
                sysType:'',
                sysTypeOption:[
                    {'label':'API','value':'API'},
                    {'label':'UI','value':'UI'},
                    {'label':'PTS','value':'PTS'},
                ],
            },
            RomeData:{
                tableData:[]
            },
            page: { 
                current: 1,// 默认显示第几页
                total: 0,// 总条数，根据接口获取数据长度(注意：这里不能为空)
                pageSize: 10, // 默认每页显示的条数（可修改）
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
                this.SelectData();
                
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
            this.$emit('getData',this.RomeData.tableData.length);
        },
        ClearSelectRomeData(){
            let self = this;
            self.SelectRomeData.sysType='';
            self.SelectData();
        },
        SelectData(){//刷新列表数据
            let self = this;
            self.RomeData.tableData= [];
            self.$axios.get('/api/info/UserOperationalInfo',{
                params:{
                    'sysType':self.SelectRomeData.sysType,
                    'current':self.page.current,
                    'pageSize':self.page.pageSize
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id =d.id;
                        obj.triggerType=d.triggerType;
                        obj.level=d.level;
                        obj.remindType=d.remindType;
                        obj.sysType = d.sysType;
                        obj.sourcePath =d.sourcePath;
                        // obj.toPro=d.toPro;
                        // obj.toPage = d.toPage;
                        // obj.toFun = d.toFun;
                        obj.info=d.info;
                        // obj.CUFront = d.CUFront;
                        // obj.CURear = d.CURear;
                        obj.is_read=d.is_read;
                        obj.createTime = d.createTime;
                        obj.userName = d.userName;

                        self.RomeData.tableData.push(obj);
                    });
                    if(self.RomeData.tableData.length==0 && self.page.current != 1){
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
        handleIsRead(index,row,types){
            let self = this;
            let infoId = null
            if(types!="ALL"){
                infoId = row.id
            }
            self.$axios.post('/api/info/EditIsReadState',Qs.stringify({
                'infoId':infoId,
                'types':types,
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
