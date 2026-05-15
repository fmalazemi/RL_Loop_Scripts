#!/usr/bin/env python3

'''
This script can generate statistics for a given loop set L 

'''

def avgHopCount(N, loopSet):
	D = [[ N*N*N for x in range(N*N)] for x in range(N*N)]
	for l in loopSet: 
		for i in range(len(l)):
			d = 0
			for j in range(len(l)):  
				j = (i+j)%len(l)
				D[l[i]][l[j]] = min(d, D[l[i]][l[j]])
				d += 1
				
	return D

def calcHopCount(N, loopSet):
	#Loops must not be in 2DCoordinate 
	D = avgHopCount(N, loopSet)				
	s = 0.0
	for i in D:
		s += sum(i)
		#print i, sum(i)
		
	for i in range(len(D)):
		for j in range(len(D[i])):
			if D[i][j] == N*N*N:
				print( "\nERROR: Not Complete interconnection.", i, j)
				exit()
				
				
	for i in D:
		for j in i:
			if j == N*N*N: ## my infinity
				print( "\nERROR: Not Complete interconnection.", i)
				exit()
	return s/(N**4-N**2)

def calcOverlappingCap(L, N):
	# calculate max, min, avg overlapping cap
	D = {}
	
	for loop in L:
		for j in range(len(loop)):
			k = (j+1)%len(loop)
			x = min(loop[j], loop[k])
			y = max(loop[j], loop[k])
			if (x,y) not in D:
				D[(x,y)] = 0
			D[(x,y)] += 1
	max_overlapping = 0 
	min_overlapping = N*N
	avg_overlapping = 0
	
	for i in range(N-1):
		for j in range(N-1):
			node = i*N + j 
			south = node + N 
			right = node + 1
			if (node, south) not in D:
				print("-->", node, south)
			if (node, right) not in D:
				print("--->",node, right)
				
				
	for i in D:
		max_overlapping = max(max_overlapping, D[i])
		min_overlapping = min(min_overlapping, D[i])
		avg_overlapping += D[i]
	avg_overlapping = avg_overlapping/len(D)
	
	return avg_overlapping, max_overlapping, min_overlapping


def calcNumLoopInNode(L, N):
	# calculate max, min, avg number of loops passing through a node  
	D = [0 for x in  range(N*N)]
	max_intersection = 0
	min_intersection = N*N
	avg_intersection = 0
	
	for loop in L:
		for i in loop:
			D[i] += 1
			
	for i in D:
		max_intersection = max(max_intersection, i)
		min_intersection = min(min_intersection, i)
		avg_intersection += i
	avg_intersection = avg_intersection/len(D)
	
	return avg_intersection, max_intersection, min_intersection

def calcNumLinks(L):
	s = 0
	for i in L:
		s += len(i)
	return s


def shortestDistance(s, t, N, L):
	
	d = N*N
	for l in L:
		if s in l and t in l : 
			i_s = l.index(s) 
			i_t = l.index(t) 
			if i_s < i_t: 
				d = min(d, i_t - i_s )
			else:
				d = min(d, len(l) - i_s + i_t )
	return d

def localDistance(N, L):
	#calc max, average, min for a node x and all nodes around it
	A = []
	for i in range(N):
		B = [] 
		for j in range(N):
			B.append(i*N + j)
		A.append(B)

	
def getStatsHeader():
	return ["NoCSize", "HopCount", "TotalNumLinks", "TotalNumLoops", "avgLoopLength", "avgOverlappingCap", "MaxOverlappingCap", "MinOverlappingCap", "avgCrossCap", "MaxCrossCap", "MinCrossCap"]

def getStats(N, L):
	'''
	Output ordered according to getStatsHeader
	'''
	x = 0.0
	for i in L:
		x += len(i)
	avgLoopLength = x/len(L)
	
	hopCount = round(calcHopCount(N, L), 5)
	numLinks = calcNumLinks(L)
	overLappingCap = calcOverlappingCap(L, N)
	crossCap = calcNumLoopInNode(L, N)
	T = [N, hopCount, numLinks, len(L), avgLoopLength] + list(overLappingCap)+list(crossCap)
	
		
	return T; 

			
			
			
			
			
def printStat(N, L):
	#print(N, "X", N)
	H = getStatsHeader()
	T = getStats(N, L)
	D = {}
	for i in range(len(H)):
		D[H[i]] = T[i]
		
	return D; 

	print("Total number of Loops =",D["TotalNumLoops"])
	print("Average Hop Count =", D["HopCount"])
	print("Total number of Links =", D["TotalNumLinks"])
	print("Average Loop length = ",D["avgLoopLength"])
	print("Overlapping-Cap (avg, min, max) =", D["avgOverlappingCap"], D["MinOverlappingCap"], D["MaxOverlappingCap"]  ) #(avg, max, min)
	print("Cross-Cap (avg, min, max) =", D["avgCrossCap"], D["MinCrossCap"], D["MaxCrossCap"]  ) #(avg, max, min)
	
	







L = [[4, 8, 12, 13, 14, 15, 11, 7, 3, 2, 1, 0],
[0, 1, 5, 9, 13, 12, 8, 4], [0, 1, 2, 6, 10, 14, 13, 12, 8, 4], [1, 2, 3, 7, 11, 15, 14, 13, 9, 5], [2, 3, 7, 11, 15, 14, 10, 6], [0, 1, 2, 3, 7, 6, 5, 4], [4, 5, 6, 7, 11, 10, 9, 8], [8, 9, 10, 11, 15, 14, 13, 12], [0, 1, 2, 6, 10, 9, 8, 4], [1, 2, 3, 7, 11, 10, 9, 5], [4, 5, 6, 10, 14, 13, 12, 8], [5, 6, 7, 11, 15, 14, 13, 9]]

printStat(4, L)