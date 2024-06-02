import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
n_cells = 100
J0 = 0.5
tau_m = 1.3 # Time constant for decay
dt = 0.01
total_time = 40
steps = int(total_time / dt)
v_c0 = 1  # Characteristic speed
delta_u = 2 * np.pi / n_cells  # Spacing between cells
epsilon1 = 0.2  # Modulation factor for EC and WC cells
delta_phi = 15  # Phase difference for EC and WC cells
v = 2

# Initialize activations
s = np.random.uniform(-1, 1, n_cells)
s_EC = np.zeros(n_cells)
s_WC = np.zeros(n_cells)

def J(delta_u):
    return J0 * np.cos(delta_u)

def G(h):
    return np.clip(h, -1, 1)


def update_activations(s, s_EC, s_WC, epsilon1):
    n_cells = len(s)
    delta_u = 2 * np.pi / n_cells
    new_s = np.zeros_like(s)
    for i in range(n_cells):
        interaction_sum = sum(J((i - j) * delta_u) * s[j] * delta_u for j in range(n_cells))
        s_EC_interaction = epsilon1 * s_EC[i]
        s_WC_interaction = epsilon1 * s_WC[i]
        nonlinear_interaction = G(interaction_sum + s_EC_interaction + s_WC_interaction)
        
        new_s[i] = s[i] + dt * (-s[i] / tau_m + nonlinear_interaction )
    return new_s


# Simulation loop
activation_history = [s.copy()]
ec_activation_history = [s_EC.copy()]
wc_activation_history = [s_WC.copy()]
for step in range(steps):
    if step >= 1000:
        s_EC = (v/v_c0) * np.roll(s, -int(delta_phi))
        s_WC = np.zeros_like(s)

    else:
        s_EC = np.zeros_like(s) 
        s_WC = np.zeros_like(s)  
    
    s = update_activations(s, s_EC, s_WC, epsilon1)
    activation_history.append(s.copy())
    ec_activation_history.append(np.roll(s_EC, int(delta_phi)).copy())
    wc_activation_history.append(np.roll(s_WC, -int(delta_phi)).copy())


np.save(os.path.join('./simulation/data/','velocity_activations.npy'), np.array(activation_history))
np.save(os.path.join('./simulation/data/','velocity_activations_ec.npy'), np.array(ec_activation_history))
np.save(os.path.join('./simulation/data/','velocity_activations_wc.npy'), np.array(wc_activation_history))

# Plot results
plt.figure(figsize=(10, 6))
plt.imshow(activation_history.T, aspect='auto', cmap='viridis')
plt.colorbar()
plt.title('Ring Attractor Dynamics with EC and WC Cells')
plt.xlabel('Time Steps')
plt.ylabel('Cell Index')
plt.show()