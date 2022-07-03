


function 切图(linePart)
	-- body
	nLog("切图运行了")
	
	检测移动位置 = function ()
		-- body
		local points = FreeGame:getPoints(t.小地图当前位置);
		if points then 
			local cP = points[1];
			local tP = linePart[2].mp;
			local gP = linePart[2].gp;
			if math.abs(cP.x-tP.x)<50 and math.abs(cP.y-tP.y)<50 then 
--				randomTap(t.关闭小地图.x,t.关闭小地图.y);
				mSleep(5000);
				
				local jobs = {
					Action(t.小地图):click():f(3000);
					
--					Action(t.未隐藏界面):click();
				}
				
				if gP ==nil then 
					table.insert(jobs,Action(t.过图圈):click():after(退出));
					table.insert(jobs,Action(t.过图圈2):click():after(退出));
					table.insert(jobs,Action(t.隐藏界面):click():except(t.未隐藏界面):f(2000));
				else
					table.insert(jobs,Action(t.隐藏界面):click():sleep(1000):click(gP):except(t.未隐藏界面):after(退出));
				end
				
				if linePart[2].npc ==nil then else 
					table.insert(jobs,Action(linePart[2].npc):click(70,-60));
					table.insert(jobs,Action(t.nPc对话前往):click():after(退出));
				end
				
				FreeGame:run(jobs);
				
				return 退出;
			end
		end
		
	end
	
	jobs = {
		
		Action(t.小地图):click(linePart[2].mp):f(5*1000);
		
		Action(t.小地图):fun(检测移动位置);
	}
	
	if linePart[2].dP ==nil then 
		table.insert(jobs,Action(linePart[1]):click());
	else 
		table.insert(jobs,Action(linePart[1]):click(linePart[2].dP):except(linePart[2].npc,t.npc界面));
		table.insert(jobs,Action(linePart[2].npc):click():sleep(3000));
		table.insert(jobs,Action(linePart[2].npc):click(40,-70):sleep(1000));
		table.insert(jobs,Action(t.npc给予):click());
		table.insert(jobs,Action(t.镖银道具):click());
		table.insert(jobs,Action(t.交镖):click():after(退出));
	
		table.insert(jobs,Action(t.npc对话郑镖头):fun(function()跑图完毕 = false end ):after(退出));
	end
	
	FreeGame:run(jobs);
	
end

function 跑图(line)
	-- body
	跑图完毕 = true;
	while (跑图完毕) do
	-- body
		for k,v in pairs(line) do 
			local points = FreeGame:getPoints(v[1]);
			local fanhui = FreeGame:getPoints(t.已隐藏界面);
			if fanhui then randomTap(t.隐藏界面返回.x,t.隐藏界面返回.y);mSleep(1000) end
			if points then 
				nLog("当前地图:"..k);
				切图(v)
				sleep(1000);
			end
		end
	end
end

--跑图(line);
