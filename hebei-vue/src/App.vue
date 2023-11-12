<!--
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-05 19:02:18
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-07-08 09:53:22
 * @FilePath: \hebei--vue\src\App.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div class="main">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  watch: {},
  created() {
    // document.title = "传送网隐患自动诊断系统";
  },
  methods: {},
};
</script>

<style scoped>
.main {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 0 auto;
}
</style>
