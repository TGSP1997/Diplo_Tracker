from pathlib import Path
import os
import csv
import numpy as np
from classes.helpers.create_folder_structure import create_folder_structure

global name
global lister
lister = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17"]
def check_unique_ids(data, after_preproc=False):
    """Check the requirement that the tracker_ids and gt_ids are unique per timestep"""
    gt_ids = data['gt_ids']
    #tracker_ids = data['tracker_ids']
    for t, gt_ids_t in enumerate(gt_ids):
        if len(gt_ids_t) > 0:
            unique_ids, counts = np.unique(gt_ids_t, return_counts=True)
            if np.max(counts) != 1:
                duplicate_ids = unique_ids[counts > 1]
                exc_str_init = 'Ground-truth has the same ID more than once in a single timestep ' \
                                '(seq: %s, frame: %i, ids:' % (name[8:10], t+1)
                exc_str = ' '.join([exc_str_init] + [str(d) for d in duplicate_ids]) + ')'
                if after_preproc:
                    exc_str_init += '\n Note that this error occurred after preprocessing (but not before), ' \
                                    'so ids may not be as in file, and something seems wrong with preproc.'
                raise ValueError(exc_str)
    print(f'{name[8:10]}: Erfolg')

def _load_simple_text_file(file, time_col=0, id_col=None, remove_negative_ids=False, valid_filter=None,
                               crowd_ignore_filter=None, convert_filter=None, is_zipped=False, zip_file=None,
                               force_delimiters=None):
   
    if remove_negative_ids and id_col is None:
        raise ValueError('remove_negative_ids is True, but id_col is not given.')
    if crowd_ignore_filter is None:
        crowd_ignore_filter = {} 
    if convert_filter is None:
        convert_filter = {}
    try:
        fp = open(file)
        read_data = {}
        crowd_ignore_data = {}
        fp.seek(0, os.SEEK_END)
        # check if file is empty
        if fp.tell():
            fp.seek(0)
            dialect = csv.Sniffer().sniff(fp.readline(), delimiters=force_delimiters)  # Auto determine structure.
            dialect.skipinitialspace = True  # Deal with extra spaces between columns
            fp.seek(0)
            reader = csv.reader(fp, dialect)
            for row in reader:
                try:
                    # Deal with extra trailing spaces at the end of rows
                    if row[-1] in '':
                        row = row[:-1]
                    timestep = str(int(float(row[time_col])))
                    # Read ignore regions separately.
                    is_ignored = False
                    for ignore_key, ignore_value in crowd_ignore_filter.items():
                        if row[ignore_key].lower() in ignore_value:
                            # Convert values in one column (e.g. string to id)
                            for convert_key, convert_value in convert_filter.items():
                                row[convert_key] = convert_value[row[convert_key].lower()]
                            # Save data separated by timestep.
                            if timestep in crowd_ignore_data.keys():
                                crowd_ignore_data[timestep].append(row)
                            else:
                                crowd_ignore_data[timestep] = [row]
                            is_ignored = True
                    if is_ignored:  # if det is an ignore region, it cannot be a normal det.
                        continue
                    # Exclude some dets if not valid.
                    if valid_filter is not None:
                        for key, value in valid_filter.items():
                            if row[key].lower() not in value:
                                continue
                    if remove_negative_ids:
                        if int(float(row[id_col])) < 0:
                            continue
                    # Convert values in one column (e.g. string to id)
                    for convert_key, convert_value in convert_filter.items():
                        row[convert_key] = convert_value[row[convert_key].lower()]
                    # Save data separated by timestep.
                    if timestep in read_data.keys():
                        read_data[timestep].append(row)
                    else:
                        read_data[timestep] = [row]
                except Exception:
                    exc_str_init = 'In file %s the following line cannot be read correctly: \n' % os.path.basename(
                        file)
                    exc_str = ' '.join([exc_str_init]+row)
                    raise ValueError(exc_str)
        fp.close()
    except Exception:
        print('Error loading file: %s, printing traceback.' % file)
        raise ValueError(
            'File %s cannot be read because it is either not present or invalidly formatted' % os.path.basename(
                file))
    return read_data, crowd_ignore_data

