#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Mar 24 19:12:15 2020
    @author: rsankar
    
    This script belongs to a modified reimplementation of the models described in -
    Pyle, R. and Rosenbaum, R., 2019.
    A reservoir computing model of reward-modulated motor learning and automaticity.
    Neural computation, 31(7), pp.1430-1461.
    
    This script loads the json descriptor files with the task and simulation parameters and creates the experiment object.
    To run: python3 run.py --parameters="<path_to_parameter_file.json>" --experiment="<path_to_experiment_file.json>"
    
    """

import argparse, json
from Experiment import Experiment


if __name__ == "__main__":

    
    # Process arguments
    parser = argparse.ArgumentParser(description='Reimplementation of Rosenbaum 2019')
    parser.add_argument('--parameters', default='default_parameter_file.json', type=str, help='Path of parameter file.')
    parser.add_argument('--experiment', default='default_experiment_file.json', type=str, help='Path of experiment description file.')
    
    args                = parser.parse_args()
    arg_parameter_file  = args.parameters
    arg_exp_file        = args.experiment
    
    # # Load experiment and parameter files
    # exp        = json.load(open("task_parameter_file_Task1_ST.json"))
    # parameters = json.load(open("simulation_parameter_file_Task1_ST.json"))
    
    # # Verify parameters
    # supp_fig_file_types = ['ps', 'eps', 'pdf', 'pgf', 'png', 'raw', 'rgba', 'svg', 'svgz', 'jpg', 'jpeg', 'tif', 'tiff']
    # assert exp['algorithm'] in ['FORCE', 'RMHL', 'SUPERTREX'],  "algorithm must be FORCE, RMHL or SUPERTREX."
    # assert exp['task_type'] in [1, 2, 3],                       "task_type must be 1, 2 or 3."
    # assert exp['n_segs'] > 0,                                   "n_seg must be greater than zero."
    # assert len(exp['arm_len']) == exp['n_segs'],                "arm_len size " + str(len(exp['arm_len'])) + " is not the same as n_seg."
    # assert len(exp['arm_cost']) == exp['n_segs'],               "arm_cost size " + str(len(exp['arm_cost'])) + " is not the same as n_seg."
    # assert exp['display_plot'] in ['Yes', 'No'],                "display_plot must be Yes or No"
    # assert exp['plot_format'] in supp_fig_file_types,           "plot_format must be a valid image format for savefig: " + str(supp_fig_file_types)
    # assert parameters['n_train_trials'] >= 5,                   "n_train_trials must be greater than 4."

    exp = {
    "rseed"                 :   0,
    "dataset_file"          :   "butterfly_coords.npz",
    "algorithm"             :   "SUPERTREX",
    "results_folder"        :   "Results/SUPERTREX_Task2_Seg2",
    "git-hash"              :   0,
    "timespan"              :   10000,
    "task_type"             :   2,
    "n_segs"                :   2,
    "arm_len"               :   [1.8, 1.8],
    "arm_cost"              :   [0.0, 0.0],
    "display_plot"          :   "No",
    "plot_format"           :   "png"
}

    parameters = {
    "N"                 :   1000,
    "lmbda"             :   1.5,
    "sparsity"          :   0.1,
    "dT"                :   0.2,
    "n_train_trials"    :   10,
    "n_test_trials"     :   1,
    "alpha"             :   0.025,
    "gamma"             :   10,
    "k"                 :   0.5,
    "tau"               :   10,
    "tau_w"             :   0.02,
    "tau_e"             :   1000,
    "tau_z"             :   2
}


    print("Exp:", exp)
    print("Parameters", parameters)


    # Simulate experiment
    experiment = Experiment(exp, parameters)                                       # Initialise experiment
    experiment.run(exp)                                                            # Comment if you want to replot previously saved results
    experiment.plot(exp)                                                             # Plot results and saves figures


    print("Pogo")
