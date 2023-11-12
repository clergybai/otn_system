/*
 * @Author: '15623702696' 2458186212@qq.com
 * @Date: 2022-08-05 10:36:20
 * @LastEditors: '15623702696' 2458186212@qq.com
 * @LastEditTime: 2022-09-06 18:06:54
 * @FilePath: \hebei--vue\src\config\formatTime.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import moment from 'moment';

export const NowDate = () => {
    const date = new Date();
    return (
        date.getFullYear() +
        "-" +
        (date.getMonth() + 1) +
        "-" +
        date.getDate() +
        " " +
        date.getHours() +
        ":" +
        date.getMinutes() +
        ":" +
        date.getSeconds()
    );
}

export const FormatShortTime = (val) => {
    return moment(val).format('YYYY-MM-DD');
}

export const FormatTime = (val) => {
    return moment(val).format('YYYY-MM-DD HH:mm:ss');
}

export const FormatSearchStartTime = (val) => {
    return moment(val).format('YYYY-MM-DD 00:00:00');
}

export const FormatSearchEndTime = (val) => {
    return moment(val).format('YYYY-MM-DD 23:59:59');
}

export const FormatLeaveTime = (val) => {
    return moment(val).format('YYYY-MM-DD HH:mm');
}

export const FormatMonthTime = (val) => {
    return moment(val).format('YYYY-MM');
}

export const FormatSecondsTime = (val) => {
    return moment(val).format('HH:mm:ss');
}

export const FormatFilterTime = (val, type = 'short') => {
    if (type == 'short') {
        return moment(val).format('HH:mm:ss');
    } else {
        return moment(val).format('YYYY-MM-DD HH:mm:ss');
    }
}

export const startOfTime = (val, dataType = 'day') => {
    return moment(val).startOf(dataType);
}

export const endOfTime = (val, dataType = 'day') => {
    return moment(val).endOf(dataType);
}

export const lastDateOfMonthTime = (val) => {
    const firstDate = moment(d).startOf('month').format('YYYY-MM-DD');
    const lastDate = moment(d).endOf('month').format('YYYY-MM-DD');
    let dateArr = [];
    dateArr.push(firstDate);
    dateArr.push(lastDate);
    return dateArr;
}