<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="600px">
        <el-card>
            <div slot="header" style="height:20px">
                <!-- <span>正在设置角色:{{RomeData.title}}</span> -->
                <el-button  type="primary" style="float: right;margin-top:-10px" @click="submitForm('RomeData')">保存</el-button>
            </div>
            <div>
                <el-form ref="RomeData" :model="RomeData" :rules="RomeData.rules" label-width="100px">
                    <el-form-item label="所属系统:" prop="sysType">
                        <el-select v-model="RomeData.sysType" clearable  placeholder="请选择" style="float: left;">
                            <el-option
                            v-for="item in RomeData.sysTypeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item  v-for="item in RomeData.menuList" :label="item.label" :key="item.id">
                        <el-checkbox-group v-model="RomeData.checkedCities">
                            <el-checkbox style="float: left;" v-for="children in item.children" :label="children.id" :key="children.id">{{children.label}}</el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                </el-form>
            </div>
        </el-card>
    </el-dialog>
</template>

<script>
import {PrintConsole} from "../../../js/Logger.js";
import store from '../../../../store/index'

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            
            RomeData:{
                roleId:'',
                sysType:'Home',
                sysTypeOptions:[
                    {'label':'Home','value':'HOME'},
                    {'label':'功能测试','value':'UI'},
                    {'label':'接口测试','value':'API'},
                    {'label':'性能测试','value':'PTS'},
                ],
                menuList:[],
                checkedCities:[],
                // menuChecked:[],//勾选完成后数据会保存在这里，用来传到后端
                // defaultChecked:[],//默认已勾选的存放，放入ID
                rules: {
                    sysType: [{ required: true, message: '请选择所属系统', trigger: 'change' }],
                }
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
                this.RomeData.roleId = newval.roleId;
                this.GetMenuList(this.RomeData.sysType);
            }
        },
        'RomeData.sysType': function (newVal,oldVal) {
            // PrintConsole('newVal',newVal)
            if(newVal!=oldVal){
                if(newVal){
                    this.GetMenuList(newVal);
                }else{
                    this.RomeData.menuList = [];
                }
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        GetMenuList(sysType){
            let self = this;
            self.RomeData.menuList = [];
            self.$axios.get('/api/role/GetMenuList',{
                params:{
                    'roleId':self.RomeData.roleId,
                    'sysType':sysType,
                }
            }).then(res => {
               if(res.data.statusCode==2000){
                   self.RomeData.menuList = res.data.TreeData;
                   self.RomeData.checkedCities = res.data.DefaultChecked;
               }else{
                   self.$message.error('菜单数据获取失败:'+res.data.errorMsg);
               }
            }).catch(function (error) {
                console.log(error);
            })

        },
        SaveRolePermissions(){//保存角色权限
            let self = this;
            PrintConsole(self.RomeData.checkedCities);
            self.$axios.post('/api/role/SaveRolePermissions',{
                'sysType':self.RomeData.sysType,
                'roleId':self.RomeData.roleId,
                'MenuChecked':self.RomeData.checkedCities,
            }).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('新增角色权限成功!');
                    self.dialogVisible = false;//关闭新增弹窗
                    self.$emit('closeDialog');
                    self.$emit('Succeed');//回调查询
                }
                else{
                    self.$message.error('角色权限保存失败:'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        handleSelectionChange(){
            // this.multipleSelection  这个数组用来存储所有半选的节点和全选的节点  用于保存的时候将数据传给后台
            // 将半选和全选的节点全都存储在一个数组里面   concat 方法是合并(全选和半选)两个数组
            this.RomeData.menuChecked = this.$refs.treeData.getHalfCheckedNodes().concat(this.$refs.treeData.getCheckedNodes());
            // console.log(data);
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.sysType = 'Home';
            self.RomeData.checkedCities=[];
        },
        submitForm(formName) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveRolePermissions();
                } 
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
      
    }
};
</script>

<style>
.test{
    text-align: left;
}
</style>
