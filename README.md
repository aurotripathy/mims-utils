###Automating data-collection from MIMS

Provide the topology and the model

<code>python automate.py -t 2h4p -m gemm</code>

or 

<code>python automate.py --topology chordal --model gemm</code>

Topologies currently available:

<code>['chordal', '2h4p']</code>

Models currently available:

<code> ['gemm', 'resnet50', 'resnext101_32x4d', 'resnext101_32x8d', 'resnext101_64x4d', 'transformer']</code>
