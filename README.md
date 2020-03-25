#### Automating data-collection from MIMS

```
C:\Users\autrip\mims_new\MIMS_AP>python automate.py --help
usage: automate.py [-h] -t {chordal,2h4p} -m
                   {gemm,resnet50,resnext101_32x4d,resnext101_32x8d,resnext101_64x4d,transformer}
                   -f ROOT_FOLDER

Provide the arguments for collecting data from MIMS

optional arguments:
  -h, --help            show this help message and exit
  -t {chordal,2h4p}, --topology {chordal,2h4p}
                        The tolopoly, chordal or fully connected two hives
  -m {gemm,resnet50,resnext101_32x4d,resnext101_32x8d,resnext101_64x4d,transformer}, --model {gemm,resnet50,resnext101_32x4d,resnext101_32x8d,resnext101_64x4d,transformer}
                        The NN model we are using
  -f ROOT_FOLDER, --root-folder ROOT_FOLDER
                        The folder that has the .ini starter files

```
