#/bin/bin -l

if [ -z "$1" ]; then
    echo "Find raw .h5 files in the current directory: $(pwd)"
    DIR=$(pwd)
else
    echo "Find raw .h5 files in: $1"
    DIR="$1"
fi

FILES=$(find "${DIR}" -maxdepth 1 -type f -name "*CCCTrio*.h5" -exec basename {} \;)

echo "> files to be reconstructed: "
echo "${FILES}"

if [ -z "${FILES}" ]; then
    echo "no raw .h5 file found. exit."
    exit
fi

if [ -z "$2" ]; then
    echo "> SPOKES set as default: 72"
    SPOKES=72
else
    NUM='^[0-9]+$'

    if [[ $2 =~ $NUM ]]; then
        SPOKES="$2"
    else
        echo "> Input $2 is not a number. SPOKES set as default: 72"
        SPOKES=72
    fi
fi


for F in ${FILES}; do

    echo "> reconstruct now ${F}"

    # reconstruct slice by slice
    python dce_recon.py --dir ${DIR} --data ${F} --spokes_per_frame ${SPOKES} --slice_idx 0 --slice_inc 192

    # combine all slices as a 4D matrix into one .h5 file
    python comb_slice.py --data ${F}

    # convert the .h5 file to dicom
    FN=${F%.h5}
    FN+=_processed/reco_spokes"${SPOKES}".h5
    python h5_to_dcm.py --h5py ${FN} --spokes_per_frame ${SPOKES}

done
