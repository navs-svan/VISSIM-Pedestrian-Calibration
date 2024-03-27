import win32com.client as com
import numpy as np


def set_vissim(resolution, seed, filename):
    Vissim = com.dynamic.Dispatch("Vissim.Vissim")
    Filename = rf"D:\Drive D\ACADS\THESIS\Model\{filename}"
    Vissim.LoadNet(Filename)

    # Set simulation Parameters
    End_of_simulation = 3610  # simulation second [s]
    Vissim.Simulation.SetAttValue("SimPeriod", End_of_simulation)

    sim_resolution = resolution
    Vissim.Simulation.SetAttValue("SimRes", sim_resolution)

    sim_seed = seed
    Vissim.Simulation.SetAttValue("RandSeed", sim_seed)
    Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 1)
    return Vissim


def set_parameters(Vissim, parameter_list):
    # Pedestrian Parameters
    parameter_names = ["Tau", "ASocIso", "BSocIso", "ASocMean", "VD"]
    parameter_dict = {
        parameter_names[i]: parameter_list[i] for i in range(len(parameter_names))
    }
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
    for i in range(time * int(Vissim.Simulation.AttValue("SimRes"))):
        Vissim.Simulation.RunSingleStep()
        All_Ped = Vissim.Net.Pedestrians.GetMultipleAttributes(
            ("No", "Speed", "SimSec", "StaRoutDecNo", "StaRoutNo")
        )
        for cur_Ped in All_Ped:
            ped_number = cur_Ped[0]
            ped_speed = cur_Ped[1]
            ped_sim_sec = cur_Ped[2]
            ped_stat_route_dec = cur_Ped[3]
            ped_stat_route = cur_Ped[4]
            sig_state_one = signal_one.AttValue("SigState")
            sig_state_two = signal_two.AttValue("SigState")

            if (
                sig_state_one == "GREEN"
                and ped_speed >= 1
                and (
                    ped_stat_route_dec == 1
                    or (ped_stat_route_dec == 2 and ped_stat_route == 1)
                )
            ):
                list_one.append(
                    (ped_number, round(ped_speed, 2), round(ped_sim_sec, 2))
                )
            if (
                sig_state_two == "GREEN"
                and ped_speed >= 1
                and (
                    ped_stat_route_dec == 3
                    or (ped_stat_route_dec == 2 and ped_stat_route == 2)
                )
            ):
                list_two.append(
                    (ped_number, round(ped_speed, 2), round(ped_sim_sec, 2))
                )
    return sorted(list_one), sorted(list_two)


def get_average(list_input, time):
    ave_speed_list = []
    for i in range(0, time, 90):
        for j in range(list_input[-1][0] + 1):
            quick_sum = []
            for point in list_input:
                if point[0] == j and i <= point[2] < (i + 90):
                    quick_sum.append(point[1])
            if len(quick_sum) > 0:
                ave_speed = np.mean(quick_sum)
                ave_speed_list.append(np.round_(ave_speed, decimals=2))

    return sorted(ave_speed_list)


def len_equalizer(list1, list2):
    if len(list1) > len(list2):
        to_sub_index = (len(list1) - len(list2)) / 2
        if to_sub_index is not int:
            list1 = list1[
                int(to_sub_index - 0.5) : int(len(list1) - (to_sub_index + 0.5))
            ]
        else:
            list1 = list1[int(to_sub_index) : int(len(list1) - to_sub_index)]
    elif len(list1) < len(list2):
        to_sub_index = (len(list2) - len(list1)) / 2
        if to_sub_index is not int:
            list2 = list2[
                int(to_sub_index - 0.5) : int(len(list2) - (to_sub_index + 0.5))
            ]
        else:
            list2 = list2[int(to_sub_index) : int(len(list2) - to_sub_index)]
    return list1, list2


def rmspe(actual, estimated):
    actual, estimated = len_equalizer(actual, estimated)
    return np.linalg.norm((actual - estimated) / actual) / np.sqrt(len(actual))
