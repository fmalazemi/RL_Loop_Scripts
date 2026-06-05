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

def HP_Layer(N):
	
	L = [] 
	if N <= 1:
		return L
	if N == 2:
		l = helper.generateLoop_2D_coordinates(0, 0, N-1, N-1)
		L = [l, l[::-1]]
		return L 
	#Group A: outer layer, Anticlockwise
	l = helper.generateLoop_2D_coordinates(0, 0, N-1, N-1)
	l.reverse()
	L.append(l)
	L.append(l[::-1])
	
	#group B: Clockwise
	for i in range(N-2):
		L.append(helper.generateLoop_2D_coordinates(0, 0, N-1, i+1))
		
	#Group C: clockwise
	for i in range(N-2):
		L.append(helper.generateLoop_2D_coordinates(0, i+1, N-1, N-1))
		
	#group D: Clockwise
	for i in range(N-2):
		L.append(helper.generateLoop_2D_coordinates(0, 0, i+1, N-1))
		
	#Group E: clockwise
	for i in range(N-2):
		L.append(helper.generateLoop_2D_coordinates(i+1, 0, N-1, N-1))
	
	return L

def RL_HP_loops(N):
	L = [] 
	NoCSize = 2
	while NoCSize <= N:
		L = helper.shiftAllLoops(L, 1, 1)
		LayerID = NoCSize//2
		L += HP_Layer(NoCSize)
		NoCSize += 2
	L = helper.convertCordinates(L, N)
	return L

HP_RL_StatsCSV = open("HP_RL_Stats_avgHop_Fail_Change.csv", "w")

line = "NoCSize, avgHop, failAvgHop, MaxHopChange"

HP_RL_StatsCSV.write(f"{line}\n")

for N in [4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]:
	#print(f"Generating {N}x{N}")
	L = RL_HP_loops(N)
	
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
	
	
	
