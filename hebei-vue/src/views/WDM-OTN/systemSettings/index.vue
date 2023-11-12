<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-13 15:56:25
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-01 18:16:55
 * @FilePath: \hebei--vue\src\views\WDM-OTN\systemSettings\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
 <template>
  <!-- 系统设置 -->
  <div class="main">
    <div class="navigation">
      <el-scrollbar>
        <el-menu
          @select="handleSelect"
          :default-active="mainIsActive"
          v-loading.lock="elmenuLoading"
          :unique-opened="true"
        >
          <template v-for="(item, index) of menuData" :key="index">
            <template v-if="item.is_authen">
              <template v-if="Array.isArray(item.route)">
                <el-sub-menu :index="index + ''">
                  <template #title>{{ item.text }}</template>
                  <template
                    v-for="(children, index) of item.route"
                    :key="index"
                  >
                    <el-menu-item
                      v-if="children.is_authen"
                      :index="children.route"
                      >{{ children.text }}</el-menu-item
                    >
                  </template>
                </el-sub-menu>
              </template>
              <template v-else>
                <el-menu-item :index="item.route">
                  {{ item.text }}
                </el-menu-item>
              </template>
            </template>
          </template>
        </el-menu>
      </el-scrollbar>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

 <script>
import { useMainStore } from "../../../store/index";
import { getIs_Authen } from "@/config/UserInfomation";
export default {
  data() {
    return {
      elmenuLoading: true,
      mainIsActive: "",
      menuData: [],
    };
  },
  watch: {
    "$route.path"() {
      this.routeListen();
    },
  },
  created() {
    this.routeLoad();
    this.routeListen();
  },
  mounted() {},
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push({
        path: key,
        params: { data: "query" },
      });
    },
    routeListen() {
      this.menuData.forEach((item) => {
        if (Array.isArray(item.route)) {
          item.route.forEach((children) => {
            if (this.$route.path.includes(children.route)) {
              this.mainIsActive = children.route;
              return;
            }
          });
        } else {
          if (this.$route.path.includes(item.route)) {
            this.mainIsActive = item.route;
            return;
          }
        }
      });
    },
    routeLoad() {
      let _this = this;
      _this.elmenuLoading = true;
      const useStateSession = getIs_Authen();
      _this.menuData = [
        {
          text: "数据导入",
          route: "/main/WDM/OTN/systemSettings/dataImport",
          is_authen: true,
        },
        {
          text: "单波数据导入",
          route: "/main/WDM/OTN/systemSettings/singleWaveDataImport",
          is_authen: true,
        },
        {
          text: "基准值规则",
          route: [
            {
              text: "默认规则",
              route: "/main/WDM/OTN/systemSettings/baselineRule/defaultRule",
              is_authen: true,
            },
            {
              text: "新增规则",
              route: "/main/WDM/OTN/systemSettings/baselineRule/createRule",
              is_authen: true,
            },
            {
              text: "查看规则",
              route: "/main/WDM/OTN/systemSettings/baselineRule/viewRule",
              is_authen: true,
            },
          ],
          is_authen: true,
        },
        {
          text: "单波规则",
          route: [
            {
              text: "新增规则",
              route: "/main/WDM/OTN/systemSettings/singleWaveRule/createRule",
              is_authen: true,
            },
            {
              text: "查看规则",
              route: "/main/WDM/OTN/systemSettings/singleWaveRule/viewRule",
              is_authen: true,
            },
          ],
          is_authen: true,
        },
        {
          text: "复用段波道数配置",
          route: "/main/WDM/OTN/systemSettings/multiChannelConf",
          is_authen: true,
        },
        {
          text: "权限配置",
          route: [
            {
              text: "用户管理",
              route:
                "/main/WDM/OTN/systemSettings/permissionsConfiguration/userManage",
              is_authen: useStateSession.can_add_user,
            },
            // {
            //   text: "角色管理",
            //   route:
            //     "/main/WDM/OTN/systemSettings/permissionsConfiguration/roleManage",
            // },
            {
              text: "权限管理",
              route:
                "/main/WDM/OTN/systemSettings/permissionsConfiguration/menuManage",
              is_authen: useStateSession.can_modify_prems,
            },
          ],
          is_authen:
            !useStateSession.can_add_user && !useStateSession.can_modify_prems
              ? false
              : true,
        },
        {
          text: "操作日志",
          route: "/main/WDM/OTN/systemSettings/operationLog",
          is_authen: useStateSession.can_add_user,
        },
      ];
      _this.elmenuLoading = false;
    },
  },
};
</script>

 <style scoped>
.main {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
}

.main .navigation {
  padding: 10px 10px 10px 20px;
  min-width: 250px;
  max-width: 250px;
  height: 100%;
  box-sizing: border-box;
  user-select: none;
}

/* .main .navigation .el-scrollbar {
  max-height: calc(100% - 100px);
  padding-top: 30px;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: var(--box-shadow);
} */

.main .navigation .el-scrollbar {
  /* max-height: calc(100% - 100px); */
  height: 100%;
  padding-top: 30px;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: var(--box-shadow);
  overflow-x: hidden;
}

.main .content {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.el-menu {
  border: none;
  width: 100%;
  overflow-x: hidden;
}

.el-menu-item {
  transition: none;
  align-items: center;
  justify-content: flex-start;
  box-sizing: content-box;
  font-size: 16px;
  border-left: 4px solid transparent;
}

.el-menu-item:hover {
  background-color: #edeffe;
  background-color: #f5f7fc;
}
.el-menu-item.is-active {
  background-color: #edeffe;
  background-color: #f5f7fc;
  border-left: 4px solid var(--theme-color);
  font-weight: bold;
  color: var(--theme-color);
}

.el-menu-item-group {
  padding: 0;
}
</style>