/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-09-19 14:32:43
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-20 16:15:00
 * @FilePath: \hebei--vue\src\router\unicom.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
///联通路由

///数据导入子路由
const dataImport_routes = [{
        path: "/main/WDM/OTN/systemSettings/dataImport/putCardLightStandardParameters",
        name: "putCardLightStandardParameters",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/dataImport/putCardLightStandardParameters"
            ),
        meta: {
            title: "光放板卡标准参数",
        },
    },
    {
        path: "/main/WDM/OTN/systemSettings/dataImport/nowNetPutCardLightInformation",
        name: "nowNetPutCardLightInformation",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/dataImport/nowNetPutCardLightInformation"
            ),
        meta: {
            title: "现网光放板卡信息",
        },
    },
    {
        path: "/main/WDM/OTN/systemSettings/dataImport/adjustableDimLiveNetConfiguration",
        name: "adjustableDimLiveNetConfiguration",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/dataImport/adjustableDimLiveNetConfiguration"
            ),
        meta: {
            title: "可调光衰现网配置",
        },
    },
];

///单波数据导入子路由
const single_wave_dataImport_routes = [{
    path: "/main/WDM/OTN/systemSettings/singleWaveDataImport/zetSweeperBoard",
    name: "zetSweeperBoard",
    component: () =>
        import(
            "../views/WDM-OTN/systemSettings/singleWaveDataImport/zetSweeperBoard"
        ),
    meta: {
        title: "中兴扫波板性能数据",
    },
},
{
    path: "/main/WDM/OTN/systemSettings/singleWaveDataImport/fhSweeperBoard",
    name: "fhSweeperBoard",
    component: () =>
        import(
            "../views/WDM-OTN/systemSettings/singleWaveDataImport/fhSweeperBoard"
        ),
    meta: {
        title: "烽火扫波板性能数据",
    },
},
];

///基准值规则子路由
const baselineRule_routes = [{
        //默认规则
        path: "/main/WDM/OTN/systemSettings/baselineRule/defaultRule",
        name: "defaultRule",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/baselineRule/defaultRule/defaultRule.vue"
            ),
        meta: {
            title: "默认规则",
        },
    },
    {
        //创建规则
        path: "/main/WDM/OTN/systemSettings/baselineRule/createRule",
        name: "createRule",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/baselineRule/createRule/createRule.vue"
            ),
        meta: {
            title: "新增规则",
        },
    },
    {
        //查看规则
        path: "/main/WDM/OTN/systemSettings/baselineRule/viewRule",
        name: "viewRule",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/baselineRule/viewRule/viewRule.vue"
            ),
        meta: {
            title: "菜单管理",
        },
    },
];

///单波规则子路由
const singleWaveRule_routes = [{
        //创建规则
        path: "/main/WDM/OTN/systemSettings/singleWaveRule/createRule",
        name: "createSingleWaveRule",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/singleWaveRule/createRule/createRule.vue"
            ),
        meta: {
            title: "新增规则",
        },
    },
    {
        //查看规则
        path: "/main/WDM/OTN/systemSettings/singleWaveRule/viewRule",
        name: "viewSingleWaveRule",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/singleWaveRule/viewRule/viewRule.vue"
            ),
        meta: {
            title: "查看规则",
        },
    },
];

///权限管理子路由
const perms_routes = [
    //用户管理
    {
        path: "/main/WDM/OTN/systemSettings/permissionsConfiguration/userManage",
        name: "userManage",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/permissionsManage/userManage/userManage.vue"
            ),
        meta: {
            title: "用户管理",
        },
    },
    //菜单管理
    {
        path: "/main/WDM/OTN/systemSettings/permissionsConfiguration/menuManage",
        name: "menuManage",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/permissionsManage/menuManage/menuManage.vue"
            ),
        meta: {
            title: "菜单管理",
        },
    },
];

