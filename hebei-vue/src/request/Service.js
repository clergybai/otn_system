/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-16 15:39:11
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-09 16:16:07
 * @FilePath: \hebei--vue\src\request\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import axios from 'axios'
import {
    ElMessage,
    ElLoading
} from "element-plus";
const ConfigBaseURL = '' //默认路径，这里也可以使用env来判断环境
let loadingInstance = null //这里是loading
//使用create方法创建axios实例
export const Service = axios.create({
    timeout: 1000 * 20, // 请求超时时间
    baseURL: ConfigBaseURL,
    method: 'post',
    headers: {
        'Content-Type': 'application/json;charset=UTF-8'
    }
})
// 添加请求拦截器
// Service.interceptors.request.use(config => {
//     loadingInstance = ElLoading.service({
//         lock: true,
//         text: 'loading...'
//     })
//     return config
// })
// 添加响应拦截器
Service.interceptors.response.use(response => {
    // loadingInstance.close()
    // console.log(response)
    return response.data
}, error => {
    console.log('TCL: error', error)
    const msg = error.Message !== undefined ? error.Message : ''
    ElMessage({
        message: '网络错误' + msg,
        type: 'error',
        duration: 3 * 1000
    })
    // loadingInstance.close()
    return Promise.reject(error)
})