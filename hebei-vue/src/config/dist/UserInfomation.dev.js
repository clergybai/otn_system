"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getPublicKey = exports.getToken = exports.getIs_Authen = exports.getUserName = void 0;

var _index = require("@/store/index");

/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-07-12 14:44:30
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-08-04 10:54:23
 * @FilePath: \hebei--vue\src\config\UserInfomation.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
var vueCookies = require('vue-cookies');

var getUserName = function getUserName() {
  var mainData = (0, _index.useMainStore)();
  var username = vueCookies.get("usn");

  if (mainData.userInformation.userName) {
    return mainData.userInformation.userName;
  } else {
    return username;
  }
};

exports.getUserName = getUserName;

var getIs_Authen = function getIs_Authen() {
  var mainData = (0, _index.useMainStore)();
  var is_authen = sessionStorage.getItem("is_authen");

  if (mainData.userInformation.userName) {
    return mainData.is_authen;
  } else {
    return JSON.parse(is_authen);
  }
};

exports.getIs_Authen = getIs_Authen;

var getToken = function getToken() {
  var mainData = (0, _index.useMainStore)();
  var is_authen = vueCookies.get("ustoken");

  if (mainData.userInformation.token) {
    return mainData.userInformation.token;
  } else {
    return is_authen;
  }
};

exports.getToken = getToken;

var getPublicKey = function getPublicKey() {
  var mainData = (0, _index.useMainStore)();
  var pK = vueCookies.get("pK");

  if (mainData.publicKey) {
    return mainData.publicKey;
  } else {
    return pK;
  }
};

exports.getPublicKey = getPublicKey;