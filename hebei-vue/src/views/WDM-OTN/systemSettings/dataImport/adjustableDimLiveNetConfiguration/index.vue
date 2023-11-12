<template>
  <!-- 可调光衰现网配置 -->
  <div class="main">
    <div class="operatingHead">
      <div class="operatingTool">
        <!-- <el-button class="button" @click="dialogVisibleParameter = true"
          >新增</el-button
        >
        <el-button class="button" @click="recountParameter">重新计算</el-button> -->
        <el-button
          class="button"
          @click="centerDialogVisible = true"
          v-if="isAuthen"
          >参数上传</el-button
        >
        <!-- href="ftp://user2:ftp123.@192.168.1.95/dl/%E5%8F%AF%E8%B0%83%E5%85%89%E8%A1%B0%E7%8E%B0%E7%BD%91%E9%85%8D%E7%BD%AE%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BF.xlsx"-->
        <el-link
          target="_blank"
          href="http://61.163.104.139:12003/%E5%8F%AF%E8%B0%83%E5%85%89%E8%A1%B0%E7%8E%B0%E7%BD%91%E9%85%8D%E7%BD%AE%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BF.xlsx"
          :underline="false"
          style="margin-left: 15px"
          ondragstart="return false"
        >
          <el-button class="button" v-if="isAuthen">模板下载</el-button>
        </el-link>
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
          prop="sub_name"
          label="网元名称（即子网元名称）"
          width="400px"
          column-key="sub_name"
          :filters="getFilters(all_sub_name_array)"
        >
        </el-table-column>
        <el-table-column label="子架号" prop="shelf_id" />
        <el-table-column label="槽位号" prop="slot_id" />
        <el-table-column label="端口" prop="port_id" />
        <el-table-column label="光口衰减率(dB)" prop="voa_vaule" />
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
      action="/paramsApi/voa_config/upload_file"
      multiple
      :before-upload="beforeUpload"
      :on-success="uploadSuccess"
      :on-error="uploadError"
      accept=".xlsx"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传模板文件对应参数</div>
    </el-upload>
  </el-dialog>
  <!-- 新增 -->
  <el-dialog
    v-model="dialogVisibleParameter"
    title="新建参数"
    width="30%"
    center
  >
    <el-form :model="form" label-width="150px">
      <el-form-item label=""> </el-form-item>
      <el-form-item label="子网元名称">
        <div class="demo-input-size">
          <el-input
            v-model="form.sub_name"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="光放板子架">
        <div class="demo-input-size">
          <el-input
            v-model="form.shelf_id"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="光放板槽位">
        <div class="demo-input-size">
          <el-input
            v-model="form.slot_id"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="端口">
        <div class="demo-input-size">
          <el-input
            v-model="form.port_id"
            class="w-50 m-2"
            placeholder="请输入"
          />
        </div>
      </el-form-item>
      <el-form-item label="光口衰减率(dB)">
        <div class="demo-input-size">
          <el-input
            v-model="form.voa_vaule"
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
import { ElMessage } from "element-plus";
import { getIs_Authen } from "@/config/UserInfomation";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  getConfigFilter,
  updateStandardCalculate,
  addBoardStandard,
  updateConfig,
  getConfig,
  setLog,
  logModuleMenu,
  operationMenu,
} from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      tableData: ref(""),
      currentPage: 1, // 每页多少条
      pageSize: 15, //每页显示个数
      pageTotal: ref(""),
      dataTotal: ref(""),
      centerDialogVisible: false,
      dialogVisibleParameter: false,
      form: {
        sub_name: "",
        shelf_id: "",
        slot_id: "",
        port_id: "",
        voa_vaule: "",
      },
      Download_FileAdress:
        "%E5%8F%AF%E8%B0%83%E5%85%89%E8%A1%B0%E7%8E%B0%E7%BD%91%E9%85%8D%E7%BD%AE%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BF.xlsx",
      all_sub_name_array: [],
      // all_board_model_array: [],

      filters_sub_name_tag: {},
      isAuthen: false,
      // filters_board_model_tag: {},
    };
  },
  methods: {
    refreshTable(data) {
      this.tableData = data.myArray;
      this.pageTotal = data.page_size;
      this.pageCount = data.page_count;
      this.dataTotal = data.total;
      this.labelSave = data.is_calculating ? "计算中" : "保存";
      this.isBtnSaveDisable = data.is_calculating;
      this.setFiltersArray(data.myArray);
    },
    async setFiltersArray(data) {
      await data.forEach((item) => {
        if (!this.all_sub_name_array.includes(item.sub_name)) {
          this.all_sub_name_array.push(item.sub_name);
        }
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
      let data = {
        page_index_begin: 0,
        page_size: this.pageSize,
      };
      getConfig(data).then((res) => {
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
    changePage() {
      let obj = {
        page_index_begin: this.currentPage,
        page_size: this.pageSize,
        filter: [this.filters_sub_name_tag],
      };
      getConfig(obj).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    editRow(data) {
      updateConfig(data).then((res) => {
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
        op_module: logModuleMenu.AODNC,
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
      updateStandardCalculate(data1).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    handleFilterChange(filterObj) {
      if (filterObj.sub_name != null) {
        this.filters_sub_name_tag = {
          name: "sub_name",
          values: filterObj.sub_name,
        };
      }
      this.changePage();
    },
    getFilter() {
      let _this = this;
      getConfigFilter().then((res) => {
        if (res.code == 200) {
          _this.setFiltersArray(res.data);
        }
      });
    },
    beforeUpload(file) {
      var testmsg = file.name.substring(file.name.lastIndexOf(".") + 1);
      const extension = testmsg === "xlsx";
      if (!extension) {
        ElMessage({
          type: "error",
          message: "上传文件只能是.xlsx格式!",
          offset: 100,
        });
      }
      return extension;
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
  },
  mounted() {
    this.init();
    this.getAuthen();
  },
  created() {
    this.Download_FileAdress =
      process.env.VUE_APP_Download_FileAdress + this.Download_FileAdress;
    this.getFilter();
  },
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
  padding: 0 20px;
  width: 100%;
  height: 40px;
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