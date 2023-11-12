<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-06-22 11:21:06
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-08 16:40:58
 * @FilePath: \hebei--vue\src\views\WDM-OTN\networkOverview\view.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="content">
    <div class="header">
      <div class="searchTemplate">
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
          <!-- 区域 -->
          <el-form-item label="区域">
            <el-select
              placeholder="地市"
              v-model="searchSelect.city"
              @change="handleCity"
            >
              <template
                v-for="(item, index) of cityAreas.cityAreasData"
                :key="index"
              >
                <template v-if="item.name == '二干/省内骨干网'">
                  <el-option :label="item.name" :value="'all'" />
                </template>
                <template v-else>
                  <el-option :label="item.name" :value="item.name" />
                </template>
              </template>
            </el-select>
          </el-form-item>
          <!-- 网络级别 -->
          <el-form-item label="网络级别">
            <el-select
              placeholder="网络级别"
              v-model="searchSelect.network_level"
            >
              <el-option label="所有" value="all" />
              <template
                v-for="item of networkLevelAreas.networkLevelData"
                :key="item.code"
              >
                <el-option :label="item.name" :value="item.value" />
              </template>
            </el-select>
          </el-form-item>
          <!-- <el-form-item>
            <el-input placeholder="输入关键字" />
          </el-form-item> -->
          <el-form-item>
            <el-button class="btnSearch" @click="onSubmit">查询</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="body" v-loading.lock="chartLoading">
      <div class="hiddenCardOne" v-loading.lock="hiddenCardOneLoading">
        <div class="untreatedHiddenDanger">
          <span>未处理隐患数量统计</span>
          <div id="untreatedHiddenDanger" ref="untreatedHiddenDanger"></div>
        </div>
        <div class="hiddenContent">
          <span>隐患内容统计</span>
          <div id="hiddenContent" ref="hiddenContent"></div>
        </div>
        <div class="networkLevelNumberHidden">
          <span>网络级别隐患数量统计</span>
          <div
            id="networkLevelNumberHidden"
            ref="networkLevelNumberHidden"
          ></div>
        </div>
      </div>
      <div class="hiddenCardTwo">
        <div class="untreatedNumberHiddenCity">
          <span>未处理隐患数量按地市排名</span>
          <div
            id="untreatedNumberHiddenCity"
            ref="untreatedNumberHiddenCity"
          ></div>
        </div>
        <div class="annualRisk">
          <span>年度隐患统计</span>
          <div id="annualRisk" ref="annualRisk"></div>
        </div>
      </div>
      <div class="hiddenCardThree">
        <div class="cityHiddenStatisticalList" :hidden="isCityGroupHidden">
          <span>地市隐患统计列表</span>
          <div class="cityHiddenTableData" :hidden="isCityGroupHidden">
            <el-table
              :data="tableCity"
              :row-style="{ height: '0' }"
              :header-cell-style="{
                'text-align': 'center',
                background: '#F3F5FA',
                padding: '10px 0',
              }"
              :cell-style="{ 'text-align': 'center', padding: '15px 0' }"
              :summary-method="getSummaries"
              show-summary
            >
              <el-table-column
                prop="city"
                label="地市"
                :filters="filtersCity"
                :filter-method="filterHandler"
              />
              />
              <el-table-column label="紧急">
                <el-table-column label="总数" prop="emergency_count">
                  <template #default="scope">
                    <!-- processed='C01':城市列表紧急总数, C02: 城市列表紧急已处理，C03: 城市列表紧急未处理-->
                    <!-- processed='C04':城市列表一般总数, C05: 城市列表一般已处理，C06: 城市列表一般未处理-->
                    <!-- processed='D01':区县列表紧急总数, D02: 区县列表紧急已处理，D03: 区县列表紧急未处理-->
                    <!-- processed='D04':区县列表一般总数, D05: 区县列表一般已处理，D06: 区县列表一般未处理-->
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.city,
                          (emergency = 'true'),
                          (processed = 'C01')
                        )
                      "
                      v-model="scope.row.emergency_count"
                      >{{ scope.row.emergency_count }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column label="已处理" prop="emergency_processedCount">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.city,
                          (emergency = 'true'),
                          (processed = 'C02')
                        )
                      "
                      v-model="scope.row.emergency_processedCount"
                      >{{ scope.row.emergency_processedCount }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column prop="emergency_untreatedCount" label="未处理">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.city,
                          (emergency = 'true'),
                          (processed = 'C03')
                        )
                      "
                      v-model="scope.row.emergency_untreatedCount"
                      >{{ scope.row.emergency_untreatedCount }}</el-link
                    >
                  </template>
                </el-table-column>
              </el-table-column>

              <el-table-column label="一般">
                <el-table-column prop="general_count" label="总数">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.city,
                          (emergency = 'false'),
                          (processed = 'C04')
                        )
                      "
                      v-model="scope.row.general_count"
                      >{{ scope.row.general_count }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column label="已处理" prop="general_processedCount">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.city,
                          (emergency = 'false'),
                          (processed = 'C05')
                        )
                      "
                      v-model="scope.row.general_processedCount"
                      >{{ scope.row.general_processedCount }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column label="未处理" prop="general_untreatedCount">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.city,
                          (emergency = 'false'),
                          (processed = 'C06')
                        )
                      "
                      v-model="scope.row.general_untreatedCount"
                      >{{ scope.row.general_untreatedCount }}</el-link
                    >
                  </template>
                </el-table-column>
              </el-table-column>
            </el-table>
            <!-- <el-pagination
              :hide-on-single-page="tableCity.length <= pageSize"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[100, 200, 300, 400]"
              :page-size="pageSize"
              layout="sizes, prev, pager, next, jumper"
              class="paging"
            >
            </el-pagination> -->
          </div>
        </div>
      </div>
      <div class="hiddenCardFour" v-show="isDistrictGroupHidden">
        <div
          class="cityHiddenStatisticalList"
          v-loading.lock="hiddenCardOneLoading"
        >
          <span>区县隐患统计列表</span>
          <div class="cityHiddenTableData">
            <el-table
              :data="tableDistrict"
              :row-style="{ height: '0' }"
              :header-cell-style="{
                'text-align': 'center',
                background: '#F3F5FA',
                padding: '10px 0',
              }"
              :cell-style="{ 'text-align': 'center', padding: '15px 0' }"
            >
              <el-table-column
                prop="district"
                label="区县"
                :filters="filtersDistrict"
                :filter-method="filterHandler"
              />
              <el-table-column label="紧急">
                <el-table-column label="总数">
                  <template #default="scope">
                    <!-- processed='C01':城市列表紧急总数, C02: 城市列表紧急已处理，C03: 城市列表紧急未处理
                  processed='C04':城市列表一般总数, C05: 城市列表一般已处理，C06: 城市列表一般未处理
                  processed='D01':区县列表紧急总数, D02: 区县列表紧急已处理，D03: 区县列表紧急未处理
                  processed='D04':区县列表一般总数, D05: 区县列表一般已处理，D06: 区县列表一般未处理 -->
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.district,
                          (emergency = 'true'),
                          (processed = 'D01')
                        )
                      "
                      v-model="scope.row.emergency_count"
                      >{{ scope.row.emergency_count }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column label="已处理">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.district,
                          (emergency = 'true'),
                          (processed = 'D02')
                        )
                      "
                      v-model="scope.row.emergency_processedCount"
                      >{{ scope.row.emergency_processedCount }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column prop="emergency_untreatedCount" label="未处理">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.district,
                          (emergency = 'true'),
                          (processed = 'D03')
                        )
                      "
                      v-model="scope.row.emergency_untreatedCount"
                      >{{ scope.row.emergency_untreatedCount }}</el-link
                    >
                  </template>
                </el-table-column>
              </el-table-column>
              <el-table-column label="一般">
                <el-table-column prop="general_count" label="总数">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.district,
                          (emergency = 'false'),
                          (processed = 'D04')
                        )
                      "
                      v-model="scope.row.general_count"
                      >{{ scope.row.general_count }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column label="已处理">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.district,
                          (emergency = 'false'),
                          (processed = 'D05')
                        )
                      "
                      v-model="scope.row.general_processedCount"
                      >{{ scope.row.general_processedCount }}</el-link
                    >
                  </template>
                </el-table-column>
                <el-table-column label="未处理">
                  <template #default="scope">
                    <el-link
                      type="primary"
                      href="javascript:;"
                      @click.prevent="
                        goHiddenTroubleList(
                          scope.row.district,
                          (emergency = 'false'),
                          (processed = 'D06')
                        )
                      "
                      v-model="scope.row.general_untreatedCount"
                      >{{ scope.row.general_untreatedCount }}</el-link
                    >
                  </template>
                </el-table-column>
              </el-table-column>
            </el-table>
            <!-- <el-pagination
              :hide-on-single-page="tableDistrict.length <= pageSize"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[100, 200, 300, 400]"
              :page-size="pageSize"
              layout="sizes, prev, pager, next, jumper"
              class="paging"
            >
            </el-pagination> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import * as _ from "lodash";
