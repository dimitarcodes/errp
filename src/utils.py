from scipy.io import loadmat
import mne
import numpy as np


def epochs_to_data_labels(epoch, picks=['FCz', 'Cz'], tmin=0.2, tmax=0.7):
    """ Extracts data and labels from an MNE Epochs object.
    Parameters
    ----------
    epoch : mne.Epochs
        MNE Epochs object containing the EEG data and events.
    picks : list of str, optional
        List of channel names to select from the data, by default ['FCz', 'Cz'].
    tmin : float, optional
        Start time for the epoch, by default 0.2 seconds.
    tmax : float, optional
        End time for the epoch, by default 0.7 seconds.

    Returns
    -------
    X : np.ndarray
        The EEG data for the selected channels and time window, shape (n_epochs, n_channels, n_times).
    y : np.ndarray  
        The labels for the epochs, where 0 indicates correct class (5 and 10) and 1 indicates error class (6 and 9).
    """
    # obtain only relevant event epochs
    data = epoch[['5', '10', '6', '9']]
    # get requested data channels and time window
    X = data.get_data(picks=picks, tmin=tmin, tmax=tmax).squeeze()
    y = data.events[:, 2]
    # 5 and 10 are the correct class (default, much more frequent)
    y[ (y==5) | (y==10)]= 0
    # 9 and 6 are the error class (target we want to detect)
    y[ (y==6) | (y==9)] = 1
    return X, y

def load_preprocess_matlab_data(file_path, l_freq=1.0, h_freq=10.0, re_fs=64, tmin=-0.2, tmax=1.0):
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

    Parameters
    ----------
    file_path : str
        Path to the .mat file containing the data.
    l_freq : float, optional
        Low cutoff frequency for bandpass filtering, by default 1.0 Hz.
    h_freq : float, optional
        High cutoff frequency for bandpass filtering, by default 10.0 Hz.
    re_fs : int, optional
        Resampling frequency, by default 64 Hz.
    tmin : float, optional
        Start time for epochs, by default -0.2 seconds.
    tmax : float, optional
        End time for epochs, by default 1.0 seconds.
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

        if re_fs is not None:
            decimfactor = sfreq / re_fs
        else:
            decimfactor = 1
        epoch = mne.Epochs(raw=filtdata, events = eventsarr, tmin=tmin, tmax=tmax, decim=decimfactor, preload=True)      
        epochs_list.append(epoch)

    # Concatenate all epochs into a single Raw object
    epochs = mne.concatenate_epochs(epochs_list)

    return epochs