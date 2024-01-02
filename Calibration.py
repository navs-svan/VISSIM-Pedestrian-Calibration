import win32com.client as com
import numpy as np
import pygad


def set_vissim(resolution, seed, filename):
    Vissim = com.dynamic.Dispatch("Vissim.Vissim")
    Filename = fr'D:\Drive D\ACADS\THESIS\Model\{filename}'
    Vissim.LoadNet(Filename)
    # Set simulation Parameters
    End_of_simulation = 3610  # simulation second [s]
    Vissim.Simulation.SetAttValue('SimPeriod', End_of_simulation)

    sim_resolution = resolution
    Vissim.Simulation.SetAttValue('SimRes', sim_resolution)

    sim_seed = seed
    Vissim.Simulation.SetAttValue('RandSeed', sim_seed)
    Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 1)
    return Vissim


def set_parameters(Vissim, parameter_list):
    # Pedestrian Parameters
    parameter_values = ['Tau', 'ASocIso', 'BSocIso', 'ASocMean', 'VD']
    parameter_dict = {parameter_values[i]: parameter_list[i] for i in range(len(parameter_values))}
    print(parameter_dict)
    Vissim.Simulation.Stop()
    for key, value in parameter_dict.items():
        Vissim.Net.WalkingBehaviors.ItemByKey(4).SetAttValue(key, value)
        print(f"{key}={Vissim.Net.WalkingBehaviors.ItemByKey(4).AttValue(key)}")


def get_data(Vissim, time):
    signal_one = Vissim.Net.SignalHeads.ItemByKey(9)
    signal_two = Vissim.Net.SignalHeads.ItemByKey(12)
    list_one = []
    list_two = []
    for i in range(time * int(Vissim.Simulation.AttValue('SimRes'))):
        Vissim.Simulation.RunSingleStep()
        All_Ped = Vissim.Net.Pedestrians.GetMultipleAttributes(('No', 'Speed', 'SimSec', 'StaRoutDecNo', 'StaRoutNo'))
        for cur_Ped in All_Ped:
            ped_number = cur_Ped[0]
            ped_speed = cur_Ped[1]
            ped_sim_sec = cur_Ped[2]
            ped_stat_route_dec = cur_Ped[3]
            ped_stat_route = cur_Ped[4]
            sig_state_one = signal_one.AttValue('SigState')
            sig_state_two = signal_two.AttValue('SigState')
            # if signal_one.AttValue('SigState')
            # print('%s  |  %.2f  |  %.2f' % (ped_number, ped_speed, ped_sim_sec))
            if sig_state_one == 'GREEN' and ped_speed >= 1 and (
                    ped_stat_route_dec == 1 or (ped_stat_route_dec == 2 and ped_stat_route == 1)):
                # print('%s  |  %.2f  |  %.2f  |  %s' % (ped_number, ped_speed, ped_sim_sec, sig_state_one))
                list_one.append((ped_number, round(ped_speed, 2), round(ped_sim_sec, 2)))
            if sig_state_two == 'GREEN' and ped_speed >= 1 and (
                    ped_stat_route_dec == 3 or (ped_stat_route_dec == 2 and ped_stat_route == 2)):
                # print('%s  |  %.2f  |  %.2f  |  %s' % (ped_number, ped_speed, ped_sim_sec, sig_state_two))
                list_two.append((ped_number, round(ped_speed, 2), round(ped_sim_sec, 2)))
    return sorted(list_one), sorted(list_two)


def get_average(list_input, time):
    ave_speed_list = []
    for i in range(0, time, 90):
        for j in range(list_input[-1][0] + 1):
            quick_sum = []
            for point in list_input:
                if point[0] == j and i <= point[2] < (i + 90):
                    quick_sum.append(point[1])
            # print(quick_sum)
            if len(quick_sum) > 0:
                ave_speed = np.mean(quick_sum)
                ave_speed_list.append(np.round_(ave_speed, decimals=2))
    # print(ave_speed_list)
    return sorted(ave_speed_list)


def len_equalizer(list1, list2):
    if len(list1) > len(list2):
        to_sub_index = (len(list1) - len(list2)) / 2
        if to_sub_index is not int:
            list1 = list1[int(to_sub_index - 0.5):int(len(list1) - (to_sub_index + 0.5))]
        else:
            list1 = list1[int(to_sub_index):int(len(list1) - to_sub_index)]
    elif len(list1) < len(list2):
        to_sub_index = (len(list2) - len(list1)) / 2
        if to_sub_index is not int:
            list2 = list2[int(to_sub_index - 0.5):int(len(list2) - (to_sub_index + 0.5))]
        else:
            list2 = list2[int(to_sub_index):int(len(list2) - to_sub_index)]
    return list1, list2


