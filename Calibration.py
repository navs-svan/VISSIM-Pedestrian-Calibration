from helper import *
import pygad

def fitness_func(ga_instance, solution, solution_idx):
    """The fitness function as defined in the Pygad Documentation. Because of 
    its strict arguments, manual editing of code is needed to perform different 
    calibrations"""
    time = 540 # time in seconds
    set_parameters(Vissim, solution)
    local_ped_list_one, local_ped_list_two = get_data(Vissim, time)

    # Uncomment when calibrating SM Aura street
    local_ave_speed_one = get_average(local_ped_list_one, time)
    output = rmspe(crosswalk_one_actual, local_ave_speed_one)

    # Uncomment when calibrating Market Market street
    # local_ave_speed_two = get_average(local_ped_list_two, time)
    # output = rmspe(crosswalk_two_actual, local_ave_speed_two)

    # Uncomment when calibrating both combined
    # local_ave_speed_combined = np.asarray(
    #     sorted(np.concatenate((get_average(local_ped_list_one, time), get_average(local_ped_list_two, time)))))
    # output = rmspe(crosswalk_combined_actual, local_ave_speed_combined)

    fitness = 1 / output
    print(fitness)
    return fitness


def genetic_algorithm() -> None:
    """Performs genetic algorithm to calibrate the walking behavior parameters"""
    # Define GA Parameters
    fitness_function = fitness_func
    num_generations = 50
    num_parents_mating = 5
    sol_per_pop = 10
    num_genes = len(parameter_list)
    parent_selection_type = "rank"
    keep_elitism = 2
    crossover_type = "uniform"
    mutation_type = "random"
    mutation_percent_genes = 20
    gene_space = [{'low': 0.1, 'high': 1, 'step': 0.001},
                  {'low': 1, 'high': 3, 'step': 0.001},
                  {'low': 0.1, 'high': 0.3, 'step': 0.001},
                  {'low': 0.3, 'high': 0.7, 'step': 0.001},
                  {'low': 3, 'high': 7, 'step': 0.001}]

    # Create GA Instance
    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           gene_space=gene_space,
                           parent_selection_type=parent_selection_type,
                           keep_elitism=keep_elitism,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           stop_criteria=['reach_25', 'saturate_15'])
    # Run GA Instance
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(f"Parameters of the best solution : {solution}")
    print(f"Fitness value of the best solution = {1 / solution_fitness}")
    ga_instance.plot_fitness()



# Define Variables
parameter_list = [0.400, 2.720, 0.200, 0.400, 3.00]
crosswalk_one_actual = np.np.genfromtxt('./csv_data/calib_cw_one.csv', delimiter=',')
crosswalk_two_actual = np.np.genfromtxt('./csv_data/calib_cw_two.csv', delimiter=',')
crosswalk_combined_actual = np.asarray(sorted(np.concatenate((crosswalk_two_actual, crosswalk_one_actual))))

# Call Functions
Vissim = set_vissim(5, 42, 'Intersection.inpx')

sm_aura_id = 1
market_market_id = 2
from_west_id = 3

Vissim.Net.PedestrianInputs.ItemByKey(sm_aura_id).SetAttValue('Volume(1)', 820)
Vissim.Net.PedestrianInputs.ItemByKey(market_market_id).SetAttValue('Volume(1)', 580)
Vissim.Net.PedestrianInputs.ItemByKey(from_west_id).SetAttValue('Volume(1)', 460)
Vissim.Net.PedestrianRoutingDecisionsStatic.ItemByKey(market_market_id).PedRoutSta.ItemByKey(1).SetAttValue(
    'RelFlow(1)', 470)
Vissim.Net.PedestrianRoutingDecisionsStatic.ItemByKey(market_market_id).PedRoutSta.ItemByKey(2).SetAttValue(
    'RelFlow(1)', 110)
set_parameters(Vissim, parameter_list)
genetic_algorithm()