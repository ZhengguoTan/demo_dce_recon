# Dynamic Contrast Enhanced (DCE) MRI Reconstruction

## Demonstration of DCE MRI reconstruction using temporal TV regularization

* Interactive code demo:

    * DCE MRI: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ZhengguoTan/demo_dce_recon/blob/main/demo_dce_sim_recon_temptv.ipynb)

    * Motion Phantom: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ZhengguoTan/demo_dce_recon/blob/main/demo_motion_phantom.ipynb)


* How to run on your local computer?

    All the jupyter notebooks provide installation instructions and are designed such that you can simply "click and go". If you want to run the script `dce_recon.py` on your local computer, you need to firstly install the required python environments, which I suggest to use `conda`.

    Here are the steps:

    1. create a new `conda` environment in ther terminal:

    ```bash
    conda create -n dce python=3.9.16
    conda activate dce
    which python  # to validate the python is under the environment
    ```

    ```bash
    python -m pip install h5py
    python -m pip install pywavelets
    python -m pip install numba
    python -m pip install scipy
    python -m pip install tqdm
    python -m pip install torch
    python -m pip install cupy
    conda install -c conda-forge cupy cudnn cutensor nccl  # if you have GPU
    conda install -c conda-forge numpy=1.24
    ```

    2. clone and install `sigpy` in the terminal:

    ```bash
    git clone https://github.com/ZhengguoTan/sigpy.git
    cd sigpy
    python -m pip install -e .
    ```

    3. Now you should be able to run the script:

    ```bash
    python dce_recon.py --data 'GeneBreast_CCCTrio#F636203.h5' --spokes_per_frame 12 --slice_idx 96 --slice_inc 1
    ```

## References:

* Zhang S, Block KT, Frahm J. [Magnetic resonance imaging in real time: advances using radial FLASH](https://doi.org/10.1002/jmri.21987). J Magn Reson Imaging 2010;31:101-109.

* Uecker M, Zhang S, Voit D, Karaus A, Merboldt KD, Frahm J. [Real-time MRI at a resolution of 20 ms](https://doi.org/10.1002/nbm.1585). NMR Biomed 2010;23:986-994.

* Block KT, Chandarana H, Milla S, Bruno M, Mulholland T, Fatterpekar G, Hagiwara M, Grimm R, Geppert C, Kiefer B, Sodickson DK. [Towards routine clinical use of radial stack-of-stars 3D gradient-echo sequences for reducing motion sensitivity](https://doi.org/10.13104/jksmrm.2014.18.2.87). J Korean Magn Reson Med 2014;18:87-106.

* Feng L, Grimm R, Block KT, Chandarana H, Kim S, Xu J, Axel L, Sodickson DK, Otazo R. [Golden‐angle radial sparse parallel MRI: combination of compressed sensing, parallel imaging, and golden‐angle radial sampling for fast and flexible dynamic volumetric MRI](https://doi.org/10.1002/mrm.24980). Magn Reson Med 2014;72:707-717.
