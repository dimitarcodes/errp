from scipy.io import loadmat
import mne
import numpy as np


def get_info_mat(file_path):
    print(f'loading file {file_path}')
    # Load the .mat file
    mat_raw = loadmat(file_path, simplify_cells=1)
    mat_data = mat_raw['run']
    trial = mat_data[0]

    header = trial['header']
    sfreq = header['SampleRate']

    # remove status channel - irrelevant as not present in data
    ch_names = list(header['Label'][:-1])
    ch_types = ['eeg'] * len(ch_names)

    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    info.set_montage("standard_1020")

    return info

def load_preprocess_matlab_data(file_path, l_freq=1.0, h_freq=10.0, re_fs=64, tmin=-0.1, tmax=0.85):
    """
    Reads a mat file containing data from experimental session.

    Assumes mat files have the following contents:

    run{idx}.eeg        raw EEG data (n_samples x n_channels) 
    run{idx}.header     metadata

    header.Subject      subject number
    header.Session      Session number
    header.SampleRate   Recording sampling rate
    header.Label        Electrode labels
    header.EVENT        Recording events

    header.EVENT.POS    Position of event
    header.EVENT.TYP    Type of event

    """
    
    print(f'loading file {file_path}')
    # Load the .mat file
    mat_raw = loadmat(file_path, simplify_cells=1)
    mat_data = mat_raw['run']

    epochs_list = []
    for trial in mat_data:

        # extract trial data and metadata

        # data comes in (samples x channels) shape
        eegdata = trial['eeg'].transpose()
        header = trial['header']

        sfreq = header['SampleRate']

        # remove status channel - irrelevant as not present in data
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