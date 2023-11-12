<template>
  <div
    class="content"
    :style="{
      background: `url(${getAssetsImages(roundImg)})`,
      'background-size': 'cover',
    }"
  >
    <!-- <img
      class="backgroundImg"
      :src="getAssetsImages(roundImg)"
      draggable="false"
      oncontextmenu="return false;"
    /> -->
    <div class="loginBox">
      <!-- <span class="title">Login</span> -->
      <span class="title">
        <img src="@/assets/logo.png" alt="" />
        传送网隐患自动诊断系统
      </span>
      <el-form label-width="120px" :model="userData" ref="userData" :rules="rules">
        <el-form-item label="用户名" prop="user_name">
          <el-input
            placeholder="用户名"
            v-model="userData.user_name"
            @keyup.enter="ConfirmLogin"
            clearable
          />
        </el-form-item>
        <el-form-item label="密码" prop="pw_word">
          <el-input
            type="password"
            placeholder="密码"
            v-model="userData.pw_word"
            @keyup.enter="ConfirmLogin"
            show-password
          />
        </el-form-item>
        <div class="confirmBtn">
          <el-button class="loginBtn" :loading="loadingBtn" @click="ConfirmLogin"
            >登录</el-button
          >
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { encrypt } from "@/JsEncrypt/index";
import { ElMessage } from "element-plus";
import { useMainStore } from "@/store/index";
import { getCookie, setCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  getSSid,
  getToken,
  UserInfoLoad,
  getPublicKey,
  getLogin,
  setLog,
  logModuleMenu,
  operationMenu,
} from "@/api/WDM-OTN/http";

export default {
  name: "login",
  data() {
    return {
      loadingBtn: false,
      roundImg: 0,
      userData: {
        user_name: "",
        mac_addr: null,
        pw_word: "",
        token: "",
      },
      status: ref(""),
      getKey: {
        addr: null,
        public_key: null,
      },
      rules: {
        user_name: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        pw_word: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
  created() {
    let _this = this;
    _this.getLocationData();
    _this.roundImg = _this.rand(1, 23) + ".jpg"; // 动态加载图片
  },
  mounted() {},
  methods: {
    getLocationData() {
      let _this = this;
      const params = window.location.search;
      if (params.startsWith("?")) {
        const index = params.indexOf("?");
        const length = params.length;
        const subParams = params.substring(index + 1, length);
        const paramArr = subParams.split("&");
        paramArr.forEach((item) => {
          const itemArr = item.split("=");
          const name = itemArr[0];
          const value = itemArr[1];
          switch (name) {
            case "globalUniqueID":
              // const seessionID = value;
              // _this.UserInfoLoad(value);
              _this.getSsid(value);
              return;
          }
        });
      }
    },
    getSsid(val) {
      let _this = this;
      const data = {
        user_name: val,
      };
      getSSid(data).then((res) => {
        if (res.code == 200) {
          _this.LoginSuccess(res.data);
        }
      });
    },
    UserInfoLoad(val) {
      let _this = this;
      const mainData = useMainStore();
      let data = {
        method: "findUserBySessionID",
        sessionID: val,
      };
      UserInfoLoad(data).then((res) => {
        if (res.code == 200) {
          const resDatas = res.data;
          mainData.userId = resDatas.userId;
          mainData.orgID = resDatas.orgID;
          mainData.userName = resDatas.userName;
          mainData.trueName = resDatas.trueName;
          mainData.mobilePhone = resDatas.mobilePhone;
          mainData.telephone = resDatas.telephone;
          mainData.fax = resDatas.fax;
          mainData.address = resDatas.address;
          mainData.email = resDatas.email;
          mainData.orgCode = resDatas.orgCode;
          mainData.personType = resDatas.personType;
          mainData.job = resDatas.job;
          mainData.professional = resDatas.professional;
          mainData.jobNum = resDatas.jobNum;
          mainData.category = resDatas.category;
          mainData.remark = resDatas.remark;
          _this.getToken(resDatas.userName);
        }
      });
    },
    getToken(val) {
      let _this = this;
      const mainData = useMainStore();
      const data = {
        userName: val,
      };
      getToken(data).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          mainData.userInformation.token = data;
          setCookie("ustoken", mainData.userInformation.token, "4h");
          _this.$router.push({ path: "/index" });
        }
      });
    },
    rand(m, n) {
      return Math.ceil(Math.random() * (n - m + 1) + m - 1);
    },
    getAssetsImages(name) {
      return require(`/src/assets/backgroundImg/${name}`);
    },
    ConfirmLogin() {
      let _this = this;
      _this.$refs.userData.validate((value) => {
        if (value) {
          _this.getPublicKey();
        }
      });
    },
    getPublicKey() {
      let _this = this;
      _this.loadingBtn = true;
      const mainData = useMainStore();
      const addr = _this.guid();
      _this.getKey.addr = addr;
      getPublicKey(_this.getKey).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          mainData.publicKey = data.public_key;
          setCookie("pK", data.public_key, "4h");
          _this.getLogin(addr);
        }
      });
    },
    LoginSuccess(data) {
      let _this = this;
      const mainData = useMainStore();

      mainData.userInformation.token = data.token;
      mainData.userInformation.userName = data.user_name;
      mainData.is_authen = data.is_authen;

      setCookie("ustoken", data.token, "4h");
      setCookie("usn", data.user_name, "4h");
      setCookie("is_authen", JSON.stringify(data.is_authen), "4h");

      const user = getCookie("usn");
      setLog({
        op_module: logModuleMenu.Login,
        op_user: user,
        op_behavior: user + operationMenu.login,
        op_time: NowDate(),
      });

      ElMessage({
        type: "success",
        message: "登录成功",
        offset: 100,
        duration: 1300,
      });

      _this.$router.push({ path: "/index" });
      _this.loadingBtn = false;
    },
    getLogin(addr) {
      let _this = this;
      //const mainData = useMainStore();
      const requestData = JSON.parse(JSON.stringify(_this.userData));
      requestData.mac_addr = addr;
      requestData.pw_word = encrypt(_this.userData.pw_word);
      getLogin(requestData).then((res) => {
        const data = res.data;
        if (res.code == 200) {
          _this.LoginSuccess(data);
          // mainData.userInformation.token = data.token;
          // mainData.userInformation.userName = data.user_name;
          // mainData.is_authen = data.is_authen;

          // setCookie("ustoken", data.token, "4h");
          // setCookie("usn", data.user_name, "4h");
          // setCookie("is_authen", JSON.stringify(data.is_authen), "4h");

          // const user = getCookie("usn");
          // setLog({
          //   op_module: logModuleMenu.Login,
          //   op_user: user,
          //   op_behavior: user + operationMenu.login,
          //   op_time: NowDate(),
          // });

          // ElMessage({
          //   type: "success",
          //   message: "登录成功",
          //   offset: 100,
          //   duration: 1300,
          // });

          // _this.$router.push({ path: "/index" });
          // _this.loadingBtn = false;
        } else {
          ElMessage({
            type: "error",
            message: "用户名或密码错误, 请重新输入!!!",
            offset: 100,
          });
          _this.$refs.userData.resetFields();
          _this.loadingBtn = false;
        }
      });
    },
    guid() {
      function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
      }
      return (
        S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4()
      );
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/plugins/styles/WDM-OTN/login.scss";
</style>
