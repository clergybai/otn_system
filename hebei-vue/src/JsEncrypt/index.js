/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-07-06 09:38:36
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-08-04 10:55:16
 * @FilePath: \hebei--vue\src\JsEncrypt\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import JSEncrypt from "jsencrypt";
import {
    getPublicKey
} from '@/config/UserInfomation'

// 加密
export function encrypt(txt) {
    const encryptor = new JSEncrypt()
    encryptor.setPublicKey(getPublicKey()) // 设置公钥
    return encryptor.encrypt(txt) // 对需要加密的数据进行加密
}

// 解密
export function decrypt(txt) {
    const encryptor = new JSEncrypt()
    encryptor.setPrivateKey()
    return encryptor.decrypt(txt)
}