def read_matrices(data):
    lines = data.strip().split('\n')
    matrices = []
    i = 0

    while i < len(lines):
        # Read matrix dimensions
        dims = list(map(int, lines[i].split()[:2]))
        rows, cols = dims[0], dims[1]
        values = list(map(float, lines[i].split()[2:]))
        i += 1

        # Read matrix values
        matrix = [values[j:j + cols] for j in range(0, len(values), cols)]
        matrices.append(matrix)

    return matrices

# Example input data
data = """4 4 0.2 0.5 0.3 0.0 0.1 0.4 0.4 0.1 0.2 0.0 0.4 0.4 0.2 0.3 0.0 0.5
4 3 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.2 0.6 0.2
1 4 0.0 0.0 0.0 1.0"""

# Read matrices
matrices = read_matrices(data)

# Print matrices
for matrix in matrices:
    for row in matrix:
        print(row)
    print()


# calc output

ProbObsEachObs= []


i = 0

for i in range(len(matrices[2][0])):
    tmp = 0
    for e in range(len(matrices[0])):
        #print(matrices[0][i][e] , matrices[2][0][i])
        tmp = tmp + matrices[0][e][i] * matrices[2][0][e]
    ProbObsEachObs.append(tmp)

#print(ProbObsEachObs)


ans= []
for i in range(len(matrices[1][0])):
    tmp = 0
    #print(len(matrices[1]),"dkdkd")
    for e in range(len(matrices[1])):

        tmp = tmp + matrices[1][e][i] * ProbObsEachObs[e]
        #tmp = tmp + matrices[0][e][i] * matrices[2][0][e]
    ans.append(round(tmp,2))

print(ans)
#transition matrix = matrix of prob to go from state to other state
#emission matrix   = matrix of prob to get to observed based on state
# initial state probability distribution = initial states prob

#output =