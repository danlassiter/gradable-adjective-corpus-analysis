import string
import random
import math

lines = [line.rstrip('\n') for line in open('web1t-contextual-rescaling-pmi.csv', 'r').readlines()]

mods = lines[0].replace('"', '').split(',')[1:]
adjs = []
values = []

hist = {}

for line in lines[1:]:
	line_split = line.replace('"', '').split(',')
	adjs.append(line_split[0])
	value_list = [float(val) for val in line_split[1:]]
	values.append(value_list)
	
	for value in value_list:
		floored = math.floor(value)
		if floored in hist:
			hist[floored] += 1
		else:
			hist[floored] = 1
	
#print hist

num_mod = len(mods)
num_adj = len(values)

#print str(num_mod) + ' ' + str(len(mods))
#print str(num_adj) + ' ' + str(len(adjs))

used_stimuli = set([])
num_stimuli = 100
my_count = 0

fout = open('stimuli.js', 'w')

def add_stimuli(f, cur_max, my_count):
	cur_count = 0
	while cur_count < cur_max:
		mod = random.randint(0, num_mod - 1)
		adj = random.randint(0, num_adj - 1)
		ser = str(mod) + ',' + str(adj)

		if ser in used_stimuli:
			continue

		if not f(values[adj][mod]): 
			continue
			
		used_stimuli.add(ser)
		fout.write('{{"trial": {0}, "isCatch": 0, "phrase": "This is {1} {2}."}}, // {3}\n'.format(my_count, mods[mod], adjs[adj], values[adj][mod]))

		cur_count += 1
		my_count += 1
	
	return my_count
	
my_count = add_stimuli(lambda x: math.floor(x) <= -4, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == -3, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == -2, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == -1, 10, my_count)
my_count = add_stimuli(lambda x: x == 0, 5, my_count)
my_count = add_stimuli(lambda x: x != 0 and math.floor(x) == 0, 5, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == 1, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == 2, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == 3, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) == 4, 10, my_count)
my_count = add_stimuli(lambda x: math.floor(x) >= 5, 10, my_count)


	
fout.write('{{"trial": {0}, "isCatch": 2, "phrase": "Please select 2"}},\n'.format(my_count))
fout.write('{{"trial": {0}, "isCatch": 6, "phrase": "Please select 6"}}\n'.format(my_count + 1))
fout.close()

