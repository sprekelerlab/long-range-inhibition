% Extracts data (calcium traces, pupil size, trial type) 
% for each mouse. Save to ../data/per_mouse/AFC

% Load data into memory as variable E
load("../data/raw_data.mat")
% Save AFC data from all mice
e = 1; % experiment 1 means AFC, 2 pseudo
num_mice = size(E(e).S(1).M,2);
num_trials = size(E(e).S(1).M(2).DeltaFF, 1); 

for m = 1:num_mice 
    d = struct; % initialize struct we'll fill w/ data
    
    % Mouse labels. Grab the one from S(1) - habituation
    d.MouseID = E(e).S(1).M(m).MouseID; 
    d.Designation = E(e).S(1).M(m).Designation; 
    d.Exp = 'AFC';
    
    % Fluorescence, S-idx denotes phase
    d.DeltaFF_hab = E(e).S(1).M(m).DeltaFF;
    d.DeltaFF_acq = E(e).S(2).M(m).DeltaFF;
    d.DeltaFF_rec = E(e).S(3).M(m).DeltaFF;
    d.DeltaFF_hab_exc = E(e).S(1).M(m).DeltaFF_CSm_exc;
    
    % Trial type: 1 = CS+, 0 = CS- 
    d.CSp_tr_hab = zeros(num_trials,1);
    d.CSp_tr_acq = zeros(num_trials,1);
    d.CSp_tr_rec = zeros(num_trials,1);
    d.CSp_tr_hab(E(e).S(1).M(m).CSp_tr) = 1;
    d.CSp_tr_acq(E(e).S(2).M(m).CSp_tr) = 1;
    d.CSp_tr_rec(E(e).S(3).M(m).CSp_tr) = 1;
    
    % Pupil size: single number (during sound) for hab/rec. 2 for acq
    % (sound & shock)
    d.Pupil_m_hab = E(e).S(1).M(m).H_AUC_pupil_m;
    d.Pupil_p_hab = E(e).S(1).M(m).H_AUC_pupil_p;
    d.Pupil_m_acq = E(e).S(2).M(m).FCsound_AUC_pupil_m;
    d.Pupil_p_aqc = E(e).S(2).M(m).FCsound_AUC_pupil_p;
    d.Pupil_m_aqc_schock = E(e).S(2).M(m).FCshock_AUC_pupil_m;
    d.Pupil_p_aqc_schock = E(e).S(2).M(m).FCshock_AUC_pupil_p;
    d.Pupil_m_rec = E(e).S(3).M(m).R_AUC_pupil_m;
    d.Pupil_p_rec = E(e).S(3).M(m).R_AUC_pupil_p;
    
    % Save
    fname = append("../data/per_mouse/AFC/", d.MouseID);
    save(fname, "-struct", "d");
end
