#!/usr/bin/env python3


def generateLoop_2D_coordinates(a, b, n, m):
	
	#a,b are upper left corner, n,m are lower right corner
	#2D Coordiantes
	L = []
	i = a
	j = b
	while j < m:
		L.append([i,j])
		j += 1	
	while i < n:
		L.append([i, j])
		i += 1
	while j > b:
		L.append([i,j])
		j -= 1
	while i > a:
		L.append([i,j])
		i -= 1
	return L



def shiftLoop(L, rowShift, colShift):
	A = [] 
	for node in L:
		A.append([node[0]+rowShift, node[1]+colShift])
	return A

def shiftAllLoops(L, rowShift, colShift):
	A = []
	for l in L:
		a = shiftLoop(l, rowShift, colShift)
		A.append(a)
	return A

def convertCordinates(L, N):
	# converts every node in every loop from [a,b] to a*N+b
	# For NxN Network
	
	A = []
	for l in L:
		newL = []
		for node in l:
			newL.append(node[0] * N + node[1])
		A.append(newL)
	return A

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
		
		
		
		
		
		
def greedyReverseOptimize(N, L):
	#Greedy Algorithm to optimize avgHopCount
	#L must not be in 2D coordinate
	
	minHopCount = calcHopCount(N, L)
	T = L[:]
	for i in range(len(T)):
		T[i].reverse() 
		curHopCount = calcHopCount(N, T)
		if curHopCount < minHopCount:
			minHopCount = curHopCount
		else:
			T[i].reverse() 
	return T


def printToFile(N, L, fileName):
	with open(fileName, "w") as f:
		f.write(str(len(L)))
		for i in range(len(L)):
			f.write("\n"+str(i+1)+": "+str(L[i]))
			
			
			
			
			
def printStat(N, L, printHeader):
	#print(N, "X", N)
	
	s = 0.0
	for i in L:
		s += len(i)
	s = s/len(L)
	
	hopCount = round(calcHopCount(N, L), 5)
	numLinks = calcNumLinks(L)
	overLappingCap = calcOverlappingCap(L, N)
	crossCap = calcNumLoopInNode(L, N)
	
	print("Total number of Loops =",len(L))
	print("Average Hop Count =", hopCount)
	print("Total number of Links =", numLinks)
	print("Average Loop length = ",s)
	print("Overlapping-Cap =", overLappingCap) #(avg, max, min)
	print("Maximum loops in a Node =", crossCap) #(avg, max, min)
	
	if printHeader:
		header = "NoCSize, HopCount, TotalNumLinks, TotalNumLoops, avgLoopLength, avgOverlappingCap, MaxOverlappingCap, MinOverlappingCap, avgCrossCap, MaxCrossCap, MinCrossCap"
		T = [N, hopCount, numLinks, len(L), s] + list(overLappingCap)+list(crossCap)
		s = ",".join([str(x) for x in T])
		#print(header)
		print(s)
	return hopCount, numLinks, overLappingCap, crossCap

	