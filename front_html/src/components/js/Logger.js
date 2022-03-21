import store from '../../store/index'

// 打印log
function PrintConsole(name,info){
    if(store.state.isDebug){
        if(info){
            console.log(name,info);
        }else{
            console.log(name);
        }
    }
  
}


export {
    PrintConsole
  };
  