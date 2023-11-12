<template>
  <div class="main">
    <div class="body">
      <div class="ruleTableData">
        <div class="baseRules">
          <span>基准值规则</span>
          <div class="baseRulesTableData">
            <div class="title">
              <span class="maintenanceTypes">维护类型</span>
              <span class="baseline">计算公式</span>
              <span class="applicationArea">理想值</span>
            </div>
            <!-- 光功率维护基线 -->
            <div class="lightPowerMaintain">
              <span class="maintenanceTypes">光功率维护基线(dbm)</span>
              <span class="baseline">
                <span class="baselineOne"
                  >标准Pout=标准单波输出Po+10*log(N)<br />(N为波道数)</span
                >
                <span class="baselineTwo">标准Pin=标准Pout-当前增益</span>
              </span>
              <span class="applicationArea">
                <span class="applicationAreaOne">标准POUT</span>
                <span class="applicationAreaTwo">标准PIN</span>
              </span>
            </div>
            <!-- 光功率波动维护基线 -->
            <div class="lightPowerVolatility">
              <span class="maintenanceTypes">光功率波动维护基线(dB)</span>
              <span class="baseline">
                <span class="baselineOne">输入光功率Max-输入光功率Min</span>
                <span class="baselineTwo">输出光功率Max-输出光功率Min</span>
              </span>
              <span class="applicationArea">
                <!-- <span class="applicationAreaOne">{{ tableData.optical_power_baseline }}</span>
                <span class="applicationAreaTwo">{{ tableData.optical_power_baseline }}</span> -->
                <span class="applicationAreaOne">{{ 0 }}</span>
                <span class="applicationAreaTwo">{{ 0 }}</span>
              </span>
            </div>
            <!-- 增益差维护基线 -->
            <div class="gainDifferenceMaintain">
              <span class="maintenanceTypes">增益差维护基线(dB)</span>
              <span class="baseline">ABS(标准增益 - 实际增益)</span>
              <!-- <span class="applicationArea">{{tableData.gain_baseline}}</span> -->
              <span class="applicationArea">{{ 0 }}</span>
            </div>
            <!-- OLP主备光功率差维护基线(dB) -->
            <div class="poorLightPowerMaintain">
              <span class="maintenanceTypes">OLP主备光功率差维护基线(dB)</span>
              <span class="baseline">ABS(主路由收光功率 - 备路由收光功率)</span>
              <!-- <span class="applicationArea">{{tableData.olp_act_stand_baseline}}</span> -->
              <span class="applicationArea">{{ 0 }}</span>
            </div>
            <!-- 光缆收发损耗差维护基线(dB) -->
            <div class="opticalCableTransmissionLossDifferenceMaintain">
              <span class="maintenanceTypes">光缆收发损耗差维护基线(dB)</span>
              <span class="baseline"
                >ABS(光缆收向实际损耗 - 光缆发向实际损耗)</span
              >
              <!-- <span class="applicationArea">{{tableData.cable_in_out_baseline}}</span> -->
              <span class="applicationArea">{{ 0 }}</span>
            </div>
            <!-- 备注 -->
            <div class="remark">
              备注：光功率维护基线的基准值为公式，不同板卡，波道数的具体值通过工具系统内部进行
            </div>
          </div>
        </div>
        <div class="hazardLevel">
          <span>隐患等级门限值</span>
          <div class="hazardLevelTableData">
            <div class="title">
              <span class="hiddenContent">隐患内容</span>
              <span class="hiddenContentGroup">
                <span class="hiddenContentGroupTotal">隐患等级门限值设定</span>
                <span class="hiddenContentGroupPoints">
                  <span class="general">一般</span>
                  <span class="emergency">紧急</span>
                </span>
              </span>
              <span class="applicationLocal">
                <span class="applicationLocalTotal">应用区域</span>
                <span class="applicationLocalPoints">
                  <span class="networkLevel">网络等级</span>
                  <span class="city">地市</span>
                </span>
              </span>
            </div>
            <!-- 板卡实际和理论光功率偏差 -->
            <div class="boardCardPracticeTheoryLightPowerDeviation">
              <span class="titleGroup">
                <span class="title">板卡实际和理论光功率偏差</span>
                <span class="inputOutputOpticalPower">
                  <span class="inputOpticalPowerElevated">输入光功率升高</span>
                  <span class="inputOpticalPowerReduce">输入光功率降低</span>
                  <span class="outputOpticalPowerElevated">输出光功率升高</span>
                  <span class="outputOpticalPowerReduce">输出光功率降低</span>
                </span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalInputOpticalPowerElevated"
                    >{{ thresholdData.oa_input_power_std_dev_up_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalInputOpticalPowerReduce"
                    >{{ thresholdData.oa_input_power_std_dev_low_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalOutputOpticalPowerElevated"
                    >{{ thresholdData.oa_output_power_std_dev_up_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalOutputOpticalPowerReduce"
                    >{{ thresholdData.oa_output_power_std_dev_low_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencyInputOpticalPowerElevated"
                    >{{ thresholdData.oa_input_power_std_dev_up_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyInputOpticalPowerReduce"
                    >{{ thresholdData.oa_input_power_std_dev_low_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyOutputOpticalPowerElevated"
                    >{{ thresholdData.oa_output_power_std_dev_up_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyOutputOpticalPowerReduce"
                    >{{ thresholdData.oa_output_power_std_dev_low_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup">
                  <span class="networkInputOpticalPowerElevated">默认全网</span>
                  <span class="networkInputOpticalPowerReduce">默认全网</span>
                  <span class="networkOutputOpticalPowerElevated"
                    >默认全网</span
                  >
                  <span class="networkOutputOpticalPowerReduce">默认全网</span>
                </span>
                <span class="cityGroup">
                  <span class="cityInputOpticalPowerElevated">默认全省</span>
                  <span class="cityInputOpticalPowerReduce">默认全省</span>
                  <span class="cityOutputOpticalPowerElevated">默认全省</span>
                  <span class="cityOutputOpticalPowerReduce">默认全省</span>
                </span>
              </span>
            </div>
            <!-- 光功率波动偏差 -->
            <div class="lightPowerVolatilityDeviation">
              <span class="titleGroup">
                <span class="title">光功率波动偏差</span>
                <span class="inputOutputOpticalPower">
                  <span class="inputOpticalPowerExcessive">输入光功率超标</span>
                  <span class="inputOpticalPowerVolatilityExcessive"
                    >输出光功率波动超标</span
                  >
                </span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalInputOpticalPowerExcessive"
                    >{{ thresholdData.oa_input_power_fluc_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalInputOpticalPowerVolatilityExcessive"
                    >{{ thresholdData.oa_output_power_fluc_risk_thr }}
                    <p>&emsp;dB</p>
                  </span>
                </span>

                <span class="emergencyGroup">
                  <span class="emergencyInputOpticalPowerExcessive"
                    >{{ thresholdData.oa_input_power_fluc_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyInputOpticalPowerVolatilityExcessive"
                    >{{ thresholdData.oa_output_power_fluc_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup">
                  <span class="networkInputOpticalPowerExcessive"
                    >默认全网</span
                  >
                  <span class="networkInputOpticalPowerVolatilityExcessive"
                    >默认全网</span
                  >
                </span>

                <span class="cityGroup">
                  <span class="cityInputOpticalPowerExcessive">默认全省</span>
                  <span class="cityInputOpticalPowerVolatilityExcessive"
                    >默认全省</span
                  >
                </span>
              </span>
            </div>
            <!-- 板卡增益范围与实际增益偏差 -->
            <div class="boardCardGainSpan">
              <span class="titleGroup">
                <span class="title">板卡增益范围与实际增益偏差</span>
                <span class="elevatedReduceActualGain">
                  <span class="ReduceActualGain">实际增益降低</span>
                  <span class="elevatedActualGain">实际增益升高</span>
                </span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalInputOpticalPowerExcessive"
                    >{{ thresholdData.oa_gain_std_dev_low_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalInputOpticalPowerVolatilityExcessive"
                    >{{ thresholdData.oa_gain_std_dev_up_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencyInputOpticalPowerExcessive"
                    >{{ thresholdData.oa_gain_std_dev_low_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyInputOpticalPowerVolatilityExcessive"
                    >{{ thresholdData.oa_gain_std_dev_up_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup">
                  <span class="networkInputOpticalPowerExcessive"
                    >默认全网</span
                  >
                  <span class="networkInputOpticalPowerVolatilityExcessive"
                    >默认全网</span
                  >
                </span>
                <span class="cityGroup">
                  <span class="cityInputOpticalPowerExcessive">默认全省</span>
                  <span class="cityInputOpticalPowerVolatilityExcessive"
                    >默认全省</span
                  >
                </span>
              </span>
            </div>
            <!-- OLP主备光功率偏差 -->
            <div class="olpMainPrepareLightPowerDeviation">
              <span class="titleGroup">
                <span class="title">OLP主备光功率偏差</span>
                <span class="mainPrepareExcessive">OLP主备光功率差超标</span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalMainPrepareExcessive"
                    >{{ thresholdData.olp_power_dev_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencyMainPrepareExcessive"
                    >{{ thresholdData.olp_power_dev_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup">
                  <span class="networkMainPrepareExcessive">默认全网</span>
                </span>
                <span class="cityGroup">
                  <span class="cityMainPrepareExcessive">默认全省</span>
                </span>
              </span>
            </div>
            <!-- 光缆收发损耗偏差 -->
            <div class="opticalCableSendReceiveLossDeviation">
              <span class="titleGroup">
                <span class="title">光缆收发损耗偏差</span>
                <span class="sendReceiveLossDeviation">光缆收发损耗差超标</span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalSendReceiveLossDeviation"
                    >{{ thresholdData.fiber_two_way_dev_risk_thr }}
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencySendReceiveLossDeviation"
                    >{{ thresholdData.fiber_two_way_dev_risk_urg }}
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup">
                  <span class="networkSendReceiveLossDeviation">默认全网</span>
                </span>
                <span class="cityGroup">
                  <span class="citySendReceiveLossDeviation">默认全省</span>
                </span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { getDefaultBaseLine, getDefaultThreshold } from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      tableData: ref(""),
      thresholdData: ref(""),
    };
  },

  methods: {
    refreshTable1(data) {
      this.tableData = data;
    },
    refreshTable2(data) {
      this.thresholdData = data;
    },
    init() {
      getDefaultBaseLine().then((res) => {
        if (res.code == 200) {
          this.refreshTable1(res.data);
        }
      });
      getDefaultThreshold().then((res) => {
        if (res.code == 200) {
          this.refreshTable2(res.data);
        }
      });
    },
  },
  mounted() {
    this.init();
  },
  watch: {},
  created() {},
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
.main {
  padding: 10px 20px 20px 10px;
  width: 100%;
  height: 100%;
}

.main > .body {
  padding: 20px;
  width: 100%;
  height: 100%;
  border-radius: 10px;
  background-color: var(--white);
  box-shadow: var(--box-shadow);
}

.ruleTableData {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}

.ruleTableData .baseRules,
.ruleTableData .hazardLevel {
  width: 50%;
  overflow: hidden;
}

.ruleTableData .baseRules {
  padding-right: 12px;
}
.ruleTableData .hazardLevel {
  padding-left: 12px;
}

.ruleTableData .baseRules > span,
.ruleTableData .hazardLevel > span {
  padding: 0 10px;
  width: 100%;
  height: 30px;
  font-size: 14px;
  line-height: 20px;
  text-align: left;
  display: inline-block;
}

.ruleTableData .baseRulesTableData,
.ruleTableData .hazardLevelTableData {
  width: 100%;
  /* height: calc(100% - 30px); */
  font-size: 14.5px;
  border-radius: 10px;
  border: 2px solid #e6e9f0;
}

/* 基准值规则Start */
/* 表头Start */
.ruleTableData .baseRulesTableData .title {
  width: 100%;
  height: 50px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
}

.ruleTableData .baseRulesTableData .title span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData .baseRulesTableData .title span {
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}
.ruleTableData .baseRulesTableData .title span:last-child {
  border-right: none;
}
/* 表头End */

/* 光功率维护基线(dbm)Start */
.ruleTableData .baseRulesTableData .lightPowerMaintain {
  width: 100%;
  height: 150px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.ruleTableData .baseRulesTableData .lightPowerMaintain > span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ruleTableData .baseRulesTableData .lightPowerMaintain span.baseline {
  display: flex;
  flex-direction: column;
}

.ruleTableData .baseRulesTableData .lightPowerMaintain span.baseline span {
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData .baseRulesTableData .lightPowerMaintain span.maintenanceTypes,
.ruleTableData .baseRulesTableData .lightPowerMaintain span.baseline {
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData .baseRulesTableData .lightPowerMaintain span.applicationArea {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData
  .baseRulesTableData
  .lightPowerMaintain
  span.applicationArea
  span {
  width: 100%;
  height: 50%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData
  .baseRulesTableData
  .lightPowerMaintain
  span.applicationArea
  span:nth-of-type(1) {
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData .baseRulesTableData .lightPowerMaintain span.baseline span {
  width: 100%;
  height: 50%;
}

.ruleTableData
  .baseRulesTableData
  .lightPowerMaintain
  span.baseline
  span:nth-of-type(1) {
  border-bottom: 1px solid #e6e9f0;
}
/* 光功率维护基线(dbm)End */

/* 光功率波动Start */
.ruleTableData .baseRulesTableData .lightPowerVolatility {
  width: 100%;
  height: 150px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.ruleTableData .baseRulesTableData .lightPowerVolatility > span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ruleTableData .baseRulesTableData .lightPowerVolatility span.baseline {
  display: flex;
  flex-direction: column;
}

.ruleTableData .baseRulesTableData .lightPowerVolatility span.baseline span {
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData .baseRulesTableData .lightPowerVolatility span.maintenanceTypes,
.ruleTableData .baseRulesTableData .lightPowerVolatility span.baseline {
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData .baseRulesTableData .lightPowerVolatility span.applicationArea {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData
  .baseRulesTableData
  .lightPowerVolatility
  span.applicationArea
  span {
  width: 100%;
  height: 50%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData
  .baseRulesTableData
  .lightPowerVolatility
  span.applicationArea
  span:nth-of-type(1) {
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData .baseRulesTableData .lightPowerVolatility span.baseline span {
  width: 100%;
  height: 50%;
}

.ruleTableData
  .baseRulesTableData
  .lightPowerVolatility
  span.baseline
  span:nth-of-type(1) {
  border-bottom: 1px solid #e6e9f0;
}
/* 光功率波动End */

/* 增益差维护Start */
.ruleTableData .baseRulesTableData .gainDifferenceMaintain {
  width: 100%;
  height: 75px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
}

.ruleTableData .baseRulesTableData .gainDifferenceMaintain span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData .baseRulesTableData .gainDifferenceMaintain span {
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}
.ruleTableData .baseRulesTableData .gainDifferenceMaintain span:last-child {
  border-right: none;
}
/* 增益差维护End */

/* OLP主备光功率差维护基线(dB)Start */
.ruleTableData .baseRulesTableData .poorLightPowerMaintain {
  width: 100%;
  height: 75px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
}

.ruleTableData .baseRulesTableData .poorLightPowerMaintain span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData .baseRulesTableData .poorLightPowerMaintain span {
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}
.ruleTableData .baseRulesTableData .poorLightPowerMaintain span:last-child {
  border-right: none;
}
/* OLP主备光功率差维护基线(dB)End */

/* 光缆收发损耗差维护基线(dB)Start */
.ruleTableData
  .baseRulesTableData
  .opticalCableTransmissionLossDifferenceMaintain {
  width: 100%;
  height: 75px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
}

.ruleTableData
  .baseRulesTableData
  .opticalCableTransmissionLossDifferenceMaintain
  span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData
  .baseRulesTableData
  .opticalCableTransmissionLossDifferenceMaintain
  span {
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}
.ruleTableData
  .baseRulesTableData
  .opticalCableTransmissionLossDifferenceMaintain
  span:last-child {
  border-right: none;
}
/* 光缆收发损耗差维护基线(dB)End */

/* 备注Start */
.ruleTableData .baseRulesTableData .remark {
  padding: 0 20px;
  width: 100%;
  height: 40px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
/* 备注End */
/* 基准值规则End */

/* 隐患等级门限值Start */
/* 表头Start */
.ruleTableData .hazardLevelTableData .title {
  width: 100%;
  height: 80px;
  display: flex;
  flex-direction: row;
}

.ruleTableData .hazardLevelTableData .title > span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData .hazardLevelTableData .title > span.hiddenContentGroup {
  border-right: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}

.ruleTableData .hazardLevelTableData .title > span.hiddenContentGroup > span {
  width: 100%;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.hiddenContentGroup
  > span.hiddenContentGroupTotal {
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.hiddenContentGroup
  > span.hiddenContentGroupPoints {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.hiddenContentGroup
  > span.hiddenContentGroupPoints
  > span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #e6e9f0;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.hiddenContentGroup
  > span.hiddenContentGroupPoints
  > span:last-of-type {
  border-right: none;
}

.ruleTableData .hazardLevelTableData .title > span.applicationLocal {
  border-right: none;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}

.ruleTableData .hazardLevelTableData .title > span.applicationLocal > span {
  width: 100%;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.applicationLocal
  > span.applicationLocalTotal {
  border-bottom: 1px solid #e6e9f0;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.applicationLocal
  > span.applicationLocalPoints {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.applicationLocal
  > span.applicationLocalPoints
  > span {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #e6e9f0;
}

.ruleTableData
  .hazardLevelTableData
  .title
  > span.applicationLocal
  > span.applicationLocalPoints
  > span:last-of-type {
  border-right: none;
}

/* 表头End */
/* 隐患等级门限值End */

/* 板卡实际和理论光功率偏差Start */
.hazardLevel .boardCardPracticeTheoryLightPowerDeviation {
  width: 100%;
  height: 260px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation > span {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.hazardLevel .boardCardPracticeTheoryLightPowerDeviation > .titleGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.hazardLevel .boardCardPracticeTheoryLightPowerDeviation > .titleGroup > span {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  > .titleGroup
  > span.title {
  width: 55%;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  > .titleGroup
  > span.inputOutputOpticalPower {
  width: 45%;
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  > .titleGroup
  > span.inputOutputOpticalPower
  > span {
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  > .titleGroup
  > span.inputOutputOpticalPower
  > span:last-of-type {
  border-right: none;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  > .titleGroup
  .inputOutputOpticalPower {
  width: 40%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  > .titleGroup
  .inputOutputOpticalPower
  > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.limitGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .limitGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  .limitGroup
  > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  .limitGroup
  > span
  > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  .limitGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  .levelGroup
  > span:last-of-type {
  border-right: none;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  .levelGroup
  > span
  > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardPracticeTheoryLightPowerDeviation
  .levelGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}

/* 板卡实际和理论光功率偏差End */

/* 光功率波动偏差Start */
.hazardLevel .lightPowerVolatilityDeviation {
  width: 100%;
  height: 120px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.hazardLevel .lightPowerVolatilityDeviation > span {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.hazardLevel .lightPowerVolatilityDeviation > .titleGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.hazardLevel .lightPowerVolatilityDeviation > .titleGroup > span {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel .lightPowerVolatilityDeviation > .titleGroup > span.title {
  width: 55%;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  > .titleGroup
  > span.inputOutputOpticalPower {
  width: 45%;
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  > .titleGroup
  > span.inputOutputOpticalPower
  > span {
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  > .titleGroup
  > span.inputOutputOpticalPower
  > span:last-of-type {
  border-right: none;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  > .titleGroup
  .inputOutputOpticalPower {
  width: 40%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  > .titleGroup
  .inputOutputOpticalPower
  > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.limitGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .lightPowerVolatilityDeviation .limitGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel .lightPowerVolatilityDeviation .limitGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .lightPowerVolatilityDeviation .limitGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  .limitGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .lightPowerVolatilityDeviation .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel .lightPowerVolatilityDeviation .levelGroup > span:last-of-type {
  border-right: none;
}

.hazardLevel .lightPowerVolatilityDeviation .levelGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .lightPowerVolatilityDeviation
  .levelGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}

/* 光功率波动偏差End */

/* 板卡增益范围与实际增益偏差Start */
.hazardLevel .boardCardGainSpan {
  width: 100%;
  height: 120px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.hazardLevel .boardCardGainSpan > span {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.hazardLevel .boardCardGainSpan > .titleGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.hazardLevel .boardCardGainSpan > .titleGroup > span {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel .boardCardGainSpan > .titleGroup > span.title {
  width: 55%;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel .boardCardGainSpan > .titleGroup > span.elevatedReduceActualGain {
  width: 45%;
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardGainSpan
  > .titleGroup
  > span.elevatedReduceActualGain
  > span {
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .boardCardGainSpan
  > .titleGroup
  > span.elevatedReduceActualGain
  > span:last-of-type {
  border-right: none;
}

.hazardLevel .boardCardGainSpan > .titleGroup .elevatedReduceActualGain {
  width: 40%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .boardCardGainSpan > .titleGroup .elevatedReduceActualGain > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.limitGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .boardCardGainSpan .limitGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel .boardCardGainSpan .limitGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .boardCardGainSpan .limitGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel .boardCardGainSpan .limitGroup > span > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .boardCardGainSpan .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel .boardCardGainSpan .levelGroup > span:last-of-type {
  border-right: none;
}

.hazardLevel .boardCardGainSpan .levelGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel .boardCardGainSpan .levelGroup > span > span:last-of-type {
  border-bottom: none;
}
/* 板卡增益范围与实际增益偏差End */

/* OLP主备光功率偏差Start */
.hazardLevel .olpMainPrepareLightPowerDeviation {
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.hazardLevel .olpMainPrepareLightPowerDeviation > span {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.hazardLevel .olpMainPrepareLightPowerDeviation > .titleGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.hazardLevel .olpMainPrepareLightPowerDeviation > .titleGroup > span {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel .olpMainPrepareLightPowerDeviation > .titleGroup > span.title {
  width: 55%;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  > .titleGroup
  > span.mainPrepareExcessive {
  width: 45%;
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  > .titleGroup
  > span.mainPrepareExcessive {
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  > .titleGroup
  > span.mainPrepareExcessive
  > span:last-of-type {
  border-right: none;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  > .titleGroup
  .mainPrepareExcessive {
  width: 40%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  > .titleGroup
  .mainPrepareExcessive
  > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.limitGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .limitGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  .limitGroup
  > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .limitGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  .limitGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  .levelGroup
  > span:last-of-type {
  border-right: none;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .levelGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel
  .olpMainPrepareLightPowerDeviation
  .levelGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}
/* OLP主备光功率偏差End */

/* 光缆收发损耗偏差Start */
.hazardLevel .opticalCableSendReceiveLossDeviation {
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.hazardLevel .opticalCableSendReceiveLossDeviation > span {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.hazardLevel .opticalCableSendReceiveLossDeviation > .titleGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.hazardLevel .opticalCableSendReceiveLossDeviation > .titleGroup > span {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel .opticalCableSendReceiveLossDeviation > .titleGroup > span.title {
  width: 55%;
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  > .titleGroup
  > span.sendReceiveLossDeviation {
  width: 45%;
  border-right: 1px solid #e6e9f0;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  > .titleGroup
  > span.sendReceiveLossDeviation
  > span:last-of-type {
  border-right: none;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  > .titleGroup
  .sendReceiveLossDeviation {
  width: 40%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  > .titleGroup
  .sendReceiveLossDeviation
  > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.limitGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .opticalCableSendReceiveLossDeviation .limitGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  .limitGroup
  > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .opticalCableSendReceiveLossDeviation .limitGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  .limitGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .opticalCableSendReceiveLossDeviation .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  .levelGroup
  > span:last-of-type {
  border-right: none;
}

.hazardLevel .opticalCableSendReceiveLossDeviation .levelGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hazardLevel
  .opticalCableSendReceiveLossDeviation
  .levelGroup
  > span
  > span:last-of-type {
  border-bottom: none;
}
/* 光缆收发损耗偏差Start */
</style>