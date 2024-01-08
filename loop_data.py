import os

DIR = os.path.dirname(os.path.realpath(__file__))

files = os.listdir(DIR)

raw_files = [f for f in files if f.endswith('.h5') and 'CCCTrio' in f]

print('> raw files to be processed: ', raw_files)

for r in raw_files:
    # reconstruction slice by slice
    os.system('python dce_recon.py --data ' + r + ' --spokes_per_frame 13 --slice_idx 0 --slice_inc 192')
    # combine all slices as a 4D matrix into one .h5 file
    os.system('python h5_to_dcm.py --data ' + r)
