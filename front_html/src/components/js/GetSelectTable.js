import Vue from 'vue'

// Vue.prototype.$axios;

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

function GetPageNameItems(proId){
    return Vue.prototype.$axios.get('/api/PageManagement/GetPageNameItems',{
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

function GetFunNameItems(proId,pageId){
    return Vue.prototype.$axios.get('/api/FunManagement/GetFunNameItems',{
        params:{
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
export {
    NoTokenGetRoleNameItems,GetRoleNameItems,GetPageNameItems,GetFunNameItems,GetUserNameItems,GetPageEnvironmentNameItems
  };
  