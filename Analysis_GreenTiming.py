from helper import *
import csv

if __name__ == "__main__":
    walking_behavior_param = {
        "CW1": (0.118, 1.052, 0.103, 0.3, 6.377),
        "DEFAULT": (0.400, 2.720, 0.200, 0.400, 3.00),
    }

    Vissim = set_vissim(10, 42, "Intersection - modified.inpx")

    # Uncomment when we want to analyze calibrated parameters
    set_parameters(Vissim, walking_behavior_param["CW1"])

    # Uncomment when we want to analyze the default parameters
    # set_parameters(Vissim, walking_behavior_param['DEFAULT'])

    time = (90 * 40) + 3
    signal_indicator = Vissim.Net.SignalHeads.ItemByKey(9)
    sm_aura_id = 1
    market_market_id = 2

    additional_time = set()
    clearance_summary_global = []
    number_summary_global = []
    speed_summary_global = []

    for volume in range(0, 5250, 250):
        if volume == 0:
            volume = 50

        Vissim.Net.PedestrianInputs.ItemByKey(sm_aura_id).SetAttValue(
            "Volume(1)", 0
        )  # We'll only analyze one crosswalk
        Vissim.Net.PedestrianInputs.ItemByKey(market_market_id).SetAttValue(
            "Volume(1)", volume
        )

        clearance_summary = []
        number_summary = []
        speed = 0
        current_green_start = 0
        curr_ped_number = 0
        previous_ped_number = 0
        previous_state = "RED"
        counter = 0

        for i in range((time * int(Vissim.Simulation.AttValue("SimRes")))):
            Vissim.Simulation.RunSingleStep()
            sig_state = signal_indicator.AttValue("SigState")
            if sig_state == "RED":
                All_Ped = Vissim.Net.Pedestrians.GetMultipleAttributes(
                    ("No", "ConstrElType", "SimSec", "Speed")
                )
                for cur_ped in All_Ped:
                    ped_number = cur_ped[0]
                    ped_location = cur_ped[1]
                    ped_sim_sec = cur_ped[2]
                    ped_speed = cur_ped[3]
                    if (
                        ped_location == "PEDESTRIANLINK"
                        and current_green_start
                        <= ped_sim_sec
                        <= (current_green_start + 45)
                    ):
                        additional_time.add(ped_sim_sec)
            elif sig_state == "GREEN" and previous_state == "RED":
                curr_ped_number = Vissim.Net.PedestrianTravelTimeMeasurements.ItemByKey(
                    1
                ).AttValue("Peds(Current,Current,40)")
                current_green_start = (counter * 90) + 2
                counter += 1
                if len(additional_time) > 0:
                    needed_clearance = max(additional_time) - min(additional_time)
                    clearance_summary.append(round(needed_clearance, 2))

                ped_number_1 = curr_ped_number - previous_ped_number

                number_summary.append(ped_number_1)

                additional_time.clear()
                previous_ped_number = curr_ped_number
            if i == (time * int(Vissim.Simulation.AttValue("SimRes"))) - 1:
                speed = Vissim.Net.AreaMeasurements.ItemByKey(1).AttValue(
                    "SpeedAvg(Current,Current,40)"
                )
            previous_state = sig_state

        clearance_summary_global.append(clearance_summary)
        number_summary_global.append(number_summary)
        speed_summary_global.append(speed)

        Vissim.Simulation.Stop()

    # Change filename when analyzing a different set of parameters
    with open("clearance.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerows(clearance_summary_global)

    with open("number.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerows(number_summary_global)

    with open("speed.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(speed_summary_global)
