// function timestampToTime(timestamp) {
//     // 时间戳为10位需*1000，时间戳为13位不需乘1000
//     var date = new Date(timestamp);
//     var Y = date.getFullYear() + "-";
//     var M =
//         (date.getMonth() + 1 < 10
//             ? "0" + (date.getMonth() + 1)
//             : date.getMonth() + 1) + "-";
//
//     var D = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + " ";
//     var h = date.getHours() + ":";
//     var m = date.getMinutes() + ":";
//     var s = date.getSeconds();
//     return Y + M + D + h + m + s;
// }
// ;



function timestampToTime(timestamp) {
    // 时间戳为10位需*1000，时间戳为13位不需乘1000
    let date = new Date(timestamp);
    let Y = date.getFullYear() + "-";
    let M =
        (date.getMonth() + 1 < 10
            ? "0" + (date.getMonth() + 1)
            : date.getMonth() + 1) + "-";

    let day = date.getDate();
    let hour = date.getHours();
    let min = date.getMinutes();
    let sec = date.getSeconds();

    let D = (day < 10 ? "0" + day : day) + " ";
    let h = (hour < 10 ? "0" + hour : hour) + ":";
    let m = (min < 10 ? "0" + min : min) + ":";
    let s = (sec < 10 ? "0" + sec : sec);
    return Y + M + D + h + m + s;
}
;

// console.log(timestampToTime(1680220807));
// console.log(timestampToTime((new Date()).valueOf()));
console.log(timestampToTime(1680260195000));
