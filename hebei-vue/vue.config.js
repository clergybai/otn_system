/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-05-05 19:02:18
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-26 17:34:30
 * @FilePath: \hebei--vue\vue.config.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
const {
  defineConfig,
} = require('@vue/cli-service');

const Env = process.env;
const isProduction = Env.environment === 'production';

module.exports = defineConfig({
  chainWebpack: (config => {
    config.plugin('html').tap(args => {
      args[0].title = "传送网隐患自动诊断系统";
      return args;
    })
  }),
  productionSourceMap: !isProduction,
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',
    open: false,
    port: 8080,
    https: false,
    // disableHostCheck: true,
    // client: {
    //   websocketURL: 'ws://0.0.0.0:6103/ws'
    // },
    headers: {
      'Access-Control-Allow-origin': '*'
    },
    proxy: {
      '/api': {
        target: Env.Hebei_webApi,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        },
      },
      '/loginApi': {
        target: Env.Hebei_loginApi,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/loginApi': ''
        },
        secure: false,
        headers: {
          Referer: Env.Hebei_loginApi,
        }
      },
      '/paramsApi': {
        target: Env.Hebei_paramsApi,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/paramsApi': ''
        },
        headers: {
          Referer: Env.Hebei_paramsApi,
        }
      },
      '/listenningApi': {
        target: Env.Hebei_listenningApi,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/listenningApi': ''
        },
        headers: {
          Referer: Env.Hebei_listenningApi,
        }
      },
      '/woOperationApi': {
        target: Env.Hebei_woOperationApi,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/woOperationApi': ''
        },
        headers: {
          Referer: Env.Hebei_woOperationApi,
        }
      }
    },
  },
})