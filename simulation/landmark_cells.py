import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
n_cells = 100
J0 = 0.5
tau_m = 1.3 # Time constant for decay
dt = 0.01
dt_T = 0.001  # Learning rate for weights
total_time = 40
steps = int(total_time / dt)
v_c0 = 1  # Characteristic speed
delta_u = 2 * np.pi / n_cells  # Spacing between cells
epsilon1 = 0.2  # Modulation factor for EC and WC cells
epsilon_LM = 0.2  # Modulation factor for landmark cells
delta_phi = 15  # Phase difference for EC and WC cells
v = 2 # Velocity of the agent

# Initialize activations
s = np.random.uniform(-1, 1, n_cells)
s_EC = np.zeros(n_cells)
s_WC = np.zeros(n_cells)
s_L1 = np.zeros(steps)
s_L2 = np.ones(steps)

# Randomly initialize weights for landmark cells
W_1 = np.random.uniform(0, 0.6, n_cells)
W_2 = np.random.uniform(0, 0.6, n_cells)



def J(delta_u):
    return J0 * np.cos(delta_u)

def G(h):
    return np.clip(h, -1, 1)

def update_activations(s, s_EC, s_WC, W_1, W_2, s_L1, s_L2, t, epsilon1=epsilon1, epsilon_LM=epsilon_LM):
    n_cells = len(s)
    new_s = np.zeros_like(s)
    delta_u = 2 * np.pi / n_cells

    for i in range(n_cells):
        interaction_sum = sum(J((i - j) * delta_u) * s[j] * delta_u for j in range(n_cells))
        s_EC_interaction = epsilon1 * s_EC[i]
        s_WC_interaction = epsilon1 * s_WC[i]
        landmark_input = epsilon_LM * (W_1[i] * s_L1[t] + W_2[i] * s_L2[t])
        nonlinear_interaction = G(interaction_sum + s_EC_interaction + s_WC_interaction + landmark_input)
    
        new_s[i] = s[i] + dt * (-s[i] / tau_m + nonlinear_interaction)

    return new_s

def update_weights(W, activation_history, s_L, dt_T):
    cum_product_u = np.zeros(len(W))
    for t in range(len(s_L)):
        for i in range(len(W)):
            cum_product_u[i] += s_L[t] * activation_history[t][i]

    s_L_sum = np.sum(s_L) if np.sum(s_L) != 0 else 1

    new_W = W.copy()
    for i in range(len(W)):
        potentiation = cum_product_u[i] / s_L_sum
        decay = W[i]
        new_W[i] += dt_T * (potentiation - decay)
    return new_W

# Simulation loop
activation_history = [s.copy()]
ec_activation_history = [s_EC.copy()]
wc_activation_history = [s_WC.copy()]
w1_history = [W_1.copy()]
w2_history = [W_2.copy()]

for step in range(steps):

    if step % 10 == 0:
        W_1 = update_weights(W_1, activation_history, s_L1[:step], dt_T)
        W_2 = update_weights(W_2, activation_history, s_L2[:step], dt_T)

    s_EC = np.zeros_like(s)
    s_WC = np.zeros_like(s)
    
    # Update main ring activations
    s = update_activations(s, s_EC, s_WC, W_1, W_2, s_L1, s_L2, step)
    activation_history.append(s.copy())
    ec_activation_history.append(np.roll(s_EC, int(delta_phi)).copy())
    wc_activation_history.append(np.roll(s_WC, -int(delta_phi)).copy())
    w1_history.append(W_1.copy())
    w2_history.append(W_2.copy())
    

np.save(os.path.join('./simulation/data/','landmark_velocity_activations.npy'), np.array(activation_history))
np.save(os.path.join('./simulation/data/','landmark_activations_ec.npy'), np.array(ec_activation_history))
np.save(os.path.join('./simulation/data/','landmark_activations_wc.npy'), np.array(wc_activation_history))
np.save(os.path.join('./simulation/data/','landmark_w1_history.npy'), np.array(w1_history))
np.save(os.path.join('./simulation/data/','landmark_w2_history.npy'), np.array(w2_history))
np.save(os.path.join('./simulation/data/','landmark_1.npy'), np.array(s_L1))
np.save(os.path.join('./simulation/data/','landmark_2.npy'), np.array(s_L2))

# Plot results
plt.figure(figsize=(10, 6))
plt.imshow(activation_history.T, aspect='auto', cmap='viridis')
plt.colorbar()
plt.title('Ring Attractor Dynamics with EC and WC Cells')
plt.xlabel('Time Steps')
plt.ylabel('Cell Index')
plt.show()