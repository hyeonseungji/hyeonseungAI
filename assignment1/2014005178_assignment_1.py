import queue
def map_import(input_string):

	i = 0
	j = 0

	f = open(input_string,'r')
	line = f.readline()
	line = line.split()
	a = int(line[0])

	size_x = int(line[1])
	size_y = int(line[2])
	input_map = [[0]*size_y for i in range(size_x)]
	i = 0

	for i in range(size_x):
		line = f.readline()
		line = line.split()
		for j in range(size_y):
			input_map[i][j] = int(line[j])
		j = 0
	f.close()
	return input_map

def map_export(output_string,input_map,result_i,result_j):

	fw = open(output_string,'w')
	for i in range(len(input_map)):
		for j in range(len(input_map[0])):
			data = "%d " % input_map[i][j]
			fw.write(data)
		fw.write('\n')
	fw.write('---\n')
	fw.write("length=%d\n" % result_j)
	fw.write("time=%d\n" % result_i)
	fw.close()

def DFS(state,input_map,output_map,stack,goal):

	size_x = len(input_map)
	size_y = len(input_map[0])

	x = state[0]
	y = state[1]

	initial_state = state

	past_x = initial_state[0]
	past_y = initial_state[1]

	i = 0

	while input_map[x][y] != goal: 
		i = i + 1
		if output_map[x][y] != 0: # past_x, past_y means parent state in tree 
			past_x = output_map[x][y][1]
			past_y = output_map[x][y][2]

		if y > 0: # left
			if input_map[x][y-1] != 1: 
				if past_x != x or past_y != y-1: # For forbiding to go back parent state
					if output_map[x][y-1] == 0:
						stack.append([x,y-1])
						output_map[x][y-1] = [0,x,y]
		if x > 0: # up
			if input_map[x-1][y] != 1:
				if past_x != x-1 or past_y != y:
					if output_map[x-1][y] == [0,x,y] or output_map[x-1][y] == 0:
						stack.append([x-1,y])
						output_map[x-1][y] = [1,x,y]
		if x < size_x-1: # down
			if input_map[x+1][y] != 1:
				if past_x != x+1 or past_y != y:
					if output_map[x+1][y] == [1,x,y] or output_map[x+1][y] == [0,x,y] or output_map[x+1][y] == 0:
						stack.append([x+1,y])
						output_map[x+1][y] = [2,x,y]
		if y < size_y-1: # right
			if input_map[x][y+1] != 1:
				if past_x != x or past_y != y+1:	
					if output_map[x][y+1] != [3,x,y]:
						stack.append([x,y+1])
						output_map[x][y+1] = [3,x,y]

		if len(stack) == 0:
				return -1
		state = stack.pop()
		x = state[0]
		y = state[1]

	answer = [x,y,i+1]
	if goal == 6:
		input_map[x][y] = 5

	j = 0
	while state != initial_state:
		x = state[0]
		y = state[1]
		state[0] = output_map[x][y][1]
		state[1] = output_map[x][y][2]
		if state != initial_state:
			input_map[state[0]][state[1]] = 5
		j = j + 1
	answer.append(j)

	return answer

def DeepS(state,input_map,output_map,stack,goal):

	size_x = len(input_map)
	size_y = len(input_map[0])

	x = state[0]
	y = state[1]

	initial_state = state

	past_x = initial_state[0]
	past_y = initial_state[1]

	i = 0
	k = 0
	limit_count = 0
	limit = 1

	while input_map[x][y] != goal:
		k = 0 
		i = i + 1
		if limit_count == limit:
			if len(stack) == 0:
				limit += 1
				x = initial_state[0]
				y = initial_state[1]
				past_x = x
				past_y = y
				output_map = [[0]*size_y for k in range(size_x)]
				limit_count = 0
				continue

			state = stack.pop()
			x = state[0]
			y = state[1]
			limit_count = output_map[x][y][3]
			continue

		if output_map[x][y] != 0: # past_x, past_y means parent state in tree 
			past_x = output_map[x][y][1]
			past_y = output_map[x][y][2]

		if y > 0: # left
			if input_map[x][y-1] != 1: 
				if past_x != x or past_y != y-1: # For forbiding to go back parent state
					if output_map[x][y-1] == 0:
						stack.append([x,y-1])
						output_map[x][y-1] = [0,x,y,limit_count+1]
		if x > 0: # up
			if input_map[x-1][y] != 1:
				if past_x != x-1 or past_y != y:
					if output_map[x-1][y] == [0,x,y] or output_map[x-1][y] == 0:
						stack.append([x-1,y])
						output_map[x-1][y] = [1,x,y,limit_count+1]
		if x < size_x-1: # down
			if input_map[x+1][y] != 1:
				if past_x != x+1 or past_y != y:
					if output_map[x+1][y] == [1,x,y] or output_map[x+1][y] == [0,x,y] or output_map[x+1][y] == 0:
						stack.append([x+1,y])
						output_map[x+1][y] = [2,x,y,limit_count+1]
		if y < size_y-1: # right
			if input_map[x][y+1] != 1:
				if past_x != x or past_y != y+1:	
					if output_map[x][y+1] != [3,x,y]:
						stack.append([x,y+1])
						output_map[x][y+1] = [3,x,y,limit_count+1]

		if len(stack) == 0:
			limit += 1
			x = initial_state[0]
			y = initial_state[1]
			past_x = initial_state[0]
			past_y = initial_state[1]
			output_map = [[0]*size_y for k in range(size_x)]
			limit_count = 0
			continue

		state = stack.pop()
		x = state[0]
		y = state[1]
		limit_count = output_map[x][y][3]

	answer = [x,y,i+1]
	if goal == 6:
		input_map[x][y] = 5

	j = 0
	while state != initial_state:
		x = state[0]
		y = state[1]
		state[0] = output_map[x][y][1]
		state[1] = output_map[x][y][2]
		if state != initial_state:
			input_map[state[0]][state[1]] = 5
		j = j + 1
	answer.append(j)

	return answer

