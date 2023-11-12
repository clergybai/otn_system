/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-05 19:02:18
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-20 14:29:48
 * @FilePath: \hebei--vue\src\main.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import {
    createApp
} from 'vue'
import App from './App.vue'
import '../src/plugins/index.css'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import locale from 'element-plus/lib/locale/lang/zh-cn'
import * as elIcons from '@element-plus/icons'
import {
    createPinia
} from 'pinia'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({
    easing: 'ease', // 动画方式
    speed: 600, // 递增进度条的速度
    showSpinner: false, // 是否显示加载ico
    trickleSpeed: 200, // 自动递增间隔
    minimum: 0.3 // 初始化时的最小百分比
})

const pinia = createPinia();
const app = createApp(App)
for (const name in elIcons) {
    app.component(name, elIcons[name])
}
app.use(ElementPlus, {
    locale: locale
})
app.use(pinia);
app.use(router).mount('#app')