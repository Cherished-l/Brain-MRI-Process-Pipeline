import os
import subprocess
from multiprocessing import Pool, cpu_count
import time

REF_PATH = 'PATH OF MNI152_T1_1mm_brain.nii.gz'

def registration(in_path, out_path):
    command = ["flirt", "-in", in_path, "-ref", REF_PATH, "-out", out_path, "-cost", "corratio", "-dof", "12", ]
    subprocess.call(command, stdout=open(os.devnull, "r"),
                    stderr=subprocess.STDOUT)

def main(in_path, out_path):
    print("Reg on: ", in_path)
    try:
        registration(in_path, out_path)
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