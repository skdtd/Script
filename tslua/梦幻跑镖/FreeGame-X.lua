require("TSLib");
--常量区
下 = 0;
右 = 1;
左 = 2;
上 = 3;
退出 = 1;
跳过 = 2;
找到退出 =1;
找不到退出 =2;
-- 常量中的 字段不允许更改，与覆盖！！！

function Point(x,y)
	local new ={};
	new["x"] = x;
	new["y"] = y;
	return new;
end

function Rect(x,y,x1,y1)
	-- body
	local new = {x,y,x1,y1};
	return new;
end

function lineprint(msg)
	nLog(msg)
	-- body
end

function findmulticolor(c)
	-- body
	--{0x141414, "139|27|0x141414,-91|-33|0x000000,-55|60|0x141414", 90, 93, 25, 633, 161};
	return findMultiColorInRegionFuzzy(c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8] or {});
end

function sleep(times)
	-- body
	mSleep(times); 
end

function messagebox(msg)
	-- body
	toast(msg,3)
end

function gettickcount()
	-- body
	return os.time()*1000;
end

----------------------FreeGame 系统提示配置
ERROR_INIT_ORE_MSG = "初始化前,请配置方法 FreeGame:home()";
ERROR_INIT_PAGE_MSG = "初始化前,请配置方法 FreeGame:page(\"特征库文件\")";
ERROR_RUN_UNKNOWPAGE = "未知游戏界面";
ERROR_JOB_NIL = "任务列表不可以为空";

PAGE_GETPAGE_MSG = "当前游戏界面:";
PAGE_UNKNOWPAGE_MSG = "未知界面";

BTN_CLICK_MSG = "点击";
BTN_CLICK_MSG_PY = "偏移点击";
BTN_CLICK_MSG_RADDOM = "范围随机点击";
POINT_SLIDE_MSG = "滑动";
INPUT_MSG = "输入";
ACTON_SLEEP = "睡眠";

ACTION_SKIP_MSG = "跳过";
ACTION_EXCEPT_SKIP_MSG = "排除";
ACTION_UNCKEC_RETURN_MSG = "未检测到特征 退出:";

RUN_EXEC_DES = "延时执行【%s】秒 后执行任务";
RUN_CARD_OPEN = true;
RUN_CARD_CLOSE = false;

----------------------
FREEGAME_LIB_WELCOME = "\r\n-------------------------\r\n欢迎您使用FreeGame-X 引擎[v2.1.1] \r\n文档地址:https://www.yuque.com/youzizai/ftzs/ut0c9e\r\n引擎交流群欢迎您【QQ:905788670】\r\n-------------------------";
lineprint(FREEGAME_LIB_WELCOME);


--常量区 over
FreeGame = {
	ore_p = nil;
	page_p = nil;
	s_p = nil;
	card_p = nil;
	fontlib_index = nil;
	status = nil;--状态
	unexe_p = nil;
	actionr_p = nil; -- 是否运行状态
	actionr_time = os.time();-- 最后一次执行action的时间
};

--初始化屏幕朝向
function FreeGame:home(ore)
	self.ore_p = ore;
	init(ore);
	return self;
end

-- 告诉框架颜色库
function FreeGame:page(colors)
	self.page_p = colors;
	for k,v in pairs(self.page_p) do
		self.page_p[k]["name"] = k;
	end
	return self;
end

--缩放分辨率
function FreeGame:size(s)
	return self;
end

function FreeGame:fontlib(v)
	if type(v) == "table" then
		lineprint("加载table 字库");
		local index = addTSOcrDictEx(v);
		self.fontlib_index = index;
	elseif type(v) == "string" then	
		lineprint("加载字库"..v);
		local index = addTSOcrDict(v);
		self.fontlib_index = index;
	end
	return self;
end

function FreeGame:card(...)
	self.card_p = {...};
	self.card_p["bit"] = timenow().."-"..getimei().."-"..rnd(0,1000);
	lineprint("您启用了激活卡功能: http://47.104.139.55/admin")
	return self;
end

-- 设置框架运行速率
function FreeGame:s(speed)
	self.s_p = speed;
	return self;
end

-- 设置框架运行速率
function FreeGame:hud(...)
	self.s_hud = {...};
	return self;
end
-- 修改框架状态
function FreeGame:cs(id)
	-- body
	FreeGame.status = id;
	return self;
end

