<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-18 16:48:28
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-19 17:12:06
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\dataImport\adjustableDimLiveNetConfiguration\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <!-- 可调光衰现网配置 -->

  <div class="main">
    <div class="content">
      <div class="operatingHead">
        <div class="operatingTool">
          <el-form :inline="true" class="demo-form-inline userSearch">
            <el-form-item label="系统名称">
              <el-input
                placeholder="输入系统名称查询"
                style="min-width: 250px"
                clearable
                v-model="searchData.sys_name"
              />
            </el-form-item>
            <el-form-item>
              <el-button class="btnSearch" @click="onSubmit">查询</el-button>
            </el-form-item>
          </el-form>
          <el-button
            class="button"
            @click="recountParameter"
            :disabled="reComputed.disabled"
            v-if="restartComputed"
            >{{ reComputed.text }}</el-button
          >
        </div>
      </div>
      <div class="body">
        <el-table
          v-loading.lock="tabLoading"
          :data="tableData.slice()"
          stripe
          :row-style="{ height: '0' }"
          :header-cell-style="{
            'text-align': 'center',
            background: '#F3F5FA',
            padding: '10px 0',
          }"
          height="100%"
          :cell-style="{ 'text-align': 'center', padding: '10px' }"
          @filter-change="handleFilterChange"
        >
          <el-table-column
            prop="sys_name"
            label="系统名称"
            column-key="sys_name"
            :filters="getFilters(all_sys_name_array)"
          >
          </el-table-column>
          <el-table-column
            prop="city"
            label="地市"
            width="100"
            column-key="city"
            :filters="getFilters(all_city_array)"
          />
          <el-table-column
            prop="net_level"
            label="网络级别"
            width="150"
            column-key="net_level"
            :filters="getFilters(all_net_level_array)"
          />
          <el-table-column prop="a_sub_name" label="A端子网元名称" />
          <el-table-column prop="a_ne_id" label="A端子网元ID" />
          <el-table-column prop="z_sub_name" label="Z端子网元名称" />
          <el-table-column prop="z_ne_id" label="Z端子网元ID" />
          <!-- <el-table-column prop="business_waves" label="复用段波道数" />         -->
          <el-table-column label="复用段波道数">
            <template #default="scope">
              <el-input-number
                class="business_waveInput"
                v-model="scope.row.business_waves"
                :controls="false"
                :min="0"
                :max="maxBusinessWaves"
                @change="handleChange"
              />
            </template>
          </el-table-column>
          <el-table-column align="center" label="操作" v-if="isAuthen" fixed="right">
            <template #default="scope">
              <div class="operationGroup">
                <!-- <el-button
                  class="submitBtn"
                  type="text"
                  @click.prevent="open(scope.row)"
                  :disabled="isBtnSaveDisable"
                  >{{ labelSave }}</el-button
                > -->
                <el-button class="submitBtn" type="text" @click.prevent="open(scope.row)"
                  >保存</el-button
                >
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pageSize"
        layout="sizes, prev, pager, next, jumper"
        class="paging"
        :page-count="pageCount"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { ElMessageBox } from "element-plus";
