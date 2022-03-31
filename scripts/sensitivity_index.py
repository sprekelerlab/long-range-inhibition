"""
Compute the sensitivity index d' for individual boutons
Save data which will then be used by sensitivity_index_fig.py
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import savemat
from pandas import DataFrame
from src.data_utils import get_all_boutons

def compute_d(X, y, stim_frames):
    """
    Sensitivity index d'
    Input:
        X: trials, frames, boutons
        y: frames 0/1
    Returns:
        d_prime: boutons
    """
    assert X.shape[0] == y.shape[0]
    assert len(stim_frames) > 0
    means = {}
    sds = {}
    for label, stim in enumerate(['cs-', 'cs+']):
	# average response per trial
        Xphase = X[y == label][:, stim_frames].mean(1)
        # mean or sd across trials
        means[stim] = Xphase.mean(0)
        sds[stim] = Xphase.std(0)
    avg_sd = np.sqrt(0.5 * sds['cs+']**2 + 0.5 * sds['cs-']**2)
    d_prime = np.abs(means['cs+'] - means['cs-']) / avg_sd
    return d_prime

experiment = 'AFC'
data_dir = f'../data/per_mouse/{experiment}'
print(f"Loading data from {data_dir}")
Xh, _, _, yh = get_all_boutons("hab", data_dir)
Xa, _, _, ya = get_all_boutons("acq", data_dir)
Xr, _, _, yr = get_all_boutons("rec", data_dir)


# Compute d', using average activity during
# stimulus presentation - except for the last 'shock' frame
print("Computing sensitivity index")
stim_frames = np.arange(12, 21)
d_prime = {}
d_prime['hab'] = compute_d(Xh, yh, stim_frames)
d_prime['acq'] = compute_d(Xa, ya, stim_frames)
d_prime['rec'] = compute_d(Xr, yr, stim_frames)

# Save data
fname = '../data/sensitivity'
print(f"Save data as {fname}.pickle and {fname}.mat")
with open(f'{fname}.pickle', 'wb') as handle:
    pickle.dump(d_prime, handle, protocol=pickle.HIGHEST_PROTOCOL)
# and one for all Matlab users
savemat(f'{fname}.mat', d_prime)

# Now make the figure
# First put the data into a data frame so we can easily use seaborn's violin plots
d_primes = np.array([value for value in d_prime.values()])
n_boutons = d_primes.shape[1]
# Numerical coding otherwise seaborn complains
phases = np.array([[i] * n_boutons for i in range(3)])
data = np.concatenate((d_primes.reshape((-1, 1)), phases.reshape((-1, 1))), 1)
df = DataFrame(data, columns=['d', 'phase'])

fig, ax = plt.subplots()
sns.violinplot(x='phase', y='d', data=df, ax=ax)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['hab', 'acq', 'rec'])
plt.xlabel("")
plt.ylabel("d'")
sns.despine()
fig.tight_layout()
fig_dir = "../figures/sensitivity.pdf"
print(f"Save figure to {fig_dir}")
plt.savefig(fig_dir, dpi=300)
