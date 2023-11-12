// const constants = require('fs').constants
// const promises = require('fs').promises
// import { access } from 'fs/promises';
// import { constants } from 'fs';
//import { cat } from 'shelljs';
//import fs from 'fs'
//import promises from 'fs/promises'
//import { promises as fsp } from 'fs';

function isEmptyStr(s){
    if(s == undefined || s == null || s == ''){
        return true
    }
    return false
}

//var R_OK = 'r'
// var R_OK = constants.R_OK
function isFileExist(path) {
    let is_empty = isEmptyStr(path)
    if(is_empty) return false
    //return fs.existsSync(path)
    let is_exist = false
    // await promises.access(path, R_OK, (err)=>{
    //     is_exist = err ? false : true
    // })
    let current
    try{
        const{c} = import(path)
        current =c
        is_exist = true
    }
    catch(e){}

    return is_exist
}

// Array.prototype.firstOrDefault = function(predicateFunction) {
//     if (predicateFunction == undefined || predicateFunction == null) {
//         return null;
//     }
//     if (this.length == 0) {
//         return null;
//     }
//     this.each(function() {
//         if (predicateFunction.call(this)) {
//             return item;
//         }
//     });
//     return null;
// };

module.exports.isEmptyStr = isEmptyStr
module.exports.isFileExist = isFileExist
//export default {
//     isEmptyStr,
//     isFileExist
//}
