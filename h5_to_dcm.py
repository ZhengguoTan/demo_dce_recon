import argparse
import datetime
import h5py
import os
import pathlib
import pydicom
# from pydicom import Dataset
from pydicom.datadict import add_dict_entry
# from pydicom.dataset import FileDataset, FileMetaDataset
# from pydicom.uid import UID

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

    parser.add_argument('--partitions', type=int, default=83,
                        help='total number of partitions')

    parser.add_argument('--TE', type=float, default=1.8,
                        help='echo time (ms)')

    parser.add_argument('--TR', type=float, default=4.87,
                        help='repetition time (ms)')

    args = parser.parse_args()

    # %%
    # read in the original dicom file
    ds = pydicom.dcmread(args.dcm)


    OUT_DIR = DIR + '/' + args.h5py
    OUT_DIR = OUT_DIR.split('.h5')[0]
    pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    f = h5py.File(DIR + '/' + args.h5py, 'r')
    R = f['temptv'][:]
    f.close()

    R = np.squeeze(abs(R))
    N_z, N_t, N_y, N_x = R.shape
    print(R.shape)

    # normalize images
    R = R * 533 / np.amax(R)

    print(np.amin(R))
    print(np.amax(R))


    slice_thickness = ds[0x00180050].value
    print('> slice_thcikness: ', slice_thickness)


    for t in range(N_t):
        for z in range(N_z):

            # Set creation date/time
            dt = datetime.datetime.now()
            ds.ContentDate = dt.strftime('%Y%m%d')
            timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
            ds.ContentTime = timeStr

            ds.PixelData = R[z, t].astype(np.uint16).tobytes()
            ds['PixelData'].VR = 'OW'
            ds.is_little_endian = True
            ds.is_implicit_VR = False

            ds[0x00100020].value = 'trial'  # PatientID
            ds[0x00201041].value = (- N_z // 2 + z) * slice_thickness  # SliceLocation
            ds[0x00200013].value = t * N_z + (z + 1)  # InstanceNumber
            ds[0x00200010].value = '1'  # StudyID
            ds[0x00080018].value = str(t * N_z + (z + 1))  # Unique SOP Instance UID !
            ds.ImageOrientationPatient = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]

            add_dict_entry(0x00186666, "DS", "TimeStamp", "Time Stamp", VM='1')
            ds.TimeStamp = str(t * N_z * args.TR)

            print('> slice ' + str(z).zfill(3) + ' frame ' + str(t).zfill(3) + ' InstanceNumber ' + str(t * N_z + (z + 1)).zfill(4))

            ds.save_as(OUT_DIR + '/slice_' + str(z).zfill(3) + '_frame_' + str(t).zfill(3) + '.dcm')

    print('> done')
