import molgrid
import numpy as np
import torch
import os

def output_grids_as_dx():
    datadir = "/content/"  # Replace with the path to your data
    typespath = '/content/'  # Replace with the path to your types file
    output_dir = "/content/"  # Replace with the path to your desired output directory

    gmaker = molgrid.GridMaker(binary=False)
    e = molgrid.ExampleProvider(data_root=datadir, shuffle=False, balanced=False)
    e.populate(typespath)

    batch = e.next_batch(1)  # Adjust the batch size if needed
    example = batch[0]  # Take the first example from the batch
    c = example.coord_sets[0]  # Assuming you want the first coord set

    dims = gmaker.grid_dimensions(e.num_types())
    center = tuple(c.center())

    mgridout = molgrid.MGrid4f(*dims)
    gmaker.forward(center, c, mgridout.cpu())

    # Include the output directory in the prefix
    prefix = f"{output_dir}/output_grid"  # Base name for the output .dx files, including the output directory
    type_names = e.get_type_names()
    resolution = gmaker.get_resolution()  # Get resolution from GridMaker

    scale = 5.0  # Default scale factor

    # Output the grids as DX files using write_dx_grids
    molgrid.write_dx_grids(prefix, type_names, mgridout.cpu(), center, resolution, scale)