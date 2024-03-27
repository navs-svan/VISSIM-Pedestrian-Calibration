from helper import *
import numpy as np


def theils_indicator(actual, simulated):
    """
    Summary:
        - Calculates the Theil's indicator U for model validation

    Arguments:
        - actual (list): The observed individual average pedestrian speeds
        - simulated (list): The simulated individual average pedestrian speeds

    Returns:
        - float: Theil's indicator U
    """
    actual, simulated = len_equalizer(actual, simulated)
    numerator = np.linalg.norm((simulated - actual)) / np.sqrt(len(actual))
    denominator = (np.linalg.norm(simulated) / np.sqrt(len(actual))) + (
        np.linalg.norm(actual) / np.sqrt(len(actual))
    )
    return numerator / denominator


if __name__ == "__main__":
    # Define Variables
    crosswalk_one_parameters = [
        [0.107, 1.416, 0.106, 0.367, 5.597],
        [0.107, 0.367, 0.107, 0.367, 5.6],
        [0.107, 1.416, 0.107, 0.367, 5.6],
        [0.122, 1.072, 0.127, 0.322, 5.343],
        [0.118, 1.061, 0.115, 0.31, 6.552],
        [0.118, 1.052, 0.103, 0.3, 6.377],
    ]

    crosswalk_two_parameters = [
        [0.107, 1.416, 0.128, 0.367, 5.6],
        [0.1, 2.397, 0.135, 0.677, 5.1],
        [0.107, 1.231, 0.113, 0.591, 6.872],
        [0.107, 0.578, 0.128, 1.416, 6.0],
        [0.135, 1.185, 0.104, 0.493, 6.885],
        [0.127, 1.357, 0.291, 0.417, 6.882],
        [0.131, 1.175, 0.27, 0.457, 6.556],
        [0.107, 1.328, 0.134, 0.586, 6.677],
        [0.14, 1.317, 0.273, 0.379, 6.526],
    ]

    crosswalk_combined_parameters = [
        [0.107, 0.684, 0.107, 0.367, 5.6],
        [0.107, 1.416, 0.107, 0.367, 5.6],
        [0.107, 1.061, 0.11, 0.367, 6.752],
        [0.157, 1.008, 0.139, 0.35, 6.308],
        [0.115, 1.029, 0.115, 0.34, 6.1],
        [0.127, 1.027, 0.113, 0.319, 6.126],
    ]

    crosswalk_comparison_parameters = [
        [0.400, 2.720, 0.200, 0.400, 3.00],
        (0.118, 1.052, 0.103, 0.3, 6.377),
        (0.14, 1.317, 0.273, 0.379, 6.526),
        (0.115, 1.029, 0.115, 0.34, 6.1),
    ]

    crosswalk_one_actual = np.np.genfromtxt(
        "./csv_data/valid_cw_one.csv", delimiter=","
    )
    crosswalk_two_actual = np.np.genfromtxt(
        "./csv_data/valid_cw_two.csv", delimiter=","
    )
    crosswalk_combined_actual = np.asarray(
        sorted(np.concatenate((crosswalk_two_actual, crosswalk_one_actual)))
    )
    results_dictonary = {}

    # Call Functions
    Vissim = set_vissim(5, 42, "Intersection.inpx")
    time = 900
    sm_aura_id = 1
    market_market_id = 2
    from_west_id = 3
    Vissim.Net.PedestrianInputs.ItemByKey(sm_aura_id).SetAttValue("Volume(1)", 675)
    Vissim.Net.PedestrianInputs.ItemByKey(market_market_id).SetAttValue(
        "Volume(1)", 600
    )
    Vissim.Net.PedestrianInputs.ItemByKey(from_west_id).SetAttValue("Volume(1)", 75)
    Vissim.Net.PedestrianRoutingDecisionsStatic.ItemByKey(
        market_market_id
    ).PedRoutSta.ItemByKey(1).SetAttValue("RelFlow(1)", 560)
    Vissim.Net.PedestrianRoutingDecisionsStatic.ItemByKey(
        market_market_id
    ).PedRoutSta.ItemByKey(2).SetAttValue("RelFlow(1)", 40)

    # CHANGE CROSSWALK_ONE_PARAMETERS TO OTHER LISTS
    for param in crosswalk_comparison_parameters:
        set_parameters(Vissim, param)
        local_ped_list_one, local_ped_list_two = get_data(Vissim, time)

        # Uncomment when validating SM Aura
        local_ave_speed_one = get_average(local_ped_list_one, time)
        error = rmspe(crosswalk_one_actual, local_ave_speed_one)
        theils_index = theils_indicator(crosswalk_one_actual, local_ave_speed_one)

        # Uncomment when validating Market Market
        # local_ave_speed_two = get_average(local_ped_list_two, time)
        # error = rmspe(crosswalk_two_actual, local_ave_speed_two)
        # theils_index = theils_indicator(crosswalk_two_actual, local_ave_speed_two)

        # Uncomment validating both combined
        # local_ave_speed_combined = np.asarray(
        #     sorted(np.concatenate((get_average(local_ped_list_one, time), get_average(local_ped_list_two, time)))))
        # error = rmspe(crosswalk_combined_actual, local_ave_speed_combined)
        # theils_index = theils_indicator(crosswalk_combined_actual, local_ave_speed_combined)

        key_param = tuple(param)
        results_dictonary[key_param] = (theils_index, error)
        print(
            f"Theil's Index: {round(theils_index, 3)}\nRMSPE value: {round(error, 3)}"
        )

    for key, value in results_dictonary.items():
        print(key, value)
