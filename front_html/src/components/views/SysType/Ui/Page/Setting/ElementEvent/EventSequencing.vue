<template>
    <el-drawer
        :title="dialogTitle"
        size="400px"
        :wrapperClosable="false"
        :visible.sync="dialogVisible"
        direction='rtl'
        :before-close="dialogClose">
            <el-tree
                v-loading="loading"
                :data="RomeData.TreeData"
                node-key="id"
                @node-drop="handleDrop"
                draggable
                :allow-drag="allowDrag"
                :allow-drop="allowDrop">
            </el-tree>
    </el-drawer>
</template>

<script>
import Qs from 'qs'
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            RomeData:{
                TreeData:[]
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
                this.LoadOperationData();

            }
        },
     
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
            this.$emit('Succeed');//回调查询
        },
        ClearRomeData(){
            let self = this;
            self.RomeData.TreeData=[];
        },
        allowDrag(draggingNode){//判断节点能否被拖拽
            PrintConsole(draggingNode);
            if(draggingNode.data.allowDrag){//可拖动时
                return true
            }else{
                return false
            }
            // return draggingNode.data.label.indexOf('二级 2-1') === -1;//这个例子是不让这个可以拖动
        },
        allowDrop(draggingNode, dropNode, type) {//拖拽时判定目标节点能否被放置
            // console.log('tree drop: ', dropNode);
            //  PrintConsole('type: ', type);
            if (dropNode.data.allowDrop === false) {
                return type !== 'inner';//这里我是没搞懂 但是功能能实现，vue官网上的例子
            } else {
                return true;
            }
        },
        handleDrop(draggingNode, dropNode, dropType, ev) {//拖拽完成后的操作
            PrintConsole('tree drop: ', dropNode);
            PrintConsole('TreeData',this.RomeData.TreeData);
            
            let self = this;
            self.loading=true;
            self.$axios.post('/api/UiElementEvent/UpdateOperationSort',{
                'TreeData':self.RomeData.TreeData
            }).then(res => {
                if(res.data.statusCode ==2002){
                    self.$message.success('排序更新成功!');
                    self.loading=false;
                }   
                else{
                    self.$message.error('排序更新失败:'+ res.data.errorMsg);
                    self.loading=false;
                }
            }).catch(function (error) {
                self.$message.error(error);
                self.loading=false;
                self.dialogClose();
            })
        },
        LoadOperationData(){
            let self = this;
            self.loading=true;
            self.$axios.get('/api/UiElementEvent/LoadOperationData',{
                params:{

                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.TreeData = res.data.treeData;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
                }
                // console.log(self.tableData);
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

</style>
