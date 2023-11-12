<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-16 10:44:44
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-27 16:06:43
 * @FilePath: \hebei--vue\src\views\main.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="main">
    <div class="header">
      <!-- 头部 -->
      <el-row type="flex" align="middle" class="header_canvas">
        <el-col :span="3">
          <div class="logo"></div>
        </el-col>
        <el-col :span="8" class="Title">
          <h2>{{ msg }}</h2>
        </el-col>
        <el-col :span="3" class="menu">
          <el-button type="danger" plain round @click="goToWdm">{{
            label_wdm
          }}</el-button>
        </el-col>
        <el-col :span="3" class="menu">
          <el-button type="danger" plain round disabled>{{ label_ipran }}</el-button>
        </el-col>
        <el-col :span="3" class="menu">
          <el-button type="danger" plain round disabled>{{ label_peotn }}</el-button>
        </el-col>
        <el-col :span="4" class="menu">
          <el-dropdown trigger="click" @command="handleCommand">
            <span class="el-dropdown-link UsersSetting">
              <span class="UserName">
                <span> 【{{ userName }}】 </span>
              </span>
              <el-avatar shape="square" :size="100" :src="imgUrl" />
            </span>
            <template #dropdown>
              <el-dropdown-menu v-for="(item, index) of dropDownArr" :key="index">
                <el-dropdown-item :command="item.value">{{ item.text }}</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-col>
      </el-row>
    </div>
    <!-- <div class="content" :style="{ 'max-width': pageMaxWidth + 'px' }"> -->
    <div class="content">
      <!-- 内容 -->
      <router-view></router-view>
    </div>
  </div>
  <el-dialog
    v-model="dialogVisibleResetPasswords"
    title="修改密码"
    width="650px"
    :close-on-click-modal="false"
  >
    <el-form
      label-width="100px"
      label-position="right"
      :rules="indexUpdatePwdrules"
      :model="indexUpdatePwdData"
      ref="indexUpdatePwdData"
    >
      <el-form-item label="当前用户" prop="userName">
        <el-input disabled placeholder="获取异常" v-model="indexUpdatePwdData.userName" />
      </el-form-item>
      <el-form-item label="新密码" prop="salt">
        <el-input
          placeholder="新密码和当前密码不能相同"
          type="password"
          v-model="indexUpdatePwdData.salt"
        />
      </el-form-item>
      <el-form-item label="确认密码" prop="resalt">
        <el-input
          placeholder="确认密码和新密码保持一致"
          type="password"
          v-model="indexUpdatePwdData.resalt"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="cancel" @click="dialogVisibleResetPasswords = false"
          >取消</el-button
        >
        <el-button class="confirm" type="primary" @click="confirmMessage('修改密码')"
          >保存</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { ElMessage, ElMessageBox } from "element-plus";
import { getUserName } from "@/config/UserInfomation.js";
import { delCookie } from "@/config/Cookies";
import { updatePwd, setLog, logModuleMenu, operationMenu } from "@/api/WDM-OTN/http";
import { NowDate } from "@/config/formatTime";

