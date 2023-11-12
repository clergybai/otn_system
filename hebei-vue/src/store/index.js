/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-30 15:14:41
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-06-21 14:45:06
 * @FilePath: \hebei--vue\src\store\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import { defineStore } from "pinia";
// 1.定义容器
// 2.使用容器中的 state
// 3.修改state
// 4.容器中的action的使用
// 参数1： 容器ID，必须唯一，将来pinia会把所有的容器挂载到跟容器
export const useMainStore = defineStore("main", {
  // 类似于data，用来存储全局状态
  state: () => {
    return {
      userInformation: {
        userId: null,
        orgID: null,
        userName: null,
        trueName: null,
        mobilePhone: null,
        telephone: null,
        fax: null,
        address: null,
        email: null,
        orgCode: null,
        personType: null,
        job: null,
        professional: null,
        jobNum: null,
        category: null,
        remark: null,
        token: null,
        userRole: null,
      },
      publicKey: null,
      authen_zones: [],
      is_authen: {},
    };
  },
  // 类似于组建的conputed，用来封装计算属性，有缓存的功能
  getters: {},
  // 类似于组建的methods，封装业务逻辑，修改state
  actions: {},
});
