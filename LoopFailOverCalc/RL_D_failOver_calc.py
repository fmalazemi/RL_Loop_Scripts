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
	originalLoopSet = RL_original.RL_original(N)
	
	L = []
	for l in originalLoopSet:
		L.append(l)
		if len(l) != 4:
			L.append(l[::-1])
	return L
		


RLDouble_StatsCSV = open("RL_double_Stats_avgHop_Fail_Change.csv", "w")
line = "NoCSize, avgHop, failAvgHop, MaxHopChange"
RLDouble_StatsCSV.write(f"{line}\n")


for N in [4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]:
	print(f"Generating RL Original Loops{N}x{N}")
	L = RL_original_Double(N)
	
	
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
	
	RLDouble_StatsCSV.write(f"{line}\n")
	print(N, "Statistic added")
	
		
	
