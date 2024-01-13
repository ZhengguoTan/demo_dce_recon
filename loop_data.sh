#/bin/bin -l

FILES=$(find * -type f -name "*CCCTrio*.h5")

echo "> files to be reconstructed: "
echo "${FILES}"

if [ -z "$1" ]; then
    echo "SPOKES set as default: 72"
    SPOKES=72
else
    NUM='^[0-9]+$'

    if [[ $1 =~ $NUM ]]; then
        SPOKES="$1"
    else
        echo "Input $1 is not a number. SPOKES set as default: 72"
        SPOKES=72
    fi
fi


for F in ${FILES}; do

    echo "> reconstruct now ${F}"

    # reconstruct slice by slice
    python dce_recon.py --data ${F} --spokes_per_frame ${SPOKES} --slice_idx 0 --slice_inc 192

    # combine all slices as a 4D matrix into one .h5 file
    python comb_slice.py --data ${F}

    # convert the .h5 file to dicom
    FN=${F%.h5}
    FN+=_processed/reco_spokes"${SPOKES}".h5
    python h5_to_dcm.py --h5py ${FN} --spokes_per_frame ${SPOKES}

done
