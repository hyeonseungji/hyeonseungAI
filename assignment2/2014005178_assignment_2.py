import math
import os
from konlpy.tag import Twitter

def Learn(input_string):

	f = open(input_string,'r')
	line = f.readline()
	T_DB = []
	S_DB = {} 
	number_of_bad = 0
	number_of_good = 0
	string_buf = []
	twitter = Twitter()

	while True:
		line = f.readline()
		if not line:
			break
		line = twitter.morphs(line)
		line.pop()
		line[0] = line.pop()
		string_buf = []
		if line[0] == '0':
			number_of_bad += 1
		else:
			number_of_good += 1

		for i in range(1,len(line)):
			if line[i] in string_buf:
				continue
			string_buf.append(line[i])
			if line[0] == '0':
				T_DB.append([line[i],1,0])
			else:
				T_DB.append([line[i],0,1])

	T_DB.sort(reverse=True)
	S_DB['# of bad,good case'] = [number_of_bad,number_of_good]
	len_db = len(T_DB)
	bad = 0
	good = 0
	string = T_DB[1][0]

	for i in range(1,len_db-1):
		buf = T_DB[i][0]
		if string == buf:
			bad += T_DB[i][1]
			good += T_DB[i][2]
			if i != len_db-1:
				continue
		else:
			S_DB[string] = [bad,good]
			string = buf
			bad = T_DB[i][1]
			good = T_DB[i][2]

		if i == len_db-1:
			if bad != 0 and good != 0:
				S_DB[string] = [bad,good]

	f.close()
	return S_DB

def Calculate(input_string,S_DB):

	f = open(input_string,'r')
	line = f.readline()

	number_of_bad = S_DB['# of bad,good case'][0]
	number_of_good = S_DB['# of bad,good case'][1]

	number_of_dict = len(S_DB)-1
	s = number_of_dict
	sum_of_bad = 0
	sum_of_good = 0
	string_buf = []
	R_DB = []
	twitter = Twitter()
	prob_bad = (number_of_bad/(number_of_good+number_of_bad))
	prob_good = (number_of_good/(number_of_good+number_of_bad))

	while True:
		line = f.readline()
		line_original = line.rstrip()
		if not line:
			break
		line = twitter.morphs(line)
		line.pop()

		string_buf = []
		sum_of_bad = 1
		sum_of_good = 1

		for j in range(1,len(line)):
			if line[j] in string_buf:
				continue
			string_buf.append(line[j])
			buf = S_DB.get(line[j])

			if buf == None:
				continue
			n = buf[0] + buf[1]
			p_bad = math.log(buf[0]+1) - math.log(s+n)
			p_good = math.log(buf[1]+1) - math.log(s+n)
			sum_of_bad += p_bad
			sum_of_good += p_good

		sum_of_bad += prob_bad
		sum_of_good += prob_good
		if sum_of_bad > sum_of_good:
			R_DB.append([line_original,0])
		elif sum_of_good > sum_of_bad:
			R_DB.append([line_original,1])
		else:
			R_DB.append([line_original,-1])

	f.close()

	return R_DB

def Export_Dictionary(output_string,S_DB):

	fw = open(output_string,'w')
	for x in S_DB.keys():
		data_bad = S_DB[x][0]
		data_good = S_DB[x][1]
		fw.write(x)
		fw.write(' ')
		fw.write(str(data_bad))
		fw.write(' ')
		fw.write(str(data_good))
		fw.write(' ')
		fw.write(str(len(x)))
		fw.write('\n')
	fw.close()

def Export_Result(output_string,R_DB):

	fw = open(output_string,'w')
	for x in R_DB:
		fw.write(x[0])
		fw.write('	')
		fw.write(str(x[1]))
		fw.write('\n')
	fw.close()

def Import_Dictionary(output_string):
	f = open(output_string,'r')
	S_DB={}
	while True:
		line = f.readline()
		if not line:
			break
		line_split = line.split()
		len_string = int(line_split[len(line_split)-1])
		good = int(line_split[len(line_split)-2])
		bad = int(line_split[len(line_split)-3])
		string = line[0:len_string]
		S_DB[string] = [bad,good]
	f.close()
	return S_DB
	
path_twitter = 'dictionary_twitter.txt'
path = path_twitter

if os.path.exists(path) == False:
	S_DB = Learn('ratings_train.txt')
	Export_Dictionary(path,S_DB)
else:
	S_DB = Import_Dictionary(path)

R_DB = Calculate('ratings_test.txt',S_DB)
Export_Result('ratings_result.txt',R_DB)
