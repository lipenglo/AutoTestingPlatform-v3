<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="900px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
            <div class="table">
                <div class="father" style="width: 100%; height:200px;">
                    <div class="son" style="width:900px; height: 150px;">
                        <div
                        v-loading="loading"
                        element-loading-text="拼命加载中"
                        element-loading-spinner="el-icon-loading"
                        style="margin-top:20px;">
                            <!-- <el-card shadow="never"> -->
                                <div>
                                    <el-form ref="RomeData" :rules="rules" :inline="true" :model="RomeData"  label-width="85px">
                                        <el-form-item label="所属页面:" prop="pageId">
                                            <el-select v-model="RomeData.pageId" clearable placeholder="请选择" style="float:left" @click.native="GetPageNameOption()">
                                                <el-option
                                                    v-for="item in RomeData.pageNameOption"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="所属功能:" prop="funId">
                                            <el-select v-model="RomeData.funId" clearable placeholder="请选择" style="float:left" @click.native="GetFunNameOption()">
                                                <el-option
                                                    v-for="item in RomeData.funNameOption"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="元素名称:" prop="elementName">
                                            <el-input clearable v-model.trim="RomeData.elementName"></el-input>
                                        </el-form-item>
                                        <el-form-item label="元素类型:" prop="elementType">
                                            <el-cascader
                                                clearable
                                                v-model="RomeData.elementType"
                                                :options="RomeData.elementTypeOption"
                                                style="float:left;">
                                            </el-cascader>
                                        </el-form-item>
                                    </el-form>
                                </div>
                                <div>
                                    <el-table
                                        :data="RomeData.tableData"
                                        height="600px"
                                        border>
                                        <el-table-column
                                            label="启用"
                                            width="70px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="定位类型"
                                            align= "center"
                                            width="120">
                                            <template slot-scope="scope">
                                                <el-select
                                                    v-model="scope.row.targetingType" clearable placeholder="请选择">
                                                    <el-option
                                                        v-for="item in RomeData.targetingTypeOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="定位地址"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.targetingPath"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            label="备注信息"
                                            width="250px"
                                            align= "center">
                                            <template slot-scope="scope">
                                                <el-input v-model="scope.row.remarks"></el-input>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                            align="center"
                                            width="100px">
                                            <template slot="header">
                                                <el-button type="primary" @click="AddTable()">新增</el-button>
                                            </template>
                                            <template slot-scope="scope" style="width:100px">
                                                <el-button
                                                    size="mini"
                                                    type="danger"
                                                    @click="handleDelete(scope.$index, scope.row)">Delete
                                                </el-button>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </div>
                                <div style="margin-top:20px">
                                    <el-button  type="success" @click="submitForm('RomeData')">保存</el-button>
                                    <el-button @click="ClearRomeData()">重置</el-button>
                                </div>
                            <!-- </el-card> -->
                        </div>
                    </div>
                </div>
            </div>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";


