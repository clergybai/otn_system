/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-30 15:13:07
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-28 19:08:30
 * @FilePath: \hebei--vue\src\API\WDM-OTN\http.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import {
    Service
} from '@/request/Service'

//获取环境
export function getEnv() {
    return Service({
        url: '/loginApi/Login/getEnv',
        method: "get",
    })
}

//登录
export function getSSid(data) {
    return Service({
        url: '/loginApi/Login/ssid/',
        method: "post",
        data: data
    })
}


export function getPublicKey(data) {
    return Service({
        url: '/loginApi/Login/key/',
        method: "post",
        data: data
    })
}

export function getLogin(data) {
    return Service({
        url: '/loginApi/Login/login/',
        method: "post",
        data: data
    })
}

export function getSsid(data) {
    return Service({
        url: '/loginApi/Login/ssid/',
        method: "post",
        data: data
    })
}

export function UserInfoLoad(data) {
    return Service({
        url: '/woOperationApi/PAOOS/aaaa/userservice/getUserInfo.do',
        method: "get",
        params: data
    })
}

export function getToken(data) {
    return Service({
        url: '/loginApi/Login/getToken',
        method: "get",
        params: data
    })
}

export function updatePwd(data) {
    return Service({
        url: '/loginApi/User/updatePwd/',
        method: "post",
        data: data
    })
}

export function restoreUser(data) {
    return Service({
        url: '/loginApi/User/restore/',
        method: "post",
        data: data
    })
}



//传输系统
export function getMenu(data) {
    return Service({
        url: '/loginApi/Permissions/getMenu/',
        method: "post",
        data: data
    })
}

export function getDraw(data) {
    return Service({
        url: '/api/DrawTopo/draw/',
        method: "post",
        data: data
    })
}

export function getOa(data) {
    return Service({
        url: '/api/DrawTopo/getOaDetails/',
        method: "post",
        data: data
    })
}

export function getFiber(data) {
    return Service({
        url: '/api/DrawTopo/getFiberDetails/',
        method: "post",
        data: data
    })
}

export function setPosition(data) {
    return Service({
        url: '/api/DrawTopo/position/',
        method: "post",
        data: data
    })
}

export function getMain(data) {
    return Service({
        url: '/api/DrawTopo/getMainSiteDetail/',
        method: "post",
        data: data
    })
}

export function getOla(data) {
    return Service({
        url: '/api/DrawTopo/getOlaDetails/',
        method: "post",
        data: data
    })
}



//用户管理
export function addUser(data) {
    return Service({
        url: '/loginApi/User/addUser/',
        method: "post",
        data: data
    })
}

export function editUser(data) {
    return Service({
        url: '/loginApi/User/editUser/',
        method: "post",
        data: data
    })
}

export function getUser(data) {
    return Service({
        url: '/loginApi/User/getUserInfo/',
        method: "post",
        data: data
    })
}

export function delUser(data) {
    return Service({
        url: '/loginApi/User/removeUser/',
        method: "post",
        data: data
    })
}



//权限配置
export function getPerm() {
    return Service({
        url: '/loginApi/Permissions/getPerm/',
        method: "get",
    })
}

export function setPerm(data) {
    return Service({
        url: '/loginApi/Permissions/setPermission/',
        method: "post",
        data: data
    })
}

export function getCity() {
    return Service({
        url: '/loginApi/Permissions/getCity/',
        method: "get",
    })
}



//基准值
export function getRule(data) {
    return Service({
        url: '/paramsApi/Threshold/get_rule_with_name',
        method: "post",
        data: data
    })
}

export function updateRule(data) {
    return Service({
        url: '/paramsApi/Threshold/update_rule',
        method: "post",
        data: data
    })
}

export function getDefaultBaseLine() {
    return Service({
        url: '/paramsApi/base_line/get_default',
        method: "get",
    })
}

export function getDefaultThreshold() {
    return Service({
        url: '/paramsApi/Threshold/get_default',
        method: "get",
    })
}

export function getOutline(data) {
    return Service({
        url: '/paramsApi/Threshold/get_outline',
        method: "post",
        data: data
    })
}

export function delRule(data) {
    return Service({
        url: '/paramsApi/Threshold/delete_rule',
        method: "post",
        data: data
    })
}

export function updateState(data) {
    return Service({
        url: '/paramsApi/Threshold/update_status_used',
        method: "post",
        data: data
    })
}



//数据导入
//可调光衰现网配置
export function getConfig(data) {
    return Service({
        url: '/paramsApi/voa_config/get',
        method: "post",
        data: data
    })
}

export function updateConfig(data) {
    return Service({
        url: '/paramsApi/voa_config/edit',
        method: "post",
        data: data
    })
}

export function addBoardStandard(data) {
    return Service({
        url: '/paramsApi/oa_board_standard/add',
        method: "post",
        data: data
    })
}

export function updateStandardCalculate(data) {
    return Service({
        url: '/paramsApi/oa_board_standard/calculate',
        method: "post",
        data: data
    })
}

