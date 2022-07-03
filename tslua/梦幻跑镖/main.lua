
require("FreeGame-X");
require("page")
require("map")

require("跑图")

FreeGame:home(右):page(t):s(10);


function 飞长安(...)
	if 已经是长安 then
		return;
	end
	-- body
	local jobs = {
		Action(t.已隐藏界面):click(t.隐藏界面返回);
		Action(t.道具):click();
		Action(t.道具界面):click(Point(642,  212)):click(Point(642,  212));
		Action(t.长安飞行界面):click(Point(952,  323)):sleep(2000):after(退出);
	}
	FreeGame:run(jobs);
	已经是长安 = true;
end

function 进镖局()
	-- body
	line = {
		{t.长安城,map.长安城.镖局};
		{t.长风镖局,map.长风镖局.郑镖头}
	}
	跑图(line);
	
	等级 = Point( 1081,  138);
	
	类型= Point(  1102,  429);
	
	lrw = {
		Action(t.npc对话郑镖头):click(等级):sleep(2000):click(类型):after(退出);
	};
	
	FreeGame:run(lrw);
	
	nLog("跑图完毕了")
	
	return 退出
	
end

function 接镖()
	-- body
	local jobs = {
		Action(t.长安城):fun(进镖局):uncheck(飞长安):except(t.道具界面);
		Action(t.道具界面):click(Point( 1071,   52));
	};
	FreeGame:run(jobs);
end


function 规划路线()
	-- body
	autoLine = nil;
	local jobs = {
		Action(t.送镖Npc_东海龙王):fun(function() autoLine=line.东海龙王 end):after(退出);
	};
	
	FreeGame:run(jobs)
	nLog("线路规划完毕");
	local 出镖局 = {
		Action(t.长风镖局):click(Point(    590,  582)):f(1000);
		Action(t.长安城):after(退出);
	};
	FreeGame:run(出镖局);
	
	nLog("开始跑图了");
	
	跑图(autoLine);
	
	
	
end


--接镖();

规划路线();

nLog("任务已经领取了")

--function a(...)
--	-- body
--	jobs = {
--		Action(t.npc郑镖头):click():f(10*1000);
--	}
--	FreeGame:run(jobs);
--end

--a();