///系统设置子路由
const system_routes = [
    //数据导入
    {
        path: "/main/WDM/OTN/systemSettings/dataImport",
        name: "dataImport",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/dataImport/index.vue"
            ),
        meta: {
            title: "数据导入",
        },
        children: dataImport_routes,
        redirect: "/main/WDM/OTN/systemSettings/dataImport/putCardLightStandardParameters",
    },
    //单波数据导入
    {
        path: "/main/WDM/OTN/systemSettings/singleWaveDataImport",
        name: "singleWaveDataImport",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/singleWaveDataImport/index.vue"
            ),
        meta: {
            title: "单波数据导入",
        },
        children: single_wave_dataImport_routes,
        redirect: "/main/WDM/OTN/systemSettings/singleWaveDataImport/zetSweeperBoard",
    },
    //基准值规则
    {
        path: "/main/WDM/OTN/systemSettings/baselineRule",
        name: "baselineRule",
        component: () =>
            import("../views/WDM-OTN/systemSettings/baselineRule"),
        meta: {
            title: "基准值规则",
        },
        children: baselineRule_routes
    },
    //单波规则
    {
        path: "/main/WDM/OTN/systemSettings/singleWaveRule",
        name: "singleWaveRule",
        component: () =>
            import("../views/WDM-OTN/systemSettings/singleWaveRule"),
        meta: {
            title: "单波规则",
        },
        children: singleWaveRule_routes
    },
    //复用段波道数配置
    {
        path: "/main/WDM/OTN/systemSettings/multiChannelConf",
        name: "multiChannelConf",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/multiChannelConf/index.vue"
            ),
        meta: {
            title: "复用段波道数配置",
        },
    },
    {
        //权限配置
        path: "/main/WDM/OTN/systemSettings/permissionsConfiguration",
        name: "permissionsConfiguration",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/permissionsManage/index.vue"
            ),
        meta: {
            title: "权限配置",
        },
        children: perms_routes
    },
    //波道数维护
    {
        path: "/main/WDM/OTN/systemSettings/channelNumberMaintenance",
        name: "channelNumberMaintenance",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/channelNumberMaintain/index.vue"
            ),
        meta: {
            title: "波道数维护",
        },
    },
    //操作日志
    {
        path: "/main/WDM/OTN/systemSettings/operationLog",
        name: "operationLog",
        component: () =>
            import(
                "../views/WDM-OTN/systemSettings/operationLog/index.vue"
            ),
        meta: {
            title: "操作日志",
        },
    },
];

///数据治理子路由
const dataManagement_routes = [
    //再生段数据
    {
        path: "/main/WDM/OTN/dataManagement/regenSectionData",
        name: "regenSectionData",
        component: () =>
            import(
                "../views/WDM-OTN/dataManagement/regenSectionData/index.vue"
            ),
        meta: {
            title: "再生段数据",
        },
    },
    //光网元数据
    {
        path: "/main/WDM/OTN/dataManagement/optNetworkData",
        name: "optNetworkData",
        component: () =>
            import(
                "../views/WDM-OTN/dataManagement/optNetworkData/index.vue"
            ),
        meta: {
            title: "光网元数据",
        },
    },
    //光放板数据
    {
        path: "/main/WDM/OTN/dataManagement/optAmplifierData",
        name: "optAmplifierData",
        component: () =>
            import(
                "../views/WDM-OTN/dataManagement/optAmplifierData/index.vue"
            ),
        meta: {
            title: "光放板数据",
        },
    },
    //可调光衰数据
    {
        path: "/main/WDM/OTN/dataManagement/adjLightAttenuationData",
        name: "adjLightAttenuationData",
        component: () =>
            import(
                "../views/WDM-OTN/dataManagement/adjLightAttenuationData/index.vue"
            ),
        meta: {
            title: "可调光衰数据",
        },
    },
    //性能数据
    {
        path: "/main/WDM/OTN/dataManagement/performanceData",
        name: "performanceData",
        component: () =>
            import(
                "../views/WDM-OTN/dataManagement/performanceData/index.vue"
            ),
        meta: {
            title: "性能数据",
        },
    },
];