def rmspe(actual, estimated):
    actual, estimated = len_equalizer(actual, estimated)
    return np.linalg.norm((actual - estimated) / actual) / np.sqrt(len(actual))


def fitness_func(ga_instance, solution, solution_idx):
    time = 540
    set_parameters(Vissim, solution)
    local_ped_list_one, local_ped_list_two = get_data(Vissim, time)

    local_ave_speed_one = get_average(local_ped_list_one, time)
    output = rmspe(crosswalk_one_actual, local_ave_speed_one)

    # local_ave_speed_two = get_average(local_ped_list_two, time)
    # output = rmspe(crosswalk_two_actual, local_ave_speed_two)

    # local_ave_speed_combined = np.asarray(
    #     sorted(np.concatenate((get_average(local_ped_list_one, time), get_average(local_ped_list_two, time)))))
    # output = rmspe(crosswalk_combined_actual, local_ave_speed_combined)

    fitness = 1 / output
    print(fitness)
    return fitness


def genetic_algorithm():
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
    # initial_population = [(0.118, 1.052, 0.103, 0.3, 6.377),
    #                       [0.300, 1.416, 0.107, 0.367, 5.60],
    #                       [0.200, 0.367, 0.107, 0.684, 5.6],
    #                       [0.128, 2.720, 0.139, 0.578, 6.00],
    #                       [0.107, 1.416, 0.128, 0.367, 5.60],
    #                       [0.385, 2.720, 0.124, 0.579, 7.00],
    #                       [0.256, 1.368, 0.110, 0.400, 7.00],
    #                       [0.200, 2.720, 0.200, 0.564, 6.00]]
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
                           # initial_population=initial_population,
                           stop_criteria=['reach_25', 'saturate_15'])
    # Run GA Instance
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(f"Parameters of the best solution : {solution}")
    print(f"Fitness value of the best solution = {1 / solution_fitness}")
    ga_instance.plot_fitness()


if __name__ == "__main__":
    # Define Variables
    parameter_list = [0.400, 2.720, 0.200, 0.400, 3.00]
    crosswalk_one_actual = np.asarray(
        [3.97, 3.97, 4.06, 4.09, 4.13, 4.18, 4.2, 4.21, 4.21, 4.23, 4.24, 4.25, 4.27, 4.27, 4.28, 4.29, 4.3, 4.32, 4.38,
         4.39, 4.4, 4.45, 4.5, 4.51, 4.51, 4.52, 4.52, 4.57, 4.57, 4.59, 4.6, 4.6, 4.62, 4.63, 4.64, 4.66, 4.67, 4.69,
         4.69, 4.71, 4.71, 4.71, 4.72, 4.72, 4.72, 4.72, 4.74, 4.75, 4.76, 4.76, 4.79, 4.79, 4.8, 4.82, 4.83, 4.83,
         4.84, 4.84, 4.86, 4.87, 4.87, 4.87, 4.88, 4.88, 4.88, 4.89, 4.9, 4.9, 4.9, 4.91, 4.91, 4.92, 4.94, 4.94, 4.94,
         4.95, 4.96, 4.98, 4.98, 4.98, 4.98, 4.99, 5, 5.01, 5.04, 5.06, 5.07, 5.09, 5.09, 5.11, 5.12, 5.14, 5.16, 5.18,
         5.23, 5.23, 5.29, 5.32, 5.32, 5.33, 5.34, 5.34, 5.35, 5.35, 5.36, 5.36, 5.37, 5.38, 5.4, 5.41, 5.44, 5.47,
         5.48, 5.53, 5.62, 5.67, 5.69, 5.7, 5.8, 5.81, 5.81, 5.94, 5.99, 6.02, 6.09, 6.15, 6.35])
    crosswalk_two_actual = np.asarray(
        [3.79, 3.97, 4.03, 4.04, 4.05, 4.05, 4.05, 4.07, 4.1, 4.12, 4.16, 4.19, 4.2, 4.2, 4.32, 4.32, 4.32, 4.34, 4.4,
         4.4, 4.4, 4.42, 4.44, 4.49, 4.5, 4.52, 4.54, 4.61, 4.62, 4.64, 4.7, 4.71, 4.71, 4.74, 4.79, 4.8, 4.81, 4.9,
         4.91, 4.94, 4.94, 4.95, 4.97, 4.97, 4.99, 5, 5.03, 5.04, 5.05, 5.08, 5.09, 5.11, 5.11, 5.16, 5.22, 5.37, 5.52,
         5.61, 5.61, 5.63, 5.71, 5.81, 5.85, 5.87, 5.93, 6.2, 6.34, 6.47])
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
