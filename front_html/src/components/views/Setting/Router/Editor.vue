<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="500px">
        <el-form ref="RomeData" :model="RomeData" :rules="rules" v-loading="loading" label-width="90px">
            <el-form-item label="所属系统:" prop="sysType">
                <el-select v-model="RomeData.sysType" clearable placeholder="请选择" style="width:150px;float:left;">
                    <el-option
                        v-for="item in RomeData.sysTypeOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="菜单级别:" prop="menuLevel">
                <el-select v-model="RomeData.menuLevel" clearable placeholder="请选择" style="width:150px;float:left;">
                    <el-option
                        v-for="item in RomeData.menuLevelOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="上级菜单:"  v-if="RomeData.disPlay_belogId" prop="belogId">
                <el-select v-model="RomeData.belogId" clearable placeholder="请选择" style="width:150px;float:left;" @click.native="GetBelogIdTable()">
                    <el-option
                        v-for="item in RomeData.belogIdOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="菜单名称:" prop="menuName">
                <el-input v-model.trim="RomeData.menuName"></el-input>
            </el-form-item>
            <el-form-item label="路由地址:">
                <el-input v-model.trim="RomeData.routerPath"></el-input>
            </el-form-item>
            <el-form-item label="菜单ICON:">
                <el-input v-model.trim="RomeData.icon"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button style="margin: auto 20px auto auto; " type="primary" @click="submitForm('RomeData')">保存</el-button>
                <el-button style="margin: auto 80px auto auto; "  @click="ClearRomeData()">重置</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script>
import Qs from 'qs'
import store from '../../../../store/index'
import {PrintConsole} from "../../../js/Logger.js";

export default {
    data() {
        return {
            loading:false,
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            RomeData:{
                routerId:'',
                sysType:'',
                sysTypeOption:[
                    {'label':'Home','value':'HOME'},
                    {'label':'UI','value':'UI'},
                    {'label':'API','value':'API'},
                    {'label':'PTS','value':'PTS'},
                ],
                menuLevel:'',
                menuLevelOption:[
                    {'label':'一级菜单','value':'1'},
                    {'label':'二级菜单','value':'2'},
                ],
                index:'',
                menuName:'',
                routerPath:'',
                disPlay_belogId:true,
                belogId:'',
                belogIdOption:[],
                icon:'',
                disPlay_icon:true,
            },
            rules: {
                sysType: [
                    { required: true, message: '请选择所属系统', trigger: 'change' }
                ],
                menuLevel: [
                    { required: true, message: '请选择菜单级别', trigger: 'change' }
                ],
                menuName: [
                    { required: true, message: '请输入菜单名称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
                belogId:[
                    { required: true, message: '请选择上级菜单', trigger: 'change' }
                ],
            }
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
                this.isAddNew = newval.isAddNew
                
                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.RomeData.routerId = newval.routerId;
                    self.LoadRouterData(newval.routerId).then(d=>{
                        if(d.statusCode==2000){
                            self.RomeData.sysType = d.dataTable.sysType;
                            self.RomeData.menuLevel = d.dataTable.menuLevel;
                            if(self.RomeData.menuLevel=='2'){
                                self.GetBelogIdTable();
                                self.RomeData.belogId = d.dataTable.belogId;
                            }
                            self.RomeData.menuName = d.dataTable.menuName;
                            self.RomeData.routerPath = d.dataTable.routerPath;
                            self.RomeData.icon = d.dataTable.icon;
                        }else{
                            self.$message.error(d.errorMsg);
                            self.$emit('closeDialog');
                        }
                    });
                }
            }
        },
        'RomeData.menuLevel': function (newVal,oldVal) {
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal!=oldVal){
                if(newVal=='1'){
                    this.RomeData.disPlay_belogId=false;
                }else{
                    this.RomeData.disPlay_belogId=true;
                }
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        GetBelogIdTable(){//加载上级菜单
            let self = this;
            if(self.RomeData.sysType){
                self.$axios.get('/api/router/GetBelogIdTable',{
                    params:{
                        "sysType":self.RomeData.sysType,
                    }
                }).then(res => {
                    if(res.data.statusCode==2000){
                        self.RomeData.belogIdOption = res.data.dataList;
                    }else{
                        self.$message.error('所属上级数据加载失败:'+res.data.errorMsg);
                    }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$message.warning('请先选择所属系统!');
            }
        },
        LoadRouterData(routerId){
            let self = this;
            self.loading=true;
            return self.$axios.get('/api/router/LoadRouterData',{
                params:{
                    "routerId":routerId,
                }
            }).then(res => {
                self.loading=false;
                return res.data;
            }).catch(function (error) {
                console.log(error);
            })
        },
        DataSave(){
            let self = this;
            if(self.isAddNew){
                self.$axios.post('/api/router/SaveData',Qs.stringify({
                    'sysType':self.RomeData.sysType,
                    'menuLevel':self.RomeData.menuLevel,
                    'menuName':self.RomeData.menuName,
                    'routerPath':self.RomeData.routerPath,
                    'belogId':self.RomeData.belogId,
                    'icon':self.RomeData.icon,
                })).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('路由新增成功');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('新增失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/router/EditData',Qs.stringify({
                    'routerId':self.RomeData.routerId,
                    'sysType':self.RomeData.sysType,
                    'menuLevel':self.RomeData.menuLevel,
                    'menuName':self.RomeData.menuName,
                    'routerPath':self.RomeData.routerPath,
                    'belogId':self.RomeData.belogId,
                    'icon':self.RomeData.icon,
                })).then(res => {
                if(res.data.statusCode==2002){
                    self.$message.success('路由修改成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('路由修改失败:'+res.data.errorMsg);
                }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        submitForm(formName) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.DataSave();
                } 
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.routerId='';
            self.RomeData.routerPath='';
            self.RomeData.icon='';
           
        },
    }
};
</script>

<style>

</style>
