def get_data(line):
    line = line[:len(line)-1]
    temp = line.split(";")
    return float(temp[0]), float(temp[1]), float(temp[2])

def isKey(key, mydict):
    if key in mydict:
        return True
    return False


f = open("../results/simulated_mult_sum_avg.csv")
l = f.readline()  # omit first line


keys = list()
lines = f.readlines()
num_to_index = dict()

current_index = 0

heatmap = open("keys.csv", "w")
for line in lines:
    c_xnor, c_summation, _ = get_data(line)
    if not isKey(c_xnor, num_to_index):
        num_to_index[c_xnor] = current_index
        keys.append(c_xnor)
        current_index += 1

    if not isKey(c_summation, num_to_index):
        num_to_index[c_summation] = current_index
        keys.append(c_summation)
        current_index += 1

for k in keys:
    heatmap.write(str(k)+";" + str(k)+"\n")

heatmap2 = open("matrix.csv", "w")
matrix = [[0 for x in range(len(keys))] for y in range(len(keys))]

c_i = 0
c_j = 0
for line in lines:
    c_xnor, c_summation, precision = get_data(line)
    if c_j >= len(keys):
        c_j = 0
        c_i += 1
    # print(c_j, num_to_index[c_xnor], c_xnor)
    assert(c_j == num_to_index[c_xnor])
    assert(c_i == num_to_index[c_summation])
    matrix[c_i][c_j] = precision
    c_j+=1


for row in matrix:
    temp = ""
    for column in row:
        if len(temp) != 0:
            temp += ";"
        temp += str(round(column, 3))
    temp += "\n"
    heatmap2.write(temp)

f.close()
heatmap.close()
heatmap2.close()