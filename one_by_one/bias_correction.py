import os
import subprocess
from multiprocessing import Pool, cpu_count
from nipype.interfaces.ants.segmentation import N4BiasFieldCorrection
import time

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def bias_field_correction(in_path, out_path):
    n4 = N4BiasFieldCorrection()
    n4.inputs.input_image = in_path
    n4.inputs.output_image = out_path
    n4.inputs.dimension = 3
    n4.inputs.n_iterations = [100, 100, 60, 40]
    n4.inputs.shrink_factor = 3
    n4.inputs.convergence_threshold = 1e-4
    n4.inputs.bspline_fitting_distance = 300
    n4.run()

    return

def main(in_path, out_path):
    print("Reg on: ", in_path)
    try:
        bias_field_correction(in_path, out_path)
    except RuntimeError:
        print("\tFalied on: ", in_path)

    return

def unwarp_main(arg, **kwarg):
    return main(*arg, **kwarg)

#-------------------------------------------------------------------------------
 
INPUT_DIR = 'PATH_FOR_INPUT'
OUTPUT_DIR = 'PATH_FOR_OUTPUT'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

input_list = [os.path.join(INPUT_DIR, img) for img in os.listdir(INPUT_DIR)]
out_list = [os.path.join(OUTPUT_DIR, img) for img in os.listdir(INPUT_DIR)]

start = time.time()
paras = zip(input_list, out_list)
pool = Pool(processes=int(cpu_count()*0.8))
pool.map(unwarp_main, paras)
print('done... time=:', time.time()-start)