import {
  FormatSearchStartTime,
  FormatSearchEndTime,
} from "@/config/formatTime";
import { getUserName } from "@/config/UserInfomation";
import { ref } from "vue";
import {
  getUnhandled,
  getStatistics,
  getLevel,
  getCityHiddenGroup,
  getAnnualRiskGroup,
  getMenu,
  getHazardLevelCityGroup,
  getHazardLevelDistrictGroup,
  getHiddenCity,
  getHiddenNetworkLevel,
} from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      chartLoading: true,
      hiddenCardOneLoading: true,
      untreatedHiddenDanger: {
        chartData: null,
      },
      currentPage: 1, // 每页多少条
      pageSize: 10, //每页显示个数
      tableCity: [],
      tableDistrict: [],
      cityAreas: ref({
        cityAreasData: [],
      }),
      networkLevelAreas: {
        networkLevelData: [],
      },
      searchSelect: {
        startTime: "",
        endTime: "",
        city: "",
        network_level: "all",
      },
      filtersCity: [],
      serachData: {
        op_timeArr: "",
      },
      filtersDistrict: [],
      isCityGroupHidden: false,
      isDistrictGroupHidden: false,
      menuArrTransitData: [],
      getCity: "",
      colors: [
        "#7536F2",
        "#851262",
        "#FD8764",
        "#0370CB",
        "#FFE48D",
        "#9D4474",
        "#A4C0D7",
        "#B0ACC6",
        "#F2C3B3",
        "#A0BBC7",
        "#FDCCA2",
        "#D7B3B0",
      ],
    };
  },
  created() {
    // this.getHiddenCity();
    this.computedCityArray();
  },
  beforeRouteLeave(to, form, next) {
    window.onresize = null;
    next();
  },
  mounted() {
    let _this = this;
    _this.chartLoading = true;
    _this.showChartUnhandled();
    _this.showChartTrouble();
    _this.showChartLevel();
    _this.showChartCity();
    _this.showChartYears();
    _this.HazardLevelCityGroup();
    _this.getHiddenNetworkLevel();
    //_this.HazardLevelDistrictGroup();
    let untreatedHiddenDanger = echarts.init(
      document.getElementById("untreatedHiddenDanger")
    );
    let hiddenContent = echarts.init(document.getElementById("hiddenContent"));
    let networkLevelNumberHidden = echarts.init(
      document.getElementById("networkLevelNumberHidden")
    );
    let untreatedNumberHiddenCity = echarts.init(
      document.getElementById("untreatedNumberHiddenCity")
    );
    let annualRisk = echarts.init(document.getElementById("annualRisk"));
    window.onresize = _.debounce(() => {
      untreatedHiddenDanger.resize();
      hiddenContent.resize();
      networkLevelNumberHidden.resize();
      untreatedNumberHiddenCity.resize();
      annualRisk.resize();
    }, 300);
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
    showChartUnhandled() {
      let _this = this;
      _this.hiddenCardOneLoading = true;
      let data = null;
      getUnhandled(_this.searchSelect).then((res) => {
        if (res.code == 200) {
          data = res.data;
          // 基于准备好的dom，初始化echarts实例
          const dom = document.getElementById("untreatedHiddenDanger");
          let myChart = echarts.init(dom);
          dom.removeAttribute("_echarts_instance_");
          // 指定图表的配置项和数据
          var option = {
            series: [
              {
                type: "gauge",
                center: ["50%", "65%"],
                startAngle: 200,
                endAngle: -20,
                min: 0,
                max: data.max,
                splitNumber: 10,
                itemStyle: {
                  color: "#677CF7",
                },
                progress: {
                  show: true,
                  width: 26,
                },
                pointer: {
                  show: false,
                },
                axisLine: {
                  lineStyle: {
                    width: 32,
                  },
                },
                axisTick: {
                  //show: false,
                  distance: -45,
                  splitNumber: 1,
                  lineStyle: {
                    width: 2,
                    color: "#999",
                  },
                },
                splitLine: {
                  show: false,
                  distance: -70,
                  length: 5,
                  lineStyle: {
                    width: 3,
                    color: "#999",
                  },
                },
                axisLabel: {
                  //show: false,
                  distance: 30,
                  color: "#999",
                  fontSize: 12,
                },
                anchor: {
                  show: false,
                },
                title: {
                  show: false,
                },
                detail: {
                  valueAnimation: true,
                  //width: '60%',
                  lineHeight: 40,
                  borderRadius: 8,
                  offsetCenter: [0, "10%"],
                  fontSize: 60,
                  fontWeight: "bolder",
                  //formatter: '{value}',
                  color: "inherit",
                },
                data: [
                  {
                    value: data.val,
                  },
                ],
              },
            ],
          };
          // 使用刚指定的配置项和数据显示图表。
          myChart.setOption(option);
        }
      });
    },
    showChartTrouble() {
      let _this = this;
      let dataTrouble = null;
      getStatistics(_this.searchSelect).then((res) => {
        if (res.code == 200) {
          dataTrouble = res.data;
          const dom = document.getElementById("hiddenContent");
          let myChart = echarts.init(dom);
          dom.removeAttribute("_echarts_instance_");
          let option = {
            // color: _this.colors,
            tooltip: {
              trigger: "item",
            },
            legend: {
              orient: "vertical",
              y: "center",
              x: "right",
            },
            series: [
              {
                name: "隐患内容统计",
                type: "pie",
                radius: ["70%", "45%"],
                center: ["50%", "50%"],
                minAngle: 8, // 最小的扇区角度（0 ~ 360），用于防止某个值过小导致扇区太小影响交互
                avoidLabelOverlap: true, // 是否启用防止标签重叠策略
                itemStyle: {
                  borderRadius: 8,
                  borderColor: "#fff",
                  borderWidth: 3,
                },
                label: {
                  show: false,
                  position: "right",
                  y: "top",
                },
                emphasis: {
                  label: {
                    show: false,
                    fontSize: "12",
                    fontWeight: "bold",
                  },
                },
                labelLine: {
                  show: false,
                },
                detail: {
                  formatter: "{value}",
                },
                data: dataTrouble,
              },
            ],
          };
          myChart.setOption(option);
        }
      });
    },
    showChartLevel() {
      let _this = this;
      let data = null;
      getLevel(_this.searchSelect).then((res) => {
        if (res.code == 200) {
          data = res.data;
          const dom = document.getElementById("networkLevelNumberHidden");
          let myChart = echarts.init(dom);
          dom.removeAttribute("_echarts_instance_");
          let option = {
            // color: _this.colors,
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)",
            },
            legend: {
              x: "right",
              y: "center",
              orient: "vertical",
            },
            series: [
              {
                name: "网络级别隐患数量统计",
                type: "pie",
                radius: ["30%", "70%"],
                center: ["50%", "50%"],
                minAngle: 8, // 最小的扇区角度（0 ~ 360），用于防止某个值过小导致扇区太小影响交互
                avoidLabelOverlap: true, // 是否启用防止标签重叠策略
                itemStyle: {
                  borderRadius: 8,
                  borderColor: "#fff",
                  borderWidth: 3,
                },
                data: data,
              },
            ],
          };
          myChart.setOption(option);
          _this.hiddenCardOneLoading = false;
        }
      });
    },
    handleCity(val) {
      this.getCity = val;
      if (val == "all") {
        this.isDistrictGroupHidden = false;
        this.isCityGroupHidden = false;
      } else {
        this.isDistrictGroupHidden = true;
      }
    },
    showChartCity() {
      let _this = this;
      getCityHiddenGroup().then((res) => {
        if (res.code == 200) {
          const data = res.data;
          const count = [],
            city = [],
            untreatedCount = [],
            processedCount = [];
          for (let item of data) {
            count.push(item.count);
            city.push(item.city);
            untreatedCount.push(item.untreatedCount);
            processedCount.push(item.processedCount);
          }
          const dom = document.getElementById("untreatedNumberHiddenCity");
          let myChart = echarts.init(dom);
          dom.removeAttribute("_echarts_instance_");
          const colors = ["#F28863", "#677CF7", "#F2C533"];
          let option = {
            color: colors,
            tooltip: {
              trigger: "axis",
            },
            legend: {
              data: ["未处理", "已处理", "总数"],
            },
            toolbox: {
              show: false,
              feature: {
                dataView: { show: true, readOnly: false },
                magicType: { show: true, type: ["line", "bar"] },
                restore: { show: true },
                saveAsImage: { show: true },
              },
            },
            calculable: true,
            xAxis: [
              {
                type: "category",
                data: city,
                axisLabel: {
                  interval: 0, //全部显示x轴
                },
              },
            ],
            yAxis: [
              {
                type: "value",
              },
            ],
            series: [
              {
                name: "未处理",
                type: "bar",
                data: untreatedCount,
              },
              {
                name: "已处理",
                type: "bar",
                data: processedCount,
              },
              {
                name: "总数",
                type: "bar",
                data: count,
              },
            ],
          };
          myChart.setOption(option);
        }
      });
    },
    showChartYears() {
      let _this = this;
      getAnnualRiskGroup().then((res) => {
        if (res.code == 200) {
          const data = res.data;
          const count = new Array(12),
            timestamp = new Array(12),
            untreatedCount = new Array(12),
            processedCount = new Array(12);
          for (let item of data) {
            switch (item.timestamp) {
              case "01":
                count[0] = item.count;
                timestamp[0] = item.timestamp;
                untreatedCount[0] = item.untreatedCount;
                processedCount[0] = item.processedCount;
                break;
              case "02":
                count[1] = item.count;
                timestamp[1] = item.timestamp;
                untreatedCount[1] = item.untreatedCount;
                processedCount[1] = item.processedCount;
                break;
              case "03":
                count[2] = item.count;
                timestamp[2] = item.timestamp;
                untreatedCount[2] = item.untreatedCount;
                processedCount[2] = item.processedCount;
                break;
              case "04":
                count[3] = item.count;
                timestamp[3] = item.timestamp;
                untreatedCount[3] = item.untreatedCount;
                processedCount[3] = item.processedCount;
                break;
              case "05":
                count[4] = item.count;
                timestamp[4] = item.timestamp;
                untreatedCount[4] = item.untreatedCount;
                processedCount[4] = item.processedCount;
                break;
              case "06":
                count[5] = item.count;
                timestamp[5] = item.timestamp;
                untreatedCount[5] = item.untreatedCount;
                processedCount[5] = item.processedCount;
                break;
              case "07":
                count[6] = item.count;
                timestamp[6] = item.timestamp;
                untreatedCount[6] = item.untreatedCount;
                processedCount[6] = item.processedCount;
                break;
              case "08":
                count[7] = item.count;
                timestamp[7] = item.timestamp;
                untreatedCount[7] = item.untreatedCount;
                processedCount[7] = item.processedCount;
                break;
              case "09":
                count[8] = item.count;
                timestamp[8] = item.timestamp;
                untreatedCount[8] = item.untreatedCount;
                processedCount[8] = item.processedCount;
                break;
              case "10":
                count[9] = item.count;
                timestamp[9] = item.timestamp;
                untreatedCount[9] = item.untreatedCount;
                processedCount[9] = item.processedCount;
                break;
              case "11":
                count[10] = item.count;
                timestamp[10] = item.timestamp;
                untreatedCount[10] = item.untreatedCount;
                processedCount[10] = item.processedCount;
                break;
              case "12":
                count[11] = item.count;
                timestamp[11] = item.timestamp;
                untreatedCount[11] = item.untreatedCount;
                processedCount[11] = item.processedCount;
                break;
            }
          }
          const dom = document.getElementById("annualRisk");
          let myChart = echarts.init(dom);
          dom.removeAttribute("_echarts_instance_");
          const colors = ["#F28863", "#677CF7", "#F2C533"];
          let option = {
            color: colors,
            tooltip: {
              trigger: "axis",
              axisPointer: {
                type: "cross",
              },
            },
            grid: {
              right: "6%",
            },
            legend: {
              data: ["未处理", "已处理", "总数"],
            },
            xAxis: [
              {
                type: "category",
                axisTick: {
                  alignWithLabel: true,
                },
                data: [
                  "1月",
                  "2月",
                  "3月",
                  "4月",
                  "5月",
                  "6月",
                  "7月",
                  "8月",
                  "9月",
                  "10月",
                  "11月",
                  "12月",
                ],
              },
            ],
            yAxis: [
              {
                type: "value",
                name: "",
                position: "left",
                alignTicks: true,
                axisLine: {
                  show: true,
                  lineStyle: {
                    color: "#A6A6A8",
                  },
                },
                axisLabel: {
                  formatter: "{value}",
                },
              },
            ],
            series: [
              {
                name: "未处理",
                type: "bar",
                data: untreatedCount,
              },
              {
                name: "已处理",
                type: "bar",
                data: processedCount,
              },
              {
                name: "总数",
                type: "line",
                yAxisIndex: 0,
                data: count,
              },
            ],
          };
          myChart.setOption(option);
        }
      });
    },
    handleSizeChange(val) {
      // 每页多少条
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      // 当前页
      this.currentPage = val;
    },
    HazardLevelCityGroup() {
      let _this = this;
      let data = {
        username: getUserName(),
      };
      getMenu(data).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          let selectArr = [];
          data.forEach((item) => {
            selectArr.push(item.name);
          });
          let searchdata = {
            timesArr: _this.searchSelect,
            selected: selectArr,
          };
          getHazardLevelCityGroup(searchdata).then((res) => {
            if (res.code == 200) {
              const data = res.data.myArray;
              _this.tableCity = data;
              _this.filterCity(data);
            }
          });
        }
      });
    },
    HazardLevelDistrictGroup() {
      let data = {
        // city: "石家庄市"
        city: this.getCity,
      };
      let _this = this;
      getHazardLevelDistrictGroup(_this.searchSelect).then((res) => {
        if (res.code == 200) {
          const data = res.data.myArray;
          _this.tableDistrict = data;
          _this.filterDistrict(data);
        }
      });
    },
    getHiddenCity() {
      let _this = this;
      getHiddenCity().then((res) => {
        if (res.code == 200) {
          _this.cityAreas.cityAreasData = res.data;
        }
      });
    },
    async computedCityArray() {
      let _this = this;
      let data = {
        username: getUserName(),
      };
      getMenu(data).then((res) => {
        if (res.code == 200) {
          const data = res.data;
          data.forEach((item) => {
            _this.cityAreas.cityAreasData.push({
              name: item.name,
              code: item.name,
            });
          });
        }
      });
    },
    getHiddenNetworkLevel() {
      let _this = this;
      getHiddenNetworkLevel().then((res) => {
        if (res.code == 200) {
          _this.networkLevelAreas.networkLevelData = res.data;
          _this.chartLoading = false;
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
      _this.showChartUnhandled();
      _this.showChartTrouble();
      _this.showChartLevel();
      _this.HazardLevelCityGroup();
      _this.HazardLevelDistrictGroup();
    },
    filter(data) {
      this.arrary = [];
      const res = new Map();
      this.arrary = data.filter((a) => !res.has(a.text) && res.set(a.text, 1));
      return this.arrary;
    },
    filterCity(data) {
      let _this = this;
      for (let item of data) {
        let city = {
          text: item.city,
          value: item.city,
        };
        _this.filtersCity.push(city);
      }
      _this.filtersCity = _this.filter(_this.filtersCity);
    },
    filterDistrict(data) {
      let _this = this;
      _this.filtersDistrict = [];
      for (let item of data) {
        let district = {
          text: item.district,
          value: item.district,
        };
        _this.filtersDistrict.push(district);
      }
      _this.filtersDistrict = _this.filter(_this.filtersDistrict);
    },
    filterHandler(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
    goHiddenTroubleList(city, emergency, processed) {
      this.$router.push({
        name: "hiddenDangerList",
        params: {
          // rule_name: name,
          city: city,
          emergency: emergency,
          processed: processed,
        },
      });
    },
    getSummaries(param) {
      const { columns, data } = param;
      const sums = [];
      columns.forEach((column, index) => {
        if (index === 0) {
          sums[index] = "合计";
          return;
        }
        const values = data.map((item) => Number(item[column.property]));
        if (!values.every((value) => Number.isNaN(value))) {
          sums[index] = `${values.reduce((prev, curr) => {
            const value = Number(curr);
            if (!Number.isNaN(value)) {
              return prev + curr;
            } else {
              return prev;
            }
          }, 0)}`;
        } else {
          sums[index] = "N/A";
        }
      });

      return sums;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/plugins/styles/WDM-OTN/networkOverview/index.scss";
</style>