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



    last_line_values = list(map(int, lines[-1].split()))[2:]
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


    print(trans_matrix)
    print(obs_matrix)
    print(init_prob)
    print(sequence_of_emissions)
    #print(obs_matrix)
    #print(init_prob)


    def forward_alg(trans_matrix,obs_matrix,init_prob,sequence_of_emissions):

        observation_0 = sequence_of_emissions[0]




        a_vector = [None]*len(sequence_of_emissions)
        a_0 = [None]*len(trans_matrix)


        for i in range(0,len(trans_matrix)): #correct

            a_0[i] = int(init_prob[0][i]) * obs_matrix[i][int(observation_0)]
        a_vector[0] = a_0





        for t in range(1,len(sequence_of_emissions)):

            observation_t = sequence_of_emissions[t]


            a_t_prev = a_vector[t-1]

            a_t = [None] * len(trans_matrix)
            for i in range(0,len(trans_matrix)):
                sum = 0
                for j in range(0,len(trans_matrix)):
                    sum += a_t_prev[j] * trans_matrix[j][i]

                a_t[i] = sum * obs_matrix[i][observation_t]

            a_vector[t] = a_t


        """
        alpha = [[init_prob[0][i] * obs_matrix[i][sequence_of_emissions[0]] for i in range(len(init_prob[0]))]]
        for t in range(1, len(sequence_of_emissions)):
            alpha.append([sum([alpha[t - 1][j] * trans_matrix[j][i]
                for j in range(len(trans_matrix))]) * obs_matrix[i][sequence_of_emissions[t]] for i in range(len(trans_matrix))])
        """

        return a_vector




    a_vector = forward_alg(trans_matrix, obs_matrix, init_prob, sequence_of_emissions)

    output = sum(a_vector[-1])

    #output2 = sum(alpha[-1])
    print(output,"output")

if __name__ == "__main__":

    main()