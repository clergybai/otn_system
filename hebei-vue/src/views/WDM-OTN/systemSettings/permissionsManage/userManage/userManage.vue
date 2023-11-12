<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-13 15:10:59
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-08 16:08:15
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\permissionsManage\userManage\userManage.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="main">
    <div class="header">
      <div class="searchTemplate" v-loading="loading">
        <el-form :inline="true" class="demo-form-inline userSearch">
          <el-form-item label="登录账号">
            <el-input
              placeholder="请输入账号"
              v-model="searchUserData.userName"
            />
          </el-form-item>
          <el-form-item label="手机号码">
            <el-input
              placeholder="请输入手机号码"
              @keyup="
                searchUserData.phone = searchUserData.phone.replace(
                  /[^\d]/g,
                  ''
                )
              "
              v-model="searchUserData.phone"
            />
          </el-form-item>
          <el-form-item label="用户状态">
            <el-select v-model="searchUserData.state" placeholder="请选择">
              <el-option label="所有" value="all" />
              <el-option label="正常" value="1" />
              <el-option label="已停用" value="0" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button class="btnSearch" @click="getUserInfo">查询</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="body">
      <div class="content" v-loading="loading">
        <div class="tableDataTools">
          <!-- <el-button class="add" @click="addUser">新增</el-button> -->
          <el-button class="add" @click="addUser">新增</el-button>
          <!-- <el-button class="batchDel" @click="RemoveSelectAll"
            >批量删除</el-button
          > -->
        </div>
        <div class="tableData">
          <el-table
            :data="
              tableUser.slice(
                (currentPage - 1) * pageSize,
                currentPage * pageSize
              )
            "
            @selection-change="selectionChangeHandle"
            stripe
            :header-cell-style="{
              'text-align': 'center',
              background: '#F3F5FA',
              padding: '10px 0',
            }"
            height="100%"
            :cell-style="{ 'text-align': 'center', padding: '20px 0' }"
          >
            <!-- <el-table-column type="selection" /> -->
            <el-table-column type="index" label="序号" width="100px" />
            <el-table-column prop="user_name" label="登录账号" />
            <el-table-column prop="cellphone_num" label="手机号码" />
            <el-table-column prop="role" label="用户角色">
              <template #default="scope">
                <template v-if="scope.row.role == 9">
                  <span class="cardLabel general">超级用户</span>
                </template>
                <template v-else>
                  <span>普通用户</span>
                </template>
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="用户状态">
              <template #default="scope">
                <template v-if="scope.row.is_active == 1">
                  <el-icon :size="20" color="#67C23A">
                    <CircleCheckFilled />
                  </el-icon>
                </template>
                <template v-else>
                  <el-icon :size="20" color="#F56C6C">
                    <CircleCloseFilled />
                  </el-icon>
                </template>
              </template>
            </el-table-column>
            <el-table-column prop="update_time" label="操作时间" />
            <el-table-column label="操作">
              <template #default="scope">
                <template v-if="scope.row.is_active == 1">
                  <div class="operationGroup">
                    <button
                      class="ToolBtn"
                      @click="EditSelect(scope.$index, scope.row)"
                    >
                      编辑
                    </button>
                    <button
                      v-show="scope.row.name != 'admin'"
                      class="ToolBtn"
                      @click="RemoveSelect(scope.$index, scope.row)"
                    >
                      删除
                    </button>
                    <button
                      class="ToolBtn"
                      @click="editPassword(scope.$index, scope.row)"
                    >
                      修改密码
                    </button>
                  </div>
                </template>
                <template v-else>
                  <div class="operationGroup">
                    <button
                      class="ToolBtn"
                      @click="Restore(scope.$index, scope.row)"
                    >
                      恢复
                    </button>
                  </div>
                </template>
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

  <!-- 新增用户 -->
  <el-dialog
    v-model="dialogVisibleUser"
    :title="UserFormTitle"
    width="900px"
    :close-on-click-modal="false"
  >
    <el-form
      label-width="100px"
      label-position="right"
      :rules="UserRules"
      :model="UserForm"
      ref="UserForm"
    >
      <el-form-item label="用户名" prop="user_name">
        <el-input
          placeholder="用户名"
          v-model="UserForm.user_name"
          :disabled="UserFormTitle == '编辑用户'"
        />
      </el-form-item>
      <template v-if="UserFormTitle === '新增用户'">
        <el-form-item label="密码" prop="salt">
          <el-input
            placeholder="密码"
            type="password"
            v-model="UserForm.salt"
          />
        </el-form-item>
      </template>
      <el-form-item label="真实姓名" prop="name">
        <el-input placeholder="真实姓名" v-model="UserForm.name" />
      </el-form-item>
      <el-form-item label="邮箱地址" prop="user_email">
        <el-input placeholder="邮箱地址" v-model="UserForm.user_email" />
      </el-form-item>
      <el-form-item label="手机号" prop="cellphone_num">
        <el-input placeholder="手机号" v-model="UserForm.cellphone_num" />
      </el-form-item>
      <el-form-item label="部门" prop="department">
        <el-input placeholder="部门" v-model="UserForm.department" />
      </el-form-item>
      <el-form-item label="职位" prop="post">
        <el-input placeholder="职位" v-model="UserForm.post" />
      </el-form-item>
      <el-form-item label="备注" prop="remark">
        <el-input
          placeholder="备注"
          v-model="UserForm.remark"
          :autosize="{ minRows: 2, maxRows: 6 }"
          type="textarea"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="cancel" @click="dialogVisibleUser = false"
          >取消</el-button
        >
        <el-button
          class="confirm"
          type="primary"
          @click="confirmMessage(UserFormTitle)"
          >保存</el-button
        >
      </span>
    </template>
  </el-dialog>

  <!-- 修改密码 -->
  <el-dialog
    v-model="dialogVisibleResetPasswords"
    title="修改密码"
    width="650px"
    :close-on-click-modal="false"
  >
    <el-form
      label-width="100px"
      label-position="right"
      :rules="editRules"
      :model="updatePwdData"
      ref="updatePwdData"
    >
      <el-form-item label="账号" prop="userName">
        <el-input
          disabled
          placeholder="获取异常"
          v-model="updatePwdData.userName"
        />
      </el-form-item>
      <el-form-item label="新密码" prop="salt">
        <el-input
          placeholder="新密码"
          type="password"
          v-model="updatePwdData.salt"
        />
      </el-form-item>
      <el-form-item label="确认密码" prop="resalt">
        <el-input
          placeholder="确认密码和新密码保持一致"
          type="password"
          v-model="updatePwdData.resalt"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button class="cancel" @click="dialogVisibleResetPasswords = false"
          >取消</el-button
        >
        <el-button
          class="confirm"
          type="primary"
          @click="confirmMessage('修改密码')"
          >保存</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { ElMessage, ElMessageBox } from "element-plus";
