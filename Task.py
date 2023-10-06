#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Mar 24 19:12:15 2020
    @author: rsankar
    
    This script belongs to a modified reimplementation of the models described in -
    Pyle, R. and Rosenbaum, R., 2019.
    A reservoir computing model of reward-modulated motor learning and automaticity.
    Neural computation, 31(7), pp.1430-1461.
    
    This script creates the task object, with task-specific functions used by all three algorithms.
    
"""

import numpy as np


class Task:
    
    def __init__(self, exp, parameters):
        """
            Initialise the task object.
            
            exp: dict
                Task description where:
                    rseed           : seed for random generator; if rseed=0, a random seed is used
                    dataset_file    : file to store task datapoints
                    algorithm       : learning algorithm to simulate
                    results_folder  : path to store results
                    git-hash        : version of model being simulated
                    timespan        : duration of 1 experiment trial
                    task_type       : type of task, the model is to be run on
                    n_segs          : no. of arm segments (irrelevant for task #1)
                    arm_len         : length of each arm segment (irrelevant for task #1)
                    arm_cost        : cost of moving each arm segment (irrelevant for task #1 and #2)
                    display_plot    : show the plot, too, or just save it
                    plot_format     : file format for saving plot (ps, eps, pdf, pgf, png, raw, rgba, svg, svgz, jpg, jpeg, tif, tiff)
                    
            parameters: dict
                Parameter values where:
                    N               : no. of neurons in reservoir
                    lmbda           : controls spectral radius
                    sparsity        : connectivity sparsity in reservoir
                    dT              : time gradient in ms
                    n_train_trials  : no. of training trials
                    n_test_trials   : no. of testing trials
                    alpha           : attenuate noise
                    gamma           : Initialising factor for P matrix
                    k               : SUPERTREX learning rate
                    tau             : time constant of reservoir
                    tau_w           : time constant of weight updation
                    tau_e           : low pass filter for MSE
                    tau_z           : low pass filter for z
        """
        
        # Task parameters
        self.task_file  = exp['dataset_file']
        self.T          = exp['timespan']
        self.type       = exp['task_type']
        
        # Arm parameters
        self.arm_segs   = np.array(exp['arm_len'],  ndmin=2)
        self.arm_cost   = np.array(exp['arm_cost'], ndmin=2)
        self.n_segs     = exp['n_segs']

        # Task data points
        self.build_dataset(parameters)
        self.data = np.load(self.task_file)
        
        
    def build_dataset(self, parameters):
        """ Builds the butterfly datapoints for the task according to given parameters. """

        # Change #1: Due to author code
        # t = np.linspace(0, 1, self.T / parameters['dT'])
        # q = 2 * np.pi
        #
        # # t = np.arange(0, self.T, parameters['dT'])                              # ms
        # # q = 2*np.pi / self.T                                                    # spans 0,2*np.pi
        #
        # # Trajectory for butterfly
        # r = 9 - np.sin(q*t) + 2*np.sin(3*q*t) + 2*np.sin(5*q*t) - np.sin(7*q*t) + 3 * np.cos(2*q*t) - 2*np.cos(4*q*t)
        # c = np.max(np.abs(r))
        # c = 14.4734                                                             # Change #2: Due to author code, clearly wrong
        # r = r/c
        #
        # # Coordinates
        # x = r * np.cos(q*t)
        # y = r * np.sin(q*t)


        ## Altered as per MATLAB codes
        theta = np.linspace(0, 2 * np.pi, int(self.T / parameters['dT']))

        xout = 9 - np.sin(theta) + 2 * np.sin(3 * theta) + 2 * np.sin(5 * theta) - np.sin(7 * theta) + 3 * np.cos(2 * theta) - 2 * np.cos(4 * theta)
        xout = xout * np.cos(theta) / 14.4734  # 14.4734 is max r
        yout = 9 - np.sin(theta) + 2 * np.sin(3 * theta) + 2 * np.sin(5 * theta) - np.sin(7 * theta) + 3 * np.cos(2 * theta) - 2 * np.cos(4 * theta)
        yout = yout * np.sin(theta) / 14.4734

        # Save in file
        np.savez(self.task_file, x=xout, y=yout)

        
    def h(self, z):
        """ Function to convert angles into cartesian coordinates. """

        if self.type == 1:
            return np.array([z[0,0], z[1,0]], ndmin=2).T
        
        else:
            x = np.dot(self.arm_segs,np.sin(np.cumsum(z)*np.pi))
            y = np.dot(self.arm_segs,np.cos(np.cumsum(z)*np.pi))-2
            return np.array([x, y])


    def psi(self, x, tn, ts):
        """ Increasing function to quench exploration when error is low. """

        if self.type == 1:      return np.sign(x) * 0.025 * np.power(10*np.abs(x), 1/4)
        elif self.type == 2:    return np.sign(x) * 0.01  * np.power(10*np.abs(x), 1/5)
        elif self.type == 3:    return np.sign(x) * 0.005 * np.power(10*np.abs(x), 1/4)
    
    
    def phi(self, x):
        """ Odd sublinear function to quench learning when error is low. """
        # In author's code, for task 1, phi is zero when x<0 and "+5" for Task 2 and 3.

        return -5 * np.sign(x) * np.power(np.abs(x), 1/4)



    def cost(self, z_hat):
        """ Function to compute cost of a certain arm movement. """

        if self.type < 3:
            return 0
        else:
            c = np.dot(self.arm_cost,np.abs(z_hat))
            return c[0,0]


    def norm(self, W):
        """ Function to compute norm as per author's code. """

        W_dot = (np.dot(W,W.T)).astype(complex)
        if np.all(np.isfinite(W_dot)) == False or np.any(np.isnan(W_dot)) == True:  W_norm = 0
        else:   W_norm = np.linalg.norm(np.sqrt(W_dot),2)

        return W_norm


    def rand_int(s, high, sz):
        """
            Function to replicate matlab's rand_int.
            It returns sz integers between 0 and high (not included).
            Note: It does not work if, by chance, r=0.
        """

        r = np.random.uniform(size=sz)
        return (np.ceil(r * high) - 1).astype(int)

    def round_up(s, n):
        """ Fuction to replicate matlab's round function (half up)."""

        return int(np.floor(n + 0.5))
    
    def compensation(self, learning_rule):
        """ Modification #1: Arbitrary function to compensate for exploding values of weights. """

        if self.type ==  2 and self.n_segs > 2:     return 0.1/self.n_segs
        elif self.type ==  3 and self.n_segs > 2:   return 0.5/self.n_segs
        else:                   return 1

    @staticmethod
    def noise_adder_sparse(arr, noise_variance, w_sparseness):
      """ Returns inputed array with sparsly (given by w_sparsness) added gaussian noise with mu = 0 and sigma=noise_variance.
            arr             = weight array which needs the added noise
            w_sparseness    = Percentage of weights which get noise added. Please input as 0.-1..
            noise_variance  = the added noise is a Gaussian Distribution with mu = 0 and sigma=noise_variance. Input as float.
      """
      noise = np.random.normal(0, noise_variance,[arr.shape[0],arr.shape[1]])
      percentage = int(arr.shape[1]-w_sparseness*arr.shape[1])
      noise[:,:percentage]  = 0
      [np.random.shuffle(noise[x]) for x in range(noise.shape[0])]

      arr = noise + arr

      return arr

    @staticmethod
    def noise_adder(arr, noise_variance):
        """ Returns inputed array with noise added on each weight.
            arr             = weight array which needs the added noise
            noise_variance  =  the added noise is a Gaussian Distribution with mu = 0 and sigma=noise_variance. Input as float.
        """
        noise = np.random.normal(0, noise_variance,[arr.shape[0],arr.shape[1]])
        arr = arr + noise
        return arr, noise

    @staticmethod
    def noise_adder_percentage(arr, noise_sigma):
      """ Returns inputed array with added noise on each weight. Gaussian Distribution Noise added.
          Mu=0, Signma based on the noise_sigma of avg weights for each output added to each weights of corresponding output.
            arr               = weight array which needs the added noise
            noise_sigma  = How much of the average signal should be added as noice. Determince the variance of noise. Input Range 0.-1..
      """
      noise_variance = np.array(np.mean(np.abs(arr), axis=1) * noise_sigma)
      noise = np.random.normal(0, noise_variance,[arr.shape[1],arr.shape[0]]).T
      noised_array = arr + noise

      return noised_array, noise 
    
    
    @staticmethod
    def running_mean(x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0)) 
        return (cumsum[N:] - cumsum[:-N]) / float(N)
