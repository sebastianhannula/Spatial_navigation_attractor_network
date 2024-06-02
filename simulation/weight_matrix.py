import numpy as np
import matplotlib.pyplot as plt

# Parameters
n_cells = 20  # Number of cells in the ring
J0 = 1.0      # Scaling factor for weights

# Synaptic weight function
def J(delta_u):
    return J0 * np.cos(delta_u)

weights = np.zeros((n_cells, n_cells))

for i in range(n_cells):
    for j in range(n_cells):
        delta_u = 2 * np.pi * (i - j) / n_cells
        weights[i, j] = J(delta_u)

# Plot the weight matrix
plt.figure(figsize=(8, 6))
plt.imshow(weights, cmap='viridis', interpolation='none')
plt.colorbar(label='Synaptic Weight')
plt.title('Synaptic Weight Matrix of Ring Attractor')
plt.xlabel('Cell Index')
plt.ylabel('Cell Index')
plt.xticks(range(n_cells))
plt.yticks(range(n_cells))
plt.show()