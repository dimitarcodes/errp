from scipy.io import loadmat
import mne
import numpy as np


def load_preprocess_matlab_data(file_path, l_freq=1.0, h_freq=20.0, re_fs=64, tmin=-0.1, tmax=0.85):
    """
    Load MATLAB data from a .mat file and convert it to MNE Raw object.

    Parameters:
    file_path (str): Path to the .mat file.

    Returns:
    mne.io.Raw: MNE Raw object containing the data.
    """
    
    
    print(f'loading file {file_path}')
    # Load the .mat file
    mat_raw = loadmat(file_path, simplify_cells=1)
    mat_data = mat_raw['run']

    epochs_list = []
    for trial in mat_data:

        # extract trial data and metadata
        eegdata = trial['eeg'].transpose()
        header = trial['header']

        sfreq = header['SampleRate']
        ch_names = list(header['Label'][:-1])
        ch_types = ['eeg'] * len(ch_names)

        info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
        info.set_montage("standard_1020")

        # Create MNE Raw object
        raw = mne.io.RawArray(eegdata, info)

        # Filter the data
        filtdata = raw.copy().filter(l_freq=l_freq, h_freq=h_freq)

        events = header['EVENT']
        events_pos = np.array(events['POS'], dtype=int)
        events_type = np.array(events['TYP'], dtype=int)

        nevents = len(events_pos)
        eventsarr = np.zeros([nevents, 3], dtype=int)
        eventsarr[:,0]= events_pos
        eventsarr[:,2] = events_type

        decimfactor = sfreq / re_fs
        epoch = mne.Epochs(raw=filtdata, events = eventsarr, tmin=tmin, tmax=tmax, decim=decimfactor, preload=True)      
        epochs_list.append(epoch)
    # Concatenate all epochs into a single Raw object
    epochs = mne.concatenate_epochs(epochs_list)

    return epochs

def load_session(session=1, subjects=[1,2,3,4,5,6]):
    datafiles = [
        f"data/sub%02d_ses%d.mat" % (subject, session) for subject in subjects
    ]

    epochs_list = []
    for fpath in datafiles:
        epochs_list.append(load_preprocess_matlab_data(fpath))
    
    epochs = mne.concatenate_epochs(epochs_list)
    return epochs
