last_id = -1

function show_probability(t_body, items, _header) {
    // 表头
    const tr_header = document.createElement('tr'); // 表头
    const tr_current = document.createElement('tr'); // 当前概率
    const tr_official = document.createElement('tr'); // 官方概率
    const th_sum = document.createElement('th'); // 表头总数
    const th_current = document.createElement('th'); // 表头当前概率
    const th_official = document.createElement('th'); // 表头官方概率
    th_sum.innerHTML = '总数:'
    th_current.innerHTML = '当前概率'
    th_official.innerHTML = '官方概率'

    th_current.style.fontSize = th_sum.style.fontSize = th_official.style.fontSize = '22px'
    th_current.style.borderRight = th_sum.style.borderRight = th_official.style.borderRight = th_official.style.borderBottom = 'solid 1px'
    tr_header.append(th_sum)
    tr_current.append(th_current)
    tr_official.append(th_official)
    let sum = 0;
    // 添加表头数据
    for (let idx in items) {
        const item = items[idx]
        const th = document.createElement('th');
        const _num = _header[item] ? _header[item][0] : 0;
        th.innerHTML = item + ':' + _num
        sum = sum + _num
        th.style.fontSize = "22px"
        th.style.width = "130px"
        th.style.borderRight = " solid 1px"
        if (_header[item]) {
            const _style = typeof (_header[item][1]) == 'string' ? _header[item][1].split(',') : ['#000000', '#FFFFFF'];
            th.style.color = _style[0]
            th.style.background = _style[1]
        }
        tr_header.append(th)
    }

    for (let idx in items) {
        const item = items[idx]
        let td1 = document.createElement('td');
        let td2 = document.createElement('td');
        const n = _header[item] ? _header[item][0] : 0;
        td1.innerHTML = '-'
        if (sum !== 0) {
            td1.innerHTML = (n / sum * 100).toFixed(1) + '%'
        }
        td1.style.textAlign = td2.style.textAlign = 'center'
        td1.style.fontSize = td2.style.fontSize = '22px'
        td1.style.borderRight = td2.style.borderRight = td2.style.borderBottom = 'solid 1px'
        tr_current.append(td1)
        // 添加该官方概率
        td2.innerHTML = (settings[item] ? settings[item].split(',')[2] : 0) + "%"
        tr_official.append(td2)
    }
    th_sum.innerHTML = '总数:' + sum
    t_body.innerHTML = ''
    t_body.append(tr_header)
    t_body.append(tr_current)
    t_body.append(tr_official)
}

function add_tr(t_body, _data) {
    const tr = document.createElement('tr')
    tr.style.display = "flex"
    tr.style.flexDirection = "column"
    t_body.append(tr)
    return tr
}

function add_td(t_tr, _data) {
    const td = document.createElement('td')
    td.style.display = "flex"
    td.style.flexDirection = "row"
    td.style.width = "125px"
    td.style.fontSize = "18px"
    const d1 = document.createElement('div')
    const d2 = document.createElement('div')
    d1.style.textAlign = d2.style.textAlign = "center"
    d1.style.fontWeight = "500"
    d2.style.fontWeight = "900"
    d1.style.width = "40%"
    d2.style.width = "60%"
    d2.style.borderRight = "solid 1px"
    d1.innerHTML = _data[2]
    if (_data[1]) {
        let cb = _data[1].split(',')
        d2.style.color = cb[0]
        d2.style.background = cb[1]
    }
    d2.innerHTML = _data[3]
    td.append(d1)
    td.append(d2)
    t_tr.append(td)
}

function show_data(t_body, _datas) {
    if (!_datas) {
        return
    }
    for (const idx in _datas) {
        add_data(t_body, _datas[idx])
    }
}


function add_data(t_body, _data) {
    if (!_data || last_id === _data[0]) {
        return
    } else {
        last_id = _data[0]
    }
    if (t_body.children.length === 0) {
        const tr = document.createElement('tr')
        tr.style.display = "flex"
        tr.style.flexDirection = "column"
        t_body.append(tr)
    }
    if (t_body.children.length === col) {
        if (t_body.children.item(col - 1).children.length === row) {
            t_body.children.item(0).remove()
            add_td(add_tr(t_body, _data), _data)
        } else {
            add_td(t_body.children.item(col - 1), _data)
        }
    } else {
        if (t_body.children.item(t_body.children.length - 1).children.length === row) {
            add_td(add_tr(t_body, _data), _data)
        } else {
            add_td(t_body.children.item(t_body.children.length - 1), _data)
        }
    }
}

function loadAd(url, pic, ad) {
    ajax_method(url, null, 'GET', (resp) => {
        if (settings['ad_pic_size'] > 0 || !settings['ad_pic_size']) {
            pic.src = resp
            pic.style = 'position: absolute; top: ' + settings['ad_pic_y'] + '; left: ' + settings['ad_pic_x'] + ';'
            pic.width = settings['ad_pic_size']
        }
    })
    const ad_text = settings['ad_text'];
    const ad_size = settings['ad_size'];
    const ad_font = settings['ad_font'];
    const ad_bg = settings['ad_bg'];
    if (!ad_text) {
        return
    }
    ad.innerHTML = ""
    const p = document.createElement("p");
    p.innerHTML = ad_text
    p.style = `max-width: 800px; color: ${ad_font}; background: ${ad_bg}; font-size: ${ad_size}px;`
    ad.appendChild(p)
}
