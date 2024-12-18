def read_data(data):
    lines = data.strip().split('\n')
    matrices = []
    i = 0

    while i < len(lines)-1:
        # Read matrix dimensions
        dims = list(map(int, lines[i].split()[:2]))
        rows, cols = dims[0], dims[1]
        values = list(map(float, lines[i].split()[2:]))
        i += 1


        # Read matrix values
        matrix = [values[j:j + cols] for j in range(0, len(values), cols)]
        matrices.append(matrix)



    last_line_values = list(map(int, lines[-1].split()))[1:]
    matrices.append(last_line_values)
    return matrices




def main():


    #read data
    data = input()
    data += "\n" + input()
    data += "\n" + input()
    data += "\n" + input()

    #print(data)


    # Read matrices
    handledfile = read_data(data)

    """
    # Print matrices
    for matrix in matrices:
        for row in matrix:
            print(row)
        print()
    """
    # calc output

    trans_matrix = handledfile[0] #A
    obs_matrix = handledfile[1]   #B  emission matrix
    init_prob = handledfile[2]    #Pi
    sequence_of_emissions = handledfile[3] # output

    A = trans_matrix
    B = obs_matrix
    π = init_prob
    o_seq = sequence_of_emissions





    #print(trans_matrix)
    #print(obs_matrix)
    #print(init_prob)
    #print(sequence_of_emissions)
    #print(obs_matrix)
    #print(init_prob)


    def forward_alg(A, B, π, o_seq):
        observation_0 = o_seq[0]
        a_vector = [None]*len(o_seq)
        a_0 = [None]*len(A)

        for i in range(0,len(A)): #correct
            a_0[i] = float(π[0][i]) * float(B[i][int(observation_0)])
        a_vector[0] = a_0

        for t in range(1,len(o_seq)):
            observation_t = o_seq[t]
            a_t_prev = a_vector[t-1]

            a_t = [None] * len(A)
            for i in range(0,len(A)):
                sum = 0
                for j in range(0,len(A)):
                    sum += float(a_t_prev[j]) * float(A[j][i])
                a_t[i] = sum * float(B[i][int(observation_t)])
            a_vector[t] = a_t

        return a_vector





    a_vector = forward_alg(trans_matrix, obs_matrix, init_prob, sequence_of_emissions)

    output = sum(a_vector[-1])

    #output2 = sum(alpha[-1])
    print(output)

if __name__ == "__main__":

    main()