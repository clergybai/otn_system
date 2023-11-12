<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-30 09:28:10
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-07-21 17:24:35
 * @FilePath: \hebei--vue\src\views\Component\pagingDevice.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="paging">
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="pageSizes"
      :page-size="pageSize"
      layout="sizes, prev, pager, next, jumper"
      class="paging"
    >
    </el-pagination>
  </div>
</template>

<script>
import { reactive, toRefs } from "vue";
export default {
  name: "paging",
  props: {
    currentPage: {
      type: Number,
      default: 1,
    },
    pageSize: {
      type: Number,
      default: 10,
    },
    pageSizes: {
      type: Array,
      default: [100, 200, 300, 400],
    },
    tableData: {
      type: Object,
      default: null,
    },
  },
  setup(props, content) {
    const handleSizeChange = (val) => {
      content.emit("handleSizeChange", val);
    };

    const handleCurrentChange = (val) => {
      content.emit("handleCurrentChange", val);
    };

    //上一页
    const prevPage = () => {
      if (props.currentPage == 1) {
        return false;
      } else {
        props.currentPage--;
        changePage();
      }
    };

    // 下一页
    const nextPage = () => {
      if (props.currentPage == props.totalPage) {
        return false;
      } else {
        this.currentPage++;
        changePage();
      }
    };

    const changePage = () => {
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
    };

    const data = reactive({
      modalShow: props.modalShow,
    });

    const dataRef = toRefs(data);

    return {
      handleSizeChange,
      handleCurrentChange,
      ...dataRef,
    };
  },
};
</script>

<style scoped>
</style>