<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-18 16:48:28
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-09 14:52:30
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\dataImport\adjustableDimLiveNetConfiguration\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <!-- 光放板卡标准参数 -->
  <div class="main">
    <div class="operatingHead">
      <div class="operatingTool">
        <br>
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item label="传输系统">
            <el-input
                  label="传输系统"
                  placeholder="传输系统"
                  v-model="qry_sys_name"
                />
          </el-form-item>
          <el-form-item label="地市">
            <el-input
                  label="地市"
                  placeholder="地市"
                  v-model="qry_city"
                />
          </el-form-item>
          <el-form-item label="数据错误类型">
            <el-input
                  label="数据错误类型"
                  placeholder="数据错误类型"
                  v-model="qry_data_error"
                />
          </el-form-item>
          <el-form-item>
            <el-button class="btnSearch" @click="init">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button
              class="btnSearch"
              @click="exportor"
              >导出</el-button
            >
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="content">
      <el-table
        :data="tableData.slice()"
        stripe
        :row-style="{ height: '0' }"
        :header-cell-style="{
          'text-align': 'center',
          background: '#F3F5FA',
          padding: '10px 0',
        }"
        :cell-style="{ 'text-align': 'center', padding: '10px' }"
        @filter-change="handleFilterChange"
        height="100%"
      >
        <el-table-column
          align="center"
          prop="sys_name"
          label="传输系统"
          column-key="sys_name"
        ></el-table-column>
        <el-table-column
          align="center"
          label="网络等级"
          prop="net_level"
        />
        <el-table-column
          align="center"
          label="地市"
          prop="city"
        />
        <el-table-column
          align="center"
          label="A端子网元名称"
          prop="a_sub_name"
        />
        <el-table-column
          align="center"
          label="A端子架ID"
          prop="a_shelf_id"
        />
        <el-table-column
          align="center"
          label="A端槽位ID"
          prop="a_slot_id"
        />
        <el-table-column
          align="center"
          label="A端口ID"
          prop="a_in_out_id"
        />
        <el-table-column
          align="center"
          label="Z端子网元名称"
          prop="z_sub_name"
        />
        <el-table-column
          align="center"
          label="Z端子架ID"
          prop="z_shelf_id"
        />
        <el-table-column
          align="center"
          label="Z端槽位ID"
          prop="z_slot_id"
        />
        <el-table-column
          align="center"
          label="Z端口ID"
          prop="z_in_out_id"
        />
        <el-table-column
          align="center"
          label="系统波道数"
          prop="full_waves"
        />
        <el-table-column
          align="center"
          label="光缆长度"
          prop="fiber_length"
        />
        <el-table-column
          align="center"
          label="数据错误类型"
          prop="data_error"
        />
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

  <el-dialog v-model="centerDialogVisible" title="参数上传" width="30%" center>
    <el-upload
      class="upload-demo"
      drag
      action="/paramsApi/oa_board_standard/upload_file"
      multiple
      :on-success="uploadSuccess"
      :on-error="uploadError"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传模板文件对应参数</div>
    </el-upload>
  </el-dialog>

  <el-dialog v-model="dialogVisibleParameter" title="新建" width="30%" center>
    <el-form :model="form" label-width="200px">
      <el-form-item label=""> </el-form-item>
      <el-form-item label="板卡类型：">
        <div class="demo-input-size">
          <el-input
            v-model="form.board_model"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="标准增益最小值">
        <div class="demo-input-size">
          <el-input
            v-model="form.standard_gain_min"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="标准增益最大值">
        <div class="demo-input-size">
          <el-input
            v-model="form.standard_gain_max"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="40波系统-单波输出标准值">
        <div class="demo-input-size">
          <el-input
            v-model="form.standard_single_40_wave_output"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="80波系统-单波输出标准值">
        <div class="demo-input-size">
          <el-input
            v-model="form.standard_single_80_wave_output"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="96波系统-单波输出标准值">
        <div class="demo-input-size">
          <el-input
            v-model="form.standard_single_96_wave_output"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisibleParameter = false">取消</el-button>
        <el-button type="primary" @click="onSubmit">保存</el-button>
      </span>
    </template>
  </el-dialog>
</template>





<script>
import { ref } from "vue";
import { ElMessageBox } from "element-plus";
import CsvExportor from "csv-exportor";
import { getIs_Authen } from "@/config/UserInfomation";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  getBoardStandardFilter,
  getComputedState,
  startComputed,
  updateBoardStandardCalculate,
  addBoardStandard,
  updateBoardStandard,
  setLog,
  logModuleMenu,
  operationMenu,
  getCheckTopology,
  exportCheckTopologyData,
} from "@/api/WDM-OTN/http";
import { filter } from 'lodash';

