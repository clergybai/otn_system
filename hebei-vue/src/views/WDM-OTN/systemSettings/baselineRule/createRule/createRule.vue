<template>
  <div class="main">
    <div class="body">
      <div class="ruleTableData">
        <div class="hazardLevel">
          <el-row type="flex" justify="center" align="middle">
            <el-col :span="18">
              <div class="inputFrameNameDisplay">
                <strong>规则名称：</strong>
                <input
                  type="text"
                  class="inputFrameName"
                  label="sdf"
                  placeholder="请输入新建规则名称"
                  v-model="rule_name"
                  @change="init(rule_name)"
                />
              </div>
            </el-col>
            <el-col :span="6">
              <div class="operatingTool">
                <button @click.prevent="open(scope)" v-if="isAuthen">保存</button>
              </div>
            </el-col>
          </el-row>
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
              <!-- <span class="status">状态</span>               -->
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
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_input_power_std_dev_up_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalInputOpticalPowerReduce"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_input_power_std_dev_low_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalOutputOpticalPowerElevated"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_output_power_std_dev_up_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalOutputOpticalPowerReduce"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_output_power_std_dev_low_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencyInputOpticalPowerElevated"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_input_power_std_dev_up_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyInputOpticalPowerReduce"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_input_power_std_dev_low_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyOutputOpticalPowerElevated"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_output_power_std_dev_up_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyOutputOpticalPowerReduce"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_output_power_std_dev_low_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup"></span>
                <span class="cityGroup"></span>
              </span>
              <!-- <span class="statusGroup"></span>                         -->
            </div>
            <!-- 光功率波动偏差 -->
            <div class="lightPowerVolatilityDeviation">
              <span class="titleGroup">
                <span class="title">光功率波动偏差</span>
                <span class="inputOutputOpticalPower">
                  <span class="inputOpticalPowerExcessive">输入光功率波动超标</span>
                  <span class="inputOpticalPowerVolatilityExcessive"
                    >输出光功率波动超标</span
                  >
                </span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalInputOpticalPowerExcessive"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_input_power_fluc_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalInputOpticalPowerVolatilityExcessive"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_output_power_fluc_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>

                <span class="emergencyGroup">
                  <span class="emergencyInputOpticalPowerExcessive"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_input_power_fluc_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyInputOpticalPowerVolatilityExcessive"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_output_power_fluc_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <span class="networkGroup">
                  <!-- <select v-model="tableData.net_level">
                      <option disabled value="">请选择</option>
                      <option>ALL</option>  
                      <option>二干</option>
                      <option>本地</option>
                    </select>   -->
                  <el-radio-group
                    v-model="tableData.net_level"
                    class="ml-4"
                    @change="handleChange"
                  >
                    <el-radio label="二干" size="large">二干</el-radio>
                    <el-radio label="本地" size="large">本地</el-radio>
                  </el-radio-group>
                </span>
                <span class="cityGroup">
                  <el-radio-group v-model="tableData.city" :disabled="tableData.net_level == '二干'">
                    <el-radio label="石家庄市" />
                    <el-radio label="唐山市" />
                    <el-radio label="秦皇岛市" />
                    <el-radio label="邯郸市" />
                    <el-radio label="邢台市" />
                    <el-radio label="保定市" />
                    <el-radio label="承德市" />
                    <el-radio label="沧州市" />
                    <el-radio label="廊坊市" />
                    <el-radio label="衡水市" />
                    <el-radio label="雄安新区" />
                    <el-radio label="张家口市" />
                  </el-radio-group>
                </span>
              </span>
              <!-- <span class="statusGroup">
                    <el-row>
                    <el-col :span="12"><el-switch v-model="tableData.is_used_bool" :active-value="true" :inactive-value="false"
                              style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"/></el-col>
                    <el-col :span="12"><p>{{tableData.is_used_bool ? "已启用" : "已停用"}}</p></el-col>
                    </el-row>
               </span>                              -->
            </div>
            <!-- 板卡增益范围与实际增益偏差 -->
            <div class="boardCardGainSpan">
              <span class="titleGroup">
                <span class="title">板卡增益范围与实际增益偏差</span>
                <span class="elevatedReduceActualGain">
                  <span class="elevatedActualGain">实际增益升高</span>
                  <span class="ReduceActualGain">实际增益降低</span>
                </span>
              </span>
              <span class="limitGroup">
                <span class="generalGroup">
                  <span class="generalelevatedActualGain"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_gain_std_dev_up_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="generalReduceActualGain"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_gain_std_dev_low_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencyelevatedActualGain"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_gain_std_dev_up_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                  <span class="emergencyReduceActualGain"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.oa_gain_std_dev_low_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <!-- <span class="networkGroup"></span>
                <span class="cityGroup"></span> -->
              </span>
              <!-- <span class="statusGroup"></span>               -->
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
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.olp_power_dev_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencyMainPrepareExcessive"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.olp_power_dev_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <!-- <span class="networkGroup"></span>
                <span class="cityGroup"></span> -->
              </span>
              <!-- <span class="statusGroup"></span>                -->
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
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.fiber_two_way_dev_risk_thr"
                      min="1"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
                <span class="emergencyGroup">
                  <span class="emergencySendReceiveLossDeviation"
                    ><input
                      type="number"
                      class="inputFrame"
                      v-model="tableData.fiber_two_way_dev_risk_urg"
                      min="3"
                      max="10"
                    />
                    <p>&emsp;dB</p></span
                  >
                </span>
              </span>
              <span class="levelGroup">
                <!-- <span class="networkGroup"></span>
                <span class="cityGroup"></span> -->
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
import { getIs_Authen, getUserName } from "@/config/UserInfomation";
import {
  getRule,
  updateRule,
  setLog,
  logModuleMenu,
  operationMenu,
} from "@/api/WDM-OTN/http";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";

