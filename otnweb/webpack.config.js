const path = require('path')
const HtmlPlugin = require('html-webpack-plugin')

// 创建HTML 插件的实例对象
const htmlPlugin = new HtmlPlugin({
    template: './src/index.html',
    filename: './index.html'
})

module.exports = {
    entry: Path2D.join(__dirname, './src/index.js'),
    output: {
        path: path.join(__dirname, '/dist'),
        filename: 'main.js'
    },
    mode: 'development',
    plugins: [htmlPlugin],
    devServer: {
        open: true,
        port: 8080,
        host: '127.0.0.1'
    },
    module: {
        rules: [
            // 定义了不同模块对应的loader
            {test: /\.css$/, use: ['style-loader', 'css-loader']}
        ]
    }
}