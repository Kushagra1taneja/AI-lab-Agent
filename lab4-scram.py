import numpy
import matplotlib.pyplot
import scipy.io
import random
import copy

scrambled = scipy.io.loadmat("D:\\ai\\lab\\scrambled_lena.mat")['Iscrambled']

matplotlib.pyplot.imshow(scrambled, cmap='gray')
matplotlib.pyplot.title("Scrambled Image")
matplotlib.pyplot.show()

def calc_diff(tile1, tile2):
    return numpy.sum(numpy.abs(tile1 - tile2))

def calc_cost(image_tiles, grid_size):
    total_cost = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if j < grid_size - 1:
                total_cost += calc_diff(image_tiles[i][j][:, -1], image_tiles[i][j+1][:, 0])
            if i < grid_size - 1:
                total_cost += calc_diff(image_tiles[i][j][-1, :], image_tiles[i+1][j][0, :])
    return total_cost

def swap_tiles(image_tiles, grid_size):
    i1, j1 = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
    i2, j2 = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
    new_tiles = copy.deepcopy(image_tiles)
    new_tiles[i1][j1], new_tiles[i2][j2] = new_tiles[i2][j2], new_tiles[i1][j1]
    return new_tiles

def sim_ann(scrambled, grid_size, initial_temp, cooling_rate, max_iterations):
    tile_height = scrambled.shape[0] // grid_size
    tile_width = scrambled.shape[1] // grid_size
    image_tiles = [[scrambled[i*tile_height:(i+1)*tile_height, j*tile_width:(j+1)*tile_width]
                    for j in range(grid_size)] for i in range(grid_size)]
    
    current_state = image_tiles
    current_cost = calc_cost(current_state, grid_size)
    temperature = initial_temp

    for iteration in range(max_iterations):
        new_state = swap_tiles(current_state, grid_size)
        new_cost = calc_cost(new_state, grid_size)
        
        if new_cost < current_cost:
            current_state, current_cost = new_state, new_cost
        else:
            probability = numpy.exp((current_cost - new_cost) / temperature)
            if random.random() < probability:
                current_state, current_cost = new_state, new_cost
        
        temperature *= cooling_rate

        if iteration % 1000 == 0:
            print(f"Iteration {iteration}, Current Cost: {current_cost}")

    return current_state

grid_size = 3
initial_temp = 1000
cooling_rate = 0.995
max_iterations = 10000

solved_tiles = sim_ann(scrambled, grid_size, initial_temp, cooling_rate, max_iterations)

solved_image = numpy.block(solved_tiles)

matplotlib.pyplot.imshow(solved_image, cmap='gray')
matplotlib.pyplot.title("Solved Image")
matplotlib.pyplot.show()
