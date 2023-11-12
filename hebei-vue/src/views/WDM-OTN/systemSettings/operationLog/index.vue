<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-13 15:11:09
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-08 16:02:05
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\operationLog\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="main">
    <div class="logSearch">
      <div class="logSearchTemplate">
        <el-form :inline="true" class="userSearch">
          <el-form-item label="操作时间">
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
          <el-form-item label="操作人">
            <el-input placeholder="操作人" v-model="serachLogData.op_user" />
          </el-form-item>
          <el-form-item>
            <el-button class="btnSearch" @click="onSubmit">查询</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="body">
      <div class="content">
        <div class="logTableData">
          <el-table
            v-loading="loading"
            :data="
              logTableData.slice(
                (currentPage - 1) * pageSize,
                currentPage * pageSize
              )
            "
            stripe
            :header-cell-style="{
              'text-align': 'center',
              background: '#F3F5FA',
              padding: '5px 0',
            }"
            :cell-style="{ 'text-align': 'center', padding: '20px 0' }"
            height="100%"
          >
            <el-table-column prop="op_time" label="操作时间" width="250px" />
            <el-table-column prop="op_module" label="操作模块" width="300px" />
            <el-table-column prop="op_user" label="操作人" width="300px" />
            <el-table-column prop="op_behavior" label="操作行为" />
          </el-table>
        </div>
        <el-pagination
          :hide-on-single-page="logTableData.length <= pageSize"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[100, 200, 300, 400]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="logTableData.length"
          class="paging"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import {
  FormatSearchStartTime,
  FormatSearchEndTime,
} from "@/config/formatTime";
import { getLog } from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      loading: true,
      currentPage: 1, // 每页多少条
      pageSize: 10, //每页显示个数
      logTableData: [],
      serachLogData: {
        startTime: "",
        endTime: "",
        op_user: null,
      },
      serachData: ref({
        op_timeArr: [],
      }),
    };
  },
  watch: {
    "serachData.op_timeArr"(val) {
      let _this = this;
      if (val == null || val == undefined) {
        _this.serachLogData.startTime = "";
        _this.serachLogData.endTime = "";
      }
    },
  },
  created() {
    this.init();
  },
  mounted() {},
  methods: {
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
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
        currentPage: this.currentPage,
        pageSize: this.pageSize,
      };
      let currentPage = obj.currentPage;
      let pageSize = obj.pageSize;
      let data = JSON.parse(JSON.stringify(this.tableDataAll));
      let begin = (currentPage - 1) * pageSize;
      let end = currentPage * pageSize;
      this.nowPageList = data.slice(begin, end);
    },
    init() {
      let _this = this;
      _this.loading = true;
      getLog(_this.serachLogData).then((res) => {
        if (res.code == 200) {
          _this.logTableData = res.data;
          _this.loading = false;
        }
      });
    },
    onSubmit() {
      let _this = this;
      const timeselected = _this.serachData.op_timeArr;
      if (Array.isArray(timeselected) && timeselected.length > 0) {
        _this.serachLogData.startTime = FormatSearchStartTime(timeselected[0]);
        _this.serachLogData.endTime = FormatSearchEndTime(timeselected[1]);
      }
      _this.init();
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/plugins/styles/WDM-OTN/systemSettings/operationLog/index.scss";
</style>