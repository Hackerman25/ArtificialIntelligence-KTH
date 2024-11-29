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



def matrixmult(a,b):
    output = [[0] * len(b[0])]*len(a)
    #print(output)

    for i in range(len(a)):

        for j in range(len(b[0])):

            for k in range(len(b)):

                output[i][j] += a[i][k] * b[k][j]

    for i in range(len(output)):
        for j in range(len(output[0])):
            output[i][j] = round(output[i][j],2)

    return output


def main():


    #read data
    data = input()
    data += "\n" + input()
    data += "\n" + input()
    #print(data)


    # Read matrices
    matrices = read_matrices(data)

    """
    # Print matrices
    for matrix in matrices:
        for row in matrix:
            print(row)
        print()
    """
    # calc output

    init_prob = matrices[2]
    obs_matrix = matrices[1]
    trans_matrix = matrices[0]


    ans = matrixmult(init_prob, trans_matrix)
    prob_dist = matrixmult(ans, obs_matrix)

    nrows = len(prob_dist)

    try:
        ncols = len(prob_dist[0])
    except:
        ncols = 1

    [prob_dist_with_shape] = prob_dist
    prob_dist_with_shape.insert(0,ncols)
    prob_dist_with_shape.insert(0, nrows)

    #transition matrix = matrix of prob to go from state to other state
    #emission matrix   = matrix of prob to get to observed based on state
    # initial state probability distribution = initial states prob

    print(*prob_dist_with_shape, sep=" ")




if __name__ == "__main__":
    main()