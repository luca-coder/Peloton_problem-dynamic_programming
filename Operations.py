import math
import Circuit
import numpy as np
import matplotlib.pyplot as plt
import timeit

ralph_speed = 1
peloton_speed = 2

def plot_circuit(vertices, points):
    """
    Function that visually displays the path followed by the peloton (in blue) and the optimal path followed by the agent (the red dotted line).
    @param vertices: The extremes that identify each edge of the path followed by the peloton.
    @param points: The points where the agent intercepts the peloton identified by the optimal solution.
    @return: No variables, the function only has graphical tasks.
    """

    '''Display the path followed by the peloton.'''
    for vertex in vertices:
        plt.scatter(vertex[0], vertex[1], color='green')
    for i in range(0, len(vertices) - 1):
        plt.plot([vertices[i][0], vertices[i + 1][0]], [vertices[i][1], vertices[i + 1][1]], color='blue',
                 linestyle='-', linewidth=2)

    '''Display the points of the optimal solution and the path followed by the agent.'''
    for point in points:
        plt.scatter(point[0], point[1], color='green')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Optimal solution')

        for j in range(0, len(points) - 1):
            plt.plot([points[j][0], points[j + 1][0]], [points[j][1], points[j + 1][1]], 'k--', color='red')

    plt.show()


def plot_circuit1(vertices):
    """
    Function that visually displays the path followed by the peloton.
    @param vertices: The extremes that identify each edge of the path followed by the peloton.
    @return: No variables, the function only has graphical tasks.
    """

    '''Display the path followed by the peloton.'''
    for vertex in vertices:
        plt.scatter(vertex[0], vertex[1], color='green')
    for i in range(0, len(vertices) - 1):
        plt.plot([vertices[i][0], vertices[i + 1][0]], [vertices[i][1], vertices[i + 1][1]], color='blue',
             linestyle='-', linewidth=2)
    plt.show()


def generate_points(start_point, end_point, n, new_vertices):
    """
    Function that, given an edge, generates the additional points required for computation.
    @param start_point: The first extreme of the n-th edge.
    @param end_point: The second extreme of the n-th edge.
    @param n: The amount of additional points to introduce.
    @param new_vertices: A list consisting of the previously generated additional points.
    @return: The list new_vertices
    """
    '''Create an array of n equally spaced values between 0 and 1'''
    distances = np.linspace(0, 1, n)
    start_point = np.array(start_point)
    end_point = np.array(end_point)
    start_point = start_point.reshape(-1, 1)
    end_point = end_point.reshape(-1, 1)

    '''Use linear interpolation to find points along the line and return them'''
    points = (1 - distances) * start_point + distances * end_point
    points = points.T
    for element in points:
        element = element.tolist()
        new_vertices.append(element)
    return new_vertices


def add_intermediate_points(vertices, n, new_vertices, final_new_vertices):
    """
    Function that, given the whole path, introduces the additional points on each edge.
    @param vertices: The points representing the whole path of the peloton.
    @param n: The amount of additional points to introduce.
    @param new_vertices: A list consisting of the previously generated additional points.
    @param final_new_vertices: A refined list consisting of the initial vertices of an edge plus all the additional points.
    @return: The list final_new_vertices.
    """

    '''Generate the additional points between the extremes of an edge for each edge'''
    for i in range(0, len(vertices) - 1):
        new_vertices = generate_points(vertices[i], vertices[i + 1], n, new_vertices)

    for z in range(0, len(new_vertices) - 1):
        if(new_vertices[z] == new_vertices[z + 1]):
            continue
        final_new_vertices.append(new_vertices[z])
    final_new_vertices.append(new_vertices[len(new_vertices) - 1])

    return final_new_vertices


def find_optimum(final_new_vertices, matrix):
    """
    Function that calculates the optimal solution.
    @param final_new_vertices: The list consisting of the initial vertices of an edge plus all the additional points.
    @param matrix: The matrix representing the time that the peloton takes to travel through each edge.
    @return: The array opt, containing the optimum calculated for each vertex, and the variable optimum, which is actually the maximum number of interceptions.
    """
    indices_list = [0]
    '''We initialize opt by assigning to each element the value 1, because we assume that an interception always happens at the starting point.'''
    opt = [1 for i in range(len(final_new_vertices))]

    '''We calculate the optimum for each vertex one at the time.'''
    for i in range(0, len(final_new_vertices)):
        Circuit.solve(matrix, final_new_vertices, ralph_speed, peloton_speed, i, opt)

    optimum = max(opt)

    return optimum, opt


def find_path(optimal_solution, final_new_vertices, current_index, current_path, matrix):
    """
    Function that, after calculating the optimal solution, calculates the optimal path.
    @param optimal_solution: array where each element specifies the maximum number of interceptions the agent can achieve up to vertex i.
    @param final_new_vertices: A refined list consisting of the initial vertices of an edge plus all the additional points.
    @param current_index: The first element in optimal_solution whose value is equal to the optimum.
    @param current_path: List representing the points in final_new_vertices that belong to the optimal path.
    @param matrix: The matrix representing the time that the peloton takes to travel through each edge.
    @return: The optimal path.
    """
    if current_index == 0:
        current_path.append(0)
        return current_path[::-1]


    longest_path = []
    '''We start this reverse loop from the first element in optimal_solution whose value is equal to the optimum.'''
    for i in range(current_index - 1, -1, -1):
        '''We find all the vertices from which the agent could move to intercept the peloton in current_index.'''
        if optimal_solution[i] == optimal_solution[current_index] - 1:
            '''We check if the agent is able to make an interception moving from the vertex i to the vertex current_index.'''
            if Circuit.check(i, current_index, ralph_speed, peloton_speed, final_new_vertices, matrix) == 1:
                '''Once we find a suitable vertex, we make a recursive call by updating the index of the vertex to check and the current_path variable.'''
                path = find_path(optimal_solution, final_new_vertices, i, current_path + [current_index], matrix)
                if len(path) > len(longest_path):
                    longest_path = path

    return longest_path