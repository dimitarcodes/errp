import requests, os, sys
from pathlib import Path

def download_data(target_folder='data'):
    """Downloads the 22. Monitoring error-related potentials (013-2015) dataset from the BNCI Horizon 2020 database.
    URL: https://bnci-horizon-2020.eu/database/data-sets
    
    Parameters
    ----------
    target_folder : str, optional
        The folder where the dataset will be saved. Defaults to 'data'.
    """
    target_folderpath = Path(target_folder)

    # create data directory if it doesn't exist
    if not os.path.exists(target_folderpath):
        os.makedirs(target_folderpath)

    # subjects 1-6
    for subject in range(1,7):
        # sessions 1-2
        for session in range(1,3):
            # procedurally generate url
            url = f"https://bnci-horizon-2020.eu/database/data-sets/013-2015/Subject%02d_s%d.mat" % (subject, session)

            # determine save file location
            target_file = 'sub%02d_ses%d.mat' % (subject, session)
            target_filepath = target_folderpath / target_file

            if not os.path.exists(target_filepath):
                # download file and write it in chunks of 10 mbs
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    print(f"Downloading {url}...")
                    with open(target_filepath, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            f.write(chunk)
                    print(f"Saved to {target_filepath}")
            else:
                print(f"File {target_filepath} associated with url {url} already exists, skipping...")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        download_data()
    else:
        download_data(sys.argv[1])