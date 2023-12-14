import argparse
import h5py
import os
import pathlib
import pydicom

import numpy as np

DIR = os.path.dirname(os.path.realpath(__file__))

# %%
if __name__ == "__main__":

    # %%
    parser = argparse.ArgumentParser('convert a h5py file to dicom')

    parser.add_argument('--dcm',
                        default='GRASP_anno00001_anon.dcm',
                        help='a dicom file with tags')

    parser.add_argument('--h5py',
                        default='/reco_spokes13.h5',
                        help='radial k-space data')

    parser.add_argument('--spokes_per_frame', type=int, default=12,
                        help='number of spokes per frame')

    parser.add_argument('--TR', type=float, default=4.87,
                        help='repetition time (ms)')

    args = parser.parse_args()

    # %%
    # read in the original dicom file
    dcm_data = pydicom.dcmread(args.dcm)


    OUT_DIR = DIR + '/' + args.h5py
    OUT_DIR = OUT_DIR.split('.h5')[0]
    pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    f = h5py.File(DIR + args.h5py, 'r')
    R = f['temptv'][:]
    f.close()

    R = np.squeeze(abs(R))
    N_z, N_t, N_y, N_x = R.shape
    print(R.shape)

    # normalize images
    R = R * 533 / np.amax(R)

    print(np.amin(R))
    print(np.amax(R))

    for z in range(N_z):
        for t in range(N_t):
            print('> slice ' + str(z).zfill(3) + ' frame ' + str(t).zfill(3))
            dcm_data.PixelData = R[z, t].astype(np.uint16).tobytes()
            # timestamp
            dcm_data.add_new([0x0018, 0x0088], 'DS', str(t * N_z * args.TR))
            dcm_data.save_as(OUT_DIR + '/slice_' + str(z).zfill(3) + '_frame_' + str(t).zfill(3) + '.dcm')

    print('> done')
