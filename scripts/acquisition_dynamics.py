"""
Analyse changes in population respose during
stimulus-response acquisition
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_utils import get_per_mouse_boutons
from src.population_utils import compute_angle
sns.set_palette("colorblind")
sns.set_context("poster")

# Compute angle between avg. response for specific stimulus
# and NP/NR boutons
stim = 'csp' # CS+, show in main fig. Set stim='csm' for CS-
responses = ['exc', 'inh']
hab_angles = {} # angle between habituation and acquisition vectors
rec_angles = {} # angle between recall and acquisition vectors
hab_hab = {} # angle between habituation vectors (trial-to-trial var.)
rec_rec = {} # angle between habituation vectors (trial-to-trial var.)
hab_rec = {} # angle between avg. habituation and avg. recall vecgtors
for resp in responses:
    Xr, yr = get_per_mouse_boutons("rec", f"../data/per_mouse/AFC_{resp}_{stim}/")
    Xa, ya = get_per_mouse_boutons("acq", f"../data/per_mouse/AFC_{resp}_{stim}/")
    Xh, yh = get_per_mouse_boutons("hab", f"../data/per_mouse/AFC_{resp}_{stim}/")
    mouse_ids = Xr.keys()
    n_mice = len(mouse_ids)
    n_trials = 15
    hab_angles[resp] = np.zeros((n_mice, n_trials))
    rec_angles[resp] = np.zeros((n_mice, n_trials))
    hab_hab[resp] = np.zeros((n_mice, ))
    rec_rec[resp] = np.zeros((n_mice, ))
    hab_rec[resp] = np.zeros((n_trials, ))

    for m, mouse_id in enumerate(mouse_ids):
        # mice x trials = 12 x 15
        hab_angles[resp][m] = [compute_angle(x, Xh[mouse_id][:, 12:21].mean((0, 1)))
                               for x in Xa[mouse_id][:, 12:21].mean(1)]
        rec_angles[resp][m] = [compute_angle(x, Xr[mouse_id][:, 12:21].mean((0, 1)))
                               for x in Xa[mouse_id][:, 12:21].mean(1)]
        # Mean during habituation vs mean during recall
        hab_rec[resp][m] = compute_angle(Xh[mouse_id][:, 12:21].mean((0, 1)),
                                         Xr[mouse_id][:, 12:21].mean((0, 1)))
        # test last hab trial against mean of others
        hab_hab[resp][m] = compute_angle(Xh[mouse_id][-1, 12:21].mean(0),
                                         Xh[mouse_id][:-1, 12:21].mean((0, 1)))
        # first rec trial against mean of others
        rec_rec[resp][m] = compute_angle(Xr[mouse_id][0, 12:21].mean(0),
                                         Xr[mouse_id][1:, 12:21].mean((0, 1)))


# Plot the result
fig, ax = plt.subplots(1, 2, figsize=(9, 3), sharey=True)
color = 'tab:blue'
for i, resp in enumerate(['inh', 'exc']):
    # Acquisition dynamics
    for j, angles in enumerate([hab_angles, rec_angles]):
        ax[i].plot(angles[resp].mean(0), color=color, alpha=.33 + 0.67*j)
        ax[i].fill_between(np.arange(15),
                           angles[resp].mean(0) - angles[resp].std(0) / np.sqrt(n_trials),
                           angles[resp].mean(0) + angles[resp].std(0) / np.sqrt(n_trials),
                           alpha=0.2+0.2*j, color=color)
    # trial-to-trial variability of habituation
    ax[i].errorbar(-1, hab_hab[resp].mean(), hab_hab[resp].std()/np.sqrt(n_trials),
                   marker='o', markersize=5, color=color, alpha=0.33)
    # trial-to-trial variability of recall
    ax[i].errorbar(15, rec_rec[resp].mean(), rec_rec[resp].std()/np.sqrt(n_trials),
                   marker='o', markersize=5, color=color, alpha=1)
    ax[i].set_xlabel("CS+ acquisition trials")
    ax[i].set_xticks([0, 5, 10, 15])

ax[0].set_ylabel(r"pop vec $\Delta$ (deg)")
ax[0].set_title("negative response")
ax[1].set_title("positive response")

sns.despine()
fig.tight_layout()
fname = '../figures/acquisition_dynamics.pdf'
print(f"Save figure as {fname}")
plt.savefig(fname, dpi=300)

# Figure 4J
plt.figure()
fig, ax = plt.subplots(1, 2, sharey=True, figsize=(7, 3.5))
for i, resp in enumerate(['exc', 'inh']):
    ax[i].bar([1, 2, 3], [rec_angles[resp][:, 0].mean(), rec_angles[resp][:, -1].mean(),
                          rec_rec[resp].mean()], alpha=0.3)
    ax[i].scatter([1] * n_mice, rec_angles[resp][:, 0], alpha=0.33)
    ax[i].scatter([2] * n_mice, rec_angles[resp][:, -1], alpha=0.33)
    ax[i].scatter([3] * n_mice, rec_rec[resp], alpha=0.33)
    ax[i].set_xticks([1, 2, 3])
    ax[i].set_xticklabels([1, 15, 'Rec'])

ax[0].set_ylabel(r"Pop vec $\Delta$ (deg)")
ax[0].set_yticks([0, 50, 100, 150])
ax[0].set_title("PR")
ax[1].set_title("NR")
sns.despine()
fig.tight_layout()
fname = '../figures/angles_1_15_rec.pdf'
print(f"Save figure as {fname}")
plt.savefig(fname, dpi=300)
