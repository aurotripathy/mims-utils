import subprocess
from pathlib import Path
import shutil
import os
import sys

def print_precision_attribute(preset_file):
    with open(preset_file) as f:
        gpu_attributes = f.readlines()
        for i, attribute in enumerate(gpu_attributes):
            if 'cBoxConfs' in attribute:
                print('Using csv file:', gpu_attributes[i].strip())

def execute_subp_run(preset_file):
    command_list = ["python", "mims.py", "-preset", preset_file]
    response = subprocess.run(command_list, shell=True, check=False, stdout=subprocess.PIPE, universal_newlines=True)
    print('+++++Out\n')
    print(response.stdout)
    print('-----Error\n')
    print(response.stderr)
    print('=====Code\n')
    print(response.returncode)

                
def execute(preset_file):
    command_list = ["python", "mims.py", "-preset", preset_file]
    print("executing:", command_list) 
    process = subprocess.Popen(command_list,
                               shell=True,
                               stdout=subprocess.PIPE,
                               # stderr=subprocess.STDOUT,
                               stderr=sys.stdout.buffer)
                               # universal_newlines=True)
    while True:
        output = process.stdout.readline()
        print(output)
        if output == b'' and process.poll() is not None:
            print(process.poll())
            break
        else:
            print('looping')
        if output:
            print(output.strip())
    rc = process.poll()
    print('return code', rc)

def gen_init_file_from_one(base_preset_file, gen_preset_file, precision_csv, model):
    """ 
    generates another ini file with the specified precision and model and writes then
    with the proper prefix
    """
    with open(base_preset_file) as f:
        gpu_attributes = f.readlines()
        for i, attribute in enumerate(gpu_attributes):
            if 'cBoxConfs' in attribute:
                gpu_attributes[i] = 'cBoxConfs' + '=' + precision_csv + '\n'
                print('Using csv file:', gpu_attributes[i].strip())
            if 'cBoxModels' in attribute:
                gpu_attributes[i] = 'cBoxModels' + '=' + model + '\n'
                print('Using model:' , model)
            if 'chBoxTraining' in attribute:
                gpu_attributes[i] = 'chBoxTraining' + '=' + 'True' + '\n'
                print('Using model:' , model)
    with open(gen_preset_file, 'w') as f:
        f.writelines(gpu_attributes)

model = 'resnet50'
gen_init_file_from_one('auro-presets/auro-gemm-fp32.ini', 'auro-presets/auro-gemm-bf16.ini',
                       'mi100_bf16.csv', model) 
gen_init_file_from_one('auro-presets/auro-gemm-fp32.ini', 'auro-presets/auro-gemm-fp16.ini',
                       'mi100_fp16.csv', model) 
    
root_folder = 'auro-presets'
# preset_files = ['auro-gemm-fp32.ini', 'auro-gemm-bf16.ini', 'auro-gemm-fp16.ini']
preset_files = ['auro-r50-fwd.ini']
# preset_files = ['auro-gemm-fp32.ini']
for preset_file in preset_files:
    print_precision_attribute(os.path.join(root_folder, preset_file))
    # execute(os.path.join(root_folder, preset_file))
    execute_subp_run(os.path.join(root_folder, preset_file))
    

