import numpy as np
import random
        
def gaussian(x, mu, sigma):
    return np.exp(-(1/2)*np.square((x-mu)/sigma))

def calculate_dopamine_activity(x):
    alpha, beta, x_star = (6,6, 0.27)
    if x < 0:
        return x/alpha
    elif x < x_star:
        return x
    else:
        return x_star + (x-x_star)/beta

N = 201 # number of trials
T = 25 # trial time in seconds
dt = 0.5 # time step in seconds
i = 1 # number of stimuli
spike = 10
mu, sigma = 20, 1
eps = 0.2
gamma = 1
T_mem = 12

domain = np.arange(0, T+dt, dt)
stimulus = np.zeros_like(domain)
stimulus[int(spike/dt)] = 1
reward = 0.5*np.array([gaussian(i, mu, sigma) for i in domain])
padded_stimulus =  np.pad(stimulus, (int(T_mem/dt), 0), 'constant')
padded_reward =  np.pad(reward, (1, 0), 'constant')

w = np.zeros(int(T_mem/dt) + 1)
results = {}


# Tapped delay line representation
for n in range(N):
    V = np.zeros(int(T/dt) + 2)
    TD = np.zeros(int(T/dt) + 1)
    delta = np.zeros(int(T/dt) + 1)
    prev_phi = np.zeros(int(T_mem/dt) + 1)

    for t in range(int(T/dt)): 
        state = np.array(padded_stimulus[t:t+int(T_mem/dt)+1][::-1])
        phi = state
        V[t+1] = np.dot(w, phi)
        TD[t] = gamma*V[t+1] - V[t]
        delta[t] = padded_reward[t] + TD[t]
        w += eps*delta[t]*prev_phi
        prev_phi = phi.copy()

    if n % 10 == 0:
        results[f"Trial {n}"] = (V.copy(), TD.copy(), delta.copy(), w.copy())


# Boxcar representation
eps = 0.01

for n in range(N):
    V = np.zeros(int(T/dt) + 2)
    TD = np.zeros(int(T/dt) + 1)
    delta = np.zeros(int(T/dt) + 1)
    prev_phi = np.zeros(int(T_mem/dt) + 1)

    for t in range(int(T/dt)): 
        state = np.array(padded_stimulus[t:t+int(T_mem/dt)+1][::-1])
        phi = np.zeros_like(state)
        if 1 in state:
            idx = np.nonzero(state)[0][0]
            phi[idx:] = 1
        V[t+1] = np.dot(w, phi)
        TD[t] = gamma*V[t+1] - V[t]
        delta[t] = padded_reward[t] + TD[t]
        w += eps*delta[t]*prev_phi
        prev_phi = phi.copy()

    if n % 10 == 0:
        results[f"Trial {n}"] = (V.copy(), TD.copy(), delta.copy(), w.copy())


# Boxcar representation with partial reinforcement (p=0.5)
N = 1001
eps = 0.01
flags = np.ones(N)
np.random.seed(42)
p = 0.5

for n in range(N):
    coin_flip = random.random()
    if coin_flip < p:
        padded_reward = np.zeros_like(padded_reward)
        flags[n] = 0
    else:
        padded_reward = np.pad(reward, (1, 0), 'constant')
      
    V = np.zeros(int(T/dt) + 2)
    TD = np.zeros(int(T/dt) + 1)
    delta = np.zeros(int(T/dt) + 1)
    prev_phi = np.zeros(int(T_mem/dt) + 1)

    for t in range(int(T/dt)): 
        state = np.array(padded_stimulus[t:t+int(T_mem/dt)+1][::-1])
        phi = np.zeros_like(state)
        if 1 in state:
            idx = np.nonzero(state)[0][0]
            phi[idx:] = 1
        V[t+1] = np.dot(w, phi)
        TD[t] = gamma*V[t+1] - V[t]
        delta[t] = padded_reward[t] + TD[t]
        w += eps*delta[t]*prev_phi
        prev_phi = phi.copy()
        
    if n >= 900:
        results[f"Trial {n}"] = (V.copy(), TD.copy(), delta.copy(), w.copy(), flags[n])

        
# Boxcar representation with partial reinforcement (p varies)
N = 1001
eps = 0.01
flags = np.ones(N)
np.random.seed(42)
p = [0.0, 0.25, 0.5, 0.75, 1]
results_per_prob = {}

for prob in p:
    w = np.zeros(int(T_mem/dt) + 1)
    for n in range(N):
        coin_flip = random.random()
        if coin_flip > prob:
            padded_reward = np.zeros_like(padded_reward)
            flags[n] = 0
        else:
            padded_reward = np.pad(reward, (1, 0), 'constant')
        
        V = np.zeros(int(T/dt) + 2)
        TD = np.zeros(int(T/dt) + 1)
        delta = np.zeros(int(T/dt) + 1)
        prev_phi = np.zeros(int(T_mem/dt) + 1)

        for t in range(int(T/dt)): 
            state = np.array(padded_stimulus[t:t+int(T_mem/dt)+1][::-1])
            phi = np.zeros_like(state)
            if 1 in state:
                idx = np.nonzero(state)[0][0]
                phi[idx:] = 1
            V[t+1] = np.dot(w, phi)
            TD[t] = gamma*V[t+1] - V[t]
            delta[t] = padded_reward[t] + TD[t]
            w += eps*delta[t]*prev_phi
            prev_phi = phi.copy()
            
        if n >= 900:
            results[f"Trial {n}"] = (delta.copy(), flags[n])

    results_per_prob[prob] = results.copy()
    results = {} 

