<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-13 15:10:59
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-07 16:13:17
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\permissionsManage\userManage\userManage.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="main">
    <div class="body">
      <div class="content">
        <!-- <div class="tableDataTools"></div> -->
        <div class="tableData">
          <el-table
            v-loading="loading"
            :data="
              tableUser.slice(
                (currentPage - 1) * pageSize,
                currentPage * pageSize
              )
            "
            stripe
            :row-style="{ height: '0' }"
            :header-cell-style="{
              'text-align': 'center',
              background: '#F3F5FA',
              padding: '15px 0',
            }"
            height="100%"
            :cell-style="{ 'text-align': 'center', padding: '10px' }"
          >
            <el-table-column type="index" label="序号" width="100px" />
            <el-table-column prop="user_name" label="登录账号" width="200" />
            <el-table-column align="center" label="操作">
              <template #default="scope">
                <div class="operationGroup">
                  <button
                    class="ToolBtn"
                    @click="EditSelect(scope.$index, scope.row)"
                  >
                    权限配置
                  </button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-pagination
          :hide-on-single-page="tableUser.length <= pageSize"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[100, 200, 300, 400]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="tableUser.length"
          class="paging"
        >
        </el-pagination>
      </div>
    </div>
  </div>
  <el-dialog
    v-model="centerDialogVisible"
    title="权限配置"
    width="650px"
    :close-on-click-modal="false"
  >
    <el-form
      :model="permData"
      label-width="100px"
      label-position="top"
      ref="editPermForm"
    >
      <el-form-item label="用户" prop="user_name">
        <el-input
          disabled
          placeholder="当前用户"
          v-model="permData.user_name"
        />
      </el-form-item>
      <el-form-item label="权限">
        <el-checkbox
          v-model="permData.can_add_standrad_param"
          label="参数导入权限"
          size="large"
          prop="can_add_standrad_param"
        />
        <el-checkbox
          v-model="permData.can_add_user"
          label="操作用户权限"
          size="large"
          prop="can_add_user"
        />
        <el-checkbox
          v-model="permData.can_modify_base_line"
          label="修改基准值权限"
          size="large"
          prop="can_modify_base_line"
        />
        <el-checkbox
          v-model="permData.can_modify_prems"
          label="修改权限表权限"
          size="large"
          prop="can_modify_prems"
        />
        <el-checkbox
          v-model="permData.can_output_hiddentrouble"
          label="导出隐患数据权限"
          size="large"
          prop="can_output_hiddentrouble"
        />
        <el-checkbox
          v-model="permData.can_save_topo_position"
          label="保存Topo默认设置"
          size="large"
          prop="can_save_topo_position"
        />
        <el-checkbox
          v-model="permData.can_set_channel_num"
          label="配置波道数权限"
          size="large"
          prop="can_set_channel_num"
        />
        <el-checkbox
          v-model="permData.can_threshold_setting"
          label="修改门限权限"
          size="large"
          prop="can_threshold_setting"
        />
      </el-form-item>
      <el-form-item label="区域配置" prop="zone_authenArr">
        <el-cascader
          style="width: 100%"
          v-model="permData.zone_authenArr"
          :options="options.optionArr"
          :props="props"
          collapse-tags
          clearable
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="cancel" @click="centerDialogVisible = false"
          >取消</el-button
        >
        <el-button class="confirm" type="primary" @click="confirmMessage"
          >保存</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { getUserName, getToken } from "@/config/UserInfomation";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  getCity,
  getPerm,
  setPerm,
  setLog,
  logModuleMenu,
  operationMenu,
} from "@/api/WDM-OTN/http";

