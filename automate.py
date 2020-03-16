import subprocess
from pathlib import Path
import shutil
import os
import sys
import argparse


def print_precision_attribute(preset_file):
    with open(preset_file) as f:
        gpu_attributes = f.readlines()
        for i, attribute in enumerate(gpu_attributes):
            if 'cBoxConfs' in attribute:
                print('Using csv file:', gpu_attributes[i].strip())

def filter_response(response):
    response = response.splitlines()
    lines = []
    for line in response:
        if "Training Throughput" in line:
            lines.append(line)
    return lines

def execute_subp_run(preset_file):
    command_list = ["python", "mims.py", "-preset", preset_file]
    print(command_list)
    response = subprocess.run(command_list, shell=True, check=False, stdout=subprocess.PIPE, universal_newlines=True)
    print('-----Error\n')
    print(response.stderr)
    print('===== Return Code\n')
    print(response.returncode)
    # print filtered response
    response = filter_response(response.stdout)
    print('+++++Out\n')
    print(response)
 

                
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


def get_args():
    parser = argparse.ArgumentParser(description='Provide the arguments for collecting data from MIMS')
    parser.add_argument('-m', '--model', type=str, required=True, help='The NN model we are using')

    args = parser.parse_args()
    print(args)
    return args


# main
args = get_args()
root_folder = 'auro-presets'
prefix = 'auro'
topology = 'chordal' # implied N=8 GPUs
model = args.model
precision = ['fp32', 'bf16', 'fp16']
file_ext = '.ini'
arch = 'mi100'

source_file = os.path.join(root_folder, '_'.join([prefix, topology, model, precision[0], file_ext]))

gen_file_1 = os.path.join(root_folder, '_'.join([prefix, topology, model, precision[1], file_ext]))
gen_init_file_from_one(source_file, gen_file_1, arch + precision[1] + '.csv', model)

gen_file_2 = os.path.join(root_folder, '_'.join([prefix, topology, model, precision[2], file_ext]))
gen_init_file_from_one(source_file, gen_file_2, arch + precision[2], model) 
    
preset_files = [source_file, gen_file_1, gen_file_2]

# preset_files = [gen_file_1]

for preset_file in preset_files:
    print_precision_attribute(preset_file)
    execute_subp_run(preset_file)
    