-- 
function FreeGame:unexe(...)
	-- body
	self.unexe_p = {...};
	return self;
end

function FreeGame:getPoints(ts)
	-- {50,182,78,200,"C8840D-000000","-4|0|CD8912-000000,4|0|CC9922-000000"};
	-- {0x141414, "139|27|0x141414,-91|-33|0x000000,-55|60|0x141414", 90, 93, 25, 633, 161};
	-- {(index, "找字,自行修改该文字", 0, 0, 0, 0, "FFFFFF , 303030 # C2BFC5 , 101010", 90};

	if #ts>2 and type(ts[2]) =="string" then
		x,y,ret=findmulticolor(ts);
		if x~=-1 then
			return {Point(x,y)};
		end
	elseif #ts>=4 and type(ts[1]) =="number" and type(ts[6]) == "string" then
		lineprint("开始识别文本了，可能会有些慢，请耐心等待");
		local ret = ocrText(ts[1], ts[2], ts[3], ts[4], ts[5],true);
		if ret.info then
			lineprint("文字识别:"..ret.text);
			for var= 1, #ret.info do
				if ret.info[var].char == ts[6] then
					return {Point(ret.info[var].x+ts[1],ret.info[var].y+ts[2])};
				end
			end
		end
	elseif type(ts[1]) =="string"  then
		if string.find(ts[1],".png") or  string.find(ts[1],".jpg") or  string.find(ts[1],".jpeg") then
			lineprint("图片识别");
			x, y = findImageInRegionFuzzy("test_alpha.png", 90, 0, 0, 320, 480, 0xffffff);
			if x ~= -1 and y ~= -1 then        --如果在指定区域找到某图片符合条件
				return {Point(x,y)};
			end
		else
			lineprint("字库识字");
			local x,y = tsFindText(FreeGame.fontlib_index,ts[1],ts[2],ts[3],ts[4],ts[5],ts[6],ts[7] or 80)
			if x>-1 or y>-1 then
				return {Point(x,y)};
			end
			lineprint("识别失败")
		end		
	end
	return nil;
end

function FreeGame:runAction(action)
	local points = nil;
	if action.except_color_f then
		for k,v in  pairs(action.except_color_f) do
			points = self:getPoints(v);
			if points then
				lineprint(ACTION_EXCEPT_SKIP_MSG..v.name..'跳过'..action.name);break;
			end
		end
	end
	if points then
	elseif action.status == nil or FreeGame.status == action.status then
		local points = nil;
		local uncheckName = nil;
		for k1,c in pairs(action.color_f) do
			if c ==nil then
				c = self.fg_p_page[c.name]
			end
			points = self:getPoints(c);
			if points == nil then
				uncheckName = k1;
				break
			end;
		end
		if points then
			
			if self:freLogic(action) then
				local ext = self:action(action,points);
				if ext then
					return ext
				end;
			end
		elseif action.uncheckP then
			ext =  action.uncheckP(action,uncheckName);
			if type(ext) == "number" then
				if ext == 退出 then ext = true; end
			end
			if ext then
				lineprint(ACTION_UNCKEC_RETURN_MSG..action.name)
				return ext;
			end
		end;

	end;

	return false;
end


function FreeGame:action(action,points)
	FreeGame.actionr_p = true;
	FreeGame.actionr_time = os.time();
	local ext;
	local skipaction;
	if action.beforeP then
		ext,skipaction = action.beforeP(action,points);
		if type(ext)=="boolean" and ext then
			return true;
		end;
		if type(ext) == "number" then
			if ext == 退出 then ext = true; return true; end
			if ext == 跳过 then ext = false; skipaction = true; end    
		end    
	end

	if (not skipaction) then
		for o=1,10000,1 do
			if action.orders[o] then
				ext = action.orders[o]:run(action,points);
				if type(ext) == "number" then
					if ext == 退出 then ext = true; end
				end
				if ext then
					return ext;
				end
			else
				break;
			end
		end
	else
		lineprint("跳过执行:"..action.name);
	end
	action.action_lastTime = gettickcount();

	if action.afterP and (not skipaction) then
		local isExt = action.afterP(action,points);
		if type(isExt) == "number" then
			if isExt == 退出 then isExt = true; end
		end 	

		return isExt or false;
	end

	return ext or false;

end

function FreeGame:freLogic(v)
	if v.action_fre and v.action_lastTime  then
		if (#v.action_fre) == 1 and (gettickcount()- v.action_lastTime) <v.action_fre[1] then
			lineprint(ACTION_SKIP_MSG..'['..v.name..'] 距下次执行:'..(v.action_fre[1]+v.action_lastTime-gettickcount())..' ms');
			return false;
		end

		if (#v.action_fre) >1  and (gettickcount()- v.action_lastTime)<math.random(v.action_fre[1],v.action_fre[2]) then
			lineprint(ACTION_SKIP_MSG..'['..v.name..'] 随机时差');
			return false;
		end
	end
	return true;
end

function FreeGame:run(job,times)
	local runTimes =1;
	while true do
		FreeGame:cardLogic();
		--keepScreen(true);
		FreeGame.actionr_p = false;
		for k,action in pairs(job) do
			if self:runAction(action) then
				return;
			end
		end
		
		if not FreeGame.actionr_p and FreeGame.unexe_p and FreeGame.unexe_p[1] then
			nLog("全部未找到")
			if type(FreeGame.unexe_p[1])  == "function" then 
				local r = FreeGame.unexe_p[1](os.time()- FreeGame.actionr_time)
				if r or r == 退出 then return; end
			end;
		end
		
		--keepScreen(false)
		sleep(self.s_p or 1000);
		if times~=nil and runTimes>= times then
			break;
		end
	end
	return self;
end


function FreeGame:runExec(job,times)
	if type(times) == "number" then
		lineprint(string.format(RUN_EXEC_DES,times/1000));
		sleep(times);
		self:run(job);
	elseif type(times) == "string" then
		local fT = string2time(times)*1000;
		local mT = fT - os.milliTime();
		lineprint(string.format(RUN_EXEC_DES,mT/1000));

		sleep(mT);
		self:run(job);
	end
end

function FreeGame:cardLogic()
	if self.card_p then
		if self.card_p["lasttime"] and os.time()- self.card_p["lasttime"] < 5*60 then
			return  RUN_CARD_OPEN,"5分心跳";
		end    
		self.card_p["lasttime"] = os.time();	


		local cardurl = "http://47.104.139.55/api/card/info"
		local eCardNumber = editgettext(self.card_p[2]);


		local send ="apply_id="..self.card_p[1]..
		"&number="..eCardNumber..
		"&bit="..self.card_p["bit"];

		lineprint("心跳"..self.card_p["bit"])

		local res = httprequest("post",cardurl,send,"utf-8","Content-Type=application/x-www-form-urlencoded");

		local ts = ""

		local result= JsonDecode(res);

		if result.data.isFree == 0 then
			local msgform = "";
			if result.data.card and result.data.card.status ==1 then
				if not carLogicRunAlredy then
					messagebox(result.data.card.typeName..":有效期至 "..result.data.card.expire);
				end
				carLogicRunAlredy = true;
				return RUN_CARD_OPEN,(result.data.card.typeName..":有效期至 "..result.data.card.expire);
			elseif  result.data.card and result.data.card.status ==0 then 
--				messagebox(result.msg);
				msgform = "激活码已过期！";
			else    
				msgform = result.msg;
			end

			local msg = "很抱歉:"..msgform.."\n"
			.."请联系QQ:"..result.data.qq.." 购买激活卡.\n\n"
			.."卡片价格:\n"
			.."日卡: "..result.data.amountDay.." \n"
			.."月卡: "..result.data.amountMonth.." \n\n"
			.."购卡后，请在配置界面激活卡片~";

			messageboxex(msg,1,50,50,0,18);
			error("");
			return RUN_CARD_CLOSE,result.msg;

		else
			if not carLogicRunAlredy then
				messagebox("免费脚本,尽情畅玩");
			end
			carLogicRunAlredy = true;
			return RUN_CARD_OPEN,"免费脚本,尽情畅玩";
		end
	end

	if not carLogicRunAlredy then
		messagebox("免费脚本,尽情畅玩");
	end    
	carLogicRunAlredy = true;
	return RUN_CARD_OPEN,"免费脚本,尽情畅玩";
end




----------------JSON CODE

-----------------------------------JsonFormat


local encode,next_char
local parse,create_set

function create_set(...)
	local res = {}
	for i = 1, select("#", ...) do
		res[ select(i, ...) ] = true
	end
	return res
end


function JsonDecode(str)	--解Json格式
	if type(str) ~= "string" then
		error("expected argument of type string, got " .. type(str))
	end
	local res, idx = parse(str, next_char(str, 1, create_set(" ", "\t", "\r", "\n"), true))
	idx = next_char(str, idx, create_set(" ", "\t", "\r", "\n"), true)
	if idx <= #str then
		decode_error(str, idx, "trailing garbage")
	end
	return res
end

function JsonEncode(val)	--转Json格式
	return ( encode(val) )
end

local escape_char_map = {
	[ "\\" ] = "\\\\",
	[ "\"" ] = "\\\"",
	[ "\b" ] = "\\b",
	[ "\f" ] = "\\f",
	[ "\n" ] = "\\n",
	[ "\r" ] = "\\r",
	[ "\t" ] = "\\t",
}

local escape_char_map_inv = { [ "\\/" ] = "/" }
for k, v in pairs(escape_char_map) do
	escape_char_map_inv[v] = k
end


local function escape_char(c)
	return escape_char_map[c] or string.format("\\u%04x", c:byte())
end


local function encode_nil(val)
	return "null"
end


local function encode_table(val, stack)
	local res = {}
	stack = stack or {}

-- Circular reference?
	if stack[val] then error("circular reference") end

	stack[val] = true

	if val[1] ~= nil or next(val) == nil then
		-- Treat as array -- check keys are valid and it is not sparse
		local n = 0
		for k in pairs(val) do
			if type(k) ~= "number" then
				error("invalid table: mixed or invalid key types")
			end
			n = n + 1
		end
		if n ~= #val then
			error("invalid table: sparse array")
		end
		-- Encode
		for i, v in ipairs(val) do
			table.insert(res, encode(v, stack))
		end
		stack[val] = nil
		return "[" .. table.concat(res, ",") .. "]"

	else
		-- Treat as an object
		for k, v in pairs(val) do
			if type(k) ~= "string" then
				error("invalid table: mixed or invalid key types")
			end
			table.insert(res, encode(k, stack) .. ":" .. encode(v, stack))
		end
		stack[val] = nil
		return "{" .. table.concat(res, ",") .. "}"
	end
end


local function encode_string(val)
	return '"' .. val:gsub('[%z\1-\31\\"]', escape_char) .. '"'
end


local function encode_number(val)
-- Check for NaN, -inf and inf
	if val ~= val or val <= -math.huge or val >= math.huge then
		error("unexpected number value '" .. tostring(val) .. "'")
	end
	return string.format("%.14g", val)
end


local type_func_map = {
	[ "nil"     ] = encode_nil,
	[ "table"   ] = encode_table,
	[ "string"  ] = encode_string,
	[ "number"  ] = encode_number,
	[ "boolean" ] = tostring,
}


encode = function(val, stack)
	local t = type(val)
	local f = type_func_map[t]
	if f then
		return f(val, stack)
	end
	error("unexpected type '" .. t .. "'")
end





-------------------------------------------------------------------------------
-- Decode
-------------------------------------------------------------------------------




local literal_map = {
	[ "true"  ] = true,
	[ "false" ] = false,
	[ "null"  ] = nil,
}


function next_char(str, idx, set, negate)
	for i = idx, #str do
		if set[str:sub(i, i)] ~= negate then
			return i
		end
	end
	return #str + 1
end


local function decode_error(str, idx, msg)
	local line_count = 1
	local col_count = 1
	for i = 1, idx - 1 do
		col_count = col_count + 1
		if str:sub(i, i) == "\n" then
			line_count = line_count + 1
			col_count = 1
		end
	end
	error( string.format("%s at line %d col %d", msg, line_count, col_count) )
end


local function codepoint_to_utf8(n)
-- http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=iws-appendixa
	local f = math.floor
	if n <= 0x7f then
		return string.char(n)
	elseif n <= 0x7ff then
		return string.char(f(n / 64) + 192, n % 64 + 128)
	elseif n <= 0xffff then
		return string.char(f(n / 4096) + 224, f(n % 4096 / 64) + 128, n % 64 + 128)
	elseif n <= 0x10ffff then
		return string.char(f(n / 262144) + 240, f(n % 262144 / 4096) + 128,
			f(n % 4096 / 64) + 128, n % 64 + 128)
	end
	error( string.format("invalid unicode codepoint '%x'", n) )
end


local function parse_unicode_escape(s)
	local n1 = tonumber( s:sub(3, 6),  16 )
	local n2 = tonumber( s:sub(9, 12), 16 )
-- Surrogate pair?
	if n2 then
		return codepoint_to_utf8((n1 - 0xd800) * 0x400 + (n2 - 0xdc00) + 0x10000)
	else
		return codepoint_to_utf8(n1)
	end
end

YZZ_DES = "---------------\nBaidu OCR - PowerBy 游自在\n 飞天助手脚本学院 QQ研学群:905788670\n---------------"

local function parse_string(str, i)
	local has_unicode_escape = false
	local has_surrogate_escape = false
	local has_escape = false
	local last
	for j = i + 1, #str do
		local x = str:byte(j)

		if x < 32 then
			decode_error(str, j, "control character in string")
		end

		if last == 92 then -- "\\" (escape char)
			if x == 117 then -- "u" (unicode escape sequence)
				local hex = str:sub(j + 1, j + 5)
				if not hex:find("%x%x%x%x") then
					decode_error(str, j, "invalid unicode escape in string")
				end
				if hex:find("^[dD][89aAbB]") then
					has_surrogate_escape = true
				else
					has_unicode_escape = true
				end
			else
				local c = string.char(x)
				if not create_set("\\", "/", '"', "b", "f", "n", "r", "t", "u")[c] then
					decode_error(str, j, "invalid escape char '" .. c .. "' in string")
				end
				has_escape = true
			end
			last = nil

		elseif x == 34 then -- '"' (end of string)
			local s = str:sub(i + 1, j - 1)
			if has_surrogate_escape then
				s = s:gsub("\\u[dD][89aAbB]..\\u....", parse_unicode_escape)
			end
			if has_unicode_escape then
				s = s:gsub("\\u....", parse_unicode_escape)
			end
			if has_escape then
				s = s:gsub("\\.", escape_char_map_inv)
			end
			return s, j + 1

		else
			last = x
		end
	end
	decode_error(str, i, "expected closing quote for string")
end


local function parse_number(str, i)
	local x = next_char(str, i, create_set(" ", "\t", "\r", "\n", "]", "}", ","))
	local s = str:sub(i, x - 1)
	local n = tonumber(s)
	if not n then
		decode_error(str, i, "invalid number '" .. s .. "'")
	end
	return n, x
end


local function parse_literal(str, i)
	local x = next_char(str, i, create_set(" ", "\t", "\r", "\n", "]", "}", ","))
	local word = str:sub(i, x - 1)
	if not create_set("true", "false", "null")[word] then
		decode_error(str, i, "invalid literal '" .. word .. "'")
	end
	return literal_map[word], x
end


local function parse_array(str, i)
	local res = {}
	local n = 1
	i = i + 1
	while 1 do
		local x
		i = next_char(str, i, create_set(" ", "\t", "\r", "\n"), true)
		-- Empty / end of array?
		if str:sub(i, i) == "]" then
			i = i + 1
			break
		end
		-- Read token
		x, i = parse(str, i)
		res[n] = x
		n = n + 1
		-- Next token
		i = next_char(str, i, create_set(" ", "\t", "\r", "\n"), true)
		local chr = str:sub(i, i)
		i = i + 1
		if chr == "]" then break end
		if chr ~= "," then decode_error(str, i, "expected ']' or ','") end
	end
	return res, i
end


local function parse_object(str, i)
	local res = {}
	i = i + 1
	while 1 do
		local key, val
		i = next_char(str, i, create_set(" ", "\t", "\r", "\n"), true)
		-- Empty / end of object?
		if str:sub(i, i) == "}" then
			i = i + 1
			break
		end
		-- Read key
		if str:sub(i, i) ~= '"' then
			decode_error(str, i, "expected string for key")
		end
		key, i = parse(str, i)
		-- Read ':' delimiter
		i = next_char(str, i, create_set(" ", "\t", "\r", "\n"), true)
		if str:sub(i, i) ~= ":" then
			decode_error(str, i, "expected ':' after key")
		end
		i = next_char(str, i + 1, create_set(" ", "\t", "\r", "\n"), true)
		-- Read value
		val, i = parse(str, i)
		-- Set
		res[key] = val
		-- Next token
		i = next_char(str, i, create_set(" ", "\t", "\r", "\n"), true)
		local chr = str:sub(i, i)
		i = i + 1
		if chr == "}" then break end
		if chr ~= "," then decode_error(str, i, "expected '}' or ','") end
	end
	return res, i
end


local char_func_map = {
	[ '"' ] = parse_string,
	[ "0" ] = parse_number,
	[ "1" ] = parse_number,
	[ "2" ] = parse_number,
	[ "3" ] = parse_number,
	[ "4" ] = parse_number,
	[ "5" ] = parse_number,
	[ "6" ] = parse_number,
	[ "7" ] = parse_number,
	[ "8" ] = parse_number,
	[ "9" ] = parse_number,
	[ "-" ] = parse_number,
	[ "t" ] = parse_literal,
	[ "f" ] = parse_literal,
	[ "n" ] = parse_literal,
	[ "[" ] = parse_array,
	[ "{" ] = parse_object,
}


parse = function(str, idx)
	local chr = str:sub(idx, idx)
	local f = char_func_map[chr]
	if f then
		return f(str, idx)
	end
	decode_error(str, idx, "unexpected character '" .. chr .. "'")
end


------------------------------------JSON END
-----------------------------------uitls
function split(str,reps)
    local resultStrList = {}
    string.gsub(str,'[^'..reps..']+',function ( w )
        table.insert(resultStrList,w)
    end)
    return resultStrList
end


-------------------------------------------------------------------------------Fragment
ActionDao = {};
ActionDao.__index = ActionDao;
function Action(...)
	local new ={};
	setmetatable(new,ActionDao);
	new.orders ={};-- 片段序列;
	new.color_f = {...}; --颜色特征
	new.except_color_f = nil; --排除颜色特征
	new.action_fre  = nil; --动作频率
	new.action_pre  = nil; --动作间隔
	new.action_slide_speed  = nil; --滑动速度
	new.action_lastTime  = nil; -- 上次执行时间
	new.beforeP = nil; --执行动作前回调
	new.afterP = nil; --执行动作后回调
	new.uncheckP = nil; -- 当特征点没找到的时候回调
	new.name = ""; --特征名称
	new.status = nil; --状态
	for k,v in pairs(new.color_f) do
		new.name = new.name..""..v.name..'->'
	end
	return new;
end

function ActionDao:before(fun)
	self.beforeP = self:filterFun(fun);
	return self;
end

function ActionDao:uncheck(fun)
	self.uncheckP = self:filterFun(fun);
	return self;
end

function ActionDao:after(fun)
	self.afterP = self:filterFun(fun);
	return self;
end


function ActionDao:except(...)
	self.except_color_f = {...};
	return self;
end


function ActionDao:p(ms)
	self.action_pre = ms;
	return self;
end

function ActionDao:speed(spe)
	self.action_slide_speed = spe;
	return self;
end

function ActionDao:f(...)
	self.action_fre = {...};
	return self;
end

-- 绑定状态
function ActionDao:s(id)
	-- body
	self.status = id;
	return self;
end


function ActionDao:filterFun(fun)
	if type(fun) == "number" then
		if fun == 退出 then
			return function() return true end;
		elseif fun == 跳过 then
			return function() return false,true end;
		elseif fun == (退出+跳过) then
			return function() return true,true end;
		end
	end
	return fun;
end


------------------------freagment
--点击片段 clickf
clickf = {p = nil;};
function clickf.new(...)
	local new ={};
	clickf.__index = clickf;
	setmetatable(new,clickf);
	new.p = {...};
	return new;
end

function randomTap(x,y)
	math.randomseed(tostring(os.time()):reverse():sub(1, 7)) -- 设置一个随机数种子
	pX = math.random(-3,3)
	pY = math.random(-3,3)
	if FreeGame.s_hud then
		tap(x+pX,y+pY,50,FreeGame.s_hud[1]);
	else
		tap(x+pX,y+pY);
	end
end

function clickf:run(action,points)
	if # self.p > 0 then
		if(type(self.p[1])=="number") then
			-- 坐标偏移拓展
			local px = self.p[1] or 0;
			local py = self.p[2] or 0;
			randomTap(points[1].x+px,points[1].y+py);
			lineprint(BTN_CLICK_MSG_PY..'['..action.name..']-坐标['..points[1].x..'+'..px..','..points[1].y..'+'..py..']')
			return ;
		elseif type(self.p[1]) =="table" and self.p[1].x == nil then
			math.randomseed(tostring(os.time()):reverse():sub(1, 7)) -- 设置一个随机数种子
			local pX = math.random(self.p[1][1],self.p[1][3]);
			local pY = math.random(self.p[1][2],self.p[1][4]);
			lineprint(BTN_CLICK_MSG_RADDOM..'['..action.name..']-随机坐标['..pX..','..pY..']');
			randomTap(pX,pY);
			return;
		end

		for k,v in pairs(self.p) do
			randomTap(v.x,v.y);
			lineprint(BTN_CLICK_MSG..'['..action.name..']-坐标['..v.x..','..v.y..']')
			sleep(action.action_pre or 0);
		end
	else
		randomTap(points[1].x,points[1].y);
		lineprint(BTN_CLICK_MSG..'['..action.name..']-坐标['..points[1].x..','..points[1].y..']')
	end
end

---- 睡眠片段
sleepf = {p = nil;};
function sleepf.new(...)
	local new ={};
	sleepf.__index = sleepf;
	setmetatable(new,sleepf);
	new.p = {...};
	return new;
end

function sleepf:run(action,points)
	if #self.p == 1 and type(self.p[1])=="number" then
		lineprint(ACTON_SLEEP..'['..action.name..']:'..self.p[1]);
		sleep(self.p[1])
	else
		lineprint(ACTON_SLEEP..'['..action.name..']:1000');
		sleep(1000);
	end
end

---滑动方法
slidf = {
	p = nil;
};

function slidf.new(...)
	local new ={};
	slidf.__index = slidf;
	setmetatable(new,slidf);
	new.p = {...};
	return new;
end

function slid(pStart,pEnd,jD)
	local X1,Y1,X2,Y2 = nil;
	X1 = pStart.x;
	X2 = pEnd.x;
	Y1 = pStart.y;
	Y2 = pEnd.y;

	local d = math.floor((((X2-X1)^2+(Y2-Y1)^2)^(1/2))/(jD or 20))
	local x,y= (X2-X1)/d,(Y2-Y1)/d
	touchDown(1, X1, Y1)
	for i = 1 ,d do
		touchMove(1, X1+x*i, Y1+y*i)
		sleep(15);
	end
	touchUp(1,X1, Y1)
end;

function slidx(points,jD)
	local X1,Y1,X2,Y2 = nil;
	function slidx_d(pStart,pEnd)
		-- body
		X1 = pStart.x;
		X2 = pEnd.x;
		Y1 = pStart.y;
		Y2 = pEnd.y;
		local d = math.floor((((X2-X1)^2+(Y2-Y1)^2)^(1/2))/(jD or 20))
		local x,y= (X2-X1)/d,(Y2-Y1)/d
		local bc = d/2/15;

		for i = 1 ,d do
			math.randomseed(tostring(os.time()):reverse():sub(1, 7)) -- 设置一个随机数种子
			local pX = math.random(-15,15)
			local pY = math.random(-15,15)
--			local pX = 0;
--			local pY = 0;
			touchMove(1, X1+x*i+pX, Y1+y*i+pY)
			sleep(math.abs(d/2-i)/bc);
		end
	end
	if type(points)=="table" then
			math.randomseed(tostring(os.time()):reverse():sub(1, 7)) -- 设置一个随机数种子
			local pM1 = math.random(-1,1)
			local pM2 = math.random(-1,1)
		touchDown(1, points[1].x,  points[1].y);
		touchDown(2, points[1].x+1,  points[1].y-1);
		for var= 1, (#points-1),1 do
			if var ==1 then
				slidx_d(points[1],points[2]);
			else
				slidx_d(points[var],points[var+1]);
			end
			sleep(400);
		end
		sleep(300);
		touchUp(1,X1, Y1)
		touchUp(2, X1, Y1);
	end
end;

function slidf:run(action,points)
	for k, v in pairs(self.p) do
		if k>1 then
			local pointLT = self.p[k-1];
			local pointRB = self.p[k];
			slid(pointLT,pointRB,action.action_slide_speed );
			sleep(action.action_pre or 15);
			lineprint(POINT_SLIDE_MSG..'['..action.name..']-起点['..pointLT.x..','..pointLT.y..']->终点['..pointRB.x..','..pointRB.y..'] 速度:['..(action.action_slide_speed or 5)..']');
		end
	end
end

---------- 文件输入
inputf = {
	p = nil;
};

function inputf.new(...)
	local new ={};
	inputf.__index = inputf;
	setmetatable(new,inputf);
	new.p = {...};
	return new;
end

function inputf:run(action,points)

	local enterStr = "";

	if #self.p<2 then
		if type(self.p[1])=="string"  then
			enterStr = self.p[1];
		elseif type(self.p[1])=="function" then
			enterStr = self.p[1]();
		end
	else
		local curPos = self.p.pos or 1;
		enterStr = self.p[curPos];
		self.p["pos"] = curPos+1;
		if self.p.pos> #self.p then 
			self.p["pos"] = 1;
		end
	end

	if string.find(enterStr,"#C#") then
		enterStr = string.gsub(enterStr,"#C#","");
		-- android delect
		for i =0,10,1 do   
			os.execute("input keyevent 67") 
		end 
		lineprint("删除 ")   


	end	

	if string.find(enterStr,"#E#") then
		enterStr = string.gsub(enterStr,"#E#","");
		-- ios
		keyDown("ReturnOrEnter")
		keyUp("ReturnOrEnter")
	end	

	inputText(enterStr);
	lineprint(INPUT_MSG..'['..action.name..']->'..enterStr)
end


---------- function
functionf = {
	p = nil;
};

function functionf.new(...)
	local new ={};
	functionf.__index = functionf;
	setmetatable(new,functionf);
	new.p = {...};
	return new;
end

function functionf:run(action,points)
	if #self.p == 1 and type(self.p[1])=="function" then
		return self.p[1](action,points);
	end
end

---------- sfind 滑动查找
sfindf = {
	p = nil;
};

function sfindf.new(...)
	local new ={};
	sfindf.__index = sfindf;
	setmetatable(new,sfindf);
	new.p = {...};
	return new;
end

function sfindf:run(action,points)
	if #self.p > 1 then
		-- p ={t.帮派任务,Point(877,502),Point(875,204),2,找不到退出}
		--检测是否存在，不存在就滚动
		keepScreen(false) -- 释放屏幕缓存
		for i=1,(self.p[4] or 3),1 do
			local point = FreeGame:getPoints(self.p[1]);
			if point then
				randomTap(point[1].x,point[1].y);
				if self.p[5] and self.p[5] == 找到退出 then
					lineprint("["..self.p[1].name.."] 找到 点击:"..point[1].x.."-"..point[1].y.." 并退出任务");
					return true     
				end;
				lineprint("["..self.p[1].name.."] 点击:"..point[1].x.."-"..point[1].y);
				return false;
			else
				lineprint("["..self.p[1].name.."] 滑动找点:("..self.p[2].x.."-"..self.p[2].y..")->("..self.p[3].x.."-"..self.p[3].y..")");
				slid(self.p[2],self.p[3]);
				sleep(500);
			end   
		end
		if self.p[5] and self.p[5] == 找不到退出 then 
			lineprint("["..self.p[1].name.."]"..(self.p[4] or 3).." 次滑动找点未找到,退出当前任务");
			return true
		end;
		lineprint("["..self.p[1].name.."]"..(self.p[4] or 3).." 次滑动找点未找到");
		return false;
	end
	return;
end

changeStatue = {
	p = nil;
};

function changeStatue.new(...)
	local new ={};
	changeStatue.__index = changeStatue;
	setmetatable(new,changeStatue);
	new.p = {...};
	return new;
end

function changeStatue:run(action,points)
	if #self.p > 0 then
		FreeGame:cs(self.p[1]);
	else
		FreeGame:cs(nil);
	end
end


------------------拓展方法:
function ActionDao:click(...)
	self.orders[#self.orders+1] = clickf.new(...);
	return self;
end

function ActionDao:sleep(...)
	self.orders[#self.orders+1] = sleepf.new(...);
	return self;
end

function ActionDao:slid(...)
	self.orders[#self.orders+1] = slidf.new(...);
	return self;
end

function ActionDao:input(...)
	self.orders[#self.orders+1] = inputf.new(...);
	return self;
end

function ActionDao:fun(...)
	self.orders[#self.orders+1] = functionf.new(...);
	return self;
end

function ActionDao:sfind(...)
	self.orders[#self.orders+1] = sfindf.new(...);
	return self;
end

function ActionDao:cs(...)
	self.orders[#self.orders+1] = changeStatue.new(...);
	return self;
end

function ActionDao:fo(times)
	for i=2,times,1 do
		self.orders[#self.orders+1] = self.orders[#self.orders];
	end
	return self;
end