import { getIs_Authen, getUserName } from "@/config/UserInfomation";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  getMslFilter,
  getComputedState,
  startComputed,
  updateMsl,
  getMsl,
  setLog,
  logModuleMenu,
  operationMenu,
  getHideMenu,
} from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      reComputed: {
        text: "重新计算",
        disabled: false,
      },
      restartComputed: false,
      tabLoading: false,
      IsActiveTabIndex: 1, //TAB下标
      IsActiveToolIndex: 1, //Tool下标
      currentPage: 1, // 每页多少条
      tableData: [],
      // pageTotal: 0,
      // dataTotal: 0,
      pageCount: ref(""),
      pageTotal: ref(""),
      dataTotal: ref(""),
      pageSize: 15, //每页显示个数
      maxBusinessWaves: 100,
      all_sys_name_array: [],
      all_city_array: [],
      all_net_level_array: [],
      filters_sys_name_tag: {},
      filters_city_tag: {},
      filters_net_level_tag: {},
      isAuthen: false,
      searchData: {
        sys_name: null,
      },
    };
  },
  methods: {
    refreshTable(data) {
      this.tableData = data.myArray;
      this.pageTotal = data.page_size;
      this.pageCount = data.page_count;
      this.dataTotal = data.total;
      // this.labelSave = data.is_calculating ? "计算中" : "保存";
      this.isBtnSaveDisable = data.is_calculating;
      this.tabLoading = false;
    },
    setFiltersArray(data) {
      new Promise(() => {
        data.forEach((item) => {
          if (
            !this.all_sys_name_array.includes(item.sys_name) &&
            item.sys_name != "" &&
            item.sys_name != null &&
            item.sys_name != undefined
          ) {
            this.all_sys_name_array.push(item.sys_name);
          }
          if (
            !this.all_city_array.includes(item.city) &&
            item.city != "" &&
            item.city != null &&
            item.city != undefined
          ) {
            console.log(item.city);
            this.all_city_array.push(item.city);
          }
          if (
            !this.all_net_level_array.includes(item.net_level) &&
            item.net_level != "" &&
            item.net_level != null &&
            item.net_level != undefined
          ) {
            this.all_net_level_array.push(item.net_level);
          }
        });
      });
    },
    getFilters(array) {
      let result = [];
      array.forEach((item) => {
        result.push({ text: item, value: item });
      });
      return result.slice();
    },
    init() {
      let _this = this;
      this.tabLoading = true;
      let data = {
        username: getUserName(),
      };
      getHideMenu(data).then((res) => {
        if (res.code == 200) {
          let selectArr = [];
          const data = res.data;
          data.forEach((item) => {
            selectArr.push(item.name);
          });
          let data0 = {
            page_index_begin: 0,
            page_size: this.pageSize,
            param: {
              selected: selectArr,
            },
          };
          getMsl(data0).then((res) => {
            if (res.code == 200) {
              _this.refreshTable(res.data);
            } else {
              _this.tableData = [];
              _this.tabLoading = false;
            }
          });
        }
      });
    },
    onSubmit() {
      let _this = this;
      this.tabLoading = true;
      this.filters_sys_name_tag = {
        name: "sys_name",
        values: [_this.searchData.sys_name],
      };
      let data = {
        username: getUserName(),
      };
      getHideMenu(data).then((res) => {
        if (res.code == 200) {
          let selectArr = [];
          const data = res.data;
          data.forEach((item) => {
            selectArr.push(item.name);
          });
          let data0 = {
            page_index_begin: 0,
            page_size: this.pageSize,
            filter: [_this.filters_sys_name_tag],
            param: {
              selected: selectArr,
            },
          };
          getMsl(data0).then((res) => {
            if (res.code == 200) {
              _this.refreshTable(res.data);
            } else {
              _this.tableData = [];
              _this.tabLoading = false;
            }
          });
        }
      });
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.changePage();
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.changePage();
    },
    prevPage() {
      if (this.currentPage == 1) {
        return false;
      } else {
        this.currentPage--;
        this.changePage();
      }
    },
    nextPage() {
      if (this.currentPage == this.totalPage) {
        return false;
      } else {
        this.currentPage++;
        this.changePage();
      }
    },
    changePage() {
      let _this = this;
      _this.tabLoading = true;
      let data = {
        username: getUserName(),
      };
      getHideMenu(data).then((res) => {
        if (res.code == 200) {
          let selectArr = [];
          const data = res.data;
          data.forEach((item) => {
            selectArr.push(item.name);
          });
          let obj = {
            page_index_begin: this.currentPage,
            page_size: this.pageSize,
            filter: [
              _this.filters_sys_name_tag,
              _this.filters_city_tag,
              _this.filters_net_level_tag,
            ],
            param: {
              selected: selectArr,
            },
          };
          getMsl(obj).then((res) => {
            if (res.code == 200) {
              this.refreshTable(res.data);
            } else {
              _this.tableData = [];
              _this.tabLoading = false;
            }
          });
        }
      });
    },
    editRow(data) {
      let _this = this;
      updateMsl(data).then((res) => {
        if (res.code == 200) {
          const user = getCookie("usn");
          setLog({
            op_module: logModuleMenu.COCNOMS,
            op_user: user,
            op_behavior: user + operationMenu.update,
            op_time: NowDate(),
          });
        }
      });
    },
    open(data) {
      this.$confirm("参数值已经修改，是否保存修改？", "确认信息", {
        distinguishCancelAndClose: true,
        confirmButtonText: "保存",
        cancelButtonText: "取消",
      })
        .then(() => {
          this.editRow(data);
          this.$message({
            type: "success",
            message: "保存修改",
          });
        })
        .catch((action) => {
          this.$message({
            type: "warning",
            message: action === "cancel" ? "放弃保存" : "停留在当前页面",
          });
        });
    },
    handleFilterChange(filterObj) {
      if (filterObj.sys_name != null) {
        this.filters_sys_name_tag = {
          name: "sys_name",
          values: filterObj.sys_name,
        };
      }
      if (filterObj.city != null) {
        this.filters_city_tag = {
          name: "city",
          values: filterObj.city,
        };
      }
      if (filterObj.net_level != null) {
        this.filters_net_level_tag = {
          name: "net_level",
          values: filterObj.net_level,
        };
      }
      this.changePage();
    },
    recountParameter() {
      let _this = this;
      let data1 = {
        tableName: "复用段波道数配置",
      };
      ElMessageBox.confirm("确定开始计算吗?", "重新计算", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        showClose: false,
        // draggable: true,
        lockScroll: true,
        closeOnClickModal: false,
      }).then(() => {
        _this.reComputed.text = "计算中...";
        _this.reComputed.disabled = true;
        startComputed().then((res) => {
          _this.getComputedState();
        });
      });
    },
    getComputedState() {
      let _this = this;
      getComputedState().then((res) => {
        if (res.code == 200) {
          const data = res.data;
          if (data == 1) {
            _this.reComputed.text = "计算中...";
            _this.reComputed.disabled = true;
          } else {
            _this.reComputed.text = "重新计算";
            _this.reComputed.disabled = false;
          }
        }
      });
    },
    getFilter() {
      let _this = this;
      getMslFilter().then((res) => {
        if (res.code == 200) {
          const result = res;
          _this.setFiltersArray(result.data);
        }
      });
    },
    getAuthen() {
      this.isAuthen = getIs_Authen().can_set_channel_num;
    },
    getRestartComputed() {
      const is_authen = getIs_Authen();
      this.restartComputed =
        (is_authen.can_add_standrad_param &&
          is_authen.can_threshold_setting &&
          is_authen.can_set_channel_num) == true
          ? true
          : false;
    },
  },
  mounted() {
    this.getAuthen();
    this.getRestartComputed();
    this.init();
    this.getComputedState();
  },
  created() {
    this.getFilter();
  },
};
</script>
<style scoped lang="scss">
@import "@/plugins/styles/WDM-OTN/systemSettings/multiChannelConf/index.scss";
</style>