export default {
  data() {
    return {
      reComputed: {
        text: "重新计算",
        disabled: false,
      },
      restartComputed: false,
      tableData: ref(""),
      currentPage: 1, // 每页多少条
      pageSize: 15, //每页显示个数
      pageTotal: ref(""),
      dataTotal: ref(""),
      labelSave: ref(""),
      centerDialogVisible: false,
      dialogVisibleParameter: false,
      form: {
        board_model: "",
        standard_gain_min: "",
        standard_gain_max: "",
        standard_single_40_wave_output: "",
        standard_single_80_wave_output: "",
        standard_single_96_wave_output: "",
      },
      // all_sub_name_array: [],
      all_board_model_array: [],

      // filters_sub_name_tag: {},
      filters_board_model_tag: {},
      isAuthen: false,
      qry_sys_name: "",
      qry_city: "",
      qry_data_error: "",
    };
  },
  methods: {
    refreshTable(data) {
      this.tableData = data.myArray;
      this.pageTotal = data.page_size;
      this.pageCount = data.page_count;
      this.dataTotal = data.total;
    },
    setFiltersArray(data) {
      new Promise(() => {
        data.forEach((item) => {
          if (!this.all_board_model_array.includes(item.board_model)) {
            this.all_board_model_array.push(item.board_model);
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
      let data0 = {
        page_index_begin: 0,
        page_size: this.pageSize,
      };

      if (this.generate_filter().length > 0){
        data0['filter'] = this.generate_filter();
      }

      getCheckTopology(data0).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
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
    generate_filter() {
      let filter = []
      if (this.qry_sys_name.trim() !== ""){
        filter.push({
          name: "sys_name",
          values: this.qry_sys_name
        });
      }
      if (this.qry_city.trim() !== ""){
        filter.push({
          name: "city",
          values: this.qry_city
        });
      }
      if (this.qry_data_error.trim() !== ""){
        filter.push({
          name: "data_error",
          values: this.qry_data_error
        });
      }
      return filter;
    },
    changePage() {
      let obj = {
        page_index_begin: this.currentPage,
        page_size: this.pageSize,

        // filter:[this.filters_sub_name_tag,this.filters_board_model_tag]
        // filter: [this.filters_board_model_tag],
      };
      if (this.generate_filter().length > 0){
        obj['filter'] = this.generate_filter();
      }

      getCheckTopology(obj).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    editRow(data) {
      updateBoardStandard(data).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
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
            type: "info",
            message: "保存修改",
          });
        })
        .catch((action) => {
          this.$message({
            type: "info",
            message: action === "cancel" ? "放弃保存" : "停留在当前页面",
          });
        });
    },
    onSubmit() {
      addBoardStandard(this.form).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
      const user = getCookie("usn");
      setLog({
        op_module: logModuleMenu.SPOTODB,
        op_user: user,
        op_behavior: user + operationMenu.add,
        op_time: NowDate(),
      });
      this.dialogVisibleParameter = false;
    },
    recountParameter() {
      let data1 = {
        tableName: "光放办卡标准参数",
      };
      updateBoardStandardCalculate(data1).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    handleFilterChange(filterObj) {
      // if(filterObj.sub_name != null){
      //   this.filters_sub_name_tag = {
      //     name:"sub_name",
      //     values:filterObj.sub_name
      //   }
      // }
      if (filterObj.board_model != null) {
        this.filters_board_model_tag = {
          name: "board_model",
          values: filterObj.board_model,
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
      getBoardStandardFilter().then((res) => {
        if (res.code == 200) {
          const result = res;
          _this.setFiltersArray(result.data);
        }
      });
    },
    uploadSuccess() {
      this.$message({
          showClose: true,
          message: '文件上传成功',
          type: 'success'
        });
    },
    uploadError() {
      this.$message({
          showClose: true,
          message: '文件上传失败！',
          type: 'error'
        });
    },
    getAuthen() {
      this.isAuthen = getIs_Authen().can_add_standrad_param;
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
    exportor() {
      let _this = this;
      let tableData = [];
      let data0 = {};

      if (this.generate_filter().length > 0){
        data0['filter'] = this.generate_filter();
      }
      new Promise((resolve, reject) => {
        exportCheckTopologyData(data0).then((res) => {
          if (res.code == 200) {
            const data = res.data;
            for (const item of data) {
              let list = {};
              list.sys_name = item.sys_name;
              list.net_level = item.net_level;
              list.city = item.city;
              list.a_sub_name = item.a_sub_name;
              list.a_shelf_id = item.a_shelf_id;
              list.a_slot_id = item.a_slot_id;
              list.a_in_out_id = item.a_in_out_id;
              list.z_sub_name = item.z_sub_name;
              list.z_shelf_id = item.z_shelf_id;
              list.z_slot_id = item.z_slot_id;
              list.z_in_out_id = item.z_in_out_id;
              list.full_waves = item.full_waves;
              list.fiber_length = item.fiber_length;
              list.data_error = item.data_error;
              tableData.push(list);
            }
            let header = [
              "传输系统",
              "网络等级",
              "地市",
              "A端子网元名称",
              "A端子架ID",
              "A端槽位ID",
              "A端口ID",
              "Z端子网元名称",
              "Z端子架ID",
              "Z端槽位ID",
              "Z端口ID",
              "系统波道数",
              "光缆长度",
              "数据错误类型",
            ];
            CsvExportor.downloadCsv(
              tableData,
              { header },
              "checkTopology" + _this.dateFormat() + ".csv"
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
  }, //methods
  mounted() {
    this.getAuthen();
    this.getRestartComputed();
    this.init();
    this.getComputedState();
  },
  created() {
    this.getFilter();
  },
  // editRow(index, data) {
  // },
  deleteRow(index, data) {},
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
.main {
  width: 100%;
  height: 100%;
  flex-direction: column;
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
  padding: 10px 20px;
  width: 100%;
  height: 50px;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  /* align-items: center; */
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

.operatingTool .button:last-of-type {
  margin-right: 0;
}

.main .content {
  width: 100%;
  height: calc(100% - 60px - 60px);
  overflow-anchor: none;
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.main .content::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>