def Heuristic(input_map,goal):
	size_x = len(input_map)
	size_y = len(input_map[0])
	i = 0 
	k = 0
	j = 0 
	l = 0

	heuristic = [[0]*size_y for i in range(size_x)]
	i = 0

	for i in range(size_x):
		for j in range(size_y):
			if input_map[i][j] == goal:
				break
	
	for k in range(size_x):
		for l in range(size_y):
			heuristic[k][l] = abs(k-i) + abs(l-j)
	
	return heuristic

def Greedy(state,input_map,output_map,goal):

	size_x = len(input_map)
	size_y = len(input_map[0])

	x = state[0]
	y = state[1]

	t = 0

	initial_state = state

	past_x = initial_state[0]
	past_y = initial_state[1]

	heuristic = Heuristic(input_map,goal)

	i = 0
	result = []

	while input_map[x][y] != goal:
		i = i + 1 
		if output_map[x][y] == 0: 
			output_map[x][y] = [past_x,past_y,0]
		if output_map[x][y] != 0:
			output_map[x][y][0] = past_x
			output_map[x][y][1] = past_y
			

		if y < size_y-1: # right
			if input_map[x][y+1] != 1:
				if x != past_x or y+1 != past_y:
					if output_map[x][y][2] % 10 != 1:
						result.append([heuristic[x][y+1],x,y+1,0])
						
		if x < size_x-1: # down
			if input_map[x+1][y] != 1:
				if x+1 != past_x or y != past_y:
					if int((output_map[x][y][2]%100)/10) != 1:
						result.append([heuristic[x+1][y],x+1,y,1])
						
		if x > 0: # up
			if input_map[x-1][y] != 1:
				if x-1 != past_x or y != past_y:
					if int((output_map[x][y][2]%1000)/100) != 1:
						result.append([heuristic[x-1][y],x-1,y,2])
						
		if y > 0: # left
			if input_map[x][y-1] != 1: 
				if x != past_x or y-1 != past_y:
					if int((output_map[x][y][2]%10000)/1000) != 1:
						result.append([heuristic[x][y-1],x,y-1,3])
							


		result.sort(reverse=True)
		result_state = result.pop()
		state = [result_state[1],result_state[2]]
		direction = result_state[3]
		x = state[0]
		y = state[1]
		if direction == 0:
			past_x = x
			past_y = y-1
			output_map[past_x][past_y][2] += 1
		elif direction == 1:
			past_x = x-1
			past_y = y
			output_map[past_x][past_y][2] += 10
		elif direction == 2:
			past_x = x+1
			past_y = y
			output_map[past_x][past_y][2] += 100
		elif direction == 3:
			past_x = x
			past_y = y+1
			output_map[past_x][past_y][2] += 1000
		else:
			print ('error!')

		if output_map[x][y] == 0: 
			output_map[x][y] = [past_x,past_y,0]

		#print('(%d %d)' %(x,y))

	answer = [x,y,i+1]

	if goal == 6:
		input_map[x][y] = 5
	j = 0
	while state != initial_state:
		x = state[0]
		y = state[1]
		state[0] = output_map[x][y][0]
		state[1] = output_map[x][y][1]
		if state != initial_state:
			input_map[state[0]][state[1]] = 5
		j = j + 1

	answer.append(j)
		
	return answer

