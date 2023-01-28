import os
import subprocess
from multiprocessing import Pool, cpu_count
from nipype.interfaces.ants.segmentation import N4BiasFieldCorrection
import time

REF_PATH = 'PATH OF MNI152_T1_1mm_brain.nii.gz'


def orient2std(in_path, out_path):
    command = ["fslreorient2std", in_path, out_path]
    subprocess.call(command)
    return

def remove_neck(in_path, out_path):
    command = ["robustfov", "-i", in_path, "-r", out_path]
    subprocess.call(command, stdout=open(os.devnull, "r"),
                    stderr=subprocess.STDOUT)
    return

def bet(in_path, out_path, frac="0.5"):
    command = ["bet", in_path, out_path, "-R", "-f", frac, "-g", "0"]
    subprocess.call(command)
    return

def registration(in_path, out_path):
    command = ["flirt", "-in", in_path, "-ref", REF_PATH, "-out", out_path, "-cost", "corratio", "-dof", "12", ]
    subprocess.call(command, stdout=open(os.devnull, "r"),
                    stderr=subprocess.STDOUT)


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
    print("Process on: ", in_path)
    try:
        orient2std(in_path, out_path)
        remove_neck(out_path, out_path)
        bet(out_path, out_path)
        registration(out_path, out_path)
        bias_field_correction(out_path, out_path) 
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