export default {
  data() {
    return {
      loading: true,
      centerDialogVisible: false,
      currentPage: 1, // 每页多少条
      pageSize: 20, //每页显示个数
      props: {
        multiple: true,
      },
      tableUser: [],
      optionsArr: [
        {
          value: 1,
          label: "河北省",
          children: [{ value: 2, label: "全省" }],
        },
        {
          value: 3,
          label: "省干",
          children: [
            {
              value: 4,
              label: "全省",
            },
          ],
        },
        {
          value: 5,
          label: "石家庄市",
          children: [
            { value: 6, label: "长安区" },
            { value: 7, label: "裕华区" },
            { value: 8, label: "桥西区" },
            { value: 9, label: "新乐市" },
            { value: 10, label: "藁城市" },
            { value: 11, label: "新华区" },
            { value: 12, label: "赵县" },
            { value: 13, label: "深泽县" },
            { value: 14, label: "栾城县" },
            { value: 15, label: "灵寿县" },
            { value: 16, label: "平山县" },
            { value: 17, label: "元氏县" },
            { value: 18, label: "晋州市" },
            { value: 19, label: "无极县" },
            { value: 20, label: "赞皇县" },
            { value: 21, label: "辛集市" },
            { value: 22, label: "高邑县" },
            { value: 23, label: "井陉县" },
            { value: 24, label: "鹿泉区" },
            { value: 25, label: "行唐县" },
            { value: 26, label: "井陉矿区" },
            { value: 27, label: "正定县" },
          ],
        },
        {
          value: 28,
          label: "唐山市",
          children: [
            { value: 29, label: "迁安市" },
            { value: 30, label: "遵化市" },
            { value: 31, label: "路北区" },
            { value: 32, label: "路南区" },
            { value: 33, label: "丰润区" },
            { value: 34, label: "迁西县" },
            { value: 35, label: "滦南县" },
            { value: 36, label: "玉田县" },
            { value: 37, label: "曹妃甸区" },
            { value: 38, label: "乐亭县" },
            { value: 39, label: "滦县" },
            { value: 40, label: "开平区" },
            { value: 41, label: "丰南区" },
            { value: 42, label: "古冶区" },
          ],
        },
        {
          value: 43,
          label: "秦皇岛市",
          children: [
            { value: 44, label: "卢龙县" },
            { value: 45, label: "抚宁县" },
            { value: 46, label: "昌黎县" },
            { value: 47, label: "青龙满族自治县" },
            { value: 48, label: "北戴河区" },
            { value: 49, label: "山海关区" },
            { value: 50, label: "海港区" },
          ],
        },
        {
          value: 51,
          label: "邯郸市",
          children: [
            { value: 52, label: "涉县" },
            { value: 53, label: "鸡泽县" },
            { value: 54, label: "邯郸县" },
            { value: 55, label: "峰峰矿区" },
            { value: 56, label: "临漳县" },
            { value: 57, label: "成安县" },
            { value: 58, label: "曲周县" },
            { value: 59, label: "肥乡县" },
            { value: 60, label: "大名县" },
            { value: 61, label: "磁县" },
            { value: 62, label: "武安市" },
            { value: 63, label: "魏县" },
            { value: 64, label: "广平县" },
            { value: 65, label: "馆陶县" },
            { value: 66, label: "永年县" },
            { value: 67, label: "邱县" },
            { value: 68, label: "邯山区" },
            { value: 69, label: "丛台区" },
            { value: 70, label: "复兴区" },
          ],
        },
        {
          value: 71,
          label: "邯郸市",
          children: [
            { value: 72, label: "南和县" },
            { value: 73, label: "柏乡县" },
            { value: 74, label: "巨鹿县" },
            { value: 75, label: "清河县" },
            { value: 76, label: "邢台县" },
            { value: 77, label: "隆尧县" },
            { value: 78, label: "广宗县" },
            { value: 79, label: "任县" },
            { value: 80, label: "威县" },
            { value: 81, label: "内丘县" },
            { value: 82, label: "新河县" },
            { value: 83, label: "宁晋县" },
            { value: 84, label: "临城县" },
            { value: 85, label: "沙河市" },
            { value: 86, label: "临西县" },
            { value: 87, label: "平乡县" },
            { value: 88, label: "南宫市" },
          ],
        },
        {
          value: 89,
          label: "桥东区",
          children: [
            { value: 90, label: "保定市" },
            { value: 91, label: "望都县" },
            { value: 92, label: "涞水县" },
            { value: 93, label: "涞源县" },
            { value: 94, label: "涿州市" },
            { value: 95, label: "曲阳县" },
            { value: 96, label: "定州市" },
            { value: 97, label: "徐水县" },
            { value: 98, label: "安国市" },
            { value: 99, label: "满城县" },
            { value: 100, label: "清苑县" },
            { value: 101, label: "唐县" },
            { value: 102, label: "北市区" },
            { value: 103, label: "顺平县" },
            { value: 104, label: "蠡县" },
            { value: 105, label: "易县" },
            { value: 106, label: "高阳县" },
            { value: 107, label: "南市区" },
            { value: 108, label: "阜平县" },
            { value: 109, label: "博野县" },
            { value: 110, label: "高碑店市" },
            { value: 111, label: "新市区" },
            { value: 112, label: "定兴县" },
          ],
        },
        {
          value: 113,
          label: "承德市",
          children: [
            { value: 114, label: "丰宁满族自治县" },
            { value: 115, label: "滦平县" },
            { value: 116, label: "平泉县" },
            { value: 117, label: "鹰手营子矿区" },
            { value: 118, label: "兴隆县" },
            { value: 119, label: "承德县" },
            { value: 120, label: "隆化县" },
            { value: 121, label: "宽城满族自治县" },
            { value: 122, label: "围场满族蒙古族自治县" },
            { value: 123, label: "双桥区" },
            { value: 124, label: "双滦区" },
          ],
        },
        {
          value: 125,
          label: "沧州市",
          children: [
            { value: 126, label: "任丘市" },
            { value: 127, label: "青县" },
            { value: 128, label: "东光县" },
            { value: 129, label: "河间市" },
            { value: 130, label: "肃宁县" },
            { value: 131, label: "海兴县" },
            { value: 132, label: "献县" },
            { value: 133, label: "吴桥县" },
            { value: 134, label: "黄骅市" },
            { value: 135, label: "沧县" },
            { value: 136, label: "盐山县" },
            { value: 137, label: "南皮县" },
            { value: 138, label: "泊头市" },
            { value: 139, label: "孟村回族自治县" },
            { value: 140, label: "运河区" },
          ],
        },
        {
          value: 141,
          label: "廊坊市",
          children: [
            { value: 142, label: "大城县" },
            { value: 143, label: "燕郊" },
            { value: 144, label: "三河市" },
            { value: 145, label: "胜芳" },
            { value: 146, label: "霸州市" },
            { value: 147, label: "大厂回族自治县" },
            { value: 148, label: "香河县" },
            { value: 149, label: "文安县" },
            { value: 150, label: "固安县" },
            { value: 151, label: "永清县" },
            { value: 152, label: "安次区" },
            { value: 153, label: "广阳区" },
          ],
        },
        {
          value: 154,
          label: "衡水市",
          children: [
            { value: 155, label: "安平县" },
            { value: 156, label: "冀州市" },
            { value: 157, label: "景县" },
            { value: 158, label: "深州市" },
            { value: 159, label: "饶阳县" },
            { value: 160, label: "故城县" },
            { value: 161, label: "武强县" },
            { value: 162, label: "阜城县" },
            { value: 163, label: "枣强县" },
            { value: 164, label: "武邑县" },
            { value: 165, label: "桃城区" },
            { value: 166, label: "安新县" },
            { value: 167, label: "雄县" },
            { value: 168, label: "容城县" },
          ],
        },
        {
          value: 169,
          label: "张家口市",
          children: [
            { value: 170, label: "沽源县" },
            { value: 171, label: "怀来县" },
            { value: 172, label: "万全县" },
            { value: 173, label: "康保县" },
            { value: 174, label: "宣化区" },
            { value: 175, label: "怀安县" },
            { value: 176, label: "张北县" },
            { value: 177, label: "涿鹿县" },
            { value: 178, label: "尚义县" },
            { value: 179, label: "下花园区" },
            { value: 180, label: "蔚县" },
            { value: 181, label: "阳原县" },
            { value: 182, label: "崇礼县" },
            { value: 183, label: "赤城县" },
            { value: 184, label: "桥东区" },
            { value: 185, label: "桥西区" },
          ],
        },
      ],
      options: {
        optionArr: reactive([]),
        modelArr: [],
      },
      permData: {
        user_name: "",
        last_update_person: "",
        zone_authen: "",
        zone_authenArr: [],
        can_add_standrad_param: false,
        can_modify_base_line: false,
        can_threshold_setting: false,
        can_add_user: false,
        can_modify_prems: false,
        can_output_hiddentrouble: false,
        can_save_topo_position: false,
        can_set_channel_num: false,
      },
    };
  },
  watch: {
    centerDialogVisible(val) {
      if (!val) {
        let _this = this;
        _this.$refs.editPermForm.resetFields(); // 清空表单
        _this.permData.zone_authenArr = [];
      }
    },
  },
  created() {
    this.getUserInfo();
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
    getUserInfo() {
      let _this = this;
      _this.loading = true;
      getPerm().then((res) => {
        if (res.code == 200) {
          _this.tableUser = res.data;
          _this.loading = false;
        }
      });
    },
    EditSelect(index, val) {
      let _this = this;
      _this.getPerm();
      _this.permData = JSON.parse(JSON.stringify(val));
      const zonArr = JSON.parse(_this.permData.zone_authen);
      const zone_authenArr = [];
      zonArr.forEach((item) => {
        const city = {
          label: item.name,
          value: item.name,
          children: [],
        };
        zone_authenArr.push(item.name);
      });
      _this.permData.zone_authenArr = zone_authenArr;
      _this.centerDialogVisible = true;
    },
    confirmMessage() {
      ElMessageBox.confirm("确定保存此次更改吗?", "权限配置", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        showClose: false,
        // draggable: true,
        lockScroll: true,
        closeOnClickModal: false,
      })
        .then(() => {
          this.confirmSelect();
        })
        .catch((err) => {});
    },
    confirmSelect() {
      let _this = this;
      let jsonData = [];
      if (
        Array.isArray(_this.permData.zone_authenArr) &&
        _this.permData.zone_authenArr.length > 0
      ) {
        _this.permData.zone_authenArr.forEach((item, index) => {
          const city = {
            name: item[0],
            children: [],
          };
          jsonData.push(city);
        });
      }
      _this.permData.zone_authen = JSON.stringify(jsonData);
      _this.permData.last_update_person = getUserName();
      _this.setPerm();
    },
    getPerm() {
      let _this = this;
      getCity().then((res) => {
        if (res.code == 200) {
          _this.ComputedCityPerm(res.data);
        }
      });
    },
    ComputedCityPerm(res) {
      let _this = this;
      let data = [];
      data.push(res);
      let options = [];
      for (let item of data[0]) {
        let city = {
          label: item.name,
          value: item.name,
          children: [],
        };
        options.push(city);
      }
      _this.options.optionArr = options;
    },
    setPerm() {
      let _this = this;
      let data = _this.permData;
      setPerm(data).then((res) => {
        const result = res;
        if (result.code == 200 && result.data) {
          ElMessage({
            type: "success",
            message: "权限配置成功",
            offset: 200,
          });
          _this.centerDialogVisible = false;
          _this.getUserInfo();
          const user = getCookie("usn");
          setLog({
            op_module: logModuleMenu.RM,
            op_user: user,
            op_behavior: user + operationMenu.update,
            op_time: NowDate(),
          });
        }
      });
    },
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
  padding-right: 20px;
  flex-direction: column;
}

