<template>
  <div class="content">
    <div class="tableData" v-loading="loading">
      <div class="tableDataSearch">
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item label="发现时间">
            <el-col>
              <el-date-picker
                v-model="serachData.op_timeArr"
                format="YYYY/M/D"
                value-format="YYYY/M/D"
                type="datetimerange"
                range-separator="To"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
              />
            </el-col>
          </el-form-item>

          <el-form-item label="工单号">
            <el-input
                  label="工单号"
                  placeholder="工单号"
                  v-model="order_id"
                />
          </el-form-item>

          <el-form-item>
            <el-button class="btnSearch" @click="onSubmit">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button
              class="btnSearch"
              @click="exportor"
              v-if="IsHiddenExportBtn"
              >导出</el-button
            >
          </el-form-item>
        </el-form>
      </div>
      <!-- <div class="tableDataOperation"></div> -->
      <div class="tableDataPresentation">
        <el-table
          :data="tableTrouble.slice()"
          @filter-change="handleFilterChange"
          stripe
          :header-cell-style="{
            'text-align': 'center',
            background: '#F3F5FA',
            padding: '10px 0',
          }"
          :cell-style="{ 'text-align': 'center', padding: '20px 0' }"
          height="100%"
        >
          <el-table-column
            prop="order_id"
            label="工单号"
            min-width="250px"
          />
          <el-table-column
            prop="discover_time"
            label="发现时间"
            min-width="200px"
          />
          <el-table-column
            prop="city"
            label="地市"
            min-width="150px"
            :filters="filtersCity"
            filterable
            column-key="city"
          >
          </el-table-column>
          <el-table-column
            prop="district_county"
            label="区县"
            min-width="150px"
            :filters="filtersCounty"
            column-key="district_county"
          />
          <el-table-column
            prop="sys_name"
            label="所属系统"
            min-width="200px"
            :filters="filtersSystem"
            column-key="sys_name"
          />
          <el-table-column prop="oms" label="复用段" min-width="450px" />
          <el-table-column
            prop="network_level"
            label="网络层级"
            min-width="150px"
            :filters="filtersNetworkLevel"
            column-key="network_level"
          />
          <!-- <el-table-column
            prop="risk_level"
            label="隐患级别"
            min-width="150px"
            :filters="filtersRisk_level"
            column-key="risk_level"
          /> -->
          <el-table-column
            label="隐患级别"
            min-width="150px"
            :filters="filtersRisk_level"
            column-key="risk_level"
          >
            <template #default="scope">
              <template v-if="scope.row.risk_level == '紧急'">
                <span class="cardLabel danger">{{
                  scope.row.risk_level
                }}</span></template
              >
              <template v-if="scope.row.risk_level == '一般'">
                <span class="cardLabel warning">{{
                  scope.row.risk_level
                }}</span></template
              >
              <!-- <template v-else>
                <span class="cardLabel general">{{
                  scope.row.risk_level
                }}</span>
              </template> -->
            </template>
          </el-table-column>
          <el-table-column
            prop="risk_content"
            label="隐患内容"
            min-width="400px"
          />
          <el-table-column prop="manufactor" label="厂家" min-width="100px" />
          <el-table-column
            prop="is_send_top"
            label="派单情况"
            width="150px"
            :filters="filtersIs_send_top"
            column-key="is_send_top"
          >
            <template #default="scope">
              <template v-if="scope.row.is_send_top == 0">
                <span>未派单</span>
              </template>
              <template v-if="scope.row.is_send_top == 1">
                <span>已派单</span>
              </template>
            </template>
          </el-table-column>
          <el-table-column
            prop="top_feedback_message"
            label="TOP处理反馈"
            width="150px"
            :filters="filtersTop_feedback_message"
            column-key="top_feedback_message"
          />
          <el-table-column
            prop="top_order_end_time"
            label="结单时间"
            min-width="150px"
            :filters="filtersTop_order_end_time"
            column-key="top_order_end_time"
          />
        </el-table>
      </div>
      <el-pagination
        :hide-on-single-page="tableTrouble.length <= pageSize"
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
import { useMainStore } from "../../../store/index";
import CsvExportor from "csv-exportor";
import { getIs_Authen, getUserName } from "@/config/UserInfomation";
import { ElMessage } from "element-plus";
import {
  FormatSearchStartTime,
  FormatSearchEndTime,
} from "@/config/formatTime";
import {
  getHideMenu,
  getTrouble,
  exportOrderListData,
  getTroubleFilter,
  getTroubleFilterLarterPart,
  getCityFilter,
} from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      loading: true,
      IsHiddenExportBtn: false,
      tableTrouble: ref([]),
      currentPage: 1, // 当前页码
      pageTotal: ref(""),
      dataTotal: ref(""),
      pageCount: 0,
      pageSize: 20, //每页显示个数
      cityAreas: null,
      filtersCity: [], // 地市筛选
      filtersCounty: [], // 区县筛选
      filtersSystem: [], // 所属系统筛选
      filtersNetworkLevel: [], // 网络层级筛选
      filtersRisk_level: [], // 隐患级别筛选
      filtersIs_send_top: [], // 派单情况筛选
      filtersTop_feedback_message: [], // top处理反馈筛选
      filtersTop_order_end_time: [], // 结单时间筛选
      all_sub_name_array: [],
      all_shelf_id_array: [],
      filters: {
        city_tag: {},
        district_county_tag: {},
        sys_name_tag: {},
        network_level_tag: {},
        risk_level_tag: {},
        is_send_top_tag: {},
        is_top_end_tag: {},
        top_feedback_message_tag: {},
        top_order_end_time_tag: {},
      },
      searchSelect: {
        startTime: "",
        endTime: "",
      },
      order_id: "",
      serachData: ref({
        op_timeArr: [],
      }),
    };
  },
  watch: {
    "serachData.op_timeArr"(val) {
      let _this = this;
      if (val == null || val == undefined) {
        _this.searchSelect.startTime = "";
        _this.searchSelect.endTime = "";
      }
    },
  },
  methods: {
    loadHiddenExportBtn() {
      let _this = this;
      const data = getIs_Authen();
      _this.IsHiddenExportBtn = data.can_output_hiddentrouble;
    },
    refreshTable(param) {
      let _this = this;
      if (!param) {
        _this.tableTrouble = [];
        _this.loading = false;
        return;
      }
      _this.tableTrouble = param.myArray;
      _this.pageTotal = param.page_size;
      _this.pageCount = param.page_count;
      _this.dataTotal = param.total;
      _this.loading = false;
    },
    init() {
      let _this = this;
      _this.loading = true;
      let data = {
        username: getUserName(),
      };
      getHideMenu(data).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          let selectArr = [];
          data.forEach((item) => {
            selectArr.push(item.name);
          });
          let data0 = {
            page_index_begin: 0,
            page_size: _this.pageSize,
            filter: [
              {
                Name: null,
                Values: null,
              },
            ],
            param: {
              order_id: _this.order_id,
              timesArr: {
                startTime: _this.searchSelect.startTime,
                endTime: _this.searchSelect.endTime,
              },
              selected: selectArr,
            },
          };
          getTrouble(data0).then((res) => {
            if (res.code == 200 && res.data) {
              _this.refreshTable(res.data);
            } else {
              _this.loading = false;
              _this.tableTrouble = [];
            }
          });
        }
      });
    },
    handleSizeChange(val) {
      this.pageSize = val;
      // this.changePage();
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
    exportor() {
      let _this = this;
      let tableData = [];
      new Promise((resolve, reject) => {
        exportOrderListData().then((res) => {
          if (res.code == 200) {
            const data = res.data;
            for (const item of data) {
              let list = {};
              list.order_id = item.order_id;
              list.discover_time = item.discover_time;
              list.city = item.city;
              list.district_county = item.district_county;
              list.sys_name = item.sys_name;
              list.oms = item.oms;
              list.network_level = item.network_level;
              list.manufactor = item.manufactor;
              list.risk_content = item.risk_content;
              list.risk_level = item.risk_level;
              tableData.push(list);
            }
            let header = [
              "发现时间",
              "地市",
              "区县",
              "所属系统",
              "复用段",
              "网络层级",
              "厂家",
              "隐患内容",
              "隐患级别",
              "派单情况",
              "TOP处理反馈",
              "结单时间",
            ];
            CsvExportor.downloadCsv(
              tableData,
              { header },
              "hiddenList" + _this.dateFormat() + ".csv"
            );
            ElMessage({
              type: "success",
              message: "导出成功",
              offset: 200,
            });
            resolve();
          }
        });
      });
    },
    dateFormat() {
      let year = new Date().getFullYear();
      let month = new Date().getMonth() + 1;
      let day = new Date().getDate();
      let hour = new Date().getHours();
      let minute = new Date().getMinutes();
      let second = new Date().getSeconds();
      let time =
        year +
        "_" +
        month +
        "_" +
        day +
        "_" +
        hour +
        "_" +
        minute +
        "_" +
        second;
      return time;
    },
    filter(data) {
      this.arrary = [];
      const res = new Map();
      this.arrary = data.filter((a) => !res.has(a.text) && res.set(a.text, 1));
      return this.arrary;
    },
    filterColumn(obj, column, pointTo) {
      let _this = this;
      _this[pointTo] = [];
      new Promise((resolve, reject) => {
        for (let item of obj) {
          if (!item[column]) continue;
          let data = {
            text: item[column],
            value: item[column],
          };
          _this[pointTo].push(data);
        }
        _this[pointTo] = _this.filter(_this[pointTo]);
      });
    },
    filterHandler(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
    handleFilterChange(filterObj) {
      let _this = this;
      if (
        filterObj.city != undefined &&
        filterObj.city != null &&
        filterObj.city.length > 0
      ) {
        _this.getCityFilter(filterObj.city);
      }
      if (filterObj.city != null) {
        _this.filters.city_tag = {
          name: "city",
          values: filterObj.city,
        };
      }
      if (filterObj.district_county != null) {
        _this.filters.district_county_tag = {
          name: "district_county",
          values: filterObj.district_county,
        };
      }
      if (filterObj.sys_name != null) {
        _this.filters.sys_name_tag = {
          name: "sys_name",
          values: filterObj.sys_name,
        };
      }
      if (filterObj.network_level != null) {
        _this.filters.network_level_tag = {
          name: "network_level",
          values: filterObj.network_level,
        };
      }
      if (filterObj.risk_level != null) {
        _this.filters.risk_level_tag = {
          name: "risk_level",
          values: filterObj.risk_level,
        };
      }
      if (filterObj.is_send_top != null) {
        const data = [];
        for (let item of filterObj.is_send_top) {
          if (item == "已处理") {
            data.push(1);
          } else {
            data.push(0);
          }
        }
        _this.filters.is_send_top_tag = {
          name: "is_send_top",
          values: data,
        };
      }
      if (filterObj.is_top_end != null) {
        _this.filters.is_top_end_tag = {
          name: "is_top_end",
          values: filterObj.is_top_end,
        };
      }
      if (filterObj.top_feedback_message != null) {
        _this.filters.top_feedback_message_tag = {
          name: "top_feedback_message",
          values: filterObj.top_feedback_message,
        };
      }
      if (filterObj.top_order_end_time != null) {
        _this.filters.top_order_end_time_tag = {
          name: "top_order_end_time",
          values: filterObj.top_order_end_time,
        };
      }
      _this.changePage();
    },
    changePage() {
      let _this = this;
      _this.loading = true;
      let data = {
        username: getUserName(),
      };
      getHideMenu(data).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          let selectArr = [];
          data.forEach((item) => {
            selectArr.push(item.name);
          });
          let obj = {
            page_index_begin: _this.currentPage,
            page_size: _this.pageSize,
            filter: [
              _this.filters.city_tag,
              _this.filters.district_county_tag,
              _this.filters.sys_name_tag,
              _this.filters.network_level_tag,
              _this.filters.risk_level_tag,
              _this.filters.is_send_top_tag,
              _this.filters.is_top_end_tag,
              _this.filters.top_feedback_message_tag,
              _this.filters.top_order_end_time_tag,
            ],
            param: {
              order_id: _this.order_id,
              timesArr: {
                startTime: _this.searchSelect.startTime,
                endTime: _this.searchSelect.endTime,
              },
              selected: selectArr,
            },
          };
          getTrouble(obj).then((res) => {
            if (res.code == 200) {
              _this.refreshTable(res.data);
            } else {
              _this.loading = false;
              _this.tableTrouble = [];
            }
          });
        } else {
          _this.loading = false;
        }
      });
    },
    onSubmit() {
      let _this = this;
      const timeselected = _this.serachData.op_timeArr;
      if (Array.isArray(timeselected) && timeselected.length > 0) {
        _this.searchSelect.startTime = FormatSearchStartTime(timeselected[0]);
        _this.searchSelect.endTime = FormatSearchEndTime(timeselected[1]);
      }
      _this.init();
    },
    switchOverviewParams(params) {
      // processed='C01':城市列表紧急总数, C02: 城市列表紧急已处理，C03: 城市列表紧急未处理
      // processed='C04':城市列表一般总数, C05: 城市列表一般已处理，C06: 城市列表一般未处理
      // processed='D01':区县列表紧急总数, D02: 区县列表紧急已处理，D03: 区县列表紧急未处理
      // processed='D04':区县列表一般总数, D05: 区县列表一般已处理，D06: 区县列表一般未处理
      let _this = this;
      let cityValues = [],
        riskLevelValues = [],
        processValues = [];
      cityValues.push(params.city);
      function check() {
        switch (params.processed) {
          case "C02":
          case "C05":
          case "D02":
          case "D05":
            processValues.push(1);
            _this.filters.is_top_end_tag = {
              name: "is_top_end",
              values: processValues,
            };
            break;
          case "C03":
          case "C06":
          case "D03":
          case "D06":
            processValues.push(0);
            _this.filters.is_top_end_tag = {
              name: "is_top_end",
              values: processValues,
            };
            break;
        }
      }
      check();
      switch (params.processed) {
        case "C01":
        case "C02":
        case "C03":
          // 城市列表紧急
          riskLevelValues.push("紧急");
          _this.filters.city_tag = {
            name: "city",
            values: cityValues,
          };
          _this.filters.risk_level_tag = {
            name: "risk_level",
            values: riskLevelValues,
          };
          _this.changePage();
          break;
        case "C04":
        case "C05":
        case "C06":
          // 城市列表一般
          riskLevelValues.push("一般");
          _this.filters.city_tag = {
            name: "city",
            values: cityValues,
          };
          _this.filters.risk_level_tag = {
            name: "risk_level",
            values: riskLevelValues,
          };
          _this.changePage();
          break;
        case "D01":
        case "D02":
        case "D03":
          // 区县列表紧急
          riskLevelValues.push("紧急");
          _this.filters.district_county_tag = {
            name: "district_county",
            values: cityValues,
          };
          _this.filters.risk_level_tag = {
            name: "risk_level",
            values: riskLevelValues,
          };
          _this.changePage();
          break;
        case "D04":
        case "D05":
        case "D06":
          // 区县列表一般
          riskLevelValues.push("一般");
          _this.filters.district_county_tag = {
            name: "district_county",
            values: cityValues,
          };
          _this.filters.risk_level_tag = {
            name: "risk_level",
            values: riskLevelValues,
          };
          _this.changePage();
          break;
      }
    },
    getFilter() {
      let _this = this;
      getTroubleFilter().then((res) => {
        if (res.code == 200) {
          _this.filterColumns1(res.data);
        }
      });
      getTroubleFilterLarterPart().then((res) => {
        if (res.code == 200) {
          _this.filterColumns2(res.data);
        }
      });
    },
    filterColumns1(data) {
      let _this = this;
      Promise.all([
        _this.filterColumn(data, "city", "filtersCity"),
        _this.filterColumn(data, "district_county", "filtersCounty"),
        _this.filterColumn(data, "sys_name", "filtersSystem"),
        _this.filterColumn(
          data,
          "top_feedback_message",
          "filtersTop_feedback_message"
        ),
        _this.filterColumn(
          data,
          "top_order_end_time",
          "filtersTop_order_end_time"
        ),
      ]);
    },
    filterColumns2(data) {
      let _this = this;
      Promise.all([
        _this.filterColumn(data, "network_level", "filtersNetworkLevel"),
        _this.filterColumn(data, "risk_level", "filtersRisk_level"),
        _this.filterColumn(data, "is_send_top", "filtersIs_send_top"),
      ]);
    },
    getCityFilter(citys) {
      let _this = this;
      getCityFilter(citys).then((res) => {
        if (res.code == 200) {
          _this.filterColumn(res.data, "district_county", "filtersCounty");
        }
      });
    },
  },
  created() {
    let _this = this;
    _this.loadHiddenExportBtn();
    _this.getFilter();
  },
  mounted() {
    let _this = this;
    const params = _this.$route.params;
    if (_this.$route.params.city) {
      _this.switchOverviewParams(params);
    } else {
      _this.init();
    }
  },
};
</script>

<style scoped lang="scss">
@import "@/plugins/styles/WDM-OTN/hiddenTroubleList/index.scss";
</style>