import { getUserName, getToken } from "@/config/UserInfomation.js";
import { getCookie } from "@/config/Cookies";
import { NowDate } from "@/config/formatTime";
import {
  restoreUser,
  updatePwd,
  delUser,
  getUser,
  addUser,
  editUser,
  setLog,
  logModuleMenu,
  operationMenu,
} from "@/api/WDM-OTN/http";
export default {
  data() {
    //确认密码校验
    var checkRePassword = (rule, value, callback) => {
      if (this.updatePwdData.salt === "") {
        callback(new Error("请输入新密码"));
      } else if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.updatePwdData.salt) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      loading: true,
      currentPage: 1, // 每页多少条
      pageSize: 10, //每页显示个数
      tableUser: [],
      searchUserData: {
        userName: null,
        phone: null,
        state: null,
        token: null,
      },
      selectionData: [],
      dialogVisibleUser: false,
      dialogVisibleResetPasswords: false,
      UserFormTitle: "",
      UserForm: {
        user_name: "",
        name: "",
        salt: "",
        user_email: "",
        cellphone_num: "",
        city: "0",
        role: "0",
        department: "",
        post: "",
        remark: "",
        is_active: "1",
        create_time: "",
        update_time: "",
        last_update_person: "",
      },
      updatePwdData: {
        userName: "",
        salt: "",
        resalt: "",
      },
      UserRules: {
        user_name: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        // name: [{ required: true, message: "请输入真实姓名", trigger: "blur" }],
        salt: [{ required: true, message: "请输入密码", trigger: "blur" }],
        user_email: [
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"],
          },
        ],
        cellphone_num: [
          {
            pattern:
              /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/,
            message: "请输入正确的手机号",
          },
        ],
      },
      editRules: {
        salt: [{ required: true, message: "请输入密码", trigger: "blur" }],
        resalt: [
          { required: true, message: "请再次输入密码", trigger: "blur" },
          { validator: checkRePassword, trigger: "blur" },
        ],
      },
    };
  },
  watch: {
    dialogVisibleUser(val) {
      let _this = this;
      if (!val) {
        _this.$refs.UserForm.resetFields(); // 清空表单
        _this.$refs.UserForm.clearValidate(); // 清空表单
      } else {
        _this.UserForm.last_update_person = getUserName();
      }
    },
    dialogVisibleResetPasswords(val) {
      let _this = this;
      if (!val) {
        _this.$refs.updatePwdData.resetFields(); // 清空表单
        _this.$refs.updatePwdData.clearValidate(); // 清空表单
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
      _this.searchUserData.token = getToken();
      getUser(_this.searchUserData).then((res) => {
        if (res.code == 200) {
          _this.loading = false;
          _this.tableUser = res.data;
        }
      });
    },
    EditSelect(index, val) {
      let _this = this;
      _this.UserFormTitle = "编辑用户";
      _this.$nextTick(() => Object.assign(_this.UserForm, val));
      _this.dialogVisibleUser = true;
    },
    RemoveSelect(index, val) {
      let _this = this;
      ElMessageBox.confirm("确定要删除该用户吗?", "删除用户", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "error",
        showClose: false,
        // draggable: true,
        lockScroll: true,
        closeOnClickModal: false,
      })
        .then(() => {
          if (val.name != "admin") {
            _this.UserForm.user_name = val.user_name;
            _this.UserForm.last_update_person = getUserName();
            _this.operationRemoveUser();
          } else {
            ElMessage({
              type: "error",
              message: "删除失败,不可删除管理员!!!",
              offset: 200,
            });
          }
        })
        .catch(() => {});
    },
    ResetSelect(index, val) {
      ElMessageBox.confirm("确定要重置该用户密码吗?", "重置密码", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        showClose: false,
        // draggable: true,
        lockScroll: true,
        closeOnClickModal: false,
      })
        .then(() => {
          if (val.name != "admin") {
            ElMessage({
              type: "success",
              message: "重置密码成功",
              offset: 200,
            });
          } else {
            ElMessage({
              type: "error",
              message: "不可重置管理员密码!!!",
              offset: 200,
            });
          }
        })
        .catch(() => {});
    },
    RemoveSelectAll() {
      if (this.selectionData.length <= 0) {
        ElMessage({
          showClose: true,
          message: "请选择行！",
          // center: true,
          grouping: true,
          type: "error",
          duration: "2000",
          offset: 200,
        });
      } else {
        ElMessageBox.confirm("确定要删除这些用户吗?", "删除用户", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          showClose: false,
          // draggable: true,
          lockScroll: true,
          closeOnClickModal: false,
        });
      }
    },
    selectionChangeHandle(val) {
      this.selectionData = val;
    },
    editPassword(index, val) {
      let _this = this;
      _this.dialogVisibleResetPasswords = true;
      _this.updatePwdData.userName = val.user_name;
    },
    addUser() {
      let _this = this;
      _this.UserFormTitle = "新增用户";
      _this.dialogVisibleUser = true;
    },
    confirmMessage(title) {
      let _this = this;
      if (_this.dialogVisibleUser) {
        _this.$refs.UserForm.validate((value) => {
          if (value) {
            ElMessageBox.confirm("确定要保存更改吗?", title, {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
              showClose: false,
              lockScroll: true,
              closeOnClickModal: false,
            }).then((res) => {
              switch (_this.UserFormTitle) {
                case "编辑用户":
                  _this.operationEditUser();
                  break;
                case "新增用户":
                  _this.operationAddUser();
                  break;
              }
            });
          }
        });
      } else if (_this.dialogVisibleResetPasswords) {
        _this.$refs.updatePwdData.validate((value) => {
          if (value) {
            ElMessageBox.confirm("确定要保存更改吗?", title, {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
              showClose: false,
              lockScroll: true,
              closeOnClickModal: false,
            })
              .then((res) => {
                _this.updatePwd();
              })
              .catch((res) => {});
          }
        });
      }
    },
    operationAddUser() {
      let _this = this;
      addUser(_this.UserForm).then((res) => {
        if (res.code != 200) return;
        if (res.data === 1) {
          ElMessage({
            type: "success",
            message: "添加成功",
            offset: 200,
            duration: 1500,
          });
          _this.getUserInfo();
          const user = getCookie("usn");
          setLog({
            op_module: logModuleMenu.UM,
            op_user: user,
            op_behavior: user + operationMenu.add,
            op_time: NowDate(),
          });
        } else if (res.data === 0) {
          ElMessage({
            type: "error",
            message: "添加失败",
            duration: 1500,
          });
        } else {
          ElMessage({
            type: "warning",
            message: "用户已存在",
            offset: 200,
            duration: 1500,
          });
        }
        _this.dialogVisibleUser = false;
      });
    },
    operationEditUser() {
      let _this = this;
      editUser(_this.UserForm).then((res) => {
        if (res.code != 200) return;
        if (res.data) {
          ElMessage({
            type: "success",
            message: "修改成功",
            offset: 200,
            duration: 1500,
          });
          _this.getUserInfo();

          const user = getCookie("usn");
          setLog({
            op_module: logModuleMenu.UM,
            op_user: user,
            op_behavior: user + operationMenu.update,
            op_time: NowDate(),
          });
        } else {
          ElMessage({
            type: "error",
            message: "修改失败",
            offset: 200,
          });
        }
        _this.dialogVisibleUser = false;
      });
    },
    operationRemoveUser() {
      let _this = this;
      delUser(_this.UserForm).then((res) => {
        if (res.code == 200) {
          ElMessage({
            type: "success",
            message: "删除成功",
            offset: 200,
          });
          _this.getUserInfo();
          _this.dialogVisibleUser = false;
          const user = getCookie("usn");
          setLog({
            op_module: logModuleMenu.UM,
            op_user: user,
            op_behavior: user + operationMenu.delete,
            op_time: NowDate(),
          });
        } else {
          ElMessage({
            type: "error",
            message: "删除失败",
            offset: 200,
          });
        }
      });
    },
    updatePwd() {
      let _this = this;
      updatePwd(_this.updatePwdData).then((res) => {
        if (res.code == 200) {
          ElMessage({
            type: "success",
            message: "修改成功",
            offset: 200,
          });
        } else {
          ElMessage({
            type: "error",
            message: "修改失败",
            offset: 200,
          });
        }
        _this.getUserInfo();
        _this.dialogVisibleResetPasswords = false;
      });
    },
    Restore(index, val) {
      let _this = this;
      ElMessageBox.confirm(
        "确定要恢复用户【" + val.user_name + "】吗?",
        "恢复用户",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          showClose: false,
          lockScroll: true,
          closeOnClickModal: false,
        }
      )
        .then((res) => {
          restoreUser().then((res) => {
            if (res.code == 200) {
              ElMessage({
                type: "success",
                message: "恢复成功",
                offset: 200,
                duration: 1300,
              });
              _this.getUserInfo();
            } else {
              ElMessage({
                type: "error",
                message: "恢复失败",
                offset: 200,
              });
            }
          });
        })
        .catch((res) => {});
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

.userSearch .el-form-item:not(.userSearch .el-form-item:nth-of-type(1)) {
  margin-left: 30px;
}

.main > .body {
  width: 100%;
  height: calc(100% - 100px);
  padding: 10px 0px 10px 10px;
}

.main > .body > .content {
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: var(--box-shadow);
}

.tableDataTools {
  width: 100%;
  height: 60px;
  padding: 0 20px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}

.tableDataTools .add {
  padding: 0 20px 0px 20px;
  border: 1px solid transparent;
  outline: none;
  background-color: var(--theme-color);
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
  padding: 0 20px 0px 20px;
  width: 100%;
  height: calc(100% - 60px - 60px);
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

.btnSearch {
  padding: 18px 35px;
  border: none;
  outline: none;
  color: #fff;
  background-color: var(--theme-color);
}

.btnSearch:hover,
.btnSearch:focus,
.btnSearch:active {
  color: #fff;
  background-color: var(--theme-color);
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