def A_star(state,input_map,output_map,goal):

	size_x = len(input_map)
	size_y = len(input_map[0])

	x = state[0]
	y = state[1]

	t = 0

	initial_state = state

	past_x = initial_state[0]
	past_y = initial_state[1]

	heuristic = Heuristic(input_map,goal)

	i = 0
	result = []

	while input_map[x][y] != goal:
		i = i + 1 
		if output_map[x][y] == 0: 
			output_map[x][y] = [past_x,past_y,0,0]

		if output_map[x][y] != 0:
			output_map[x][y][0] = past_x
			output_map[x][y][1] = past_y
			if x != initial_state[0] and y != initial_state[1]:
				output_map[x][y][3] = output_map[past_x][past_y][3] + 1
			
		r = output_map[x][y][3]

		if y < size_y-1: # right
			if input_map[x][y+1] != 1:
				if x != past_x or y+1 != past_y:
					if output_map[x][y][2] % 10 != 1:
						result.append([r+heuristic[x][y+1],x,y+1,0])
						
		if x < size_x-1: # down
			if input_map[x+1][y] != 1:
				if x+1 != past_x or y != past_y:
					if int((output_map[x][y][2]%100)/10) != 1:
						result.append([r+heuristic[x+1][y],x+1,y,1])
						
		if x > 0: # up
			if input_map[x-1][y] != 1:
				if x-1 != past_x or y != past_y:
					if int((output_map[x][y][2]%1000)/100) != 1:
						result.append([r+heuristic[x-1][y],x-1,y,2])
						
		if y > 0: # left
			if input_map[x][y-1] != 1: 
				if x != past_x or y-1 != past_y:
					if int((output_map[x][y][2]%10000)/1000) != 1:
						result.append([r+heuristic[x][y-1],x,y-1,3])
							


		result.sort(reverse=True)
		result_state = result.pop()
		state = [result_state[1],result_state[2]]
		direction = result_state[3]
		x = state[0]
		y = state[1]
		if direction == 0:
			past_x = x
			past_y = y-1
			output_map[past_x][past_y][2] += 1
		elif direction == 1:
			past_x = x-1
			past_y = y
			output_map[past_x][past_y][2] += 10
		elif direction == 2:
			past_x = x+1
			past_y = y
			output_map[past_x][past_y][2] += 100
		elif direction == 3:
			past_x = x
			past_y = y+1
			output_map[past_x][past_y][2] += 1000
		else:
			print ('error!')

		if output_map[x][y] == 0: 
			output_map[x][y] = [past_x,past_y,0,0]


	answer = [x,y,i+1]

	if goal == 6:
		input_map[x][y] = 5
	j = 0
	while state != initial_state:
		x = state[0]
		y = state[1]
		state[0] = output_map[x][y][0]
		state[1] = output_map[x][y][1]
		if state != initial_state:
			input_map[state[0]][state[1]] = 5
		j = j + 1

	answer.append(j)
		
	return answer
def BFS(state,input_map,output_map,goal):

	size_x = len(input_map)
	size_y = len(input_map[0])

	x = state[0]
	y = state[1]

	initial_state = state

	past_x = initial_state[0]
	past_y = initial_state[1]
	
	que = queue.Queue()

	i = 0

	while input_map[x][y] != goal:
		i = i + 1 
		if output_map[x][y] != 0: # past_x, past_y means parent state in tree 
			past_x = output_map[x][y][1]
			past_y = output_map[x][y][2]

		if y < size_y-1: # right
			if input_map[x][y+1] != 1:
				if past_x != x or past_y != y+1:	
					if output_map[x][y+1] == 0:
						que.put([x,y+1])
						output_map[x][y+1] = [0,x,y]

		if x < size_x-1: # down
			if input_map[x+1][y] != 1:
				if past_x != x+1 or past_y != y:
					if output_map[x+1][y] == [0,x,y] or output_map[x+1][y] == 0:
						que.put([x+1,y])
						output_map[x+1][y] = [1,x,y]
		if x > 0: # up
			if input_map[x-1][y] != 1:
				if past_x != x-1 or past_y != y:
					if output_map[x-1][y] == [1,x,y] or output_map[x-1][y] == [0,x,y] or output_map[x-1][y] == 0:
						que.put([x-1,y])
						output_map[x-1][y] = [2,x,y]
		if y > 0: # left
			if input_map[x][y-1] != 1: 
				if past_x != x or past_y != y-1: # For forbiding to go back parent state
					if output_map[x][y-1] != [3,x,y]:
						que.put([x,y-1])
						output_map[x][y-1] = [3,x,y]

		if que.qsize() == 0:
				return -1

		state = que.get()
		x = state[0]
		y = state[1]

	answer = [x,y,i+1]
	if goal == 6:
		input_map[x][y] = 5
	j = 0
	while state != initial_state:
		x = state[0]
		y = state[1]
		state[0] = output_map[x][y][1]
		state[1] = output_map[x][y][2]
		if state != initial_state:
			input_map[state[0]][state[1]] = 5
		j = j + 1

	answer.append(j)
		
	return answer

