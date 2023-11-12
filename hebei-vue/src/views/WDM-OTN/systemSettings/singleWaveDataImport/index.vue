<template>
  <div class="body">
    <div class="content">
      <div class="operatingHead">
        <ul class="operatingTab">
          <template v-for="item of tabData" :key="item.route">
            <li
              @click="handleSelect(item.route)"
              :class="{ IsActive: item.route == $route.path }"
            >
              {{ item.text }}
            </li>
          </template>
        </ul>
      </div>
      <div class="DataContent">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tabData: [
        {
          text: "中兴扫波板性能数据",
          route:
            "/main/WDM/OTN/systemSettings/singleWaveDataImport/zetSweeperBoard",
        },
        {
          text: "烽火扫波板性能数据",
          route:
            "/main/WDM/OTN/systemSettings/singleWaveDataImport/fhSweeperBoard",
        },
      ],
    };
  },
  created() {},
  mounted() {},
  methods: {
    handleSelect(index) {
      this.$router.push({
        path: index,
        params: { data: "query" },
      });
    },
  },
};
</script>

<style scoped>
.body {
  width: 100%;
  height: 100%;
  padding: 10px 20px 20px 10px;
  box-sizing: border-box;
}
.content {
  position: relative;
  padding: 10px 20px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: var(--box-shadow);
}

div.operatingHead {
  position: absolute;
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
  z-index: 0;
}

.DataContent {
  width: 100%;
  height: 100%;
  z-index: 0;
}

.el-table .el-table-column {
  text-align: center;
}

.operatingHead .operatingTab {
  position: absolute;
  padding: 0 20px;
  width: 100%;
  height: 100%;
  font-family: SimHei;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: flex-start;
  box-sizing: border-box;
}

.operatingHead .operatingTab li {
  padding: 4px 15px;
  height: 60%;
  list-style: none;
  box-sizing: border-box;
  font-weight: bold;
  font-size: 16px;
  background-color: transparent;
  margin-left: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
}

.operatingHead .operatingTab li.IsActive {
  background-color: #4c64f2;
  color: #fff;
}

.operatingHead .operatingTab li:nth-of-type(1) {
  margin-left: 0;
}

.el-table .el-table__empty-block {
  background-color: #f2f5fa;
}

.operationGroup {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.el-button.ToolBtn,
.el-button.ToolBtn:hover,
.el-button.ToolBtn:active,
.el-button.ToolBtn:focus {
  color: #4c64f2;
  border: none;
  background-color: transparent;
  margin: 0;
}
</style>