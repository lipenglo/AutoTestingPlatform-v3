<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="780px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
                <el-card style="height:870px" v-loading="loading">
                    <div style=" height:830px;overflow:auto">
                        <el-timeline style="text-align: left;">
                            <el-timeline-item 
                                placement="top"
                                v-for="(activity, index) in RomeData.activities"
                                :key="index"
                                :timestamp="activity.timestamp">
                            <el-card style="width:600px">
                                <h4>{{activity.title}}</h4>
                                <p v-html="activity.content" style="white-space: pre-line;"></p>
                            </el-card>
                            </el-timeline-item>
                        </el-timeline>
                    </div>
                </el-card>
            </el-drawer>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import {PrintConsole} from "../../../../../../js/Logger.js";


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
                activities:[],
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
                // this.isAddNew = newval.isAddNew;
                this.SelectData(newval.apiId);
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        ClearRomeData(){
            let self=this;
            self.RomeData.activities=[];
        },
        SelectData(apiId){
            let self = this;
            self.loading=true;
            self.$axios.get('/api/ApiIntMaintenance/SelectLifeCycle',{
                params:{
                    "apiId":apiId,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.activities=res.data.TableData;
                    self.loading=false;
                }else{
                    self.$message.error('获取数据失败:'+res.data.errorMsg);
                    self.loading=false;
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

</style>
