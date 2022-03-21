import axios from 'axios'
import router from '../router/index'
import store from '../store/index'
import Qs from 'qs'
import Cookies from 'js-cookie' //引用

function webService()
{
    let baseURL = store.state.BackService;
    let isDebug = store.state.isDebug;
    var api=axios.create(
        {
            baseURL:baseURL

        }
    );
   
    // Ajax 请求拦截器
    api.interceptors.request.use(
        (config)=>{
            if(isDebug){
                console.log('拦截请求流',config);
            }
            let token = Cookies.get('token');
            console.log("token:"+token);
            config.headers["token"]=token||"";
            return config
        }
        ,(err)=>{}
    )

    // Ajax 请求响应拦截器
    api.interceptors.response.use(
        (config)=>{
            if(isDebug){
                console.log('拦截响应流:'+config.config.url,config);
            }
            if(config.data.code==1001){
                
            }else{
                // 跳转登录
                console.log('无效登录,跳回主页');
                router.push('/');//这里需要用到上面的引用，不然会提示不能push
            }
            return config
        }
        ,(err)=>{

        }
    )  
    return api;
}



export default { webService } ;
