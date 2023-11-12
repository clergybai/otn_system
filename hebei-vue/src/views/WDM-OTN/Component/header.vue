<template>
  <div class="Header">
    <div class="HeaderOne">
      <el-row :gutter="20" type="flex" align="middle" class="header_canvas">
        <el-col :span="3"><div class="logo"></div></el-col>
        <el-col :span="8" class="Title"
          ><h2>{{ msg }}</h2></el-col
        >
        <el-col :span="3" class="menu"
          ><el-button type="danger" plain round @click="goToWdm">{{
            label_wdm
          }}</el-button></el-col
        >
        <el-col :span="3" class="menu"
          ><el-button type="danger" plain round disabled>{{
            label_ipran
          }}</el-button></el-col
        >
        <el-col :span="3" class="menu"
          ><el-button type="danger" plain round disabled>{{
            label_peotn
          }}</el-button></el-col
        >
      </el-row>
    </div>
    <div class="HeaderTwo">
      <el-row :gutter="20" class="header_canvas">
        <el-col class="menu"
          ><el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            active-text-color="transparent"
            @select="handleSelect"
          >
            <el-menu-item index="/main/network" class="el-menu-demo-item"
              ><h2>网络概览</h2></el-menu-item
            >
            <el-menu-item index="/main/topo" class="el-menu-demo-item"
              ><h2>传输系统</h2></el-menu-item
            >
            <el-menu-item index="/main/trouble" class="el-menu-demo-item"
              ><h2>隐患列表</h2></el-menu-item
            >
            <el-menu-item index="/main/sys" class="el-menu-demo-item"
              ><h2>系统管理</h2></el-menu-item
            >
          </el-menu></el-col
        >
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "net_select",
  data() {
    return {
      msg: "河北联通传输网隐患自动诊断AI工具",
      label_wdm: "WDM/OTN",
      label_ipran: "IPRAN",
      label_peotn: "PeOTN",
      current: "mail",
      activeIndex: "1",
      defaultActive: "1",
    };
  },
  activeIndex() {
    return activeIndex;
  },
  methods: {
    goToWdm() {
      this.$router.push({ path: "/main" });
    },
    handleSelect(key, keyPath) {
      this.$router.push({
        path: key,
        params: { data: "query" },
      });
    },
  },
};
</script>

<style scoped>
html,
body {
  width: 100%;
  height: 100%;
}
html,
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.Header {
  width: 100%;
  display: flex;
  box-sizing: border-box;
  flex-direction: column;
  overflow: hidden;
}

.HeaderOne {
  height: 60px;
}

.HeaderOne > .header_canvas {
  height: 100%;
  background: linear-gradient(
    to left,
    rgba(194, 84, 84, 0.5),
    rgb(255, 48, 48, 1)
  );
}

.HeaderOne > .header_canvas .el-col {
  height: 100%;
}

.logo {
  width: 150px;
  height: 100%;
  background: url("../../assets/unicom_logo_mini.png") no-repeat center;
  background-size: 60% 100%;
  object-fit: cover;
}

.HeaderOne > .header_canvas .Title {
  font-family: "STXihei";
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.HeaderOne > .header_canvas .menu {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.HeaderTwo {
  width: 100%;
  margin-top: 10px;
}

.HeaderTwo > .header_canvas .el-menu-demo {
  background: #f2f5fa;
}

.HeaderTwo > .header_canvas .el-menu-demo {
  padding: 0px;
  padding-left: 12px;
  display: flex;
  align-items: center;
}

.HeaderTwo > .header_canvas .menu {
  padding: 0;
}

.el-menu--horizontal {
  border-bottom: none;
}

.el-menu--horizontal > .el-menu-item {
  background-color: #ffffff;
  height: 56px;
  padding: 8px 18px;
  box-sizing: border-box;
}

.el-menu--horizontal > .el-menu-item h2 {
  box-sizing: border-box;
  padding: 0px 25px;
  width: 100%;
  height: 100%;
  color: #333;
  font-size: 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-menu--horizontal > .el-menu-item:hover {
  background-color: #ffffff;
}
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
}
.el-menu--horizontal > .el-menu-item:last-of-type {
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
}

.el-menu--horizontal .el-menu-item:not(.is-disabled):focus,
.el-menu--horizontal .el-menu-item:not(.is-disabled):hover {
  background-color: #ffffff;
}

.el-menu--horizontal > .el-menu-item.is-active {
  border: none;
}

.el-menu--horizontal > .el-menu-item.is-active h2 {
  height: 100%;
  background-color: var(--theme-color);
  color: #ffffff;
}
</style>