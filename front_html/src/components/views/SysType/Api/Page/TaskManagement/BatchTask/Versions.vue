<template>
    <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-click-modal=false
        :before-close="dialogClose"
        width="400px">
        <el-form ref="RomeData" :model="RomeData"  label-width="70px">
            <el-form-item label="版本号:">
                <el-input v-model.trim="RomeData.versions" placeholder="非必填"></el-input>
            </el-form-item>
            <el-button  type="primary" @click="RunBatch()">运行</el-button>
            <el-button @click="ClearRomeData()">重置</el-button>
        </el-form>
    </el-dialog>
</template>

<script>
// import store from '../../../../store/index'
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";

export default {
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            RomeData:{
                batchId:'',
                versions:'',
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
                this.RomeData.batchId = newval.batchId;
                
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self = this;
            self.RomeData.versions='';
        },
        RunBatch(){
            let self = this;
            self.$axios.post('/api/ApiBatchTask/ExecuteBatchTask',Qs.stringify({
                'batchId':self.RomeData.batchId,
                'versions':self.RomeData.versions
            })).then(res => {
            if(res.data.statusCode ==2001){
                self.$message.success('批量任务已启动,任务ID:'+res.data.celeryTaskId+',请稍后在测试报告页面查看结果!');
                self.dialogClose();
            }
            else{
                self.$message.error('批量任务启动失败:'+ res.data.errorMsg);
                self.dialogClose();
            }
            }).catch(function (error) {
                console.log(error)
                self.dialogClose();
            })
        },
    }
};
</script>

<style>
.Item-Button{
    margin-left: -30px;
}
</style>
