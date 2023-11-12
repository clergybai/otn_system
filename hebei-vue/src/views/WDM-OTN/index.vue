<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-13 15:48:39
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-07 18:31:35
 * @FilePath: \hebei--vue\src\views\WDM-OTN\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <!-- WDM/OTM主页 -->
  <div class="WDM-OTM-main">
    <div class="header">
      <el-row class="header_canvas">
        <el-col class="menu">
          <el-menu
            :default-active="mainIsActive"
            class="el-menu-demo"
            mode="horizontal"
            active-text-color="transparent"
            @select="handleSelect"
          >
            <el-menu-item
              v-for="(item, index) in headerData"
              :key="index"
              :index="item.route"
            >
              <h2>{{ item.text }}</h2>
            </el-menu-item>
          </el-menu>
        </el-col>
      </el-row>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mainIsActive: "",
      headerData: [
        { text: "隐患概览", route: "/main/WDM/OTN/networkOverview" },
        { text: "传输系统", route: "/main/WDM/OTN/transmissionSystem" },
        { text: "隐患列表", route: "/main/WDM/OTN/hiddenDangerList" },
        { text: "数据治理", route: "/main/WDM/OTN/dataManagement" },
        { text: "系统管理", route: "/main/WDM/OTN/systemSettings" },
      ],
    };
  },
  watch: {
    "$route.path"() {
      this.routeListen();
    },
  },
  created() {
    this.routeListen();
  },
  mounted() {},
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push({
        path: key,
        params: { data: "query" },
      });
    },
    routeListen() {
      this.headerData.forEach((item) => {
        if (Array.isArray(item.route)) {
          item.route.forEach((children) => {
            if (this.$route.path.includes(children.route)) {
              this.mainIsActive = children.route;
              return;
            }
          });
        } else {
          if (this.$route.path.includes(item.route)) {
            this.mainIsActive = item.route;
            return;
          }
        }
      });
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
.WDM-OTM-main {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
.header {
  width: 100%;
  user-select: none;
}
.header > .header_canvas .el-menu-demo {
  background: #f2f5fa;
}

.header > .header_canvas .el-menu-demo {
  padding: 10px 20px 2px 20px;
  display: flex;
  align-items: center;
}

.header > .header_canvas .menu {
  width: 100%;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.el-menu--horizontal {
  border-bottom: none;
}

.el-menu--horizontal > .el-menu-item {
  background-color: #ffffff;
  height: 54px;
  padding: 8px 18px;
  box-sizing: border-box;
  outline: none;
}

.el-menu--horizontal > .el-menu-item h2 {
  box-sizing: border-box;
  padding: 0px 25px;
  width: 100%;
  height: 100%;
  color: #333;
  font-size: 16px;
  border-radius: 8px;
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

.content {
  width: 100%;
  height: calc(100% - 54px - 20px);
}
</style>