def first_floor():

	input_map = map_import('first_floor_input.txt')
	size_x = len(input_map)
	size_y = len(input_map[0])

	i = 0

	for i in range(size_y):
		if input_map[0][i] == 3:
			state = [0,i]
			break
	if i == size_y:
		return -1
	i = 0
	
	stack = []
	output_map = [[0]*size_y for i in range(size_x)]
	result = DFS(state,input_map,output_map,stack,6)
	state = [result[0],result[1]]
	result_i = result[2]
	result_j = result[3]

	stack2 = []
	output_map = [[0]*size_y for i in range(size_x)]
	result = DFS(state,input_map,output_map,stack2,4)
	result_i += result[2]
	result_j += result[3]
	
	map_export('first_floor_output.txt',input_map,result_i,result_j)

def second_floor():

	input_map = map_import('second_floor_input.txt')
	size_x = len(input_map)
	size_y = len(input_map[0])

	i = 0

	for i in range(size_y):
		if input_map[0][i] == 3:
			state = [0,i]
			break
	if i == size_y:
		return -1
	i = 0
	
	stack = []
	output_map = [[0]*size_y for i in range(size_x)]
	result = DFS(state,input_map,output_map,stack,6)
	state = [result[0],result[1]]
	result_i = result[2]
	result_j = result[3]

	stack2 = []
	output_map = [[0]*size_y for i in range(size_x)]
	result = DFS(state,input_map,output_map,stack2,4)
	result_i += result[2]
	result_j += result[3]
	
	map_export('second_floor_output.txt',input_map,result_i,result_j)

def third_floor():

	input_map = map_import('third_floor_input.txt')
	size_x = len(input_map)
	size_y = len(input_map[0])

	i = 0

	for i in range(size_y):
		if input_map[0][i] == 3:
			state = [0,i]
			break
	if i == size_y:
		return -1
	i = 0
	
	stack = []
	output_map = [[0]*size_y for i in range(size_x)]
	result = DFS(state,input_map,output_map,stack,6)
	state = [result[0],result[1]]
	result_i = result[2]
	result_j = result[3]

	stack2 = []
	output_map = [[0]*size_y for i in range(size_x)]
	result = DFS(state,input_map,output_map,stack2,4)
	result_i += result[2]
	result_j += result[3]
	
	map_export('third_floor_output.txt',input_map,result_i,result_j)

def fourth_floor():

	input_map = map_import('fourth_floor_input.txt')
	size_x = len(input_map)
	size_y = len(input_map[0])

	i = 0

	for i in range(size_y):
		if input_map[0][i] == 3:
			state = [0,i]
			break
	if i == size_y:
		return -1
	i = 0
	
	output_map = [[0]*size_y for i in range(size_x)]
	result = Greedy(state,input_map,output_map,6)
	state = [result[0],result[1]]
	result_i = result[2]
	result_j = result[3]

	output_map = [[0]*size_y for i in range(size_x)]
	result = Greedy(state,input_map,output_map,4)
	result_i += result[2]
	result_j += result[3]
	
	map_export('fourth_floor_output.txt',input_map,result_i,result_j)

def fifth_floor():

	input_map = map_import('fifth_floor_input.txt')
	size_x = len(input_map)
	size_y = len(input_map[0])

	i = 0

	for i in range(size_y):
		if input_map[0][i] == 3:
			state = [0,i]
			break
	if i == size_y:
		return -1
	i = 0
	
	output_map = [[0]*size_y for i in range(size_x)]
	result = Greedy(state,input_map,output_map,6)
	state = [result[0],result[1]]
	result_i = result[2]
	result_j = result[3]

	output_map = [[0]*size_y for i in range(size_x)]
	result = Greedy(state,input_map,output_map,4)
	result_i += result[2]
	result_j += result[3]
	
	map_export('fifth_floor_output.txt',input_map,result_i,result_j)

first_floor()
second_floor()
third_floor()
fourth_floor()
fifth_floor()
