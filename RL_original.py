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

def oddLayers(N):
	L = [] 
	if N <= 1:
		return L
	if N == 2:
		l = helper.generateLoop_2D_coordinates(0, 0, N-1, N-1)
		L = [l, l[::-1]]
		return L 
	#Group A: outer layer, clockwise
	L.append(helper.generateLoop_2D_coordinates(0, 0, N-1, N-1))
	
	#group B: antiClockwise
	for i in range(N-2):
		l = helper.generateLoop_2D_coordinates(0, 0, i+1, N-1)
		l.reverse() 
		L.append(l)
		
	#Group C: anticlockwise
	for i in range(N-2):
		l = helper.generateLoop_2D_coordinates(i+1, 0, N-1, N-1)
		l.reverse() 
		L.append(l) 
		
	#Group D: anticlockwise
	for i in range(N-1):
		l = helper.generateLoop_2D_coordinates(0, i, N-1, i+1)
		l.reverse() 
		L.append(l)
	return L 

	
		
	
	
	
	
def evenLayer(N):
	
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
	
	#group B: Clockwise
	for i in range(N-2):
		L.append(helper.generateLoop_2D_coordinates(0, 0, N-1, i+1))
		
	#Group C: clockwise
	for i in range(N-2):
		L.append(helper.generateLoop_2D_coordinates(0, i+1, N-1, N-1))
		
	#Group D: clockwise
	for i in range(N-1):
		L.append(helper.generateLoop_2D_coordinates(i, 0, i+1, N-1))
	return L

def RL_original(N):
	L = [] 
	NoCSize = 2
	while NoCSize <= N:
		L = helper.shiftAllLoops(L, 1, 1)
		LayerID = NoCSize//2
		if LayerID % 2 == 0:
			L += evenLayer(NoCSize)
		else:
			L += oddLayers(NoCSize)
		NoCSize += 2
	L = helper.convertCordinates(L, N)
	return L





RL_StatsCSV = open("RL_Stats.csv", "w")
header = ",".join(loopStatistic.getStatsHeader())
RL_StatsCSV.write(f"{header}\n")



for N in [4,6,8,10,12,14,16]:
	print(f"Generating RL Original Loops{N}x{N}")
	L = RL_original(N)
	
	T = loopStatistic.getStats(N,L)
	line = ",".join(str(i) for i in T)
	RL_StatsCSV.write(f"{line}\n")
	print("Statistic added")
	#routingTable.RoutingTable(N, L)
	routingTable.RoutingTableToFile(N, L, f"RLConfig{N}.txt")
	print("Routing Table To File Done.")
	
	