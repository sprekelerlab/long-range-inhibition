"""
Figure 4K: learning angle between
habituation and recall population vectors.
"""
import pickle
import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_utils import get_per_mouse_boutons
from src.population_utils import compute_angle, get_learning_angles
sns.set_palette("colorblind")
sns.set_context("poster")


# Compute angles for both pseudo and fear conditioning
pc_angles = {}
afc_angles = {}
for stim in ['cs1', 'cs2']:
    pc_angles[stim] = get_learning_angles(stim, 'Pseudo')

for stim in ['csm', 'csp']:
    afc_angles[stim] = get_learning_angles(stim, 'AFC')

# Save data
angles = {'pc': pc_angles, 'afc': afc_angles}
fname = f'../data/learning_angles'
print(f"Save data to {fname}.pickle and {fname}.mat")

with open(f'{fname}.pickle', 'wb') as handle:
    pickle.dump(angles, handle, protocol=pickle.HIGHEST_PROTOCOL)
savemat(f"{fname}.mat", angles)

# Plot the result
alpha = 0.5
s = 30
# First pseudo-conditioning. We average angles for CS1 and CS2
# since neither is special
for i, resp in enumerate(['exc', 'inh']):
    pc_avg = (pc_angles['cs1'][resp]+ pc_angles['cs2'][resp])/2
    # Mean across mice
    plt.bar(i, pc_avg.mean(), color='gray', alpha=alpha)
    # individual mice
    plt.scatter([i] * len(pc_avg), pc_avg, s=s, alpha=alpha)

# Now conditioning. Don't average since CS+ is special
# Means across mice
plt.bar(3, afc_angles['csm']['exc'].mean(), color='tab:green', alpha=alpha)
plt.bar(4, afc_angles['csm']['inh'].mean(), color='tab:green', alpha=alpha)

plt.bar(6, afc_angles['csp']['exc'].mean(), color='tab:blue', alpha=alpha)
plt.bar(7, afc_angles['csp']['inh'].mean(), color='tab:blue', alpha=alpha)

# individual mice
plt.scatter([3]* len(afc_angles['csm']['exc']), afc_angles['csm']['exc'], s=s, alpha=alpha)
plt.scatter([4]* len(afc_angles['csm']['inh']), afc_angles['csm']['inh'], s=s, alpha=alpha)

plt.scatter([6]* len(afc_angles['csp']['exc']), afc_angles['csp']['exc'], s=s, alpha=alpha)
plt.scatter([7]* len(afc_angles['csp']['inh']), afc_angles['csp']['inh'], s=s, alpha=alpha)

# Add labels
plt.xticks([0, 1, 3, 4, 6, 7], ['PN', 'NR']*3)
plt.text(0, -50, "CS1/2", fontsize=20)
plt.text(3, -50, "CS-", fontsize=20)
plt.text(6, -50, "CS+", fontsize=20)
plt.ylabel(r"Learning $\theta$ (deg.)")

sns.despine()
plt.tight_layout()
fname = '../figures/learning_angle.pdf'
print(f"Save to {fname}")
plt.savefig(fname, dpi=300)