export default {
  data() {
    return {
      rule_name: ref(""),
      tableData: {
        net_level: "二干",
      },
      isCityGroupDisable: false,
      isAuthen: false,
      dataCheck: false,
    };
  },
  methods: {
    refreshTable(data) {
      if (data == null) {
        this.tableData = {};
        return;
      }
      this.tableData = data;
    },
    init(name) {
      let obj = {
        rule_name: name,
      };
      getRule(obj).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    SaveAction() {
      let _this = this;
      _this.tableData.rule_name = _this.rule_name;
      _this.tableData.owner = getUserName();
      updateRule(_this.tableData).then((res) => {
        if (res.code == 200) {
          _this.$message({
            type: "success",
            message: "保存修改",
          });
          const user = getCookie("usn");
          setLog({
            op_module: logModuleMenu.TNR,
            op_user: user,
            op_behavior:
              user + _this.dataCheck ? operationMenu.update : operationMenu.add,
            op_time: NowDate(),
          });
        }
      });
    },
    open(data) {
      let _this = this;
      _this
        .$confirm("参数值已经修改，是否保存修改？", "确认信息", {
          distinguishCancelAndClose: true,
          confirmButtonText: "保存",
          cancelButtonText: "取消",
        })
        .then(() => {
          _this.SaveAction(data);
        })
        .catch((action) => {
          _this.$message({
            type: "info",
            message: action === "cancel" ? "放弃保存" : "停留在当前页面",
          });
        });
    },
    handleChange(val) {
      // if (val == "二干") {
      //   this.isCityGroupDisable = true;
      // } else {
      //   this.isCityGroupDisable = false;
      // }
    },
    getAuthen() {
      this.isAuthen = getIs_Authen().can_threshold_setting;
    },
  },
  mounted() {
    this.getAuthen();
    if (
      this.$route.params.rule_name == null ||
      this.$route.params.rule_name == undefined ||
      this.$route.params.rule_name == ""
    ) {
      this.dataCheck = true;
      return;
    }
    this.rule_name = this.$route.params.rule_name;
    this.init(this.rule_name);
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
.main {
  padding: 10px 20px 10px 10px;
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

.el-main {
  height: 100%;
}
.el-row {
  height: 100%;
}

.ruleTableData {
  width: 90%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}

.ruleTableData .baseRules,
.ruleTableData .hazardLevel {
  width: 100%;
  overflow: hidden;
  flex-direction: row;
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
  height: calc(100% - 30px);
  font-size: 13px;
  border-radius: 10px;
  border: 2px solid #e6e9f0;
}

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
  border-right: 1px solid #e6e9f0;
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
  border-right: 1px solid #e6e9f0;
}

.ruleTableData .hazardLevelTableData .title > span.status {
  border-right: none;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}

.ruleTableData .hazardLevelTableData.title > span:last-of-type {
  border-bottom: none;
}
/* 表头End */
/* 隐患等级门限值End */

/* 板卡实际和理论光功率偏差Start */
.hazardLevel .boardCardPracticeTheoryLightPowerDeviation {
  width: 100%;
  height: 160px;
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

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation > .titleGroup > span.title {
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

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .limitGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .limitGroup > span > span {
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

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .levelGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .levelGroup > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: none;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation .levelGroup > span:last-of-type {
  border-bottom: none;
}
.hazardLevel .boardCardPracticeTheoryLightPowerDeviation > .statusGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .boardCardPracticeTheoryLightPowerDeviation > .statusGroup > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
  border-right: none;
}

/* 板卡实际和理论光功率偏差End */

/* 光功率波动偏差Start */
.hazardLevel .lightPowerVolatilityDeviation {
  width: 100%;
  height: 80px;
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

.hazardLevel .lightPowerVolatilityDeviation > .titleGroup > span.inputOutputOpticalPower {
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

.hazardLevel .lightPowerVolatilityDeviation > .titleGroup .inputOutputOpticalPower {
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

.hazardLevel .lightPowerVolatilityDeviation .limitGroup > span > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .lightPowerVolatilityDeviation .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom: none;
}

.hazardLevel .lightPowerVolatilityDeviation .levelGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
  border-bottom: none;
}

.hazardLevel .lightPowerVolatilityDeviation > .statusGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .lightPowerVolatilityDeviation > .statusGroup > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
  border-right: none;
}

/* 光功率波动偏差End */

/* 板卡增益范围与实际增益偏差Start */
.hazardLevel .boardCardGainSpan {
  width: 100%;
  height: 80px;
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

.hazardLevel .boardCardGainSpan > .titleGroup > span.elevatedReduceActualGain > span {
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
  border-bottom: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .boardCardGainSpan .levelGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
  border-bottom: none;
}

.hazardLevel .boardCardGainSpan > .statusGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .boardCardGainSpan > .statusGroup > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 板卡增益范围与实际增益偏差End */

/* OLP主备光功率偏差Start */
.hazardLevel .olpMainPrepareLightPowerDeviation {
  width: 100%;
  height: 40px;
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

.hazardLevel .olpMainPrepareLightPowerDeviation > .titleGroup .mainPrepareExcessive {
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

.hazardLevel .olpMainPrepareLightPowerDeviation .limitGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .limitGroup > span > span {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .limitGroup > span > span:last-of-type {
  border-bottom: none;
}

.levelGroup {
  display: flex;
  flex-direction: row;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .levelGroup > span {
  flex: 1;
  border-right: 1px solid #e6e9f0;
  border-bottom: none;
  display: flex;
  flex-direction: column;
}

.hazardLevel .olpMainPrepareLightPowerDeviation .levelGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
  border-bottom: none;
}

.hazardLevel .olpMainPrepareLightPowerDeviation > .statusGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .olpMainPrepareLightPowerDeviation > .statusGroup > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e6e9f0;
  border-right: none;
}

/* OLP主备光功率偏差End */

/* 光缆收发损耗偏差Start */
.hazardLevel .opticalCableSendReceiveLossDeviation {
  width: 100%;
  height: 40px;
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

.hazardLevel .opticalCableSendReceiveLossDeviation .limitGroup > span:last-of-type {
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
  border-bottom: none;
  display: flex;
  flex-direction: column;
}

.hazardLevel .opticalCableSendReceiveLossDeviation .levelGroup > span:last-of-type {
  border-right: 1px solid #e6e9f0;
  border-bottom: none;
}

.hazardLevel .opticalCableSendReceiveLossDeviation > .statusGroup {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.hazardLevel .opticalCableSendReceiveLossDeviation > .statusGroup > span {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 光缆收发损耗偏差End */

.inputFrameNameDisplay {
  width: 100%;
  height: 50px;
  /* justify-content: ; */
}

.inputFrameName {
  width: 300px;
  height: 30px;
  /* align-items: center; */
}

.inputFrame {
  width: 60px;
  /* align-items: center;
  justify-content: center; */
}

.operatingTool {
  padding: 0 20px;
  width: 100%;
  height: 50px;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  align-items: center;
  /* justify-content: flex-end; */
  justify-content: flex-end;
  overflow: hidden;
}
.operatingTool button {
  margin-right: 20px;
  height: 50%;
  padding: 2px 16px;
  font-family: SimHei;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #a5b1f8;
  font-size: 15px;
  color: #788af5;
  background-color: transparent;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
}

.operatingTool button:active,
.operatingTool button:focus,
.operatingTool button:hover {
  background-color: #4c64f2;
  border: 1px solid transparent;
  color: #fff;
}

.operatingTool button:last-of-type {
  margin-right: 0;
}
.cityGroup .el-radio-group {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: center;
}
</style>
