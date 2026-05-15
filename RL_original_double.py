#!/usr/bin/env python3

'''
This is the original RL Loop set that includes Group A, B, C, D for each layer except 2x2 where we have two loops only. 
Read Paper. 
IF you want to generate routing Table use Program "XXX".py

'''


#!/usr/bin/env python3

import loopStatistic 
import helper
import routingTable
import RL_original



def RL_original_Double(N):
	originalLoopSet = RL_original(N)
	
	L = []
	for l in originalLoopSet:
		L.append(l)
		L.append(l[::-1])
	return L
		


RLDouble_StatsCSV = open("RL_double_Stats.csv", "w")
header = ",".join(loopStatistic.getStatsHeader())
RLDouble_StatsCSV.write(f"{header}\n")



for N in [4,6,8,10,12,14,16]:
	print(f"Generating RL Original Loops{N}x{N}")
	L = RL_original.RL_original(N)
	
	T = loopStatistic.getStats(N,L)
	line = ",".join(str(i) for i in T)
	RLDouble_StatsCSV.write(f"{line}\n")
	print("Statistic added")
	#routingTable.RoutingTable(N, L)
	routingTable.RoutingTableToFile(N, L, f"RL_double_Config{N}.txt")
	print("Routing Table To File Done.")
	
	