/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-05 19:02:18
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-28 19:36:42
 * @FilePath: \hebei--vue\src\router\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import {
  createRouter,
  createWebHistory
} from "vue-router";
import Unicom_routes from '@/router/unicom'
// import Mobile_routes from '@/router/mobile'
import {
  getCookie
} from "@/config/Cookies"
import NProgress from "nprogress";

// import {
//   getEnv
// } from "@/api/WDM-OTN/http"

// let EnvType = null;
// let EnvRoutes = [];
// getEnv().then(res => {
//   if (res.code == 200) {
//     EnvType = res.data;
//     //alert(res.data)
//   }
// })

// if (EnvType === '') {
//   //联通
//   EnvRoutes = [...Unicom_routes];
// } else {
//   //移动
//   EnvRoutes = [...Mobile_routes];
// }


const router = createRouter({
  history: createWebHistory(),
  routes: Unicom_routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title + " - 传送网隐患自动诊断系统";
  }
  const token = getCookie("ustoken");
  if (token) {
    next();
  } else {
    if (to.path == "/login") {
      next();
    } else {
      next({
        path: "/login",
      });
    }
  }
  NProgress.start();
});

router.afterEach(() => {
  // 在即将进入新的页面组件前，关闭掉进度条
  NProgress.done();
});

export default router;