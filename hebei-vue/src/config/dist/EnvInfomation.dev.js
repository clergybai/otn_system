"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getFileAddress = void 0;

/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-07-13 16:29:27
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-07-13 16:30:13
 * @FilePath: \hebei--vue\src\config\EnvInfomation.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
var getFileAddress = function getFileAddress() {
  return process.env.Vue_Env;
};

exports.getFileAddress = getFileAddress;