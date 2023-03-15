Date.prototype.pattern = function (fmt) {
    // var date = (new Date()).pattern("yyyy/MM/dd")
    const o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours() % 12 === 0 ? 12 : this.getHours() % 12, //小时
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    const week = {
        "0": "/u65e5", "1": "/u4e00", "2": "/u4e8c", "3": "/u4e09", "4": "/u56db", "5": "/u4e94", "6": "/u516d"
    };
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    if (/(E+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[this.getDay() + ""]);
    }
    for (const k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }
    return fmt;
}

function watermark(settings) {
    //默认设置
    const defaultSettings = {
        watermark_txt: "text", watermark_x: 20,//水印起始位置x轴坐标
        watermark_y: 20,//水印起始位置Y轴坐标
        watermark_rows: 20,//水印行数
        watermark_cols: 20,//水印列数
        watermark_x_space: 0,//水印x轴间隔
        watermark_y_space: 0,//水印y轴间隔
        watermark_color: '#FF0000',//水印字体颜色
        watermark_alpha: 0.2,//水印透明度
        watermark_fontsize: '23px',//水印字体大小
        watermark_font: '微软雅黑',//水印字体
        watermark_width: 280,//水印宽度
        watermark_height: 120,//水印长度
        watermark_angle: 15//水印倾斜度数
    }
    //采用配置项替换默认值，作用类似jquery.extend
    if (arguments.length === 1 && typeof arguments[0] === "object") {
        const src = arguments[0] || {};
        for (let key in src) {
            if (src[key] && defaultSettings[key] && src[key] === defaultSettings[key]) continue; else if (src[key]) defaultSettings[key] = src[key];
        }
    }
    const oTemp = document.createDocumentFragment();
    //获取页面最大宽度
    const page_width = Math.max(document.body.scrollWidth, document.body.clientWidth);
    //获取页面最大长度
    const page_height = Math.max(document.body.scrollHeight, document.body.clientHeight);
    //如果将水印列数设置为0，或水印列数设置过大，超过页面最大宽度，则重新计算水印列数和水印x轴间隔
    if (defaultSettings.watermark_cols === 0 || (parseInt(defaultSettings.watermark_x + defaultSettings.watermark_width * defaultSettings.watermark_cols + defaultSettings.watermark_x_space * (defaultSettings.watermark_cols - 1)) > page_width)) {
        defaultSettings.watermark_cols = parseInt((page_width - defaultSettings.watermark_x + defaultSettings.watermark_x_space) / (defaultSettings.watermark_width + defaultSettings.watermark_x_space));
        defaultSettings.watermark_x_space = parseInt((page_width - defaultSettings.watermark_x - defaultSettings.watermark_width * defaultSettings.watermark_cols) / (defaultSettings.watermark_cols - 1));
    }
    //如果将水印行数设置为0，或水印行数设置过大，超过页面最大长度，则重新计算水印行数和水印y轴间隔
    if (defaultSettings.watermark_rows === 0 || (parseInt(defaultSettings.watermark_y + defaultSettings.watermark_height * defaultSettings.watermark_rows + defaultSettings.watermark_y_space * (defaultSettings.watermark_rows - 1)) > page_height)) {
        defaultSettings.watermark_rows = parseInt((defaultSettings.watermark_y_space + page_height - defaultSettings.watermark_y) / (defaultSettings.watermark_height + defaultSettings.watermark_y_space));
        defaultSettings.watermark_y_space = parseInt(((page_height - defaultSettings.watermark_y) - defaultSettings.watermark_height * defaultSettings.watermark_rows) / (defaultSettings.watermark_rows - 1));
    }
    let x;
    let y;
    for (let i = 0; i < defaultSettings.watermark_rows; i++) {
        y = defaultSettings.watermark_y + (defaultSettings.watermark_y_space + defaultSettings.watermark_height) * i;
        for (let j = 0; j < defaultSettings.watermark_cols; j++) {
            x = defaultSettings.watermark_x + (defaultSettings.watermark_width + defaultSettings.watermark_x_space) * j;

            const mask_div = document.createElement('div');
            mask_div.id = 'mask_div' + i + j;
            mask_div.appendChild(document.createTextNode(defaultSettings.watermark_txt));
            //设置水印div倾斜显示
            mask_div.style.webkitTransform = "rotate(-" + defaultSettings.watermark_angle + "deg)";
            mask_div.style.MozTransform = "rotate(-" + defaultSettings.watermark_angle + "deg)";
            mask_div.style.msTransform = "rotate(-" + defaultSettings.watermark_angle + "deg)";
            mask_div.style.OTransform = "rotate(-" + defaultSettings.watermark_angle + "deg)";
            mask_div.style.transform = "rotate(-" + defaultSettings.watermark_angle + "deg)";
            mask_div.style.visibility = "";
            mask_div.style.position = "absolute";
            mask_div.style.left = x + 'px';
            mask_div.style.top = y + 'px';
            mask_div.style.overflow = "hidden";
            mask_div.style.zIndex = "9999";
            mask_div.style.opacity = defaultSettings.watermark_alpha;
            mask_div.style.fontSize = defaultSettings.watermark_fontsize;
            mask_div.style.fontFamily = defaultSettings.watermark_font;
            mask_div.style.color = defaultSettings.watermark_color;
            mask_div.style.textAlign = "center";
            mask_div.style.fontWeight = "bolder";
            mask_div.style.width = defaultSettings.watermark_width + 'px';
            mask_div.style.height = defaultSettings.watermark_height + 'px';
            mask_div.style.display = "block";
            mask_div.style.pointerEvents = "none"; //禁止水印被复制并防止遮挡【实体虚化】
            oTemp.appendChild(mask_div);
        }
    }
    document.body.appendChild(oTemp);
}

function ajax_method(url, data, method, success, async) {
    const ajax = new XMLHttpRequest();
    ajax.open(method, url, async)
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4 && ajax.status === 200) {
            if (success) {
                success(ajax.responseText)
            }
        } else {
            // nothing todo
        }
    }
    if (method.toUpperCase() === 'GET') {
        ajax.send()
    } else if (method.toUpperCase() === 'POST') {
        if (data) {
            if (data.constructor.name !== 'FormData') {
                ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            }
            ajax.send(data)
        } else {
            ajax.send()
        }
    } else {
        console.log('Unsupported method')
    }
}

