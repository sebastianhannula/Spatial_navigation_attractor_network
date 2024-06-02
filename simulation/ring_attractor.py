import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
n_cells = 100  # Number of cells in the ring
J0 = 0.4  # Strength of the synaptic weights
tau_m = 1.3 # Time constant for decay
dt = 0.01  # Time step for the simulation
total_time = 14  # Total time to simulate
steps = int(total_time / dt)  # Number of steps in the simulation
delta_u = 2 * np.pi / n_cells  # Spacing between cells


# Initialize activations
initial_activations = np.random.uniform(-1, 1, n_cells)

# Synaptic weight function
def J(delta_u):
    return J0 * np.cos(delta_u)

# Nonlinearity function
def G(h):
    return np.clip(h, -1, 1)

# Compute interactions and update activations
def update_activations(activations):
    new_activations = np.zeros_like(activations)
    for i in range(n_cells):
        interaction_sum = 0
        for j in range(n_cells):
            interaction_sum += J((i - j) * delta_u) * activations[j] * delta_u
        input_i = G(interaction_sum)
        new_activations[i] = activations[i] + dt * (-activations[i] / tau_m + input_i)
    return new_activations


display_duration = 100 

activation_history = [initial_activations.copy()] * display_duration 
activations = initial_activations
for step in range(steps):
    activations = update_activations(activations)
    activation_history.append(activations.copy())

np.save(os.path.join('./simulation/data/', 'attractor_activations.npy'), np.array(activation_history))

# Plotting the results
plt.figure(figsize=(10, 6))
plt.imshow(activation_history.T, aspect='auto', interpolation='nearest', cmap='viridis')
plt.colorbar(label='Activation')
plt.xlabel('Time step')
plt.ylabel('Cell index')
plt.title('Evolution of Cell Activations in Ring Attractor with Extended Initial and Disturbance Display')
plt.show()