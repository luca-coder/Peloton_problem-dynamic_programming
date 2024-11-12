import math


def compute_peloton_times(vertices, peloton_speed):
    """
    Function that, based on the path of the peloton and the speed of the peloton, calculated how much time the peloton takes to travel through each edge.
    @param vertices: The extremes that identify each edge of the path followed by the peloton.
    @param peloton_speed: The speed of the peloton.
    @return: The variable Matrix, which represents the time that the peloton takes to travel from the (n-th - 1) vertex to the (n-th) vertex.
    """
    matrix = [[0 for j in range(len(vertices) - 1)] for i in range(len(vertices) - 1)]
    for i in range(0, len(matrix)):
        matrix[i][i] = (math.dist(vertices[i], vertices[i+1]))/peloton_speed
    for i in range(1, len(matrix)):
        for j in range(i-1, -1, -1):
            matrix[i][j] = matrix[j][j] + matrix[i][j+1]
    return matrix


def check(first_vertex, last_vertex, ralph_speed, peloton_speed, vertices, matrix):
    """
    Function that checks if, when both the agent and the peloton are located at vertex j, going straight to vertex i results in an interception.
    @param first_vertex: The vertex where the agent and the peloton are located (here happened an interception).
    @param last_vertex: The vertex for which we want to calculate if an interception is achievable.
    @param ralph_speed: The speed of the agent.
    @param peloton_speed: The speed of the peloton
    @param vertices: The extremes that identify each edge of the path followed by the peloton.
    @param matrix: The matrix representing the time that the peloton takes to travel through each edge.
    @return: 1 if the interception is achievable, 0 otherwise.
    """

    ralph_distance = math.dist(vertices[first_vertex], vertices[last_vertex])

    if((ralph_distance/ralph_speed) <= (matrix[last_vertex - 1][first_vertex])):
        return 1
    return 0


def is_reachable(j, vertices, matrix, ralph_speed):
    """
    Function that calculates if, moving from the first vertex, the agent is able to intercept the peloton at vertex j;
    @param j: The vertex for which we want to calculate if an interception is achievable.
    @param vertices: The extremes that identify each edge of the path followed by the peloton.
    @param matrix: The matrix representing the time that the peloton takes to travel through each edge.
    @param ralph_speed: The speed of the agent.
    @return:
    """
    if (j == 0):
        return 1
    else:
        ralph_distance = math.dist(vertices[0], vertices[j])

        if(ralph_distance/ralph_speed <= matrix[j - 1][0]):
            return 1
        return 0


def solve(matrix, vertices, ralph_speed, peloton_speed, i, opt):
    """
    Function that actually calculates the optimal solution by employing dynamic programming.
    @param matrix: The matrix representing the time that the peloton takes to travel through each edge.
    @param vertices: The extremes that identify each edge of the path followed by the peloton plus the additional vertices.
    @param ralph_speed: The speed of the agent.
    @param peloton_speed: The speed of the peloton.
    @param i: The vertex for which the optimal solution is calculated.
    @param opt: array where each element OPT[i] specifies the maximum number of interceptions the agent can achieve up to vertex i.
    @return: Nothing, the variable opt is modified and then used in other parts.
    """


    values = [(opt[j] + 1) * (check(j, i, ralph_speed, peloton_speed, vertices, matrix)) * is_reachable(j, vertices, matrix, ralph_speed) for j in range (0, i)]

    if len(values) > 0:
        opt[i] = max(values)
