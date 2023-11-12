<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-18 16:48:28
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-08 16:43:21
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\dataImport\adjustableDimLiveNetConfiguration\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <!-- 现网光放板卡信息 -->
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
        <el-link
          target="_blank"
          href="http://61.163.104.139:12003/%E7%8E%B0%E7%BD%91%E5%85%89%E6%94%BE%E6%9D%BF%E5%8D%A1%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BF.xlsx"
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
          label="子网元名称"
          column-key="sub_name"
          :filters="getFilters(all_sub_name_array)"
        />
        <el-table-column label="光放板子架" prop="shelf_id" />
        <el-table-column label="光放板槽位" prop="slot_id" />
        <el-table-column
          label="板卡类型"
          column-key="board_model"
          :filters="getFilters(all_board_model_array)"
          prop="board_model"
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
  <!-- 参数上传 -->
  <el-dialog v-model="centerDialogVisible" title="参数上传" width="30%" center>
    <el-upload
      class="upload-demo"
      drag
      action="/paramsApi/oa_board_type/upload_file"
      multiple
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
      <el-form-item label="板卡类型">
        <div class="demo-input-size">
          <el-input
            v-model="form.board_model"
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
  getTypeFilter,
  updateTypeCalculate,
  addBoardType,
  updateBoard,
  getBoard,
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
      labelSave: ref(""),
      isBtnSaveDisable: false,
      form: {
        sub_name: "",
        shelf_id: 0,
        slot_id: 0,
        board_model: 0,
      },
      Download_FileAdress:
        "%E7%8E%B0%E7%BD%91%E5%85%89%E6%94%BE%E6%9D%BF%E5%8D%A1%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BF.xlsx",
      all_sub_name_array: [],
      all_board_model_array: [],

      filters_sub_name_tag: {},
      filters_board_model_tag: {},
      isAuthen: false,
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
    },
    setFiltersArray(data) {
      new Promise(() => {
        data.forEach((item) => {
          if (!this.all_sub_name_array.includes(item.sub_name)) {
            this.all_sub_name_array.push(item.sub_name);
          }
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
      let data = {
        page_index_begin: 0,
        page_size: this.pageSize,
      };
      getBoard(data).then((res) => {
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
        filter: [this.filters_sub_name_tag, this.filters_board_model_tag],
      };
      getBoard(obj).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    editRow(data) {
      updateBoard(data).then((res) => {
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
      addBoardType(this.form).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
      const user = getCookie("usn");
      setLog({
        op_module: logModuleMenu.IATODBOTLN,
        op_user: user,
        op_behavior: user + operationMenu.add,
        op_time: NowDate(),
      });
      this.dialogVisibleParameter = false;
    },
    handleFilterChange(filterObj) {
      if (filterObj.sub_name != null) {
        this.filters_sub_name_tag = {
          name: "sub_name",
          values: filterObj.sub_name,
        };
      }
      if (filterObj.board_model != null) {
        this.filters_board_model_tag = {
          name: "board_model",
          values: filterObj.board_model,
        };
      }
      this.changePage();
    },
    recountParameter() {
      // let tableName = "nowNetPutCardLightInformation";
      let data1 = {
        name: "现网光放板卡信息",
      };
      updateTypeCalculate(data1).then((res) => {
        if (res.code == 200) {
          this.refreshTable(res.data);
        }
      });
    },
    getFilter() {
      let _this = this;
      getTypeFilter().then((res) => {
        if (res.code == 200) {
          const result = res;
          _this.setFiltersArray(result.data);
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
  }, //methods
  mounted() {
    this.init();
    this.getAuthen();
  },
  created() {
    this.Download_FileAdress =
      process.env.VUE_APP_Download_FileAdress + this.Download_FileAdress;
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