def _load_raw_file(file, num_timesteps):
    zip_file = None
    # Load raw data from text file
    read_data, ignore_data = _load_simple_text_file(file)

    # Convert data to required format
    data_keys = ['ids', 'classes', 'dets']
    data_keys += ['gt_crowd_ignore_regions', 'gt_extras']
    raw_data = {key: [None] * num_timesteps for key in data_keys}

    # Check for any extra time keys
    current_time_keys = [str( t+ 1) for t in range(num_timesteps)]
    extra_time_keys = [x for x in read_data.keys() if x not in current_time_keys]
    if len(extra_time_keys) > 0:
        text = 'Ground-truth'
        raise ValueError(
            text + ' data contains the following invalid timesteps in seq ')

    for t in range(num_timesteps):
        time_key = str(t+1)
        if time_key in read_data.keys():
            try:
                time_data = np.asarray(read_data[time_key], dtype=float)
            except ValueError:
                raise ValueError(
                        'Cannot convert gt data for sequence  to float. Is data corrupted?')
            try:
                raw_data['dets'][t] = np.atleast_2d(time_data[:, 2:6])
                raw_data['ids'][t] = np.atleast_1d(time_data[:, 1]).astype(int)
            except IndexError:
                err = 'Cannot load gt data from sequence , because there is not enough ' \
                            'columns in the data.'
                raise ValueError(err)
            if time_data.shape[1] >= 8:
                raw_data['classes'][t] = np.atleast_1d(time_data[:, 7]).astype(int)
            else:
                raise ValueError(
                        'GT data is not in a valid format, there is not enough rows in seq , timestep .')
            gt_extras_dict = {'zero_marked': np.atleast_1d(time_data[:, 6].astype(int))}
            raw_data['gt_extras'][t] = gt_extras_dict
        else:
            raw_data['dets'][t] = np.empty((0, 4))
            raw_data['ids'][t] = np.empty(0).astype(int)
            raw_data['classes'][t] = np.empty(0).astype(int)
            gt_extras_dict = {'zero_marked': np.empty(0)}
            raw_data['gt_extras'][t] = gt_extras_dict
           
        raw_data['gt_crowd_ignore_regions'][t] = np.empty((0, 4))
    key_map = {'ids': 'gt_ids',
                    'classes': 'gt_classes',
                    'dets': 'gt_dets'}
    for k, v in key_map.items():
        raw_data[v] = raw_data.pop(k)
    raw_data['num_timesteps'] = num_timesteps
    raw_data['seq'] = 0
    return raw_data

def get_raw_seq_data(file):
    raw_gt_data = _load_raw_file(file, num_timesteps=num_timesteps)
    raw_tracker_data={}
    raw_data = {**raw_tracker_data, **raw_gt_data}  # Merges dictionaries

    # Calculate similarities for each timestep.
    similarity_scores = []
    raw_data['similarity_scores'] = similarity_scores
    return raw_data

sequence_names,fr_list, total_frames_list = create_folder_structure()
for i, sequence_name in enumerate(sequence_names):
    name = sequence_name
    num_timesteps = total_frames_list[i]
    file = Path(f'./Sequences/test/{sequence_name}/gt/gt.txt')
    if file.is_file():
        raw_data =  get_raw_seq_data(file.as_posix())
        check_unique_ids(raw_data)
        remove_list= []
        if name[8:10] in lister:
            remove_list.append(name[8:10])
        if len(remove_list)>0:
            for entry in remove_list:
                lister.remove(entry)

if len(lister)>0:
        print('Es fehlen noch die Nummern: ',lister)
else:
    print('Komplett Fertig')