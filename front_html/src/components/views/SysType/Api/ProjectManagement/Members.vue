<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="900px">
       <el-tabs type="border-card" style="height:650px" v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="项目成员" name="joinMembers">
                <el-form :inline="true"  method="post">
                    <el-form-item label="用户角色:">
                        <el-select v-model="JoinRomeData.roleId" clearable placeholder="请选择" style="float:left" @click.native="GetRoleNameOption()">
                            <el-option
                                v-for="item in JoinRomeData.roleOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="用户名称:">
                        <el-input clearable v-model.trim="JoinRomeData.userName"></el-input>
                    </el-form-item>
                    <el-button type="primary" @click="SelectJoinData()">查询</el-button>
                    <el-button type="info"  @click="ClearJoinRomeData()">重置</el-button>
                </el-form>
                <el-table
                    :data="JoinRomeData.tableData"
                    height="520px">
                    <el-table-column
                        label="用户角色"
                        align= "center">
                        <template slot-scope="scope">
                            <el-tag type="info">{{scope.row.roleName}}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column
                        label="用户名称"
                        align= "center"
                        prop="userName">
                    </el-table-column>
                    <el-table-column
                        label="用户昵称"
                        align= "center"
                        prop="nickName">
                    </el-table-column>
                    <el-table-column
                        label="用户状态"
                        align= "center">
                        <template slot-scope="scope">
                            <el-tag type="warning" v-if="scope.row.isLock">禁用</el-tag>
                            <el-tag type="success" v-else>正常</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column
                        label="操作"
                        align="center"
                        width="100px">
                        <template slot-scope="scope" style="width:100px">
                            <el-button
                                :disabled="scope.row.isDelete"
                                size="mini"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)">移除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="邀请成员" name="notInJoinMembers">
                <el-form :inline="true"  method="post">
                    <el-form-item label="用户角色:">
                        <el-select v-model="NotInJoinRomeData.roleId" clearable placeholder="请选择" style="float:left" @click.native="GetRoleNameOption()">
                            <el-option
                                v-for="item in RomeData.roleOption"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="用户名称:">
                        <el-input clearable v-model.trim="NotInJoinRomeData.userName"></el-input>
                    </el-form-item>
                    <el-button type="primary" @click="SelectNotInJoinData()">查询</el-button>
                    <el-button type="info"  @click="ClearNotInJoinRomeData()">重置</el-button>
                </el-form>
                <el-table
                    :data="NotInJoinRomeData.tableData"
                    height="520px">
                    <el-table-column
                        label="用户角色"
                        align= "center">
                        <template slot-scope="scope">
                            <el-tag type="info">{{scope.row.roleName}}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column
                        label="用户名称"
                        align= "center"
                        prop="userName">
                    </el-table-column>
                    <el-table-column
                        label="用户昵称"
                        align= "center"
                        prop="nickName">
                    </el-table-column>
                    <el-table-column
                        label="用户状态"
                        align= "center">
                        <template slot-scope="scope">
                            <el-tag type="warning" v-if="scope.row.isLock">禁用</el-tag>
                            <el-tag type="success" v-else>正常</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column
                        label="操作"
                        align="center"
                        width="100px">
                        <template slot-scope="scope" style="width:100px">
                            <el-button
                                :disabled="scope.row.isDelete"
                                size="mini"
                                type="success"
                                @click="handleJoin(scope.$index, scope.row)">加入
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
    </el-dialog>
</template>

<script>
import Qs from 'qs'
import store from '../../../../../store/index'
import {PrintConsole} from "../../../../js/Logger.js";
import {GetRoleNameItems} from "../../../../js/GetSelectTable.js";

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            activeName:'joinMembers',
            RomeData:{
                proId:'',
                roleOption:[],
            },
            JoinRomeData:{
                roleId:'',
               
                userName:'',
                tableData:[],//已加入
                // notInJoinTableData:[],//未加入
            },
            NotInJoinRomeData:{
                roleId:'',
                userName:'',
                tableData:[],//已加入
                // notInJoinTableData:[],//未加入
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
                this.activeName='joinMembers';
                this.dialogTitle = newval.dialogTitle;
                this.RomeData.proId = newval.proId; 
                this.SelectJoinData();
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
            this.$emit('Succeed');//回调查询
            
        },
        ClearJoinRomeData(){
            let self = this;
            self.JoinRomeData.roleId='';
            self.JoinRomeData.userName='';
            self.JoinRomeData.joinTableData=[];
            self.SelectJoinData();
        },
        ClearNotInJoinRomeData(){
            let self = this;
            self.NotInJoinRomeData.roleId='';
            self.NotInJoinRomeData.userName='';
            self.NotInJoinRomeData.joinTableData=[];
            self.SelectNotInJoinData();
        },
        GetRoleNameOption(){
            GetRoleNameItems().then(d=>{
                this.RomeData.roleOption = d;
            });
        },
        handleClick(tab, event){
            let self = this;
            if(tab.name=='joinMembers'){
                self.ClearJoinRomeData();
            }else{
                self.ClearNotInJoinRomeData();
            }
        },
        SelectJoinData(){
            let self = this;
            self.JoinRomeData.tableData= [];
            self.$axios.get('/api/ProjectManagement/SelectJoinData',{
                params:{
                    'sysType':'API',
                    'proId':self.RomeData.proId,
                    'roleId':self.JoinRomeData.roleId,
                    'userName':self.JoinRomeData.userName,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id=d.id;
                        obj.roleName = d.roleName;
                        obj.userName=d.userName;
                        obj.nickName=d.nickName;
                        obj.isLock=d.isLock;

                        self.JoinRomeData.tableData.push(obj);
                    });
          
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        SelectNotInJoinData(){
            let self = this;
            self.NotInJoinRomeData.tableData= [];
            self.$axios.get('/api/ProjectManagement/SelectNotInJoinData',{
                params:{
                    'sysType':'API',
                    'proId':self.RomeData.proId,
                    'roleId':self.NotInJoinRomeData.roleId,
                    'userName':self.NotInJoinRomeData.userName,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    res.data.TableData.forEach(d => {
                        let obj = {};
                        obj.id=d.id;
                        obj.roleName = d.roleName;
                        obj.userName=d.userName;
                        obj.nickName=d.nickName;
                        obj.isLock=d.isLock;

                        self.NotInJoinRomeData.tableData.push(obj);
                    });
          
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                }
                // console.log(self.tableData);
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleJoin(index,row){//加入
            let self = this;
            self.$axios.post('/api/ProjectManagement/JoinMembers',Qs.stringify({
                'sysType':'API',
                'userId':row.id,
                'proId':self.RomeData.proId,
            })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('成员加入成功');
                    self.SelectNotInJoinData();
                }
                else{
                    self.$message.error('成员加入失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleDelete(index,row){//移除
            let self = this;
            self.$axios.post('/api/ProjectManagement/DeleteMembers',Qs.stringify({
                'sysType':'API',
                'userId':row.id,
                'proId':self.RomeData.proId,
            })).then(res => {
                if(res.data.statusCode==2003){
                    self.$message.success('成员移除成功');
                    self.SelectJoinData();
                }
                else{
                    self.$message.error('成员移除失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
      
    }
};
</script>

<style>
</style>
