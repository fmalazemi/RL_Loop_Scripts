#!/usr/bin/env python3

import helper
import loopStatistic
import routingTable

def generateOnionLayerN(N):
	#This generates loops for one layer of NxN
	if N == 2:
		#Reversed
		l = helper.generateLoop_2D_coordinates(0, 0, 1, 1)
		l.reverse() 
		return [l]
	
	
	
	# outer loop Reversed
	l = helper.generateLoop_2D_coordinates(0, 0, N-1, N-1)
	l.reverse() 
	L = [l]
	
	# upper left loops
	for i in range(1, N-1):
		l = helper.generateLoop_2D_coordinates(0, 0, i, i)
		L.append(l)
	
	
	# upper right loops
	
	ul = [0,1] # upper left Node
	lr = [N-2, N-1]  # lower right Node
	for i in range(N-2):
		l = helper.generateLoop_2D_coordinates(ul[0], ul[1], lr[0], lr[1])
		L.append(l)
		ul[1] += 1 #move ul column to right
		lr[0] -= 1 #move lr row up
	
	# lower left loops
	ul = [1,0] # upper left Node
	lr = [N-1, N-2]  # lower right Node
	for i in range(N-2):
		l = helper.generateLoop_2D_coordinates(ul[0], ul[1], lr[0], lr[1])
		L.append(helper.generateLoop_2D_coordinates(ul[0], ul[1], lr[0], lr[1]))
		ul[0] += 1 #move ul row  down
		lr[1] -= 1 #move lr column left
	
	# lower right loops
	ul = [1,1] # upper left Node
	lr = [N-1, N-1]  # lower right Node
	for i in range(N-2):
		l = helper.generateLoop_2D_coordinates(ul[0], ul[1], lr[0], lr[1])
		L.append(l)
		ul[0] += 1 #move ul row down
		ul[1] += 1 #move ul column left
	return L

def RL_onion(N):
	#generate loops for all onion layers
	#Assume N is even (it works for odd but we don't consider it here)
	L = [] 
	NoLayers = N//2
	shift = 1
	for i in range(2,N,2):
		loops = generateOnionLayerN(N-i)
		loops = helper.shiftAllLoops(loops, shift, shift)
		L = L + loops
		shift += 1 
		
	L += generateOnionLayerN(N)
	L = helper.convertCordinates(L, N)
	
	return L 





HP_RL_StatsCSV = open("OINION_Stats.csv", "w")


header = ",".join(loopStatistic.getStatsHeader())
HP_RL_StatsCSV.write(f"{header}\n")





for N in [4,6,8,10,12,14,16]:
	print(f"Generating {N}x{N}")
	L = RL_onion(N)
	
	T = loopStatistic.getStats(N,L)
	line = ",".join(str(i) for i in T)
	HP_RL_StatsCSV.write(f"{line}\n")
	print("Statistic added")
	#routingTable.RoutingTable(N, L)
	routingTable.RoutingTableToFile(N, L, f"RLOnion{N}.txt")
	#print("Routing Table To File Done.")
	
	
	