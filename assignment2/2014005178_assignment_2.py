import math
import os
from konlpy.tag import Twitter

'''
Training Data를 이용해 Dictionary DB를 만드는 함수입니다.
같은 폴더 내에 이미 Dictionary DB가 있는 경우 이 함수를 실행하지 않습니다.
'''

def Learn(input_string):

	f = open(input_string,'r')
	line = f.readline()
	T_DB = []
	S_DB = {}  # 리턴할 Dictionary
	number_of_bad = 0 # 부정적 반응의 리뷰 개수
	number_of_good = 0 # 긍정적 반응의 리뷰 개수
	string_buf = []
	twitter = Twitter()

	while True:
		line = f.readline()
		if not line:
			break
		line = twitter.morphs(line)
		line.pop()	# '\n' 제거
		line[0] = line.pop() #'긍정/부정 점수'를 리스트의 가장 앞쪽으로 옮김
		string_buf = []
		if line[0] == '0':
			number_of_bad += 1
		else:
			number_of_good += 1
		'''
		형태소를 T_DB에 임시로 등록하는 과정, [형태소,부정여부,긍정여부]로 등록.
		ex) '아름다움'이 긍정적 평가에 나타난 경우 ['아름다움',0,1]로 등록
		'''

		for i in range(1,len(line)):
			if line[i] in string_buf: # 하나의 리뷰에서 2개 이상 나오는 단어는 중복하여 사전에 등재하지 않습니다.
				continue
			string_buf.append(line[i])
			if line[0] == '0':
				T_DB.append([line[i],1,0])
			else:
				T_DB.append([line[i],0,1])

	T_DB.sort(reverse=True)
	''' S_DB에 부정적 리뷰 갯수, 긍정적 리뷰 갯수를 먼저 등록함 '''
	S_DB['# of bad,good case'] = [number_of_bad,number_of_good]
	len_db = len(T_DB)
	bad = 0
	good = 0
	string = T_DB[1][0]

	''' T_DB에 중복으로 등록된 형태소들의 갯수를 각각 합하여 하나로 등록한 뒤 S_DB에 등록하는 과정 '''
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

''' Training Data(S_DB)를 기반으로 input file의 긍정/부정을 분류 '''

def Calculate(input_string,S_DB):

	f = open(input_string,'r')
	line = f.readline()

	number_of_bad = S_DB['# of bad,good case'][0]
	number_of_good = S_DB['# of bad,good case'][1]

	sum_of_bad = 0
	sum_of_good = 0
	string_buf = []
	R_DB = []
	twitter = Twitter()
	prob_bad = math.log((number_of_bad/(number_of_good+number_of_bad))) # 전체 리뷰 중 부정적 리뷰의 비율(log scale)
	prob_good = math.log((number_of_good/(number_of_good+number_of_bad))) # 전체 리뷰 중 긍정적 리뷰의 비율(log scale)

	while True:
		line = f.readline()
		line_original = line.rstrip()
		if not line:
			break
		line = twitter.morphs(line)
		line.pop() #\n 제거

		string_buf = []
		sum_of_bad = 1
		sum_of_good = 1

		for j in range(1,len(line)):
			if line[j] in string_buf: # 한 리뷰에서 중복된 단어는 확률에 반영하지 않습니다.
				continue
			string_buf.append(line[j])
			buf = S_DB.get(line[j])

			if buf == None: # 사전에 있지 않은 단어는 무시합니다.
				continue

			p_bad = math.log(buf[0]+1) - math.log(number_of_bad)
			# 사전에 있는 단어 중 빈도수가 0인 경우 log scale에서 제대로 된 값이 나오지 않기 때문에 1을 더해줍니다.
			p_good = math.log(buf[1]+1) - math.log(number_of_good)
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

''' S_DB의 내용을 바탕으로 'output_string'이라는 이름의 파일을 작성하는 함수입니다.'''
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
''' 최종 결과(리뷰의 긍정/부정 분류)를 'output_string'이라는 이름의 파일로 작성하는 함수입니다.'''
def Export_Result(output_string,R_DB):

	fw = open(output_string,'w')
	fw.write('id	document	label\n')
	for x in R_DB:
		fw.write(x[0])
		fw.write('	')
		fw.write(str(x[1]))
		fw.write('\n')
	fw.close()

''' S_DB를 저장한 파일이 있는 경우, 이를 import하는 함수입니다. '''
def Import_Dictionary(input_string):
	f = open(input_string,'r')
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
