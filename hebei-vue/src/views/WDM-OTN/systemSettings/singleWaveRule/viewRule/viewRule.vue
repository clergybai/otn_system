<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-18 16:48:28
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-09 14:43:40
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\dataImport\adjustableDimLiveNetConfiguration\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <!-- 可调光衰现网配置 -->

  <div class="main">
    <div class="content">
      <div class="operatingHead">
        <div class="operatingTool">
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
          :data="
            tableData.slice(
              (currentPage - 1) * pageSize,
              currentPage * pageSize
            )
          "
          stripe
          :row-style="{ height: '0' }"
          :header-cell-style="{
            'text-align': 'center',
            background: '#F3F5FA',
            padding: '10px 0',
          }"
          :cell-style="{ 'text-align': 'center', padding: '5px' }"
        >
          <el-table-column prop="rule_name" label="规则名称" width="250px" />
          <el-table-column prop="net_level" label="网络等级" width="100px" />
          <el-table-column prop="city" label="地市" width="100px" />
          <el-table-column prop="owner" label="创建人" width="150px" />
          <el-table-column align="center" label="操作">
            <template #default="scope">
              <div class="operationGroup">
                <el-button
                  class="ToolBtn"
                  type="text"
                  @click.prevent="editRow(scope.row.rule_name)"
                  >查看</el-button
                >
                <!-- <el-button
                class="ToolBtn"
                type="text"
                @click.prevent="deleteRow(scope.$index, tableData)"
                >停用/启用</el-button
              > -->
                <!-- <el-button
                class="ToolBtn"
                type="text"
                @click.prevent="deleteRow(scope.$index, tableData)"
                >修改</el-button
              > -->
                <el-button
                  class="ToolBtn"
                  type="text"
                  @click.prevent="deleteRow(scope.row.rule_name)"
                  v-if="isAuthen"
                  >删除</el-button
                >
              </div>
            </template>
          </el-table-column>
          <el-table-column label="是否启用" v-if="isAuthen">
            <template #default="scope">
              <div class="operationGroup">
                <el-switch
                  v-model="scope.row.is_used_bool"
                  :active-value="true"
                  :inactive-value="false"
                  v-on:change="handleIsUsedChanged(scope.row, $event)"
                  style="
                    --el-switch-on-color: #13ce66;
                    --el-switch-off-color: #ff4949;
                  "
                />
                <p
                  :style="{
                    color: scope.row.is_used_bool ? 'var(--theme-color)' : '',
                    'margin-left': '10px',
                  }"
                >
                  {{ scope.row.is_used_bool ? "已启用" : "已停用" }}
                </p>
              </div>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          :hide-on-single-page="tableData.length <= pageSize"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 30, 40]"
          :page-size="pageSize"
          layout="sizes, prev, pager, next, jumper"
          class="paging"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { getIs_Authen } from "@/config/UserInfomation";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  getComputedState,
  startComputed,
  updateState,
  delRule,
  getOutline,
  setLog,
  logModuleMenu,
  operationMenu,
} from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      reComputed: {
        text: "重新计算",
        disabled: false,
      },
      restartComputed: false,
      IsActiveTabIndex: 1, //TAB下标
      IsActiveToolIndex: 1, //Tool下标
      currentPage: 1, // 当前页
      pageSize: 20, //每页显示个数
      pageCount: 0,
      pageTotal: 0,
      dataTotal: 0,
      tableData: [],
      isAuthen: false,
    };
  },
  created() {},
  mounted() {},
  methods: {
    refreshTable(data) {
      if (data == null) {
        this.tableData = [];
        //this.pageTotal = data.page_size
        this.pageCount = 0;
        this.dataTotal = 0;
        return;
      }
      this.tableData = data.myArray;
      this.pageTotal = data.page_size;
      this.pageCount = data.page_count;
      this.dataTotal = data.total;
    },
    init() {
      let data = {
        page_index_begin: 0,
        page_size: 20,
      };
      getOutline(data).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    handleSizeChange(val) {
      this.pageSize = val;
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
      let _this = this;
      if (_this.currentPage == _this.totalPage) {
        return false;
      } else {
        _this.currentPage++;
        _this.changePage();
      }
    },
    changePage() {
      let _this = this;
      let obj = {
        page_index_begin: _this.currentPage,
        page_size: _this.pageSize,
      };
      getOutline(obj).then((res) => {
        if (res.code == 200) {
          _this.refreshTable(res.data);
        }
      });
    },
    editRow(name) {
      this.$router.push({
        name: "createRule",
        params: {
          rule_name: name,
        },
      });
    },
    deleteRow(name) {
      let _this = this;
      let obj = {
        rule_name: name,
      };
      ElMessageBox.confirm("确认删除" + name + "吗?", "删除", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "error",
        showClose: false,
        lockScroll: true,
        closeOnClickModal: false,
      })
        .then((res) => {
          delRule(obj).then((res) => {
            if (res.code == 200) {
              const user = getCookie("usn");
              setLog({
                op_module: logModuleMenu.VTR,
                op_user: user,
                op_behavior: user + operationMenu.delete,
                op_time: NowDate(),
              });
            }
            _this.init();
          });
        })
        .catch((res) => {});
    },
    handleIsUsedChanged(val, checked) {
      let _this = this;
      let obj = {
        rule_name: val.rule_name,
        city: val.city,
        is_used_bool: checked,
      };
      if (checked) {
        let index = _this.tableData.findIndex(
          (item) => item.net_level == val.net_level && item.is_used == 1
        );
        if (index > 0) {
          ElMessageBox.confirm("已有启用的相同地市, 是否继续启用?", "启用", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
            showClose: false,
            lockScroll: true,
            closeOnClickModal: false,
          })
            .then((res) => {
              updateState(obj);
              setTimeout(() => {
                _this.init();
              }, 100);
            })
            .catch((res) => {
              setTimeout(() => {
                _this.init();
              }, 100);
            });
        } else {
          updateState(obj);
          setTimeout(() => {
            _this.init();
          }, 100);
        }
      } else {
        updateState(obj);
        setTimeout(() => {
          _this.init();
        }, 100);
      }
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
      getComputedState((res) => {
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
    getAuthen() {
      this.isAuthen = getIs_Authen().can_threshold_setting;
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
    this.getComputedState();
    this.getRestartComputed();
    this.init();
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

/* .main {
  width: 100%;
  height: 100%;
  flex-direction: column;
} */

.main {
  padding: 10px 20px 10px 10px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.main .content {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  background-color: var(--white);
  box-shadow: var(--box-shadow);
}

.main .operatingHead {
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  box-sizing: border-box;
}

.operatingHead .operatingTool {
  padding: 0 20px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  overflow: hidden;
}

.operatingTool .button {
  margin-right: 20px;
  height: 30px;
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
  z-index: 1;
}

.operatingTool button.button:not(.is-disabled):active,
.operatingTool button.button:not(.is-disabled):focus,
.operatingTool button.button:not(.is-disabled):hover {
  background-color: #4c64f2;
  border: 1px solid transparent;
  color: #fff;
}

.operatingTool button:last-of-type {
  margin-right: 0;
}

.main .body {
  padding: 0 20px 20px 20px;
  width: 100%;
  height: calc(100% - 60px);
  box-sizing: border-box;
  overflow-anchor: none;
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  justify-content: flex-end;
}

.main .content::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>