export default {
  name: "net_select",
  data() {
    //邮箱校验
    var checkEmail = (rule, value, cb) => {
      const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
      if (value === "") {
        cb(new Error("请输入邮箱！"));
      } else if (regEmail.test(value)) {
        return cb();
      }
      cb(new Error("请输入合法的邮箱！"));
    };
    //密码校验
    var checkPassword = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        callback();
      }
    };
    //确认密码校验
    var checkRePassword = (rule, value, callback) => {
      if (this.indexUpdatePwdData.salt === "") {
        callback(new Error("请输入新密码"));
      } else if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.indexUpdatePwdData.salt) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      gap_time: 0,
      beforeUnload_time: 0,
      pageMaxWidth: 0,
      dialogVisibleResetPasswords: false,
      msg: "传送网隐患自动诊断系统",
      label_wdm: "WDM/OTN",
      label_ipran: "IPRAN",
      label_peotn: "PeOTN",
      index: "/home",
      names: "left",
      transitionName: "",
      userName: "",
      imgUrl: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      dropDownArr: [
        { text: "修改密码", value: "updatePwd" },
        // { text: "系统设置", value: "/main/WDM/OTN/systemSettings" },
        { text: "退出登录", value: "exit" },
      ],
      indexUpdatePwdData: {
        userName: "",
        salt: "",
        resalt: "",
      },
      indexUpdatePwdrules: {
        salt: [
          { required: false, message: "请输入密码", trigger: "blur" },
          { validator: checkPassword, trigger: "blur" },
        ],
        resalt: [
          { required: false, message: "请再次输入密码", trigger: "blur" },
          { validator: checkRePassword, trigger: "blur" },
        ],
      },
    };
  },
  watch: {
    dialogVisibleResetPasswords(val) {
      let _this = this;
      if (val) {
        _this.indexUpdatePwdData.userName = _this.userName;
      } else {
        _this.$refs.indexUpdatePwdData.resetFields(); // 清空表单
        _this.$refs.indexUpdatePwdData.clearValidate(); // 清空表单验证
      }
    },
  },
  created() {
    let _this = this;
    _this.getUserInfomation();
  },
  mounted() {
    window.addEventListener("beforeunload", () => this.beforeunloadHandler());
    window.addEventListener("unload", () => this.unloadHandler());
  },
  unmounted() {
    window.removeEventListener("beforeunload", () => this.beforeunloadHandler());
    window.removeEventListener("unload", () => this.unloadHandler());
  },
  methods: {
    getUserInfomation() {
      this.userName = getUserName();
    },
    goToWdm() {
      this.$router.push({ path: "/index" });
    },
    handleCommand(val) {
      let _this = this;
      switch (val) {
        case "exit":
          _this.exit();
          break;
        case "updatePwd":
          _this.dialogVisibleResetPasswords = true;
          break;
        default:
          _this.$router.push({ path: val });
          break;
      }
    },
    confirmMessage(title) {
      let _this = this;
      if (_this.dialogVisibleResetPasswords) {
        _this.$refs.indexUpdatePwdData.validate((value) => {
          if (value) {
            ElMessageBox.confirm("确定要保存更改吗?", title, {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
              showClose: false,
              lockScroll: true,
              closeOnClickModal: false,
            })
              .then((res) => {
                _this.updatePwd();
              })
              .catch((res) => {});
          }
        });
      }
    },
    updatePwd() {
      let _this = this;
      updatePwd(_this.indexUpdatePwdData).then((res) => {
        if (res.code == 200 && res.data) {
          ElMessage({
            type: "success",
            message: "修改成功",
            offset: 200,
          });
        } else {
          ElMessage({
            type: "error",
            message: "修改失败",
            offset: 200,
          });
        }
        _this.dialogVisibleResetPasswords = false;
      });
    },
    exit() {
      ElMessageBox.confirm("确定要退出系统吗?", "退出系统", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        showClose: false,
        lockScroll: true,
        closeOnClickModal: false,
      }).then(() => {
        this.removeUserInfomation();
      });
    },
    removeUserInfomation() {
      let _this = this;
      //清空用户信息
      const user = getUserName();
      setLog({
        id: "",
        op_module: logModuleMenu.Login,
        op_user: user,
        op_behavior: user + operationMenu.logout,
        op_time: NowDate(),
      });
      delCookie("ustoken");
      delCookie("usn");
      delCookie("is_authen");
      ElMessage({
        type: "success",
        message: "退出成功",
        offset: 200,
      });
      _this.$router.push({ path: "/login" });
    },
    beforeunloadHandler() {
      this.beforeUnload_time = new Date().getTime();
    },
    unloadHandler() {
      this.gap_time = new Date().getTime() - this.beforeUnload_time;
      if (this.gap_time <= 10) {
        const user = getUserName();
        setLog({
          id: "",
          op_module: logModuleMenu.Login,
          op_user: user,
          op_behavior: user + operationMenu.logout,
          op_time: NowDate(),
        });
        delCookie("ustoken");
        delCookie("usn");
        delCookie("is_authen");
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/plugins/styles/WDM-OTN/index.scss";
</style>