.main > .header {
  padding: 10px 0px 10px 10px;
  width: 100%;
  height: 100px;
}

.main > .header > .searchTemplate {
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: var(--box-shadow);
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.searchTemplate .el-form {
  padding: 10px 20px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}

.searchTemplate .el-form .el-form-item {
  display: flex;
  align-items: center;
}

.el-form-item {
  margin: 0;
}

.main > .body {
  width: 100%;
  height: calc(100%);
  padding: 10px 0px 10px 10px;
}

.main > .body > .content {
  padding: 20px;
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: var(--box-shadow);
}

.tableDataTools {
  width: 50%;
  padding: 20px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}

.tableDataTools .add {
  padding: 0 20px 0px 20px;
  border: 1px solid transparent;
  outline: none;
  background-color: #4c64f2;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tableDataTools .batchDel {
  padding: 0 20px 0px 20px;
  border: 1px solid var(--theme-color);
  outline: none;
  background-color: var(--white);
  color: var(--theme-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tableData {
  /* padding: 0 20px 20px 20px; */
  width: 100%;
  height: calc(100% - 40px);
  margin: auto;
}

.operationGroup {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.operationGroup .ToolBtn {
  border: none;
  background: transparent;
  padding: 0 10px;
  color: var(--theme-color);
  cursor: pointer;
}

.cancel,
.cancel:hover,
.cancel:active,
.cancel:focus {
  padding: 0 20px 0px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--theme-color);
  background-color: var(--white);
  border: 1px solid var(--theme-color);
  outline: none;
}

.confirm,
.confirm:hover,
.confirm:active,
.confirm:focus {
  padding: 0 20px 0px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background-color: var(--theme-color);
  border: 1px solid transparent;
  outline: none;
}
</style>

<style>
.dialog-footer button:first-child {
  margin-right: 10px;
}

.columndiv {
  flex-direction: column;
}

.divwushi {
  width: 40%;
}

.example-block {
  margin: 1rem;
}
.example-demonstration {
  margin: 1rem;
}
</style>