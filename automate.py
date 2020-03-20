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
        if line.startswith("Training Throughput"):
            lines.append(line)
    return lines

def execute_subp_run(preset_file):
    command_list = ["python", "mims.py", "-preset", preset_file]
    print(command_list)
    response = subprocess.run(command_list, shell=True, check=False, stdout=subprocess.PIPE, universal_newlines=True)
    if response.stderr:
        print('-----Error-----')
        print(response.stderr)
    if response.returncode != 1:
        print('===== Return Code=====')
        print(response.returncode)
    # print filtered response
    filtered_response = filter_response(response.stdout)
    print('+++++Result+++++')
    print(filtered_response)
 


def gen_init_file_from_one(base_preset_file, gen_preset_file, precision_csv, model):
    """ 
    generates another ini file with the specified precision and model and writes then
    with the proper prefix
    """
    with open(base_preset_file) as f:
        gpu_attributes = f.readlines()
        for i, attribute in enumerate(gpu_attributes):
            if attribute.startswith('cBoxConfs'):
                gpu_attributes[i] = 'cBoxConfs' + '=' + precision_csv + '\n'
                # print('Changed attribute:', gpu_attributes[i].strip())
            if attribute.startswith('cBoxModels'):
                gpu_attributes[i] = 'cBoxModels' + '=' + model + '\n'
                # print('Changed attribute:', gpu_attributes[i])
            if attribute.startswith('chBoxTraining'):
                gpu_attributes[i] = 'chBoxTraining' + '=' + 'true' + '\n'
                # print('Changed attribute:', gpu_attributes[i])
    with open(gen_preset_file, 'w') as f:
        f.writelines(gpu_attributes)


def get_args():
    parser = argparse.ArgumentParser(description='Provide the arguments for collecting data from MIMS')
    parser.add_argument('-t', '--topology', type=str, choices=['chordal', '2h4p'],
                        required=True, help='The tolopoly, chordal or fully connected two hives')
    parser.add_argument('-m', '--model', type=str, choices=['gemm', 'resnet50', 'resnext101_32x4d', 'resnext101_32x8d', 'resnext101_64x4d', 'transformer'],
                        required=True, help='The NN model we are using')
    parser.add_argument('-f', '--root-folder', type=str,
                        required=True, help='The folder that has the .ini starter files')
    args = parser.parse_args()
    print(args)
    return args


# main
args = get_args()
root_folder = args.root_folder
prefix = 'auro'
topology = args.topology # implied N=8 GPUs
model = args.model
precision = ['fp32', 'bf16', 'fp16']
file_ext = '.ini'
arch = 'mi100_'

source_file = os.path.join(root_folder, '_'.join([prefix, topology, model, precision[0], file_ext]))
if os.path.isfile(source_file):
    print (source_file, 'exist...proceeding')
else:
    print ("File", source_file, 'does not exist, stopping')
    exit(2)

gen_file_1 = os.path.join(root_folder, '_'.join([prefix, topology, model, precision[1], file_ext]))
gen_init_file_from_one(source_file, gen_file_1, arch + precision[1] + '.csv', model)

gen_file_2 = os.path.join(root_folder, '_'.join([prefix, topology, model, precision[2], file_ext]))
gen_init_file_from_one(source_file, gen_file_2, arch + precision[2] + '.csv', model) 
    
preset_files = [source_file, gen_file_1, gen_file_2]

# preset_files = [gen_file_1]

for preset_file in preset_files:
    print_precision_attribute(preset_file)
    execute_subp_run(preset_file)
    

