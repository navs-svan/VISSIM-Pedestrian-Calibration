import win32com.client as com
import numpy as np
from typing import Tuple, List


def set_vissim(resolution: int, seed: int, filename: str) -> object:
    """
    Summary:
        - Creates a Vissim COM object using Dispatch() and sets the
        simulation resolution and random seed of the simulation software

    Arguments:
        - resolution (int): The simulation resolution or the number of
            times the position of a pedestrian/vehicle will be calculated
            within one simulated second. A higher resolution will allow a
            pedestrian to change behavior at higher frequencies. Value
            ranges from 1 to 10.
        - seed (int): The random seed number of the simulation.
        - filename (str): Path of the model.inpx file

    Returns:
        - object: Vissim COM object used to access the COM interface
    """
    Vissim = com.dynamic.Dispatch("Vissim.Vissim")

    Vissim.LoadNet(filename)

    # Set simulation Parameters
    End_of_simulation = 3610  # simulation second [s]
    Vissim.Simulation.SetAttValue("SimPeriod", End_of_simulation)

    sim_resolution = resolution
    Vissim.Simulation.SetAttValue("SimRes", sim_resolution)

    sim_seed = seed
    Vissim.Simulation.SetAttValue("RandSeed", sim_seed)
    Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 1)
    return Vissim


def set_parameters(Vissim: object, parameter_list: list) -> None:
    """
    Summary:
        - Sets the walking parameters of pedestrians under the Social
        Force model of Vissim

    Arguments:
        - Vissim (COM object): COM object needed to access the COM interface
        - parameter_list (list): List of walking parameters that will be set.
            The order of the parameters should be
            ["Tau", "ASocIso", "BSocIso", "ASocMean", "VD"].
    """
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


def get_data(Vissim: object, time: int) -> Tuple[List, List]:
    """
    Summary:
        - Retrieves the individual pedestrian speeds per simulation resolution
        for SM Aura and Market Market over a set amount of simulation time.

    Arguments:
        - Vissim (COM object): COM object needed to access the COM interface
        - time (int): Total simulation time in seconds

    Returns:
        - Tuple[List, List]: A tuple containing two lists of individual pedestrian
            speeds. The first item is for the SM Aura crosswalk, while the second item is
            for the Market Market crosswalk. Both lists contain the
            [pedestrian number, pedestrian speed, and simulation second]
    """

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


def get_average(list_input: list, time: int) -> list:
    """
    Summary:
        - Gets the individual average speeds of pedestrian. Due to Vissim repeating
        pedestrian numbers over its simulation duration, a rudimentary approach 
        involving the pedestrian cycle time was implemented to separate pedestrians
        with the same pedestrian number.


    Arguments:
        - list_input (list): list of individual pedestrian speeds per simulation resolution
            obtained from helper.get_data()
        - time (int): Simulation time in seconds

    Returns:
        - list: List of individual average pedestrian speeds
    """
    ave_speed_list = []
    # The range step value is equal to the observed cycle time of pedestrian signal
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


def len_equalizer(list1: list, list2: list) -> Tuple[List, List]:
    """
    Summary:
        - Equalizes the len between two lists by removing the upper
        and lower ends the larger list

    Arguments:
        - list1 (list): The first list
        - list2 (list): The second list

    Returns:
        - Tuple[List, List]: Returns the equalized lists
    """
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


def rmspe(actual: list, simulated: list) -> float:
    """
    Summary:
        - Calculates the root mean square percentage error between the actual
        and simulated pedestrian speeds

    Arguments:
        - actual (list): The observed individual average pedestrian speeds
        - simulated (list): The simulated individual average pedestrian speeds 

    Returns:
        - float: The root mean square percentage error
    """
    actual, simulated = len_equalizer(actual, simulated)
    return np.linalg.norm((actual - simulated) / actual) / np.sqrt(len(actual))
