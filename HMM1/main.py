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

    matrices.append(lines[-1][2:])
    return matrices




def main():


    #read data
    data = input()
    data += "\n" + input()
    data += "\n" + input()
    data += "\n" + input()
    print(data)
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


    sequence_of_emissions = handledfile[3]
    init_prob = handledfile[2]
    obs_matrix = handledfile[1]
    trans_matrix = handledfile[0]

    print(sequence_of_emissions)


if __name__ == "__main__":
    main()