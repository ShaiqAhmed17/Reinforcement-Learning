import matplotlib.pyplot as plt
import matplotlib.cm as cm
from RL import *

# Plotting stimulus and reward against time
def plot_stimulus_and_reward():
    ax = plt.subplot(211)
    ax.plot(domain, stimulus, "b")
    ax.set_title('Stimulus against time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Stimulus')
   
    ax = plt.subplot(212)
    ax.plot(domain, reward, "r")
    ax.set_title('Reward against time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Reward')

    plt.tight_layout()
    plt.show()

#plot_stimulus_and_reward()

# Plotting V, TD, and delta (tapped delay line, boxcar)
def plot_201_trials(results):
    trial_names = sorted(results.keys(), key=lambda x: int(x.split()[1]))
    colors = cm.plasma(np.linspace(0, 1, len(trial_names)))[::-1]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

    for i, n in enumerate(trial_names):
        ax1.plot(domain, results[n][0][1:], color=colors[i])
    ax1.set_title('Value function against time')
    ax1.set_ylabel('Value')

    for i, n in enumerate(trial_names):
        ax2.plot(domain, results[n][1], color=colors[i])
    ax2.set_title('Temporal difference against time')
    ax2.set_ylabel('Temporal difference')

    for i, n in enumerate(trial_names):
        ax3.plot(domain, results[n][2], color=colors[i], label=n)
    ax3.set_title('Delta against time')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Delta')

    ax3.legend(loc='center left', bbox_to_anchor=(1, 1.8))

    fig.subplots_adjust(right=0.8, hspace=0.4)
    plt.show()

#plot_201_trials(results)

# Plotting average over last 100 trials of V, TD, and delta under partial reinforcement
def plot_average_last_100_trials(results):
    trial_names = sorted(results.keys(), key=lambda x: int(x.split()[1]))
    uncued = [n for n in trial_names if results[n][4] == 0]
    cued = [n for n in trial_names if results[n][4] == 1]
    colors = cm.plasma(np.linspace(0, 1, 3))[::-1] # for each variation

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

    for i, variation in enumerate([trial_names, uncued, cued]):
        ax1.plot (domain, np.mean([results[n][0][1:] for n in variation], axis=0), color=colors[i])
        ax1.set_title('Value function against time')
        ax1.set_ylabel('Value')
        ax2.plot (domain, np.mean([results[n][1] for n in variation], axis=0), color=colors[i])
        ax2.set_title('Temporal difference against time')
        ax2.set_ylabel('Temporal difference')
        ax3.plot (domain, np.mean([results[n][2] for n in variation], axis=0), color=colors[i])
        ax3.set_title('Delta against time')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Delta')
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 1.8), labels=['All trials', 'Uncued trials', 'Cued trials'])
    
    fig.subplots_adjust(right=0.8, hspace=0.4)
    plt.show()

#plot_average_last_100_trials(results)

'''Fix: I have passed the averaged version into the DA function, rather than passing the individual trials and then averaging'''

# Plot dopamine activity and delta with p=0.5
def plot_dopamine_activity(results):
    trial_names = sorted(results.keys(), key=lambda x: int(x.split()[1]))
    activities = {}
    for n in trial_names:
        dopamine_activity = np.array([calculate_dopamine_activity(x) for x in results[n][2]])
        activities[n] = dopamine_activity

    average_DA = np.mean([activities[n] for n in trial_names], axis=0)

    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.plot(domain, average_DA, "b")
    ax.plot(domain, np.mean([results[n][2] for n in trial_names], axis=0), "r")
    ax.set_title('Dopamine activity against time')
    ax.set_xlabel('Time (s)')
    ax.legend(["Dopamine activity", "Delta"])
    plt.tight_layout()
    plt.show()

#plot_dopamine_activity(results)

# Plot average dopamine time course for all p
def plot_average_dopamine_over_p():
    dict_of_tuples = {}
    colors = cm.plasma(np.linspace(0, 1, len(p)))[::-1]
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    for i, prob in enumerate(p):
        results = results_per_prob[prob]
        trial_names = sorted(results.keys(), key=lambda x: int(x.split()[1]))
        activities = {}
        for n in trial_names:
            dopamine_activity = np.array([calculate_dopamine_activity(x) for x in results[n][0]])
            activities[n] = dopamine_activity

        average_DA = np.mean([activities[n] for n in trial_names], axis=0)
        dict_of_tuples[prob] = (average_DA[int(10/dt)],average_DA[int(20/dt)]) 
        ax.plot(domain, average_DA, color=colors[i], label=f"p={prob}")
        
    ax.set_title('Average dopamine activity against time over p')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Dopamine activity')
    ax.legend()
    plt.show()
    return dict_of_tuples

dict_of_tuples = plot_average_dopamine_over_p()

def plot_max_stimulus_reward_time_DA_over_p(dict_of_tuples):
    p_values = list(dict_of_tuples.keys())
    max_stimulus_time_DA = [dict_of_tuples[p][0] for p in p_values]
    max_reward_time_DA = [dict_of_tuples[p][1] for p in p_values]

    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.plot(p_values, max_stimulus_time_DA, "b", label="Max DA at stimulus time")
    ax.plot(p_values, max_reward_time_DA, "r", label="Max DA at reward time")
    ax.set_title('Max dopamine activity at stimulus and reward time against p')
    ax.set_xlabel('p')
    ax.set_ylabel('Dopamine activity')
    ax.legend()
    plt.tight_layout()
    plt.show()

plot_max_stimulus_reward_time_DA_over_p(dict_of_tuples)


