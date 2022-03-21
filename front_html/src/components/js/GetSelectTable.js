import Vue from 'vue'

// Vue.prototype.$axios;

//通用
// 获取项目名称下拉列表-无Token版本
function NoTokenGetRoleNameItems(){
    return Vue.prototype.$axios.get('/api/role/NoTokenGetRoleNameItems',{
        params:{
            // 'data':{}
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}

function GetRoleNameItems(){
    return Vue.prototype.$axios.get('/api/role/GetRoleNameItems',{
        params:{
            // 'data':{}
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}

function GetPageNameItems(sysType,proId){
    return Vue.prototype.$axios.get('/api/PageManagement/GetPageNameItems',{
        params:{
            'sysType':sysType,
            'proId':proId,
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}

function GetFunNameItems(sysType,proId,pageId){
    return Vue.prototype.$axios.get('/api/FunManagement/GetFunNameItems',{
        params:{
            'sysType':sysType,
            'proId':proId,
            'pageId':pageId,
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}

function GetPageEnvironmentNameItems(proId){
    return Vue.prototype.$axios.get('/api/PageEnvironment/GetPageEnvironmentNameItems',{
        params:{
            'proId':proId,
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}

function GetUserNameItems(){
    return Vue.prototype.$axios.get('/api/userManagement/GetUserNameItems',{
        params:{
  
        }
    }).then(res => {
        if(res.data.statusCode == 2000){
            // console.log(res.data.itemsData)
            return res.data.itemsData;
        }
    }).catch(function (error) {
        console.log(error);
    })
}

//加载关联页面
function GetAssociatedPageNameItems(sysType,passPageId){
    return Vue.prototype.$axios.get('/api/PageManagement/GetAssociatedPageNameItems',{
        params:{
            'sysType':sysType,
            'passPageId':passPageId
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}

//加载数据库环境的IP及以下可用的库名
function GetConnectBaseItems(){
    return Vue.prototype.$axios.get('/api/DataBaseEnvironment/GetConnectBaseItems',{
        params:{
            // 'sysType':sysType
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}


//API


//UI
//加载元素的操作类型
function GetElementOperationTypeItems(){
    return Vue.prototype.$axios.get('/api/UiElementEvent/GetElementOperationTypeItems',{
        params:{
            
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}


//加载元素
function GeElementNameItems(pageIdList){
    return Vue.prototype.$axios.get('/api/UiElementMaintenance/GetElementNameItems',{
        params:{
            'pageIdList':pageIdList
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}

//加载用例列表,根据页面Id及需要排除的用例id
function GetUiCaseNameItems(proId,pageIdList,passCaseId){
    return Vue.prototype.$axios.get('/api/UiCaseMaintenance/GetCaseNameItems',{
        params:{
            'proId':proId,
            'pageIdList':pageIdList,
            'passCaseId':passCaseId,
        }
    }).then(res => {
        return res.data;
    }).catch(function (error) {
        console.log(error);
    })
}

export {
    NoTokenGetRoleNameItems,GetRoleNameItems,GetPageNameItems,GetFunNameItems,GetUserNameItems,GetPageEnvironmentNameItems,GetAssociatedPageNameItems,GetConnectBaseItems,

    
    GetElementOperationTypeItems,GeElementNameItems,GetUiCaseNameItems
  };
  