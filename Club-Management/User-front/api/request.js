import axios from "axios"

const request = axios.create({
    baseURL: "http://localhost:8080/happy",
    timeout: 10000,
})

request.interceptors.request.use((config) => {
    return config;
},error => {
    return Promise.reject(error);
});

request.interceptors.response.use((response)=>{
    return response.data;
},(error)=>{
    let message = '';
    const status = error.response?.status ? error.response?.status : 0;

    switch(status){
        case 401:
            message = "TOKEN过期"
            break;
        case 403:
            message = "无权访问"
            break;
        case 404:
            message = "请求页面错误"
            break;
        case 500:
            message = "服务器错误"
            break;
        default:
            message = "网络错误"
            break;
    }

    uni.showToast({
      title: message,
      icon: 'error'
    })
    return Promise.reject(error);
})

export default request;