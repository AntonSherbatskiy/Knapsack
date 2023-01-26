from parameter import *
import random
import sys
import os


def genetic(param) -> tuple[list, list, list]:
    weight, fitness = generate_metaheuristic(param.items_quantity, param.max_item_fitness, param.max_weight)
    population = generate_population(param.population_quantity, param.items_quantity, weight, param.max_weight)

    iteration = []
    fitness_chart = []
    weight_chart = []

    for i in range(param.iterations_quantity):
        if i % param.iterations_to_log == 0:
            print_info(population, weight, fitness, i)
        parent1, parent2 = select_parents(population, fitness)
        successor1, successor2 = crossing(parent1, parent2, weight, param)

        if random.random() <= float(param.mutation_chance):
            successor1, successor2 = mutation(successor1, successor2, weight, param.max_weight)

        if param.is_local_upgrade == True:
            successor1, successor2 = local_upgrade(successor1, successor2, weight, param.max_weight)
            
        add_successor(population, successor1, successor2, fitness, param)

        if i % param.iterations_to_log == 0:
            iteration.append(i)
            fitness_chart.append(chart_info(population, fitness))
            weight_chart.append(chart_info(population, weight))

    return iteration, fitness_chart, weight_chart


def local_upgrade(first_knap, second_knap, weight, max_weight) -> tuple[list, list]:
    knap1 = first_knap[:]
    knap2 = second_knap[:]
    
    available_items1 = []
    available_items2 = []

    for i in range(len(first_knap)):
        if knap1[i] == 0:
            available_items1.append(i)
        if knap2[i] == 0:
            available_items2.append(i)

    if len(available_items1) == 0 or len(available_items2) == 0:
        return knap1, knap2

    gene_to_upgrade1 = available_items1[random.randint(0, len(available_items1) - 1)]
    gene_to_upgrade2 = available_items2[random.randint(0, len(available_items2) - 1)]

    if get_total_heuristic(knap1, weight) + weight[gene_to_upgrade1] <= max_weight:
        knap1[gene_to_upgrade1] = 1
    if get_total_heuristic(knap2, weight) + weight[gene_to_upgrade2] <= max_weight:
        knap2[gene_to_upgrade2] = 1
    
    return knap1, knap2


def print_info(population, weight, fitness, iteration):
    av_fitness = float(0)
    av_weight = float(0)

    for knap in population:
        av_fitness += get_total_heuristic(knap, fitness)
        av_weight += get_total_heuristic(knap, weight)

    av_fitness /= len(population)
    av_weight /= len(population)

    print(f"Iteration {iteration + 1}: [Average weight: {av_weight:.3f} Average fitness: {av_fitness:.3f}]")


def chart_info(population, metaheuristic) -> float:
    av_fitness = float(0)
    av_weight = float(0)

    for knap in population:
        av_fitness += get_total_heuristic(knap, metaheuristic)

    av_fitness /= len(population)
    return av_fitness


def get_max_fitness(population, fitness) -> int:
    max_fitness = -1
    max_fitness_id = -1

    for i in range(len(population)):
        if get_total_heuristic(population[i], fitness) > max_fitness:
            max_fitness = get_total_heuristic(population[i], fitness)
            max_fitness_id = i
    return max_fitness_id
        

def add_successor(population, successor1, successor2, fitness, crossing):
    if crossing.crossing_successor == 1:
        if get_total_heuristic(successor1, fitness) > get_total_heuristic(successor2, fitness):
            best_successor = successor1[:]
        else:
            best_successor = successor2[:]
        population.pop(get_min_fitness_id(population, fitness))
        population.append(best_successor)
    else:
        population.pop(get_min_fitness_id(population, fitness))
        population.pop(get_min_fitness_id(population, fitness))
        population.append(successor1[:])
        population.append(successor2[:])


def get_min_fitness_id(population, fitness) -> int:
    min_fitness = sys.maxsize
    min_fitness_id = -1

    for i in range(len(population)):
        if get_total_heuristic(population[i], fitness) < min_fitness:
            min_fitness = get_total_heuristic(population[i], fitness)
            min_fitness_id = i
    
    return min_fitness_id


def mutation(first_knap, second_knap, weight, max_weight):
    gene_to_mutate = random.randint(0, len(first_knap) - 1)
    knap1 = first_knap[:]
    knap2 = second_knap[:]

    if knap1[gene_to_mutate] == 1:
        knap1[gene_to_mutate] = 0
    else:
        knap1[gene_to_mutate] = 1

    if knap2[gene_to_mutate] == 1:
        knap2[gene_to_mutate] = 0
    else:
        knap2[gene_to_mutate] = 1

    if get_total_heuristic(knap1, weight) > max_weight or get_total_heuristic(knap2, weight) > max_weight:
        return first_knap, second_knap
    return knap1, knap2


def crossing(parent1, parent2, weight, param):
    first_parent = parent1[:]
    second_parent = parent2[:]

    first_successor = []
    second_successor = []

    if param.crossing_type == "point":
        first_successor = first_parent[:int(len(first_parent) / 2)] + second_parent[int(len(second_parent) / 2):]
        second_successor = second_parent[:int(len(second_parent) / 2)] + first_parent[int(len(first_parent) / 2):]
    elif param.crossing_type == "prop":
        for i in range(len(parent1)):
            if random.random() >= 0.5:
                first_successor.append(parent1[i])
            else:
                first_successor.append(parent2[i])
            
            if random.random() >= 0.5:
                second_successor.append(parent1[i])
            else:
                second_successor.append(parent2[i])
    else:
        raise ValueError("Only 'point' or 'prop' allowed!")

    if get_total_heuristic(first_successor, weight) > param.max_weight or get_total_heuristic(second_successor, weight) > param.max_weight:
        return parent1, parent2
    return first_successor, second_successor


def select_parents(population, fitness):
    max_fitness = -1
    max_fitness_id = -1

    for i in range(len(population)):
        if get_total_heuristic(population[i], fitness) > max_fitness:
            max_fitness = get_total_heuristic(population[i], fitness)
            max_fitness_id = i

    best_parent = population[max_fitness_id][:]
    while True:
        knap_to_select = random.randint(0, len(population) - 1)
        if id(population[knap_to_select]) != id(best_parent):
            random_parent = population[knap_to_select]
            break
    return best_parent, random_parent


def generate_metaheuristic(items_quantity, max_fitness_per_element, max_weight) -> tuple[list, list]:
    weight = []
    fitness = []
    for i in range(items_quantity):
        weight.append(random.randint(1, max_weight))
        fitness.append(random.randint(1, max_fitness_per_element))
    return weight, fitness


def generate_population(population_quantity, items_quantity, weight, max_weight) -> list:
    population = []
    for i in range(population_quantity):
        os.system('cls')
        print(f"Generating {i + 1} knapsack, please wait...")
        population.append(initial_package(items_quantity, weight, max_weight))
    return population


def initial_package(items_quantity, weight, max_weight) -> list:
    items = []
    for _ in range(items_quantity):
        items.append(int(0))

    for _ in range(int(items_quantity / 4)):
        available = False
        for j in range(len(items)):
            if get_total_heuristic(items, weight) + weight[j] < max_weight:
                available = True
                break

        if available == True:
            item_to_add = random.randint(0, items_quantity - 1)
            if get_total_heuristic(items, weight) + weight[item_to_add] <= max_weight:
                items[item_to_add] = 1
        else:
            break

    return items


def get_total_heuristic(items, characteristic_array) -> int:
    total_heuristic = int(0)
    for i in range(len(items)):
        if items[i] == 1:
            total_heuristic += characteristic_array[i]
    return total_heuristic