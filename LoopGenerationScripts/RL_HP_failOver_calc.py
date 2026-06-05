#!/usr/bin/env python3

'''
This is the High performance RL Loop set that includes Group A, B, C, D, E for each layer except 2x2 where we have two loops only. 
loops in Group D,E are similar to Group B,C except they are rotated 90 deg. 
There are no even or odd layer. 


Read Paper. 
IF you want to generate routing Table use Program "XXX".py

'''


#!/usr/bin/env python3

import helper 
import loopStatistic
import routingTable
import RL_HP_loops 


HP_RL_StatsCSV = open("HP_RL_Stats_avgHop_Fail_Change.csv", "w")

line = "NoCSize, avgHop, failAvgHop, MaxHopChange"

HP_RL_StatsCSV.write(f"{line}\n")

for N in [4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]:
	#print(f"Generating {N}x{N}")
	L = RL_HP_loops.RL_HP_loops(N)
	
	avgHop = loopStatistic.calcHopCount(N,L)
	
	count = 0
	s = 0.0 
	mx = -1

	for i in range(len(L)):
		T = L[0:i] + L[i+1:len(L)]
		a = loopStatistic.calcHopCount(N, T)
		s += a
		mx = max(a, mx)
		count+=1
	s = s/count
	line = f"{N},{avgHop},{s},{mx}"
		
	HP_RL_StatsCSV.write(f"{line}\n")
	print(N, "Statistic added")
	#routingTable.RoutingTable(N, L)
	
	
	
