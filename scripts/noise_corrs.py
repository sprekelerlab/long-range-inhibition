"""
Pairwise "noise" correlations among neurons.
"""
import pickle
import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_utils import get_per_mouse_boutons
from src.corr_utils import compute_noise_corrs, compute_response_integral
sns.set_palette("colorblind")
sns.set_context("poster")


data_dir = '../data/per_mouse/AFC'

phases = ['hab', 'acq', 'rec']
all_corrs = {'CS+': {}, 'CS-': {}} # stack them
C = {} # Per mouse
stim_frames = np.arange(12, 21)
stims = ['CS-', 'CS+']

for i, phase in enumerate(phases):
    print(f"Computing noise corrs. phase {phase}")
    X, y = get_per_mouse_boutons(phase, data_dir)
    Xint = {}
    all_corrs['CS+'][phase] = []
    all_corrs['CS-'][phase] = []
    for mouse_id in X.keys():
        if i == 0: # init.
            C[mouse_id] = {'CS+': {}, 'CS-': {}}
        # Exclude first trials (one per stim.) since these had huge corrs. during habituation
        Xint[mouse_id] = compute_response_integral(X[mouse_id][2:], stim_frames)
        for label, CS in enumerate(stims):
            # sub. mean response (although doesn't matter for corr.)
            fluctuation = Xint[mouse_id][y[mouse_id][2:] == label]
            fluctuation -= Xint[mouse_id][y[mouse_id][2:] == label].mean(0, keepdims=True)
            C[mouse_id][CS][phase], _ = compute_noise_corrs(fluctuation)
            all_corrs[CS][phase] += list(C[mouse_id][CS][phase])

# Save data
fname = "../data/noise_corrs"
print(f"Save data as {fname}.pickle and {fname}.mat")
with open(f'{fname}.pickle', 'wb') as handle:
    pickle.dump(all_corrs, handle, protocol=pickle.HIGHEST_PROTOCOL)
savemat(f'{fname}.mat', all_corrs)

# Figure
plt.figure()
plt.bar([0, 1, 2], [np.mean(all_corrs['CS+'][phase]) for phase in phases])
plt.xticks([0, 1, 2], phases)
plt.yticks([0, 0.05, 0.1])
plt.ylabel("Noise corr.")
sns.despine()
plt.tight_layout()
fname = "../figures/noise_corrs.pdf"
print(f"Save figure as {fname}")
plt.savefig(fname, dpi=300)
