import numpy as np
import os

# Get the current working directory
current_dir = os.getcwd()

# Specify the name of the .npz file you want to open
file_name = 'Data.npz'

# Construct the full file path
file_path = os.path.join(current_dir, file_name)

# Load the .npz file
loaded_data = np.load("Data.npz")

# Access the individual arrays stored in the .npz file using keys
# For example, if you have an array named 'array1' in the file:
array1 = loaded_data['error']

# You can access other arrays in a similar manner, using their respective keys

# Close the .npz file when you're done
loaded_data.close()

def pogo (x):
  return -.5 * np.tanh(500000 * (np.abs(x) - (1.5e-3))) + .5

b=pogo(array1[-1,:])
print(b)

print("pogo")



