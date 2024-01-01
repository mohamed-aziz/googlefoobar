"""
Doomsday Fuel
=============
Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state). You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
[0,1,0,0,0,1], # s0, the initial state, goes to s1 and s5 with equal probability
[4,0,0,3,2,0], # s1 can become s0, s3, or s4, but with different probabilities
[0,0,0,0,0,0], # s2 is terminal, and unreachable (never observed in practice)
[0,0,0,0,0,0], # s3 is terminal
[0,0,0,0,0,0], # s4 is terminal
[0,0,0,0,0,0], # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
[[Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)],
[Fraction(0, 1), Fraction(1, 1), Fraction(0, 1), Fraction(3, 7), Fraction(4, 7)],
[Fraction(0, 1), Fraction(0, 1), Fraction(1, 1), Fraction(0, 1), Fraction(0, 1)],
[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(1, 1), Fraction(0, 1)],
 [Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)]]

"""

def solution(m):
    from fractions import Fraction, gcd
    
    def invert_matrix(matrix):
        # use gauss jordan elimination
        size = len(matrix)
        identity = [[Fraction(1 if i == j else 0) for j in range(size)] for i in range(size)]

        for i in range(size):
            factor = matrix[i][i]
            if factor == 0:
                raise ZeroDivisionError("Matrix is not invertible")

            for j in range(size):
                matrix[i][j] /= factor
                identity[i][j] /= factor

            for k in range(i + 1, size):
                factor = matrix[k][i]
                for j in range(size):
                    matrix[k][j] -= factor * matrix[i][j]
                    identity[k][j] -= factor * identity[i][j]

        for i in range(size - 1, 0, -1):
            for k in range(i - 1, -1, -1):
                factor = matrix[k][i]
                for j in range(size):
                    matrix[k][j] -= factor * matrix[i][j]
                    identity[k][j] -= factor * identity[i][j]

        return identity

    def lcm(a, b):
        return abs(a * b) // gcd(a, b) if a and b else 0
    
    # multiply matrix
    def multiply_matrix(m1, m2):
        return [
            [sum([m1[i][k] * m2[k][j] for k in range(len(m2))]) for j in range(len(m2[0]))]
            for i in range(len(m1))
        ]


    size = len(m)
    matrix = [
        [Fraction(m[i][j], sum(m[i])) if sum(m[i]) else 0 for j in range(size)]
        for i in range(size)    
    ]    
    reachability_matrix = [sum(row) == 0 for row in m]
    if reachability_matrix.count(True) == 1:
        return [1, 1]
    ident = [[Fraction(int(i == j)) for i in range(size)] for j in range(size)]
    fundamental_matrix = [
        [ident[i][j] - matrix[i][j] for j in range(size)] for i in range(size)
    ]
    
    inv_fundamental_matrix = invert_matrix(fundamental_matrix)
    probs = multiply_matrix([
        row for i, row in enumerate(matrix) if not reachability_matrix[i]
    ], inv_fundamental_matrix)
    probs = [probs[0][i] for i in range(size) if reachability_matrix[i]]

    common_denominator = 1
    for item in probs:
        common_denominator = lcm(common_denominator, item.denominator)
    
    terminal_probs = []
    for item in probs:
        terminal_probs.append(item.numerator * common_denominator // item.denominator)

    terminal_probs.append(common_denominator)
    return terminal_probs

print(solution([[0, 1, 0, 0, 0, 1], 
                [4, 0, 0, 3, 2, 0], 
                [0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0]]))
print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))

print(solution([[0, 0, 0, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))