///WDM/OTN子路由
const WDM_OTN_routes = [
    //网络概览
    {
        path: "/main/WDM/OTN/networkOverview",
        name: "networkOverview",
        component: () =>
            import("../views/WDM-OTN/networkOverview/index.vue"),
        meta: {
            title: "隐患概览",
        },
    },
    //传输系统
    {
        path: "/main/WDM/OTN/transmissionSystem",
        name: "transmissionSystem",
        component: () =>
            import("../views/WDM-OTN/transmissionSystem/index.vue"),
        meta: {
            title: "传输系统",
        },
    },
    //隐患列表
    {
        path: "/main/WDM/OTN/hiddenDangerList",
        name: "hiddenDangerList",
        component: () =>
            import("../views/WDM-OTN/hiddenTroubleList/index.vue"),
        meta: {
            title: "隐患列表",
        },
    },
    //数据治理
    {
        path: "/main/WDM/OTN/dataManagement",
        name: "dataManagement",
        component: () =>
            import("../views/WDM-OTN/dataManagement/index.vue"),
        meta: {
            title: "数据治理",
        },
        children: dataManagement_routes,
        redirect: "/main/WDM/OTN/dataManagement/regenSectionData",
    },
    //系统设置
    {
        path: "/main/WDM/OTN/systemSettings",
        name: "systemSettings",
        component: () =>
            import("../views/WDM-OTN/systemSettings/index.vue"),
        meta: {
            title: "系统设置",
        },
        children: system_routes,
        redirect: "/main/WDM/OTN/systemSettings/dataImport",
    },
];

///主页面子路由
const index_routes = [
    //WDM/OTN
    {
        path: "/main/WDM/OTN",
        name: "WDM/OTN",
        component: () => import("../views/WDM-OTN/index.vue"),
        meta: {
            title: "WDM/OTN",
        },
        children: WDM_OTN_routes,
        redirect: "/main/WDM/OTN/networkOverview",
    },
    //IPRAN
    {
        path: "/main/IPRAN",
        name: "IPRAN",
        component: () => import("../views/IPRAN/index.vue"),
        meta: {
            title: "IPRAN",
        },
    },
    //PeOTN
    {
        path: "/main/PeOTN",
        name: "PeOTN",
        component: () => import("../views/PeOTN/index.vue"),
        meta: {
            title: "PeOTN",
        },
    },
];

const routes = [
    //登录
    {
        path: "/",
        redirect: "/index",
    },
    //登录
    {
        path: "/login",
        name: "login",
        component: () => import("../views/login.vue"),
        meta: {
            title: "登录",
            requiresAuth: false,
        },
    },
    //注册
    {
        path: "/register",
        name: "register",
        component: () => import("../views/register.vue"),
        meta: {
            title: "注册",
            requiresAuth: false,
        },
    },
    //主页
    {
        path: "/index",
        name: "index",
        component: () => import("../views/index.vue"),
        meta: {
            title: "主页",
            requiresAuth: true,
        },
        children: index_routes,
        redirect: "/main/WDM/OTN",
    },
    //关于
    {
        path: "/about",
        name: "about",
        component: () => import("../views/about.vue"),
        meta: {
            title: "关于",
            requiresAuth: false,
        },
    },
    //403
    {
        path: "/403",
        name: "403",
        component: () => import("../views/Error/403.vue"),
        meta: {
            title: "403",
            requiresAuth: false,
        },
    },
    //404
    {
        path: "/404",
        name: "404",
        component: () => import("../views/Error/404.vue"),
        meta: {
            title: "404",
            requiresAuth: false,
        },
    },
    //不存在路由跳转至登录
    {
        path: "/:pathMatch(.*)",
        redirect: "/404",
    },
];

export default routes;