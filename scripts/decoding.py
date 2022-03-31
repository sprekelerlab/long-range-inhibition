"""
Predict stimulus based on neural data pooled across animals
"""
import pickle
import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("colorblind")
sns.set_context("poster")
from src.data_utils import get_all_boutons
from src.decoding_utils import classify

NUM_PCS = 200 # retain ~90% of variance
DATADIR = '../data/per_mouse/AFC/'

ACCURACIES = {}
CORRECT = {}
for phase in ['hab', 'acq', 'rec']:
    print(f"Decoding phase {phase}")
    X, Xred, pca, y = get_all_boutons(phase, DATADIR, NUM_PCS)
    predictions, classifiers = classify(Xred, y, 0)
    correct = predictions == y[:, None] # stim. labels y are same for entire trial
    accuracy = correct.mean(0) # Mean over trials
    ACCURACIES[phase] = accuracy
    CORRECT[phase] = correct

result_dict = {'accuracy': ACCURACIES, 'correct': CORRECT}
file_name = f'../data/decoding'
print(f"Save data to {file_name}.pickle and {file_name}.mat")
with open(f'{file_name}.pickle', 'wb') as handle:
    pickle.dump(result_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
savemat(f"{file_name}.mat", result_dict)

# Make the figure
plt.figure()
for i, phase in enumerate(['hab', 'acq', 'rec']):
    # Mean and sd over trials, in %
    m, sd = 100*CORRECT[phase].mean(0), 100*CORRECT[phase].std(0)
    n_trials, n_frames = CORRECT[phase].shape
    plt.plot(np.arange(n_frames), m, color='tab:blue', alpha=0.33 + 0.33 * i, label=phase)
    # SEM
    plt.fill_between(np.arange(n_frames), m- sd/np.sqrt(n_trials), m + sd/np.sqrt(n_trials),
                     color='gray', alpha=0.2)

plt.xlabel("Time (frames)")
plt.legend(handlelength=1)
plt.ylabel("Accuracy (%)")
plt.ylim([25, 105])
plt.yticks([25, 50, 75, 100])
sns.despine()
plt.tight_layout()
fig_name = f"../figures/decoding.pdf"
plt.savefig(fig_name, dpi=300)
print(f"Save figure as {fig_name}")
