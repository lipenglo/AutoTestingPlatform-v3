<template>
    <div style="height: 775px;">
        <el-form ref="RomeData"  :model="RomeData">
            <el-form-item>
                <el-row :gutter="20">
                    <el-col :span="16">
                        <div style="margin-top:-18px">
                            <el-divider>代码编写区</el-divider>
                            <el-row>
                                <el-col :span="22">
                                    <div style="text-align: center;">
                                        <!-- <sapn>lipenglo(古雨辰) 最后更新时间:2021-21-12 14:22:22</sapn> -->
                                        <span>{{RomeData.titleInfo}}</span>
                                    </div>
                                </el-col>
                                <el-col :span="2">
                                    <div style="float:right">
                                        <el-form-item>
                                            <el-button  type="primary" @click="DataSave()">Save</el-button>
                                        </el-form-item>
                                    </div>
                                </el-col>
                            </el-row>
                            
                        </div>
                        <div style="margin-top:10px">
                            <el-form-item>
                                <el-input 
                                    type="textarea" 
                                    tabindex
                                    :autosize="{ minRows: 30, maxRows: 30}" 
                                    v-model="RomeData.codeEditText">
                                </el-input>
                            </el-form-item>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div style="margin-top:-18px">
                            <el-divider>代码调试区</el-divider>
                            <el-form-item>
                                <el-input v-model="RomeData.debugInput" placeholder="请输入调用方法" style="width:400px"></el-input>
                                <el-button  type="success" @click="RunDebug()">Run</el-button>
                            </el-form-item>
                            <el-divider>代码返回区</el-divider>
                            <div
                                v-loading="loading"
                                element-loading-text="调用执行中"
                                element-loading-spinner="el-icon-loading">
                                <el-input 
                                    type="textarea" 
                                    tabindex
                                    readonly
                                    :autosize="{ minRows: 28, maxRows: 4}" 
                                    v-model="RomeData.codeReturnText">
                                </el-input>
                            </div>
                        </div>
                    </el-col>
                </el-row>
            
            </el-form-item>
        </el-form>
    </div>
</template>

<script>

export default {
    components: {
    },
    data() {
        return {
            loading:false,
            RomeData:{
                titleInfo:'',
                codeEditText:'',
                debugInput:'',
                codeReturnText:'',

            },

        };
    },
    mounted(){
        this.SelectData();
    },
    methods: {
        SelectData(){//刷新列表数据
            let self = this;
            self.RomeData.codeEditText='';
            self.$axios.get('/api/DebugTalk/SelectData',{
                params:{
                    'sysType':'UI',
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.titleInfo = res.data.titleInfo;
                    self.RomeData.codeEditText = res.data.Text;
                }else{
                    self.$message.error(res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        DataSave(){
            let self = this;
            self.$axios.post('/api/DebugTalk/DataSave',{
                'sysType':'UI',
                'text':self.RomeData.codeEditText,
            }).then(res => {
                if(res.data.statusCode==2001){
                    self.$message.success('DebugTalk保存完成!');
                    this.SelectData();
                }else{
                    self.$message.error('DebugTalk保存失败'+res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        RunDebug(){
            let self = this;
            self.loading=true;
            self.RomeData.codeReturnText= '';
            self.$axios.get('/api/DebugTalk/RunDebug',{
                params:{
                    'sysType':'UI',
                    'methods':self.RomeData.debugInput,
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.codeReturnText = res.data.retData;
                    self.loading=false;
                }else{
                    self.RomeData.codeReturnText = res.data.errorMsg;
                    self.loading=false;
                }
            }).catch(function (error) {
                console.log(error);
                self.loading=false;
            })
        },
    }
};
</script>

<style>

</style>
