from Calibration import *
import numpy as np


def theils_indicator(actual, simulated):
    actual, simulated = len_equalizer(actual, simulated)
    numerator = np.linalg.norm((simulated - actual)) / np.sqrt(len(actual))
    denominator = (np.linalg.norm(simulated) / np.sqrt(len(actual))) + (np.linalg.norm(actual) / np.sqrt(len(actual)))
    return numerator / denominator


if __name__ == '__main__':
    crosswalk_one_parameters = [[0.107, 1.416, 0.106, 0.367, 5.597], [0.107, 0.367, 0.107, 0.367, 5.6],
                                [0.107, 1.416, 0.107, 0.367, 5.6], [0.122, 1.072, 0.127, 0.322, 5.343],
                                [0.118, 1.061, 0.115, 0.31, 6.552], [0.118, 1.052, 0.103, 0.3, 6.377]]
    crosswalk_two_parameters = [[0.107, 1.416, 0.128, 0.367, 5.6], [0.1, 2.397, 0.135, 0.677, 5.1],
                                [0.107, 1.231, 0.113, 0.591, 6.872], [0.107, 0.578, 0.128, 1.416, 6.0],
                                [0.135, 1.185, 0.104, 0.493, 6.885], [0.127, 1.357, 0.291, 0.417, 6.882],
                                [0.131, 1.175, 0.27, 0.457, 6.556], [0.107, 1.328, 0.134, 0.586, 6.677],
                                [0.14, 1.317, 0.273, 0.379, 6.526]]
    crosswalk_combined_parameters = [[0.107, 0.684, 0.107, 0.367, 5.6], [0.107, 1.416, 0.107, 0.367, 5.6],
                                     [0.107, 1.061, 0.11, 0.367, 6.752], [0.157, 1.008, 0.139, 0.35, 6.308],
                                     [0.115, 1.029, 0.115, 0.34, 6.1], [0.127, 1.027, 0.113, 0.319, 6.126]]
    crosswalk_comparison_parameters = [[0.400, 2.720, 0.200, 0.400, 3.00], (0.118, 1.052, 0.103, 0.3, 6.377),
                                       (0.14, 1.317, 0.273, 0.379, 6.526), (0.115, 1.029, 0.115, 0.34, 6.1)]

    crosswalk_one_actual = np.asarray(
        [3.601, 3.722, 3.75, 3.755, 3.817, 3.887, 3.901, 3.926, 3.986, 3.987, 4.048, 4.058, 4.063, 4.074, 4.091, 4.093,
         4.094, 4.107, 4.158, 4.209, 4.211, 4.234, 4.238, 4.245, 4.248, 4.256, 4.258, 4.26, 4.26, 4.268, 4.269, 4.274,
         4.283, 4.292, 4.328, 4.341, 4.345, 4.369, 4.384, 4.4, 4.406, 4.441, 4.462, 4.472, 4.474, 4.475, 4.483, 4.487,
         4.496, 4.509, 4.513, 4.52, 4.524, 4.532, 4.556, 4.563, 4.563, 4.563, 4.565, 4.58, 4.582, 4.582, 4.584, 4.588,
         4.588, 4.596, 4.6, 4.611, 4.612, 4.616, 4.618, 4.619, 4.629, 4.67, 4.679, 4.679, 4.681, 4.686, 4.688, 4.69,
         4.692, 4.695, 4.699, 4.733, 4.747, 4.757, 4.759, 4.775, 4.777, 4.792, 4.793, 4.796, 4.799, 4.807, 4.813, 4.816,
         4.839, 4.843, 4.845, 4.85, 4.853, 4.861, 4.862, 4.87, 4.874, 4.875, 4.88, 4.886, 4.892, 4.899, 4.908, 4.915,
         4.923, 4.926, 4.926, 4.933, 4.942, 4.95, 4.952, 4.955, 4.966, 4.969, 4.98, 4.985, 4.987, 4.99, 4.99, 4.993,
         5.004, 5.022, 5.026, 5.036, 5.048, 5.055, 5.061, 5.066, 5.071, 5.073, 5.091, 5.106, 5.135, 5.137, 5.153, 5.162,
         5.165, 5.188, 5.2, 5.213, 5.218, 5.235, 5.257, 5.258, 5.272, 5.273, 5.299, 5.309, 5.319, 5.322, 5.328, 5.335,
         5.344, 5.354, 5.364, 5.365, 5.378, 5.384, 5.41, 5.411, 5.417, 5.423, 5.424, 5.464, 5.466, 5.512, 5.535, 5.536,
         5.551, 5.563, 5.564, 5.584, 5.593, 5.595, 5.596, 5.6, 5.618, 5.626, 5.641, 5.643, 5.683, 5.684, 5.687, 5.7,
         5.708, 5.762, 5.766, 5.773, 5.78, 5.787, 5.799, 5.801, 5.806, 5.865, 5.885, 5.889, 5.956, 5.99, 5.99, 6.004,
         6.023, 6.024, 6.034, 6.039, 6.079, 6.082, 6.096, 6.114, 6.172, 6.241])
    crosswalk_two_actual = np.asarray(
        [4.231, 4.245, 4.368, 4.452, 4.49, 4.513, 4.549, 4.58, 4.582, 4.609, 4.667, 4.668, 4.673, 4.793, 4.853, 4.861,
         4.884, 4.913, 4.942, 5.02, 5.078, 5.086, 5.117, 5.14, 5.245, 5.27, 5.279, 5.311, 5.34, 5.36, 5.521, 5.566,
         5.803, 5.927])
    crosswalk_combined_actual = np.asarray(sorted(np.concatenate((crosswalk_two_actual, crosswalk_one_actual))))
    results_dictonary = {}
    Vissim = set_vissim(5, 42, 'Intersection.inpx')
    time = 900
    sm_aura_id = 1
    market_market_id = 2
    from_west_id = 3
    Vissim.Net.PedestrianInputs.ItemByKey(sm_aura_id).SetAttValue('Volume(1)', 675)
    Vissim.Net.PedestrianInputs.ItemByKey(market_market_id).SetAttValue('Volume(1)', 600)
    Vissim.Net.PedestrianInputs.ItemByKey(from_west_id).SetAttValue('Volume(1)', 75)
    Vissim.Net.PedestrianRoutingDecisionsStatic.ItemByKey(market_market_id).PedRoutSta.ItemByKey(1).SetAttValue(
        'RelFlow(1)', 560)
    Vissim.Net.PedestrianRoutingDecisionsStatic.ItemByKey(market_market_id).PedRoutSta.ItemByKey(2).SetAttValue(
        'RelFlow(1)', 40)
    # CHANGE CROSSWALK_ONE_PARAMETERS TO OTHER LISTS
    for param in crosswalk_comparison_parameters:
        set_parameters(Vissim, param)
        local_ped_list_one, local_ped_list_two = get_data(Vissim, time)

        local_ave_speed_one = get_average(local_ped_list_one, time)
        error = rmspe(crosswalk_one_actual, local_ave_speed_one)
        theils_index = theils_indicator(crosswalk_one_actual, local_ave_speed_one)

        # local_ave_speed_two = get_average(local_ped_list_two, time)
        # error = rmspe(crosswalk_two_actual, local_ave_speed_two)
        # theils_index = theils_indicator(crosswalk_two_actual, local_ave_speed_two)

        # local_ave_speed_combined = np.asarray(
        #     sorted(np.concatenate((get_average(local_ped_list_one, time), get_average(local_ped_list_two, time)))))
        # error = rmspe(crosswalk_combined_actual, local_ave_speed_combined)
        # theils_index = theils_indicator(crosswalk_combined_actual, local_ave_speed_combined)

        key_param = tuple(param)
        results_dictonary[key_param] = (theils_index, error)
        print(f"Theil's Index: {round(theils_index, 3)}\nRMSPE value: {round(error, 3)}")

    for key, value in results_dictonary.items():
        print(key, value)
