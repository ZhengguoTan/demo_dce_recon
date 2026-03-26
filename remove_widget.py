import nbformat

notebooks = ['demo_dce_sim_recon_temptv',
             'demo_motion_phantom']

for notebook in notebooks:

    nb = nbformat.read(notebook + '.ipynb', as_version=4)

    if "widgets" in nb["metadata"]:
        del nb["metadata"]["widgets"]

    nbformat.write(nb, notebook + "_widgets.ipynb")