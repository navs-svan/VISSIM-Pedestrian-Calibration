import numpy as np
from helper import *
from scipy import stats


def check_halfwidth(speed):
    stand_dev = np.std(speed, ddof=1)
    mean = np.mean(speed)
    t_val = stats.t.ppf(1 - (alpha / 2), len(speed) - 1)  # 95% confidence
    h = t_val * stand_dev / np.sqrt(len(speed))

    return mean, h


if __name__ == '__main__':
    walking_behavior_param = {'CW1': (0.118, 1.052, 0.103, 0.3, 6.377), 'DEFAULT': (0.400, 2.720, 0.200, 0.400, 3.00)}

    Vissim = set_vissim(10, 42, 'Intersection - uninterrupted.inpx')

    # Uncomment when we want to analyze calibrated parameters
    set_parameters(Vissim, walking_behavior_param["CW1"])

    # Uncomment when we want to analyze the default parameters
    # set_parameters(Vissim, walking_behavior_param['DEFAULT'])

    Sim_break_at = 3599
    Vissim.Simulation.SetAttValue('SimBreakAt', Sim_break_at)
    
    link_1 = 1
    link_2 = 2
    sm_aura_id = 1
    market_market_id = 2
    street_id = 3
    alpha = 0.05
    margin_of_error = 0.05
    speed_den_relation_bi = []
    speed_den_relation_uni = []

    for volume in range(0, 5000, 250):
        print(f'\nVOLUME: {volume}\n')
        if volume == 0:
            volume = 100
        Vissim.Net.PedestrianInputs.ItemByKey(sm_aura_id).SetAttValue('Volume(1)', volume)
        Vissim.Net.PedestrianInputs.ItemByKey(market_market_id).SetAttValue('Volume(1)', volume)
        Vissim.Net.PedestrianInputs.ItemByKey(street_id).SetAttValue('Volume(1)', volume)
        counter = 0

        # Bidirectional Flow
        speed_list_1 = []
        density_list_1 = []
        number_list_1 = []

        # Unidirectional Flow
        speed_list_2 = []
        density_list_2 = []
        number_list_2 = []
        while True:
            seed = 42 + (2 * counter)
            print(seed)
            Vissim.Simulation.SetAttValue('RandSeed', seed)
            Vissim.Simulation.RunContinuous()

            density_bi = Vissim.Net.AreaMeasurements.ItemByKey(link_1).AttValue('DensAvg(Current,Current)')
            speed_bi = Vissim.Net.AreaMeasurements.ItemByKey(link_1).AttValue('SpeedAvg(Current,Current,40)')
            number_bi = Vissim.Net.AreaMeasurements.ItemByKey(link_1).AttValue('NumPedsAvg(Current,Current,40)')

            density_uni = Vissim.Net.AreaMeasurements.ItemByKey(link_2).AttValue('DensAvg(Current,Current)')
            speed_uni = Vissim.Net.AreaMeasurements.ItemByKey(link_2).AttValue('SpeedAvg(Current,Current,40)')
            number_uni = Vissim.Net.AreaMeasurements.ItemByKey(link_2).AttValue('NumPedsAvg(Current,Current,40)')

            Vissim.Simulation.Stop()

            # print(f'Seed = {42 + (2 * counter)}\nDensity = {density} ped/square meter\nAverage Speed = {speed} km/hr')

            speed_list_1.append(speed_bi / 3.6)
            density_list_1.append(density_bi)
            number_list_1.append(number_bi)

            speed_list_2.append(speed_uni / 3.6)
            density_list_2.append(density_uni)
            number_list_2.append(number_uni)

            if counter >= 4:
                mean_1, h_1 = check_halfwidth(speed_list_1)
                mean_2, h_2 = check_halfwidth(speed_list_2)
                if h_1 <= margin_of_error and h_2 <= margin_of_error:

                    mean_density_1 = np.mean(density_list_1)
                    mean_number_1 = np.mean(number_list_1)
                    mean_density_2 = np.mean(density_list_2)
                    mean_number_2 = np.mean(number_list_2)
                    break

            counter += 1

        speed_den_relation_bi.append([mean_density_1, mean_1, h_1, mean_number_1])
        speed_den_relation_uni.append([mean_density_2, mean_2, h_2, mean_number_2])

    np.savetxt("bidirectional.csv", speed_den_relation_bi, delimiter=", ", fmt='% s')
    np.savetxt("unidirectional.csv", speed_den_relation_uni, delimiter=", ", fmt='% s')
