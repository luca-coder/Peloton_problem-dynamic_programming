import math
import Circuit
import numpy as np
import matplotlib.pyplot as plt
import timeit
import Operations

vertices = [[2, 120], [70, 140], [80, 20], [60, 90], [10, 60], [40, 20], [85, 10], [100, 70], [120, 30], [110, 140], [180, 90], [150, 40], [200, 75], [260, 10]]
ralph_speed = 1
peloton_speed = 2

if __name__ == '__main__':
    start_time = timeit.default_timer()
    new_vertices = []
    final_new_vertices = []
    n = 10
    optimum_list = []
    input_sizes = []
    final_path = []

    '''First plot of the path followed by the peloton.'''
    Operations.plot_circuit1(vertices)

    '''Add intermediate points on each edge.'''
    final_new_vertices = Operations.add_intermediate_points(vertices, 50, new_vertices, final_new_vertices)

    '''Calculate how much time the peloton takes to travel through each edge.'''
    matrix = Circuit.compute_peloton_times(final_new_vertices, peloton_speed)

    '''Find the optimal solution.'''
    optimum, opt = Operations.find_optimum(final_new_vertices, matrix)

    '''Identify the first element in the array opt whose value is equal to the optimum.'''
    for i in range(0, len(opt)):
        if(opt[i] == optimum):
            break

    '''Identify the optimal path.'''
    indices_list = Operations.find_path(opt, final_new_vertices, i, [], matrix)
    for element in indices_list:
        final_path.append(final_new_vertices[element])
    print(final_path)

    end_time = timeit.default_timer()
    total_time = end_time - start_time
    print("total time")
    print(total_time)
    '''Plot the paths followed by the peloton and the agent.'''
    Operations.plot_circuit(vertices, final_path)


    '''Here, we test what happens by introducing 3-4-5...-n intermediate points on the edges.'''
    for i in range(3, n):
        new_vertices = []
        final_new_vertices = []

        final_new_vertices = Operations.add_intermediate_points(vertices, i, new_vertices, [])
        matrix = Circuit.compute_peloton_times(final_new_vertices, peloton_speed)

        optimum, opt = Operations.find_optimum(final_new_vertices, matrix)
        optimum_list.append(optimum)
        input_sizes.append((i - 2))

    '''For each amount of introduced points, we plot the value of the optimal solution.'''
    plt.plot(input_sizes, optimum_list, color='blue', marker='o')
    plt.xlabel('Amount of extra points')
    plt.ylabel('Optimum value')
    plt.title('Input Size vs. Optimum Solution Quality')
    plt.show()