// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');


function mask_show() {
    console.log('mask_show');
    const ele = document.getElementById('loading');
    if (ele) {
        ele.style.display = 'block';
        return;
    }
    const __html = `
            <div class="container-loading" >
                <div class="mask"></div>
                <div class="sk-chase">
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                  </div>
            </div>
            `;
    var obj = document.createElement('div');
    obj.setAttribute('id', 'loading');
    obj.innerHTML = __html;
    const body = document.getElementsByTagName("body")[0];
    body.appendChild(obj);
    // const ele = document.getElementById('loading');
    // ele.style.display = 'block';
    // 消失的话直接ele.style.display = 'none';或者移除
}


function mask_hide() {
    console.log('mask_hide');
    const ele = document.getElementById('loading');
    // 消失的话直接
    ele.style.display = 'none';
}

// var su_data;
function dispatch(url, id, cls_name, tag) {
    mask_show();
    // 1. 创建 xhr 对象
    var xhr = new XMLHttpRequest();
    // 2. 调用 open()
    console.log(`POST：${url}`);
    xhr.open('POST', url);
    // 3. 设置 Content-Type 属性（固定写法）
    // xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('Content-Type', 'application/json');
    // try {
    // 4. 调用 send()，同时将数据以查询字符串的形式，提交给服务器
    // xhr.send('dashboard_id=水浒传&slice_name=施耐庵&publisher=天津图书出版社');
    // xhr.send("index_id=" + index_id + "&slice_name=" + '0');
    // xhr.send("id=" + id + "&cls_name=" + cls_name + "&tag=" + tag);
    var reqParam = {
        "id": id,
        "cls_name": cls_name,
        "tag": tag
    };
    xhr.send(JSON.stringify(reqParam));
    // 5. 监听 onreadystatechange 事件
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // console.log(xhr.responseText);
                var ret = JSON.parse(xhr.responseText);
                console.log(ret);
                if (ret.status) {
                    alert("success:\n" + ret.msg);
                    mask_hide();
                } else {
                    alert("failed:\n" + ret.msg);
                    mask_hide();
                }

            } else {
                console.log(xhr.responseText);
                alert("执行失败，failed:\n" + `xhr.readyState:${xhr.readyState} xhr.status:${xhr.status}`);
                mask_hide();
            }
        }
    };

    // }
    // catch (err) {
    // alert(err.message);
    // console.log(err.message);
    // mask_hide();
    // }
    console.log(`POST：${url} finished.`);
    // mask_hide();
}

function set_last_column_width() {
    // var td_list = document.querySelectorAll('td:last-child');
    // var th_list = document.querySelectorAll('th:last-child');
    let result_list = $('#result_list');
    // if (result_list.length !== 0) {
    if (result_list[0].querySelector('tbody').children.length !== 0) {
        let td_list = $('td:last-child');
        let th_list = $('th:last-child');
        let width = 0;
        let btns = td_list[0].getElementsByTagName('button');
        let btns_cnt = td_list[0].getElementsByTagName('button').length;
        for (let i = 0; i < btns.length; i++) {
            let font_cnt = btns[i].getElementsByTagName('span')[0].textContent.length;
            width = width + font_cnt * 14; // 一个字给14px的宽度
            // console.log(btns[i].getElementsByTagName('span')[0].textContent)
        }
        // console.log(width);
        // width = width + btns_cnt * 14 + 16; // 按钮padding14、加上按钮margin 4px 加上左右10px margin，
        width = width + btns_cnt * 14 + (btns_cnt - 1) * 4 + 14; // 按钮padding14、加上按钮margin 4px 加上左右10px margin，
        // console.log(width);
        let width_str = String(width > 180 ? 180 : width) + 'px';
        console.log(width_str);
        td_list.css("width", width_str);
        th_list.css("width", width_str);
    } else {
        console.log('dom #result_list have no data.')
    }
}

window.onload = function () {
    set_last_column_width()
};


