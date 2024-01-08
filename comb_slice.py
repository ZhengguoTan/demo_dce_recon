import argparse
import h5py
import os
import pathlib

import numpy as np
DIR = os.path.dirname(os.path.realpath(__file__))

# %%
if __name__ == "__main__":

    # %% parse
    parser = argparse.ArgumentParser(description='combine all dce slices.')

    parser.add_argument('--data',
                        default='GeneBreast_CCCTrio#F636203.h5',
                        help='radial k-space data')

    parser.add_argument('--images_per_slab', type=int, default=192,
                        help='total number of images per slab [default: 192]')

    args = parser.parse_args()

    OUT_DIR = DIR + '/' + args.data
    OUT_DIR = OUT_DIR.split('.h5')[0]

    assert os.path.exists(OUT_DIR), ['The directory ' + OUT_DIR + ' does not exist.']

    # %%
    acq_slices = []

    for s in range(args.images_per_slab):

        print('> slice ' + str(s).zfill(3))

        fstr = OUT_DIR + '/reco_slice_' + str(s).zfill(3)

        f = h5py.File(fstr + '.h5', 'r')
        acq_slices.append(f['temptv'][:])
        spokes_per_frame = f['spokes_per_frame'][()]
        f.close()

    acq_slices = np.array(acq_slices)
    print('> acq_slices shape: ', acq_slices.shape)

    f = h5py.File(OUT_DIR + '/reco_spokes' + str(spokes_per_frame).zfill(2) + '.h5', 'w')
    f.create_dataset('temptv', data=acq_slices)
    f.close()