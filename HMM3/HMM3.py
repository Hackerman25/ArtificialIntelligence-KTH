import math
import sys


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


# HMM3 -----------------------------------------------------------------------------------
# Input: The transition matrix A, the observation matrix B,
#        the initial state distribution π and the observation sequence o_seq.
# Output: A vector α_vector containing all the alphas.
def forward_alg2(A, B, π, o_seq):
    scale_factor = 0
    scale_sum = []
    observation_0 = o_seq[0]
    alpha_matrix = [[0] * len(A) for _ in range(len(o_seq))]


    for i in range(0, len(A)):
        alpha_matrix[0][i] = float(π[0][i]) * float(B[i][int(observation_0)])
        scale_factor = scale_factor + alpha_matrix[0][i]
    scale_factor = 1 / scale_factor
    scale_sum.append(scale_factor)

    for i in range(0, len(A)):
        alpha_matrix[0][i] = alpha_matrix[0][i] * scale_factor

    for t in range(1, len(o_seq)):
        observation_t = o_seq[t]


        scale_factor_t = 0
        for i in range(0, len(A)):
            alpha_matrix[t][i] = 0
            for j in range(0, len(A)):


                alpha_matrix[t][i] += alpha_matrix[t-1][j] * float(A[j][i])
            alpha_matrix[t][i] = alpha_matrix[t][i] * float(B[i][int(observation_t)])
            scale_factor_t += alpha_matrix[t][i]

        scale_factor_t = 1 / scale_factor_t
        scale_sum.append(scale_factor_t)

        for i in range(0, len(A)):
            alpha_matrix[t][i] = alpha_matrix[t][i] * scale_factor_t

    return alpha_matrix, scale_sum


def backward_alg(A, B, o_seq, scale_factor):
   # Initialize beta vector (backward probabilities) for all time steps
   T = len(o_seq)
   N = len(A)
   beta_vector = [[0] * N for _ in range(T)]

   for i in range(N):
       beta_vector[T-1][i] = scale_factor[T - 1]

   # Iterate backward through the observation sequence
   for t in range(T - 2, -1, -1):
       for i in range(N):
           beta_vector[t][i] = 0
           for j in range(N):
               beta_vector[t][i] += float(A[i][j]) * float(B[j][int(o_seq[t+1])]) * float(beta_vector[t+1][j])
           beta_vector[t][i] *= scale_factor[t]

   return beta_vector


def compute_gamma(A, B, o_seq, alpha_matrix, beta_matrix):
    T = len(o_seq)
    N = len(A)
    gamma_matrix = [[[0]* N for _ in range(N)] for _ in range(T)]
    gamma_vector = [[0] * N for _ in range(T)]

    for t in range(T - 1):
        for i in range(N):
            #gamma_vector[t][i] = 0
            for j in range(N):
                gamma_matrix[t][i][j] = alpha_matrix[t][i] * A[i][j] * B[j][int(o_seq[t + 1])] * beta_matrix[t + 1][j]
                gamma_vector[t][i] += gamma_matrix[t][i][j]

    for i in range(N):
        gamma_vector[T - 1][i] = alpha_matrix[T - 1][i]

    return gamma_vector, gamma_matrix


def re_estimate(A, B, π, o_seq, gamma_vector, gamma_matrix):
    T = len(o_seq)
    N = len(A)
    M = len(B[0])

    # Re-estimate π
    for i in range(N):
        π[0][i] = gamma_vector[0][i]

    # Re-estimate A
    for i in range(N):
        den = 0
        for t in range(T - 1):
            den += gamma_vector[t][i]
        for j in range(N):
            num = 0
            for t in range(T - 1):
                num += gamma_matrix[t][i][j]
            A[i][j] = round(num / den,6)

    # Re-estimate B
    for i in range(N):
        den = 0
        for t in range(T):
            den += gamma_vector[t][i]
        for j in range(M):
            num = 0
            for t in range(T):
                if o_seq[t] == j:
                    num += gamma_vector[t][i]
            B[i][j] = round(num / den , 6)

    return A, B, π


import math


def hmm3(A, B, pi, seq, max_iterations=500):  # Renamed and added max_iterations as parameter
    """
    Implements the Baum-Welch algorithm for HMM parameter estimation.

    Args:
        A: Transition matrix (list of lists).
        B: Emission matrix (list of lists).
        pi: Initial state probabilities (list of lists).
        seq: Observation sequence (list of integers).
        max_iterations: Maximum number of iterations (default: 50).

    Returns:
        A tuple containing the re-estimated A, B, and pi.
    """
    old_prob = -math.inf  # Initialize with negative infinity

    for i in range(max_iterations):  # Use max_iterations parameter
        prob = 0
        alpha_matrix, alpha_sums = forward_alg2(A, B, pi, seq)  # Use provided forward algorithm
        beta_matrix = backward_alg(A, B, seq, alpha_sums)  # Use provided backward algorithm
        gamma_sums, gamma_matrix = compute_gamma(A, B, seq, alpha_matrix, beta_matrix)  # Use provided di_gamma function

        # Correct log probability calculation (same as in your second code snippet)
        for j in range(len(seq)):
            prob += math.log(alpha_sums[j])
        prob = -prob

        if prob > old_prob:
            old_prob = prob
        else:
            break  # Stop if log probability decreases or stays the same
        A, B, pi = re_estimate(A, B, pi, seq, gamma_sums, gamma_matrix)  # Use provided re-estimation function

    return A, B, pi


# ... (Your existing forward_algorithm2, backward_algorithm2, di_gamma_func, and get_estimates functions remain unchanged)


def compute_log_prob(A, B, π, o_seq, scale_sum):
    log_prob = 0
    for i in range(len(o_seq)):
        log_prob += math.log(scale_sum[i])
    log_prob = -log_prob
    return log_prob




def printOutput(matrix):
    # count rows and columns in the matrix
    rows = len(matrix)
    columns = len(matrix[0])

    print(rows, columns, end=" ")
    for i in range(rows):
        for j in range(columns):
            print(matrix[i][j], end=" ")
    print()


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



    A, B, π = hmm3(A,B,π,o_seq)

    printOutput(A)
    printOutput(B)




















if __name__ == "__main__":

    main()