export function getConfigFilter() {
    return Service({
        url: '/paramsApi/voa_config/getFilter',
        method: "get",
    })
}



//现网光放板卡信息
export function getBoard(data) {
    return Service({
        url: '/paramsApi/oa_board_type/get',
        method: "post",
        data: data
    })
}

export function updateBoard(data) {
    return Service({
        url: '/paramsApi/oa_board_type/edit',
        method: "post",
        data: data
    })
}

export function addBoardType(data) {
    return Service({
        url: '/paramsApi/oa_board_type/add',
        method: "post",
        data: data
    })
}

export function updateTypeCalculate(data) {
    return Service({
        url: '/paramsApi/oa_board_type/calculate',
        method: "post",
        data: data
    })
}

export function getTypeFilter() {
    return Service({
        url: '/paramsApi/oa_board_type/getFilter',
        method: "get",
    })
}



//光放板卡标准参数
export function getBoardStandard(data) {
    return Service({
        url: '/paramsApi/oa_board_standard/get',
        method: "post",
        data: data
    })
}

export function updateBoardStandard(data) {
    return Service({
        url: '/paramsApi/oa_board_standard/edit',
        method: "post",
        data: data
    })
}

export function updateBoardStandardCalculate(data) {
    return Service({
        url: '/paramsApi/oa_board_standard/calculate',
        method: "post",
        data: data
    })
}

export function getBoardStandardFilter() {
    return Service({
        url: '/paramsApi/oa_board_standard/getFilter',
        method: "get",
    })
}



//复用段波道数配置
export function getMsl(data) {
    return Service({
        url: '/paramsApi/msl/get',
        method: "post",
        data: data
    })
}

export function updateMsl(data) {
    return Service({
        url: '/paramsApi/msl/edit',
        method: "post",
        data: data
    })
}



//隐患列表
export function getHideMenu(data) {
    return Service({
        url: '/loginApi/Permissions/getMenu/',
        method: "post",
        data: data
    })
}

export function getTrouble(data) {
    return Service({
        url: '/api/GetTrouble/getTrouble',
        method: "post",
        data: data
    })
}

export function exportOrderListData() {
    return Service({
        url: '/api/GetTrouble/exportOrderListData/',
        method: "get",
    })
}

export function getTroubleFilter() {
    return Service({
        url: '/api/GetTrouble/getFilter',
        method: "get",
    })
}

export function getTroubleFilterLarterPart() {
    return Service({
        url: '/api/GetTrouble/getFilterLarterPart',
        method: "get",
    })
}

export function getCityFilter(data) {
    return Service({
        url: '/api/GetTrouble/getCityFilter',
        method: "post",
        data: data
    })
}



//隐患概览
export function getUnhandled(data) {
    return Service({
        url: '/api/GetTrouble/unhandled/',
        method: "post",
        data: data
    })
}

export function getStatistics(data) {
    return Service({
        url: '/api/GetTrouble/Statistics/',
        method: "post",
        data: data
    })
}

export function getLevel(data) {
    return Service({
        url: '/api/GetTrouble/level/',
        method: "post",
        data: data
    })
}

export function getCityHiddenGroup() {
    return Service({
        url: '/api/GetTrouble/cityHiddenGroup',
        method: "get",
    })
}

export function getAnnualRiskGroup() {
    return Service({
        url: '/api/GetTrouble/annualRiskGroup',
        method: "get",
    })
}

export function getHazardLevelCityGroup(data) {
    return Service({
        url: '/api/GetTrouble/HazardLevelCityGroup/',
        method: "post",
        data: data
    })
}

export function getHazardLevelDistrictGroup(data) {
    return Service({
        url: '/api/GetTrouble/HazardLevelDistrictGroup',
        method: "post",
        data: data
    })
}

export function getHiddenCity() {
    return Service({
        url: '/api/GetTrouble/getHiddenCity',
        method: "get",
    })
}

export function getHiddenNetworkLevel() {
    return Service({
        url: '/api/GetTrouble/getHiddenNetworkLevel',
        method: "get",
    })
}
















//计算
export function startComputed() {
    return Service({
        url: '/listenningApi/PGListening/startComputed',
        method: "get",
    })
}

export function getComputedState() {
    return Service({
        url: '/listenningApi/PGListening/getComputedState',
        method: "get",
    })
}

export function getMslFilter() {
    return Service({
        url: '/paramsApi/msl/getFilter',
        method: "get",
    })
}



// 操作日志
export const logModuleMenu = Object.freeze({
    Login: "登录模块",
    SPOTODB: "系统管理/数据导入/光放板卡标准参数",
    IATODBOTLN: "系统管理/数据导入/现网光放板卡信息",
    AODNC: "系统管理/数据导入/可调光衰现网配置",
    TNR: "系统管理/基准值规则/新增规则",
    VTR: "系统管理/基准值规则/查看规则",
    COCNOMS: "系统管理/复用段波道数配置",
    UM: "系统管理/权限配置/用户管理",
    RM: "系统管理/权限配置/权限管理",
    MORV: "TOP平台/基准值修改",
});

