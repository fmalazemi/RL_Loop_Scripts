#!/usr/bin/env python3

'''
Use RoutingTable(N, L) to generate routing Table, 
All other functions are used by RoutingTable. 

I will create another one to save directly to file. 


'''

def findLoopsXY(NoCSize, L, D, x, y):
	#L all loops
	#D dict() split loops according to layers
	#x,y nodes
	
	xLayer = nodeLayer(NoCSize, x)
	yLayer = nodeLayer(NoCSize, y)
	curLayer = max(xLayer, yLayer)
	
	s = {}
#	for loopIndex in range(len(L)):
	
	for loopIndex in D[curLayer]:
		curL = L[loopIndex]
		
		if x in curL and y in curL:
			x_index = curL.index(x)
			y_index = curL.index(y) 
			distance = 0
			if x_index < y_index:
				distance = y_index-x_index 
				
			else:
				distance = len(curL) - (x_index-y_index)
				
				
			if distance not in s:
				s[distance] = set()
			s[distance].add(loopIndex+1)
	x = [] 
	for i in sorted(s.keys()):
		x += list(s[i])
	return x


def nodeLayer(NoCSize, x):
	p = [0, NoCSize-1]
	curLayer = NoCSize//2
	r = x//NoCSize 
	c = x%NoCSize 
	while p[0] < p[1]:
		if r in p or c in p:
			return curLayer 
		p[0] += 1
		p[1] -= 1
		curLayer-=1
	return -1

def splitLoopsIntoLayers(NoCSize, L):
	A = dict()
	for i in range(1, NoCSize//2+1):
		A[i] = []
	for loopIndex in range(len(L)):
		maxLayer = -1
		for x in L[loopIndex]:
			maxLayer = max(maxLayer, nodeLayer(NoCSize, x))
		A[maxLayer].append(loopIndex)
	return A

def RoutingTable(NoCSize, L):
	totalNodes = NoCSize*NoCSize 
	loopsMap = splitLoopsIntoLayers(NoCSize, L)
	print(len(L))
	for i in range(len(L)):
		x = i+1
		print(f'{x}: {L[i]}')
	print(totalNodes)
	for i in range(totalNodes):
		print(i)
		for j in range(totalNodes):
			if i == j:
				print(f'{i}: []')
			else:
				A = findLoopsXY(NoCSize, L, loopsMap, i, j)
				print(f'{j}: {A}') 
				if len(A) == 0:
					print("Error", i, j, A)
					return 

def RoutingTableToFile(NoCSize, L, F):
	totalNodes = NoCSize * NoCSize
	loopsMap = splitLoopsIntoLayers(NoCSize, L)
	
	with open(F, "w") as file:
		file.write(f"{len(L)}\n")
		
		for i in range(len(L)):
			x = i + 1
			file.write(f"{x}: {L[i]}\n")
			
		file.write(f"{totalNodes}\n")
		
		for i in range(totalNodes):
			file.write(f"{i}\n")
			
			for j in range(totalNodes):
				if i == j:
					file.write(f"{i}: []\n")
				else:
					A = findLoopsXY(NoCSize, L, loopsMap, i, j)
					file.write(f"{j}: {A}\n")
					
					if len(A) == 0:
						file.write(f"Error {i} {j} {A}\n")
						print("Error: Loop are incorrect!")
						return