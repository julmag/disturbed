import numpy as np

def noise_adder_percentage(arr, noise_sigma):
    """ Returns inputed array with added noise on each weight. Gaussian Distribution Noise added.
        Mu=0, Signma based on the noise_sigma of avg weights for each output added to each weights of corresponding output.
        arr               = weight array which needs the added noise
        noise_sigma  = How much of the average signal should be added as noice. Determince the variance of noise. Input Range 0.-1..
    """
    noise_variance = np.array(np.mean(np.abs(arr), axis=1) * noise_sigma)
    print("noise_variance", noise_variance)
    noise = np.random.normal(0, noise_variance,[arr.shape[1],arr.shape[0]]).T
    print("noise", noise)
    noised_array = arr + noise
    print("noised_array", noised_array)

    return noised_array, noise 


a = np.zeros((2,10))

b = noise_adder_percentage(a, 0.005)

print("pogo")