export const operationMenu = Object.freeze({
    login: "登录",
    logout: "注销",
    add: "增",
    delete: "删",
    update: "改",
    add_del_update: "增/删/改"
});

export function setLog(data) {
    return Service({
        url: '/loginApi/OperationLog/setLog/',
        method: "post",
        data: data
    })
}

export function getLog(data) {
    return Service({
        url: '/loginApi/OperationLog/getLog/',
        method: "post",
        data: data
    })
}

export function getPmMca(data) {
    return Service({
        url: '/paramsApi/pm_mca/',
        method: "get",
        params: data
    })
}

//再生数据段参数
export function getCheckTopology(data) {
    return Service({
        url: '/paramsApi/check_topology/get',
        method: "post",
        data: data
    })
}

export function updateCheckTopology(data) {
    return Service({
        url: '/paramsApi/check_topology/edit',
        method: "post",
        data: data
    })
}

export function updateCheckTopologyCalculate(data) {
    return Service({
        url: '/paramsApi/check_topology/calculate',
        method: "post",
        data: data
    })
}

export function getCheckTopologyFilter() {
    return Service({
        url: '/paramsApi/check_topology/getFilter',
        method: "get",
    })
}

export function exportCheckTopologyData(data) {
    return Service({
        url: '/paramsApi/check_topology/exportData/',
        method: "post",
        data: data
    })
}

//光网元数据参数
export function getCheckOpticalNe(data) {
    return Service({
        url: '/paramsApi/check_optical_ne/get',
        method: "post",
        data: data
    })
}

export function updateCheckOpticalNe(data) {
    return Service({
        url: '/paramsApi/check_optical_ne/edit',
        method: "post",
        data: data
    })
}

export function updateCheckOpticalNeCalculate(data) {
    return Service({
        url: '/paramsApi/check_optical_ne/calculate',
        method: "post",
        data: data
    })
}

export function getCheckOpticalNeFilter() {
    return Service({
        url: '/paramsApi/check_optical_ne/getFilter',
        method: "get",
    })
}

export function exportCheckOpticalNeData(data) {
    return Service({
        url: '/paramsApi/check_optical_ne/exportData/',
        method: "post",
        data: data
    })
}

//光放板数据参数
export function getCheckOaBoardType(data) {
    return Service({
        url: '/paramsApi/check_oa_board_type/get',
        method: "post",
        data: data
    })
}

export function updateCheckOaBoardType(data) {
    return Service({
        url: '/paramsApi/check_oa_board_type/edit',
        method: "post",
        data: data
    })
}

export function updateCheckOaBoardTypeCalculate(data) {
    return Service({
        url: '/paramsApi/check_oa_board_type/calculate',
        method: "post",
        data: data
    })
}

export function getCheckOaBoardTypeFilter() {
    return Service({
        url: '/paramsApi/check_oa_board_type/getFilter',
        method: "get",
    })
}

export function exportCheckOaBoardTypeData(data) {
    return Service({
        url: '/paramsApi/check_oa_board_type/exportData/',
        method: "post",
        data: data
    })
}

//可调光衰数据参数
export function getCheckVoa(data) {
    return Service({
        url: '/paramsApi/check_voa/get',
        method: "post",
        data: data
    })
}

export function updateCheckVoa(data) {
    return Service({
        url: '/paramsApi/check_voa/edit',
        method: "post",
        data: data
    })
}

export function updateCheckVoaCalculate(data) {
    return Service({
        url: '/paramsApi/check_voa/calculate',
        method: "post",
        data: data
    })
}

export function getCheckVoaFilter() {
    return Service({
        url: '/paramsApi/check_voa/getFilter',
        method: "get",
    })
}

export function exportCheckVoaData(data) {
    return Service({
        url: '/paramsApi/check_voa/exportData/',
        method: "post",
        data: data
    })
}

//性能数据参数
export function getCheckPm(data) {
    return Service({
        url: '/paramsApi/check_pm/get',
        method: "post",
        data: data
    })
}

export function updateCheckPm(data) {
    return Service({
        url: '/paramsApi/check_pm/edit',
        method: "post",
        data: data
    })
}

export function updateCheckPmCalculate(data) {
    return Service({
        url: '/paramsApi/check_pm/calculate',
        method: "post",
        data: data
    })
}

export function getCheckPmFilter() {
    return Service({
        url: '/paramsApi/check_pm/getFilter',
        method: "get",
    })
}

export function exportCheckPmData(data) {
    return Service({
        url: '/paramsApi/check_pm/exportData/',
        method: "post",
        data: data
    })
}

// import { getCookie } from "@/config/Cookies";
// import { NowDate } from "@/config/formatTime";
// import {
//     setLog,
//     logModuleMenu,
//     operationMenu,
// } from "@/api/WDM-OTN/http";

// const user = getCookie("usn");
// setLog({
//     op_module: logModuleMenu.Login,
//     op_user: user,
//     op_behavior: user + operationMenu.login,
//     op_time: NowDate(),
// });