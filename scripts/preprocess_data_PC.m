% Extracts data (calcium traces, pupil size, trial type) 
% for each mouse. Save to ../data/per_mouse/PC

% Load data into memory as variable E
e = 2; % experiment 1 means AFC, 2 pseudo
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
    
    % Trial type: 1 = CS+, 0 = CS- 
    d.CS2_tr_hab = zeros(num_trials,1);
    d.CS2_tr_rec = zeros(num_trials,1);
    d.CS2_tr_hab(E(e).S(1).M(m).CS2_tr) = 1;
    d.CS2_tr_rec(E(e).S(3).M(m).CS2_tr) = 1;
    % acquisition: 
    d.CS2_tr_acq = ones(45,1) * -1;
    d.CS2_tr_acq(E(e).S(2).M(m).CS2_tr) = 1; % CS2 == 1, CS1 == 0
    d.CS2_tr_acq(E(e).S(2).M(m).CS1_tr) = 0;
    
    % Pupil size: single number (during sound) for hab/rec. 2 for acq
    % (sound & shock)
    d.Pupil_m_hab = E(e).S(1).M(m).H_AUC_pupil_CS1;
    d.Pupil_m_aqc = E(e).S(2).M(m).PCsound_AUC_pupil_CS1;
    d.Pupil_m_aqc_schock = E(e).S(2).M(m).PCshock_AUC_pupil_CS1;
    d.Pupil_m_rec = E(e).S(3).M(m).R_AUC_pupil_CS1;
    
    d.Pupil_p_hab = E(e).S(1).M(m).H_AUC_pupil_CS2;
    d.Pupil_p_aqc = E(e).S(2).M(m).PCsound_AUC_pupil_CS2;
    d.Pupil_p_aqc_schock = E(e).S(2).M(m).PCshock_AUC_pupil_CS2;
    d.Pupil_p_rec = E(e).S(3).M(m).R_AUC_pupil_CS2;
    
    % Save
    fname = append("../data/per_mouse/PC/", d.MouseID);
    save(fname, "-struct", "d");
end
