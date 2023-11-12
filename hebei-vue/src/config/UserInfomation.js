/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-07-12 14:44:30
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-08-31 18:08:07
 * @FilePath: \hebei--vue\src\config\UserInfomation.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import {
    useMainStore
} from "@/store/index";
import {
    getCookie
} from "@/config/Cookies"
// const vueCookies = require('vue-cookies')

export const getUserName = () => {
    const mainData = useMainStore();
    // const usn = vueCookies.get("usn");
    const usn = getCookie("usn");
    if (mainData.userInformation.userName) {
        return mainData.userInformation.userName;
    } else {
        return usn;
    }
}

export const getIs_Authen = () => {
    const mainData = useMainStore();
    // const is_authen = sessionStorage.getItem("is_authen");
    // const is_authen = vueCookies.get("is_authen");
    const is_authen = getCookie("is_authen");
    if (mainData.userInformation.userName) {
        return mainData.is_authen;
    } else {
        return is_authen;
    }
}

export const getToken = () => {
    const mainData = useMainStore();
    // const ustoken = vueCookies.get("ustoken");
    const ustoken = getCookie("ustoken");
    if (mainData.userInformation.token) {
        return mainData.userInformation.token;
    } else {
        return ustoken;
    }
}

export const getPublicKey = () => {
    const mainData = useMainStore();
    // const pK = vueCookies.get("pK");
    const pK = getCookie("pK");
    if (mainData.publicKey) {
        return mainData.publicKey;
    } else {
        return pK;
    }
}