export default {
    components: {

    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            RomeData:{
                elementId:'',
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                elementName:'',
                elementType:'',
                elementTypeOption:[
                    {'label':'点击事件','value':'ClickEvent',children:[
                        {'label':'元素点击','value':'Click'},
                        {'label':'坐标点击=>L','value':'LocationClick_L'},
                        {'label':'坐标点击=>R','value':'LocationClick_R'},
                    ]},
                    {'label':'显示事件','value':'DisplayEvent',children:[
                        {'label':'显示文本','value':'Label'},
                    ]},
                    {'label':'输入事件','value':'InputEvent',children:[
                        {'label':'输入','value':'Input'},
                        {'label':'引用变量赋值','value':'ReferenceVariableAssignment',disabled: true},
                        {'label':'变量顺序输入','value':'VariableSequentialInput',disabled: true},
                        {'label':'上传','value':'Upload'},
                    ]},
                    {'label':'验证事件','value':'VerificationEvent',children:[
                        {'label':'元素验证','value':'ElementVerification'},
                        // {'label':'图片对比器','value':'PictureContrast'},
                    ]},
                    {'label':'其他事件','value':'OrderEvent',children:[
                        // {'label':'时间停顿','value':'Sleep'},
                        {'label':'独立方法','value':'Method'},
                        // {'label':'坐标偏移清除','value':'PositionOffsetClear'},
                        // {'label':'修改URL参数','value':'EditUrlParams'},
                        // {'label':'句柄切换','value':'HandleSwitch'},
                    ]},         
                ],
                targetingTypeOption:[
                    {'label':'Id','value':'Id'},
                    {'label':'Name','value':'Name'},
                    {'label':'Css','value':'Css'},
                    {'label':'Text','value':'Text'},
                    {'label':'Xpath','value':'Xpath'},
                    {'label':'坐标','value':'Coordinate'},
                ],
                tableData:[],
            },
            rules:{
                pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                elementType:[{ required: true, message: '请选择元素类型', trigger: 'change' }],
                elementName: [
                    { required: true, message: '请输入元素名称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                ],
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
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                    let self = this;
                    self.RomeData.elementId =  newval.elementId;
                    self.LoadData(newval.elementId);
                }
            }
        }
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.resetForm('RomeData');
            self.RomeData.elementId='';
            self.RomeData.pageId='';
            self.RomeData.funId='';
            self.RomeData.elementName='';
            self.RomeData.elementType='';
            self.RomeData.tableData=[];
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                this.$refs[formName].resetFields();
            }
        },
        submitForm(formName,id) {//保存
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.SaveData();
                } 
            });
        },
        GetPageNameOption(){
            GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                this.RomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            if(this.RomeData.pageId){
                GetFunNameItems('UI',this.$cookies.get('proId'),this.RomeData.pageId).then(d=>{
                    this.RomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        AddTable(){
            let self = this;
            let obj = {};
            obj.state=true;
            obj.targetingType ='';
            obj.targetingPath='';
            obj.remarks='';

            self.RomeData.tableData.push(obj);
        },
        handleDelete(index,row){
            let self = this;
            self.RomeData.tableData.splice(index, 1)//删除列表中的数据
        },
        SaveData(){
            let self = this;
            if(self.isAddNew){  
                self.$axios.post('/api/UiElementMaintenance/SaveData',{
                    'baseData':{
                        'proId':self.$cookies.get('proId'),
                        'pageId':self.RomeData.pageId,
                        'funId':self.RomeData.funId,
                        'elementName':self.RomeData.elementName,
                        'elementType':self.RomeData.elementType,
                    },
                    'elementLocation':self.RomeData.tableData
                }).then(res => {
                    if(res.data.statusCode==2001){
                        self.$message.success('新增元素成功!');
                        self.dialogClose();
                        self.$emit('Succeed');//回调查询  
                    
                    }else{
                        self.$message.error('新增元素失败'+res.data.errorMsg);
                    }
                }).catch(function (error) {
                    console.log(error);
                })
            }else{
                self.$axios.post('/api/UiElementMaintenance/EditData',{
                    'baseData':{
                        'elementId':self.RomeData.elementId,
                        'proId':self.$cookies.get('proId'),
                        'pageId':self.RomeData.pageId,
                        'funId':self.RomeData.funId,
                        'elementName':self.RomeData.elementName,
                        'elementType':self.RomeData.elementType,
                    },
                    'elementLocation':self.RomeData.tableData
                }).then(res => {
                    if(res.data.statusCode==2002){
                        self.$message.success('修改元素成功!');
                        self.dialogClose();
                        self.$emit('Succeed');//回调查询  
                    }else{
                        self.$message.error('修改元素败'+res.data.errorMsg);
                    }
                }).catch(function (error) {
                    console.log(error);
                })
            }
        },
        LoadData(elementId){
            let self = this;
            self.loading=true;
            return self.$axios.get('/api/UiElementMaintenance/LoadData',{
                params:{
                  'elementId':elementId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    GetPageNameItems('UI',this.$cookies.get('proId')).then(d=>{
                        self.RomeData.pageNameOption = d;
                        self.RomeData.pageId=res.data.baseData.pageId;
                        GetFunNameItems('UI',this.$cookies.get('proId'),this.RomeData.pageId).then(d=>{
                            self.RomeData.funNameOption = d;
                            self.RomeData.funId=res.data.baseData.funId;

                            self.RomeData.elementName=res.data.baseData.elementName;
                            self.RomeData.elementType=res.data.baseData.elementType;
                            self.RomeData.tableData = res.data.locationTable;
                            self.loading=false;
                        });
                    });
                }else{
                    self.loading=false;
                    self.$message.error('数据加载失败:'+res.data.errorMsg);
                    self.dialogClose();
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
                self.dialogClose();
            })
        },

    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
</style>
