#/bin/bin -l

FILES=$(find * -type f -name "*CCCTrio*.h5")

echo ${FILES}

SPOKES=13


for F in ${FILES}; do

    echo ${F}

    # reconstruct slice by slice
    python dce_recon.py --data ${F} --spokes_per_frame ${SPOKES} --slice_idx 0 --slice_inc 192

    # combine all slices as a 4D matrix into one .h5 file
    python comb_slice.py --data ${F}

    # convert the .h5 file to dicom
    FN=${F%.h5}
    FN+=_processed/reco_spokes"${SPOKES}".h5
    python h5_to_dcm.py --h5py ${FN}

done
