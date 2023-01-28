import os
import subprocess
from multiprocessing import Pool, cpu_count
import time

def remove_neck(in_path, out_path):
    command = ["robustfov", "-i", in_path, "-r", out_path]
    subprocess.call(command, stdout=open(os.devnull, "r"),
                    stderr=subprocess.STDOUT)
    return

def main(in_path, out_path):
    print("Rm neck on: ", in_path)
    try:
        remove_neck(in_path, out_path)
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