/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-08-31 15:47:10
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-08-31 17:21:52
 * @FilePath: \hebei--vue\src\config\Cookies.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
// import VueCookies from "vue-cookies";
const vueCookies = require('vue-cookies')

//获取cookie
export function getCookie(name) {
    return vueCookies.get(name);
}

//设置cookie,增加到vue实例方便全局调用
export function setCookie(c_name, value, expiredays) {
    // var exdate = new Date(); // 获取当前登录的时间
    // exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * expiredays);
    vueCookies.set(c_name, value, {
        expires: expiredays
    });
};

//删除cookieF
export function delCookie(name) {
    vueCookies.remove(name);
};